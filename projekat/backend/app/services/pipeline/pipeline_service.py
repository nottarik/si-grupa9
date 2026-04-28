import re
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# PII masking patterns (GDPR / privacy)
# Order matters: more specific patterns first.
# ---------------------------------------------------------------------------
PII_PATTERNS: list[tuple[str, str]] = [
    # JMBG — BiH/YU national ID (13 digits)
    (r"\b\d{13}\b", "[JMBG]"),
    # Credit/debit card numbers (4×4 digit groups, optional separators)
    (r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b", "[KARTICA]"),
    # IBAN (e.g. BA39 1234 5678 9012 3456)
    (r"\b[A-Z]{2}\d{2}(?:[\s\-]?\d{4}){2,5}\b", "[IBAN]"),
    # Email addresses
    (r"\b[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}\b", "[EMAIL]"),
    # BiH mobile: 06x-xxx-xxx (with/without +387 prefix)
    (r"\b(\+?387|0)\s?6[0-9][\s\-]?\d{3}[\s\-]?\d{3}\b", "[TELEFON]"),
    # BiH/HR fixed line: 0[1-5]x-xxx-xxx
    (r"\b0[1-5]\d[\s\-]?\d{3}[\s\-]?\d{3}\b", "[TELEFON]"),
    # International phone with + prefix
    (r"\+[1-9]\d{0,2}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}\b", "[TELEFON]"),
    # Name after common Bosnian/English introductory phrases
    # Keeps the phrase and replaces only the name(s)
    (
        r"(?i)((?:my name is|i am|i'm|zovem se|moje ime je|ime mi je|ja sam)\s+)"
        r"([A-ZČŠŽĐ][a-zčšžđ]+(?:\s+[A-ZČŠŽĐ][a-zčšžđ]+)?)",
        r"\1[IME]",
    ),
]


@dataclass
class ProcessedTranscript:
    raw_text: str
    normalized_text: str
    masked_text: str
    segments: list[dict]   # [{"role": "agent"|"user"|"unknown", "text": "..."}]
    qa_pairs: list[dict]   # [{"question": "...", "answer": "..."}]


class PipelineService:
    """
    Processes a raw transcript through all pipeline stages:
      1. Normalize whitespace / line endings
      2. Split into role-labelled segments
      3. Mask PII (GDPR)
      4. Extract Q&A pairs for knowledge base
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
        Expects lines prefixed with 'Agent:' or 'Korisnik:' / 'Customer:'.
        Falls back to 'unknown' role when no prefix is found.
        """
        segments: list[dict] = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            low = line.lower()
            if low.startswith("agent:"):
                segments.append({"role": "agent", "text": line[6:].strip()})
            elif low.startswith("korisnik:") or low.startswith("customer:"):
                cut = 9 if low.startswith("korisnik:") else 9
                segments.append({"role": "user", "text": line[cut:].strip()})
            else:
                segments.append({"role": "unknown", "text": line})
        return segments

    def _mask_pii(self, text: str) -> str:
        for pattern, replacement in PII_PATTERNS:
            text = re.sub(pattern, replacement, text)
        return text

    def _extract_qa(self, segments: list[dict]) -> list[dict]:
        """Pair each user turn with the following agent turn."""
        qa_pairs: list[dict] = []
        for i, seg in enumerate(segments):
            if seg["role"] == "user" and i + 1 < len(segments):
                nxt = segments[i + 1]
                if nxt["role"] == "agent":
                    qa_pairs.append({"question": seg["text"], "answer": nxt["text"]})
        return qa_pairs
