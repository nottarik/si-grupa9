import asyncio
import re
import time

_INJECTION_RE = re.compile(
    r'\b(ignore|forget|disregard|override|bypass|reset|clear)\b.{0,40}'
    r'\b(instructions?|rules?|guidelines?|system|prompt|constraints?|directions?|context)\b'
    r'|\bact as\b|\bpretend (you are|to be)\b|\byou are now\b'
    r'|\broleplay\b|\bjailbreak\b|\bdeveloper mode\b|\bdan mode\b'
    r'|\bno restrictions?\b|\bunlock(ed)?\b.{0,20}\bmode\b',
    re.IGNORECASE,
)

_ESCALATION_REQUEST_RE = re.compile(
    r'\b(talk|speak|chat|connect|transfer|get|put me through)\b.{0,30}\b(agent|human|person|operator|representative|staff|support|someone)\b'
    r'|\b(want|need|prefer)\b.{0,20}\b(human|person|agent|operator|real person|live support|live agent)\b'
    r'|\bhuman (agent|support|help)\b|\blive (agent|support|chat)\b'
    r'|\breal (person|human|agent)\b|\bspeak to (someone|a person|a human)\b',
    re.IGNORECASE,
)

# Pronouns/references that indicate the question depends on prior context (English + Bosnian)
_CONTEXT_REF_RE = re.compile(
    r'^\s*(it|they|them|that|this|those|these'
    r'|to|taj|ta|ti|te|taj|ova|ovaj|ove|ovi|ona|oni|one|ono|toga|tome|tim|tom)\b'
    r'|\b(it|they|them|their|to|ono|oni|one)\s+'
    r'(is|are|was|were|does|did|has|have|will|would|can|could'
    r'|je|su|nije|nisu|ima|imaju|može|mogu|će|bi|treba|trebaju)\b',
    re.IGNORECASE,
)

_EXPLICIT_ESCALATION_MSG = "Of course! Let me connect you with a support agent right away. Please hold on while we find someone available for you."
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.knowledge import Anomalija, ChatSesija, Poruka, Odgovor
from app.schemas.chat import ChatResponse
from app.services.ai.embedding_service import get_embedding_service
from app.services.ai.llm_service import get_llm_service
from app.services.ai.vector_store import get_vector_store

_CONNECT_AGENT_MSG = "I don't have enough information in my knowledge base to answer that. Let me connect you with a support agent who can help."

_OUT_OF_SCOPE_MSG = (
    "I'm a virtual assistant for a telecom provider — I help with questions about internet, TV, "
    "mobile services, billing, and technical support. I'm not able to help with that "
    "particular request, but feel free to ask me anything about our services!"
)

_UNCERTAIN_SUFFIX = "\n\nNote: I'm not fully confident in this answer. If you need a definitive response, I'd recommend contacting a support agent."

_PII_RE = re.compile(r'\[[A-Z]+_\d+\]')


def _strip_pii(text: str) -> str:
    cleaned = _PII_RE.sub('', text)
    cleaned = re.sub(r',\s*,', ',', cleaned)
    cleaned = re.sub(r'^\s*[,;]\s*', '', cleaned)
    cleaned = re.sub(r'  +', ' ', cleaned).strip()
    return cleaned


def _needs_rewrite(question: str, history: list) -> bool:
    """Only rewrite when the question references prior context via pronouns or is very short."""
    if len(history) < 2:
        return False
    words = question.split()
    if len(words) <= 4:
        return True
    return bool(_CONTEXT_REF_RE.search(question))


class RagService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def answer(
        self,
        question: str,
        user_id: UUID,
        history: list[dict] | None = None,
        session_id: int | None = None,
    ) -> ChatResponse:
        import logging
        logger = logging.getLogger(__name__)

        t_start = time.perf_counter()

        llm = get_llm_service()
        embedding_svc = get_embedding_service()
        vector_store = get_vector_store()
        trimmed_history = (history or [])[-6:]

        # --- Classify intent ---
        prefetched_vector: list[float] | None = None

        if _INJECTION_RE.search(question):
            intent = "out_of_scope"
            logger.info("Prompt injection detected, short-circuiting: %r", question[:100])
        elif _ESCALATION_REQUEST_RE.search(question):
            intent = "escalation_request"
            logger.info("Explicit escalation request detected: %r", question[:100])
        else:
            # Classify intent and pre-embed the question in parallel — both are independent
            t_intent = time.perf_counter()
            results = await asyncio.gather(
                asyncio.to_thread(llm.classify_intent, question),
                asyncio.to_thread(embedding_svc.embed, question),
                return_exceptions=True,
            )
            intent = results[0] if not isinstance(results[0], Exception) else "domain"
            prefetched_vector = results[1] if not isinstance(results[1], Exception) else None
            if isinstance(results[0], Exception):
                logger.warning("Intent classification failed, assuming domain: %s", results[0])
            logger.info("PERF intent_classify+embed=%.0fms", (time.perf_counter() - t_intent) * 1000)

        logger.info("Intent classification: %r → %s", question[:80], intent)

        confidence = 0.0
        source_id = None
        needs_escalation = False
        hits: list = []

        if intent == "escalation_request":
            answer_text = _EXPLICIT_ESCALATION_MSG
            metoda = "Fallback"
            needs_escalation = True
            logger.info("Explicit escalation: routing to agent queue")

        elif intent == "out_of_scope":
            answer_text = _OUT_OF_SCOPE_MSG
            metoda = "Fallback"
            logger.info("Out-of-scope message rejected: %r", question[:100])

        elif intent == "smalltalk":
            try:
                t0 = time.perf_counter()
                answer_text = await asyncio.to_thread(
                    llm.generate_without_context, question, trimmed_history
                )
                logger.info("PERF llm_only=%.0fms", (time.perf_counter() - t0) * 1000)
                metoda = "Generativno"
            except Exception as exc:
                logger.error("LLM conversational call failed: %s", exc)
                answer_text = "Hello! I'm your ISP virtual assistant. How can I help you today?"
                metoda = "Fallback"

        else:
            # Domain question — attempt RAG retrieval

            # Query rewriting — only when history exists AND question references prior context
            search_query = question
            if _needs_rewrite(question, trimmed_history):
                try:
                    search_query = await asyncio.to_thread(
                        llm.rewrite_query, question, trimmed_history
                    )
                    logger.info("Rewritten query: %r → %r", question, search_query)
                except Exception as exc:
                    logger.warning("Query rewrite failed, using original: %s", exc)

            # Use the pre-fetched embedding when the query wasn't rewritten
            try:
                if prefetched_vector is not None and search_query == question:
                    vector = prefetched_vector
                    logger.info("PERF embed=0ms (prefetched)")
                else:
                    t_embed = time.perf_counter()
                    vector = await asyncio.to_thread(embedding_svc.embed, search_query)
                    logger.info("PERF embed=%.0fms", (time.perf_counter() - t_embed) * 1000)

                t_search = time.perf_counter()
                hits = await asyncio.to_thread(
                    vector_store.search, vector, settings.RAG_TOP_K
                )
                logger.info("PERF vector_search=%.0fms", (time.perf_counter() - t_search) * 1000)
            except Exception as exc:
                logger.error("Retrieval failed: %s", exc)
                hits = []

            confidence = hits[0].score if hits else 0.0
            logger.info(
                "RAG search: %d hits, scores=%s, thresholds=(high=%.2f, low=%.2f)",
                len(hits),
                [round(h.score, 3) for h in hits],
                settings.RAG_CONFIDENCE_THRESHOLD,
                settings.RAG_CONFIDENCE_THRESHOLD_LOW,
            )

            if not hits or confidence < settings.RAG_CONFIDENCE_THRESHOLD_LOW:
                answer_text = _CONNECT_AGENT_MSG
                metoda = "Fallback"
                needs_escalation = True

            else:
                context_parts = []
                for h in hits:
                    p = h.payload
                    if "question" in p and "answer" in p:
                        context_parts.append(f"Question: {p['question']}\nAnswer: {p['answer']}")
                    elif "text" in p:
                        context_parts.append(p["text"])
                context = "\n\n".join(context_parts) if context_parts else ""

                source_id = hits[0].payload.get("item_id")
                best_answer = _strip_pii(hits[0].payload.get("answer", ""))

                is_uncertain = confidence < settings.RAG_CONFIDENCE_THRESHOLD

                try:
                    t_llm = time.perf_counter()
                    answer_text = await asyncio.to_thread(
                        llm.generate, question, context, trimmed_history
                    )
                    answer_text = _strip_pii(answer_text)
                    if is_uncertain:
                        answer_text += _UNCERTAIN_SUFFIX
                    logger.info("PERF llm_generate=%.0fms", (time.perf_counter() - t_llm) * 1000)
                    metoda = "Retrieval"
                except Exception as exc:
                    logger.error("LLM call failed: %s — returning stored answer", exc)
                    answer_text = best_answer if best_answer else _CONNECT_AGENT_MSG
                    if is_uncertain and best_answer:
                        answer_text += _UNCERTAIN_SUFFIX
                    needs_escalation = not bool(best_answer)
                    metoda = "Retrieval"

        # Total pipeline latency
        latencija_ms = int((time.perf_counter() - t_start) * 1000)
        logger.info(
            "PERF total=%.0fms intent=%s method=%s confidence=%.3f",
            latencija_ms, intent, metoda, confidence,
        )

        # --- Persist session + messages ---
        sesija: ChatSesija | None = None
        if session_id:
            result = await self.db.execute(
                select(ChatSesija).where(
                    ChatSesija.id == session_id,
                    ChatSesija.id_korisnika == user_id,
                )
            )
            sesija = result.scalar_one_or_none()
            if sesija:
                sesija.broj_poruka = (sesija.broj_poruka or 0) + 1

        if sesija is None:
            sesija = ChatSesija(
                id_korisnika=user_id,
                kanal_pristupa="web",
                status="Aktivna",
                broj_poruka=1,
            )
            self.db.add(sesija)
            await self.db.flush()

        poruka = Poruka(
            tekst=question,
            tip="KorisnickoP",
            timestamp_msg=datetime.now(timezone.utc),
            id_sesije=sesija.id,
        )
        self.db.add(poruka)
        await self.db.flush()

        odgovor = Odgovor(
            tekst_odgovora=answer_text,
            id_unosa_baze_znanja=source_id,
            metoda_generisanja=metoda,
            skor_pouzdanosti=confidence,
            latencija_ms=latencija_ms,
            id_poruke=poruka.id,
        )
        self.db.add(odgovor)
        await self.db.flush()

        poruka.id_odgovora = odgovor.id

        # Log an Issue (Anomalija) only when the bot/KB actually failed. An
        # explicit "talk to a human" request is healthy routing — it belongs in
        # the escalation queue, not the issues list.
        if needs_escalation and intent != "escalation_request":
            anomalija_tip = "BezOdgovora" if not hits else "NiskaPouzdanost"
            nivo = "Visoka" if anomalija_tip == "BezOdgovora" else "Niska"
            self.db.add(Anomalija(
                tip=anomalija_tip,
                nivo_ozbiljnosti=nivo,
                status="Otvorena",
                opis=f"score={confidence:.3f}, question={question[:200]}",
                id_poruke=poruka.id,
                id_odgovora=odgovor.id,
            ))

        await self.db.commit()
        await self.db.refresh(odgovor)
        await self.db.refresh(sesija)

        source_topic: str | None = None
        if hits and confidence >= settings.RAG_CONFIDENCE_THRESHOLD_LOW:
            source_topic = hits[0].payload.get("question")

        return ChatResponse(
            answer=answer_text,
            confidence_score=confidence,
            is_low_confidence=needs_escalation and intent != "escalation_request",
            source_id=source_id,
            source_topic=source_topic,
            interaction_id=odgovor.id,
            session_id=sesija.id,
            needs_escalation=needs_escalation,
            escalation_trigger="EksplicitanZahtjev" if intent == "escalation_request" else None,
        )
