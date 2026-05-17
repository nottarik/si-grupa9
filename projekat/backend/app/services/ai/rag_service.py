import asyncio
import re
import time
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.knowledge import Anomalija, ChatSesija, Poruka, Odgovor
from app.schemas.chat import ChatResponse
from app.services.ai.embedding_service import EmbeddingService
from app.services.ai.llm_service import LLMService
from app.services.ai.vector_store import VectorStoreService

_FALLBACK_MSG = (
    "I'm not confident in my answer to your question. "
    "Please contact an agent for further assistance."
)

_PII_RE = re.compile(r'\[[A-Z]+_\d+\]')


def _strip_pii(text: str) -> str:
    cleaned = _PII_RE.sub('', text)
    cleaned = re.sub(r',\s*,', ',', cleaned)   # double commas: "x, , y" → "x, y"
    cleaned = re.sub(r'^\s*[,;]\s*', '', cleaned)  # leading comma: ", I can..." → "I can..."
    cleaned = re.sub(r'  +', ' ', cleaned).strip()
    return cleaned


class RagService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def answer(self, question: str, user_id: UUID, history: list[dict] | None = None) -> ChatResponse:
        import logging
        logger = logging.getLogger(__name__)

        llm = LLMService()
        # Trim history to last 6 messages (3 exchanges) to cap token usage
        trimmed_history = (history or [])[-6:]

        # --- Query rewriting (only when conversation history exists) ---
        search_query = question
        if trimmed_history:
            try:
                search_query = await asyncio.to_thread(
                    llm.rewrite_query, question, trimmed_history
                )
                logger.info("Rewritten query: %r → %r", question, search_query)
            except Exception as exc:
                logger.warning("Query rewrite failed, using original: %s", exc)

        # --- Retrieval ---
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
            "RAG search: %d hits, scores=%s, threshold=%.2f",
            len(hits),
            [round(h.score, 3) for h in hits],
            settings.RAG_CONFIDENCE_THRESHOLD,
        )
        is_low_confidence = confidence < settings.RAG_CONFIDENCE_THRESHOLD

        # --- Generate or fallback ---
        if is_low_confidence or not hits:

            source_id = None
            try:
                t0 = time.perf_counter()
                answer_text = await asyncio.to_thread(
                    llm.generate_without_context, question, trimmed_history
                )
                latencija_ms = int((time.perf_counter() - t0) * 1000)
                metoda = "Generativno"
            except Exception as exc:
                logger.error("LLM no-context call failed: %s", exc)
                answer_text = _FALLBACK_MSG
                latencija_ms = None
                metoda = "Fallback"
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

            try:
                t0 = time.perf_counter()
                answer_text = await asyncio.to_thread(
                    llm.generate, question, context, trimmed_history
                )
                answer_text = _strip_pii(answer_text)
                latencija_ms = int((time.perf_counter() - t0) * 1000)
                metoda = "Retrieval"
            except Exception as exc:
                logger.error("LLM call failed: %s — returning stored answer", exc)
                answer_text = best_answer if best_answer else _FALLBACK_MSG
                latencija_ms = None
                metoda = "Retrieval"

        # --- Persist session + messages ---
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

        # Log anomaly for low-confidence / no-result events
        if is_low_confidence or not hits:
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

        return ChatResponse(
            answer=answer_text,
            confidence_score=confidence,
            is_low_confidence=(metoda == "Fallback"),
            source_id=source_id,
            interaction_id=odgovor.id,
        )
