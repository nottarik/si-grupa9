import re
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# PII masking patterns (GDPR)
# ---------------------------------------------------------------------------
PII_PATTERNS = [
    (r"\b\d{13}\b", "[JMBG]"),                          # JMBG
    (r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b", "[KARTICA]"),  # broj kartice
    (r"\b[\w.+-]+@[\w-]+\.[a-z]{2,}\b", "[EMAIL]"),     # email
    (r"\b(\+?387|0)\s?6[0-9][\s-]?\d{3}[\s-]?\d{3}\b", "[TELEFON]"),  # BiH mobitel
]


@dataclass
class ProcessedTranscript:
    raw_text: str
    normalized_text: str
    masked_text: str
    segments: list[dict]   # [{"role": "agent"|"user", "text": "..."}]
    qa_pairs: list[dict]   # [{"question": "...", "answer": "..."}]


class PipelineService:
    """
    Processes a raw transcript text through all pipeline stages:
      1. Normalize
      2. Split by role
      3. Mask PII
      4. Extract Q&A pairs
    """

    def process(self, raw_text: str) -> ProcessedTranscript:
        normalized = self._normalize(raw_text)
        segments = self._split_roles(normalized)
        masked_text = self._mask_pii(normalized)
        qa_pairs = self._extract_qa(segments)

        return ProcessedTranscript(
            raw_text=raw_text,
            normalized_text=normalized,
            masked_text=masked_text,
            segments=segments,
            qa_pairs=qa_pairs,
        )

    # ------------------------------------------------------------------
    def _normalize(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    def _split_roles(self, text: str) -> list[dict]:
        """
        Expects lines prefixed with 'Agent:' or 'Korisnik:'.
        Falls back to alternating turns if no prefix found.
        """
        segments = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith("agent:"):
                segments.append({"role": "agent", "text": line[6:].strip()})
            elif line.lower().startswith("korisnik:"):
                segments.append({"role": "user", "text": line[9:].strip()})
            else:
                segments.append({"role": "unknown", "text": line})
        return segments

    def _mask_pii(self, text: str) -> str:
        for pattern, replacement in PII_PATTERNS:
            text = re.sub(pattern, replacement, text)
        return text

    def _extract_qa(self, segments: list[dict]) -> list[dict]:
        """
        Simple heuristic: pair each user turn with the following agent turn.
        More sophisticated extraction can replace this later.
        """
        qa_pairs = []
        for i, seg in enumerate(segments):
            if seg["role"] == "user" and i + 1 < len(segments):
                next_seg = segments[i + 1]
                if next_seg["role"] == "agent":
                    qa_pairs.append({
                        "question": seg["text"],
                        "answer": next_seg["text"],
                    })
        return qa_pairs
