from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.knowledge import ChatInteraction
from app.schemas.chat import ChatResponse

# TODO: instantiate once at startup via lifespan, not per-request
# from app.services.ai.embedding_service import EmbeddingService
# from app.services.ai.llm_service import LLMService
# from app.services.ai.vector_store import VectorStoreService


class RagService:
    """
    Orchestrates the RAG pipeline:
      1. Embed the user question
      2. Retrieve top-k similar Q&A pairs from Qdrant
      3. Compute confidence score (cosine similarity)
      4. If confident: send context + question to LLM and return answer
      5. If not confident: return fallback message
      6. Persist interaction to DB
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        # self.embedder = EmbeddingService()
        # self.llm = LLMService()
        # self.vector_store = VectorStoreService()

    async def answer(self, question: str, user_id: UUID) -> ChatResponse:
        # Step 1: embed question
        # question_vector = await self.embedder.embed(question)

        # Step 2: semantic search
        # hits = await self.vector_store.search(question_vector, top_k=settings.RAG_TOP_K)

        # Step 3: confidence score (max similarity of top hit)
        # confidence = hits[0].score if hits else 0.0
        confidence = 0.9  # placeholder

        is_low_confidence = confidence < settings.RAG_CONFIDENCE_THRESHOLD

        if is_low_confidence:
            answer_text = (
                "Nisam siguran/a u odgovor na vaše pitanje. "
                "Molimo kontaktirajte agenta za dodatnu pomoć."
            )
            source_id = None
        else:
            # Step 4: build prompt and call LLM
            # context = "\n\n".join([h.payload["answer"] for h in hits])
            # answer_text = await self.llm.generate(question=question, context=context)
            answer_text = "Placeholder odgovor – LLM integracija u toku."  # placeholder
            source_id = None  # hits[0].payload.get("item_id") if hits else None

        # Step 5: persist interaction
        interaction = ChatInteraction(
            user_id=user_id,
            question=question,
            answer=answer_text,
            confidence_score=confidence,
            source_item_id=source_id,
            is_low_confidence=is_low_confidence,
        )
        self.db.add(interaction)
        await self.db.commit()
        await self.db.refresh(interaction)

        return ChatResponse(
            answer=answer_text,
            confidence_score=confidence,
            is_low_confidence=is_low_confidence,
            source_id=source_id,
            interaction_id=interaction.id,
        )
