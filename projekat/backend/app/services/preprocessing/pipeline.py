import asyncio
import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.transcript import Segment, TokenMapRecord
from app.db.models.knowledge import UnosBazeZnanja
from app.services.ai.embedding_service import EmbeddingService
from app.services.ai.vector_store import VectorStoreService
from .models import PipelineResult
from .normalize import normalize
from .speakers import split_turns
from .speakers_llm import label_speakers_llm
from .chunking import chunk_turns
from .pii.masker import mask
from .pii.token_store import encrypt_token_map
from . import audit

logger = logging.getLogger(__name__)

_embedder = EmbeddingService()
_vector_store = VectorStoreService()

_MIN_QUESTION_WORDS = 5
_MIN_ANSWER_WORDS = 10
_MAX_PLACEHOLDER_RATIO = 0.15


def _is_procedural_qa(question: str, answer: str) -> bool:
    """
    Returns True only if the Q&A pair looks like generalizable procedural knowledge.
    Rejects: too short, or answer is mostly placeholders (account-specific interaction).
    """
    q_words = question.split()
    a_words = answer.split()
    if len(q_words) < _MIN_QUESTION_WORDS or len(a_words) < _MIN_ANSWER_WORDS:
        return False
    placeholder_count = sum(1 for w in a_words if w.startswith("[") and w.endswith("]"))
    if placeholder_count / len(a_words) > _MAX_PLACEHOLDER_RATIO:
        return False
    return True


async def run_pipeline(
    transcript_id: int,
    raw_text: str,
    db: AsyncSession,
) -> PipelineResult:
    audit.safe_log("start", transcript_id=transcript_id, chars=len(raw_text))

    normalized = normalize(raw_text)

    # Mask BEFORE anything else. NER runs in a thread to avoid blocking the event loop.
    masked_text, token_map = await asyncio.to_thread(mask, normalized)
    audit.safe_log("masked", transcript_id=transcript_id, entities=len(token_map))

    turns = split_turns(masked_text)
    if all(t.role == "unknown" for t in turns):
        # No speaker prefixes found (e.g. raw audio transcript) — use LLM to label.
        # Safe: masked_text has already had PII replaced; raw values never reach Groq.
        llm_turns = await label_speakers_llm(masked_text)
        if llm_turns:
            turns = llm_turns
    audit.safe_log("speakers", transcript_id=transcript_id, turns=len(turns))

    # Persist encrypted token map — raw values never leave this scope unencrypted.
    encrypted = encrypt_token_map(token_map)
    db.add(TokenMapRecord(transkript_id=transcript_id, encrypted_blob=encrypted))

    chunks = chunk_turns(turns)

    # turn_position → (first_segment_id, first_vector_id) — used to link Q&A pairs
    turn_repr: dict[int, tuple[int, str]] = {}

    for chunk in chunks:
        vector = await asyncio.to_thread(_embedder.embed, chunk.text)
        vector_id = str(uuid.uuid4())

        await asyncio.to_thread(
            _vector_store.index_item,
            vector_id,
            vector,
            {
                "transcript_id": transcript_id,
                "tip_segmenta": chunk.tip_segmenta,
                "position": chunk.position,
                "text": chunk.text,
            },
        )

        seg = Segment(
            tekst=chunk.text,
            tip_segmenta=chunk.tip_segmenta,
            pozicija_u_transkriptu=chunk.position,
            id_transkripta=transcript_id,
            status="Validan",
        )
        db.add(seg)
        await db.flush()

        if chunk.turn_position not in turn_repr:
            turn_repr[chunk.turn_position] = (seg.id, vector_id)

    qa_count = 0
    dropped_count = 0
    for i, turn in enumerate(turns):
        if turn.role == "user" and i + 1 < len(turns) and turns[i + 1].role == "agent":
            agent_turn = turns[i + 1]
            if not _is_procedural_qa(turn.text, agent_turn.text):
                dropped_count += 1
                continue
            seg_id, vec_id = turn_repr.get(turn.position, (None, None))
            db.add(UnosBazeZnanja(
                pitanje=turn.text,
                odgovor=agent_turn.text,
                id_segmenta=seg_id,
                vector_id=vec_id,
                status_aprovacije="NaCekanju",
            ))
            qa_count += 1

    audit.safe_log(
        "done",
        transcript_id=transcript_id,
        chunks=len(chunks),
        qa_pairs=qa_count,
        qa_dropped=dropped_count,
    )

    return PipelineResult(
        transcript_id=transcript_id,
        masked_text=masked_text,
        qa_pair_count=qa_count,
        chunk_count=len(chunks),
        entity_count=len(token_map),
    )
