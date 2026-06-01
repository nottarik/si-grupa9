import asyncio
import logging
import re

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.transcript import Segment, TokenMapRecord
from app.db.models.knowledge import UnosBazeZnanja
from .models import PipelineResult
from .normalize import normalize
from .speakers import split_turns
from .speakers_llm import label_speakers_llm
from .chunking import chunk_turns
from .qa_extractor import extract_qa_pairs_llm
from .qa_validator import validate_qa_pairs
from .qa_scrubber import scrub_placeholders
from .pii.masker import mask
from .pii.name_verifier import drop_false_positive_names
from .pii.token_store import encrypt_token_map
from . import audit

logger = logging.getLogger(__name__)

_SPEAKER_PREFIX_RE = re.compile(
    r'^(\s*(?:USER|KORISNIK|AGENT|AGENTICA|OPERATOR|OPERATER|CUSTOMER|KLIJENT|CALLER)\s*:)',
    re.IGNORECASE | re.MULTILINE,
)


def _protect_prefixes(text: str) -> tuple[str, list[tuple[str, str]]]:
    replacements: list[tuple[str, str]] = []
    counter = [0]

    def _replace(m: re.Match) -> str:
        token = f"SPKR{counter[0]:03d}X"
        replacements.append((token, m.group(1)))
        counter[0] += 1
        return token

    protected = _SPEAKER_PREFIX_RE.sub(_replace, text)
    return protected, replacements


def _restore_prefixes(text: str, replacements: list[tuple[str, str]]) -> str:
    for token, original in replacements:
        text = text.replace(token, original)
    return text

_MIN_QUESTION_WORDS = 3
_MIN_ANSWER_WORDS = 5
_MAX_PLACEHOLDER_RATIO = 0.30


def _is_procedural_qa(question: str, answer: str) -> bool:
    q_words = question.split()
    a_words = answer.split()
    if len(q_words) < _MIN_QUESTION_WORDS or len(a_words) < _MIN_ANSWER_WORDS:
        return False
    placeholder_count = sum(1 for w in a_words if w.startswith("[") and w.endswith("]"))
    if placeholder_count / len(a_words) > _MAX_PLACEHOLDER_RATIO:
        return False
    return True


def _extract_qa_pattern(turns: list, turn_first_seg: dict[int, int]) -> list[tuple[str, str, int | None]]:
    pairs: list[tuple[str, str, int | None]] = []
    for i, turn in enumerate(turns):
        if turn.role == "user" and i + 1 < len(turns) and turns[i + 1].role == "agent":
            agent_turn = turns[i + 1]
            if not _is_procedural_qa(turn.text, agent_turn.text):
                continue
            pairs.append((turn.text, agent_turn.text, turn_first_seg.get(turn.position)))
    return pairs


async def run_pipeline(
    transcript_id: int,
    raw_text: str,
    db: AsyncSession,
) -> PipelineResult:
    audit.safe_log("start", transcript_id=transcript_id, chars=len(raw_text))

    normalized = normalize(raw_text)

    protected, prefix_map = _protect_prefixes(normalized)
    masked_text, token_map = await asyncio.to_thread(mask, protected)
    masked_text = _restore_prefixes(masked_text, prefix_map)
    # Undo noisy NER false positives (e.g. "Simply" wrongly masked as [PERSON_1]).
    masked_text, token_map = await drop_false_positive_names(masked_text, token_map)
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

    turn_first_seg: dict[int, int] = {}

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

    llm_pairs = await extract_qa_pairs_llm(turns)

    if llm_pairs:
        raw_count = len(llm_pairs)
        llm_pairs = await validate_qa_pairs(llm_pairs)
        llm_pairs = await scrub_placeholders(llm_pairs)
        qa_count = 0
        for question, answer in llm_pairs:
            db.add(UnosBazeZnanja(
                pitanje=question,
                odgovor=answer,
                id_segmenta=None,
                # Live in the KB (Odobren) but not yet human-reviewed; embedded by the
                # resumable embed_pending() sweep after this atomic commit.
                status_aprovacije="Odobren",
                pregledano=False,
            ))
            qa_count += 1
        audit.safe_log(
            "done",
            transcript_id=transcript_id,
            chunks=len(chunks),
            qa_pairs=qa_count,
            qa_filtered=raw_count - qa_count,
            qa_method="llm",
        )
    else:
        pattern_pairs = _extract_qa_pattern(turns, turn_first_seg)
        raw_count = len(pattern_pairs)
        texts = [(q, a) for q, a, _ in pattern_pairs]
        valid_texts = set(await validate_qa_pairs(texts))
        pattern_pairs = [(q, a, s) for q, a, s in pattern_pairs if (q, a) in valid_texts]
        seg_ids = [s for _, _, s in pattern_pairs]
        scrubbed = await scrub_placeholders([(q, a) for q, a, _ in pattern_pairs])
        pattern_pairs = [(q, a, s) for (q, a), s in zip(scrubbed, seg_ids)]
        qa_count = 0
        for question, answer, seg_id in pattern_pairs:
            db.add(UnosBazeZnanja(
                pitanje=question,
                odgovor=answer,
                id_segmenta=seg_id,
                # Live in the KB (Odobren) but not yet human-reviewed; embedded by the
                # resumable embed_pending() sweep after this atomic commit.
                status_aprovacije="Odobren",
                pregledano=False,
            ))
            qa_count += 1
        audit.safe_log(
            "done",
            transcript_id=transcript_id,
            chunks=len(chunks),
            qa_pairs=qa_count,
            qa_filtered=raw_count - qa_count,
            qa_method="pattern",
        )

    return PipelineResult(
        transcript_id=transcript_id,
        masked_text=masked_text,
        qa_pair_count=qa_count,
        chunk_count=len(chunks),
        entity_count=len(token_map),
    )
