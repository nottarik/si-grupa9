import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.transcript import Segment, TokenMapRecord
from app.db.models.knowledge import UnosBazeZnanja
from .models import PipelineResult
from .normalize import normalize
from .speakers import split_turns
from .speakers_llm import label_speakers_llm
from .chunking import chunk_turns
from .pii.masker import mask
from .pii.token_store import encrypt_token_map
from . import audit

logger = logging.getLogger(__name__)

_MIN_QUESTION_WORDS = 5
_MIN_ANSWER_WORDS = 10
_MAX_PLACEHOLDER_RATIO = 0.15


def _is_procedural_qa(question: str, answer: str) -> bool:
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

    masked_text, token_map = await asyncio.to_thread(mask, normalized)
    audit.safe_log("masked", transcript_id=transcript_id, entities=len(token_map))

    turns = split_turns(masked_text)
    if all(t.role == "unknown" for t in turns):
        llm_turns = await label_speakers_llm(masked_text)
        if llm_turns:
            turns = llm_turns
    audit.safe_log("speakers", transcript_id=transcript_id, turns=len(turns))

    encrypted = encrypt_token_map(token_map)
    db.add(TokenMapRecord(transkript_id=transcript_id, encrypted_blob=encrypted))

    chunks = chunk_turns(turns)

    # Save segments — no embedding here, done at approval time to avoid OOM on free tier
    turn_first_seg: dict[int, int] = {}  # turn_position → first segment id

    for chunk in chunks:
        seg = Segment(
            tekst=chunk.text,
            tip_segmenta=chunk.tip_segmenta,
            pozicija_u_transkriptu=chunk.position,
            id_transkripta=transcript_id,
            status="Validan",
        )
        db.add(seg)
        await db.flush()
        if chunk.turn_position not in turn_first_seg:
            turn_first_seg[chunk.turn_position] = seg.id

    qa_count = 0
    dropped_count = 0
    for i, turn in enumerate(turns):
        if turn.role == "user" and i + 1 < len(turns) and turns[i + 1].role == "agent":
            agent_turn = turns[i + 1]
            if not _is_procedural_qa(turn.text, agent_turn.text):
                dropped_count += 1
                continue
            db.add(UnosBazeZnanja(
                pitanje=turn.text,
                odgovor=agent_turn.text,
                id_segmenta=turn_first_seg.get(turn.position),
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
