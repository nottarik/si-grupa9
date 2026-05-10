from .models import Turn, Chunk

_MAX_WORDS = 200
_OVERLAP_WORDS = 30


def _tip_for_role(role: str) -> str:
    if role == "user":
        return "Pitanje"
    if role == "agent":
        return "Odgovor"
    return "Kontekst"


def chunk_turns(turns: list[Turn]) -> list[Chunk]:
    chunks: list[Chunk] = []
    position = 0

    for turn in turns:
        words = turn.text.split()
        if not words:
            continue
        tip = _tip_for_role(turn.role)

        if len(words) <= _MAX_WORDS:
            chunks.append(Chunk(text=turn.text, position=position, tip_segmenta=tip, turn_position=turn.position))
            position += 1
        else:
            i = 0
            while i < len(words):
                chunk_text = " ".join(words[i:i + _MAX_WORDS])
                chunks.append(Chunk(text=chunk_text, position=position, tip_segmenta=tip, turn_position=turn.position))
                position += 1
                i += _MAX_WORDS - _OVERLAP_WORDS

    return chunks
