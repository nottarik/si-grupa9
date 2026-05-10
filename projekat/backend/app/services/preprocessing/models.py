from dataclasses import dataclass


@dataclass
class Turn:
    role: str  # "agent" | "user" | "unknown"
    text: str  # masked text
    position: int


@dataclass
class Chunk:
    text: str         # masked text
    position: int
    tip_segmenta: str  # "Pitanje" | "Odgovor" | "Kontekst"
    turn_position: int  # position of the source Turn


@dataclass
class PipelineResult:
    transcript_id: int
    masked_text: str
    qa_pair_count: int
    chunk_count: int
    entity_count: int
