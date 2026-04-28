from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.knowledge import ChatSesija, Poruka, Odgovor
from app.schemas.chat import ChatResponse


class RagService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def answer(self, question: str, user_id: UUID) -> ChatResponse:
        # Step 1: embed question
        # question_vector = await self.embedder.embed(question)

        # Step 2: semantic search
        # hits = await self.vector_store.search(question_vector, top_k=settings.RAG_TOP_K)

        confidence = 0.9  # placeholder
        is_low_confidence = confidence < settings.RAG_CONFIDENCE_THRESHOLD

        if is_low_confidence:
            answer_text = (
                "Nisam siguran/a u odgovor na vaše pitanje. "
                "Molimo kontaktirajte agenta za dodatnu pomoć."
            )
            metoda = "Fallback"
            source_id = None
        else:
            answer_text = "Placeholder odgovor – LLM integracija u toku."
            metoda = "Retrieval"
            source_id = None

        # Create session
        sesija = ChatSesija(
            id_korisnika=user_id,
            kanal_pristupa="web",
            status="Aktivna",
            broj_poruka=1,
        )
        self.db.add(sesija)
        await self.db.flush()

        # Create user message — id_odgovora set after Odgovor is created
        poruka = Poruka(
            tekst=question,
            tip="KorisnickoP",
            timestamp_msg=datetime.now(timezone.utc),
            id_sesije=sesija.id,
        )
        self.db.add(poruka)
        await self.db.flush()

        # Create the answer
        odgovor = Odgovor(
            tekst_odgovora=answer_text,
            id_unosa_baze_znanja=source_id,
            metoda_generisanja=metoda,
            skor_pouzdanosti=confidence,
            id_poruke=poruka.id,
        )
        self.db.add(odgovor)
        await self.db.flush()

        # Link poruka → odgovor
        poruka.id_odgovora = odgovor.id
        await self.db.commit()
        await self.db.refresh(odgovor)

        return ChatResponse(
            answer=answer_text,
            confidence_score=confidence,
            is_low_confidence=is_low_confidence,
            source_id=source_id,
            interaction_id=odgovor.id,
        )
