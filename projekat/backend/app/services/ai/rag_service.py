import asyncio
import re
import time
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.knowledge import Anomalija, ChatSesija, Poruka, Odgovor
from app.schemas.chat import ChatResponse
from app.services.ai.embedding_service import EmbeddingService
from app.services.ai.llm_service import LLMService
from app.services.ai.vector_store import VectorStoreService

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

        llm = LLMService()
        trimmed_history = (history or [])[-6:]

        # --- Classify intent: smalltalk / domain / out_of_scope ---
        try:
            intent = await asyncio.to_thread(llm.classify_intent, question)
        except Exception as exc:
            logger.warning("Intent classification failed, assuming domain: %s", exc)
            intent = "domain"

        logger.info("Intent classification: %r → %s", question[:80], intent)

        confidence = 0.0
        source_id = None
        needs_escalation = False
        hits: list = []

        if intent == "out_of_scope":
            answer_text = _OUT_OF_SCOPE_MSG
            latencija_ms = None
            metoda = "Fallback"
            logger.info("Out-of-scope message rejected: %r", question[:100])

        elif intent == "smalltalk":
            try:
                t0 = time.perf_counter()
                answer_text = await asyncio.to_thread(
                    llm.generate_without_context, question, trimmed_history
                )
                latencija_ms = int((time.perf_counter() - t0) * 1000)
                metoda = "Generativno"
            except Exception as exc:
                logger.error("LLM conversational call failed: %s", exc)
                answer_text = "Hello! I'm your ISP virtual assistant. How can I help you today?"
                latencija_ms = None
                metoda = "Fallback"

        else:
            # Domain question — attempt RAG retrieval

            # Query rewriting (only useful with enough context)
            search_query = question
            if len(trimmed_history) >= 2:
                try:
                    search_query = await asyncio.to_thread(
                        llm.rewrite_query, question, trimmed_history
                    )
                    logger.info("Rewritten query: %r → %r", question, search_query)
                except Exception as exc:
                    logger.warning("Query rewrite failed, using original: %s", exc)

            # Retrieval
            try:
                vector = await asyncio.to_thread(EmbeddingService().embed, search_query)
                hits = await asyncio.to_thread(
                    VectorStoreService().search, vector, settings.RAG_TOP_K
                )
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
                # Very low confidence or no results — escalate to agent
                answer_text = _CONNECT_AGENT_MSG
                latencija_ms = None
                metoda = "Fallback"
                needs_escalation = True

            else:
                # Build context from top hits
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
                    t0 = time.perf_counter()
                    answer_text = await asyncio.to_thread(
                        llm.generate, question, context, trimmed_history
                    )
                    answer_text = _strip_pii(answer_text)
                    if is_uncertain:
                        answer_text += _UNCERTAIN_SUFFIX
                    latencija_ms = int((time.perf_counter() - t0) * 1000)
                    metoda = "Retrieval"
                except Exception as exc:
                    logger.error("LLM call failed: %s — returning stored answer", exc)
                    answer_text = best_answer if best_answer else _CONNECT_AGENT_MSG
                    if is_uncertain and best_answer:
                        answer_text += _UNCERTAIN_SUFFIX
                    needs_escalation = not bool(best_answer)
                    latencija_ms = None
                    metoda = "Retrieval"

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

        if needs_escalation:
            anomalija_tip = "BezOdgovora" if not hits else "NiskaPouzdanost"
            self.db.add(Anomalija(
                tip=anomalija_tip,
                nivo_ozbiljnosti="Visoka",
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
            is_low_confidence=needs_escalation,
            source_id=source_id,
            source_topic=source_topic,
            interaction_id=odgovor.id,
            session_id=sesija.id,
            needs_escalation=needs_escalation,
        )
