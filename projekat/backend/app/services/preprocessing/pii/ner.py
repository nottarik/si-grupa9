import json
import logging
from typing import Any

from groq import Groq

from .recognizers import Span

logger = logging.getLogger(__name__)

_nlp: Any = None
_nlp_loaded = False

_LABEL_MAP = {
    "PER":    "PERSON",
    "PERSON": "PERSON",
    "LOC":    "LOKACIJA",
    # ORG omitted — noisy on call-center content; product/service names are not PII
}


def _get_nlp() -> Any:
    global _nlp, _nlp_loaded
    if not _nlp_loaded:
        _nlp_loaded = True
        try:
            import spacy
            _nlp = spacy.load("xx_ent_wiki_sm")
        except Exception as exc:
            logger.warning("spaCy NER unavailable; name/location/org detection disabled. %s", exc)
            _nlp = None
    return _nlp


_COMMON_WORDS = frozenset({
    "yes", "no", "ok", "okay", "hi", "hello", "thanks", "thank", "sure",
    "right", "well", "please", "bye", "goodbye", "sorry", "great", "good",
    "fine", "nice", "alright", "yep", "nope", "yeah", "nah",
})


_VERIFY_SYSTEM_PROMPT = """\
You are a PII filter for a Bosnian/English call center transcript.
You receive a JSON list of candidate words or phrases that an automatic detector
flagged as possible person names or place names. The detector is noisy and often
flags ordinary capitalized words (e.g. sentence-initial adverbs like "Simply").

Return ONLY the candidates that are genuinely the personal name of an individual
or a specific geographic location (real PII). Exclude everything else: common
words, verbs, adverbs, greetings, generic nouns, job titles, and company,
product, or brand names.

Return ONLY valid JSON in this exact format: {"pii": ["<candidate>", ...]}
Each returned string must be copied exactly from the input list. If none qualify,
return {"pii": []}.\
"""


def _verify_pii_candidates(surfaces: list[str]) -> set[str]:
    """Ask the LLM which candidate strings are genuine name/location PII.

    Fails safe toward masking: on a missing key or any error, returns every
    candidate (keep masking) so PII is never under-masked when the LLM is down.
    """
    from app.core.config import settings

    if not settings.GROQ_API_KEY:
        return set(surfaces)

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": _VERIFY_SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(surfaces, ensure_ascii=False)},
            ],
            response_format={"type": "json_object"},
            max_tokens=512,
            temperature=0.0,
        )
        data = json.loads(response.choices[0].message.content)
        confirmed = data.get("pii", [])
        if not isinstance(confirmed, list):
            return set(surfaces)

        # Match the model's answer back to the exact original surfaces,
        # tolerating case/whitespace drift in the echoed strings.
        by_norm = {s.strip().casefold(): s for s in surfaces}
        result: set[str] = set()
        for c in confirmed:
            if isinstance(c, str):
                original = by_norm.get(c.strip().casefold())
                if original is not None:
                    result.add(original)
        return result

    except Exception as exc:
        logger.warning("PII candidate verification failed; keeping all candidates. %s", exc)
        return set(surfaces)


def find_named_entities(text: str) -> list[Span]:
    """Detect person names and locations via spaCy NER, then drop false
    positives by verifying the candidates with the LLM."""
    nlp = _get_nlp()
    if nlp is None:
        return []
    doc = nlp(text)
    candidates: list[Span] = []
    for ent in doc.ents:
        if ent.label_ not in _LABEL_MAP:
            continue
        surface = ent.text
        # Drop very short tokens and common conversational words (xx model is noisy)
        if len(surface) <= 2:
            continue
        if surface.lower() in _COMMON_WORDS:
            continue
        candidates.append(Span(ent.start_char, ent.end_char, _LABEL_MAP[ent.label_]))

    if not candidates:
        return []

    surfaces = list({text[s.start:s.end] for s in candidates})
    confirmed = _verify_pii_candidates(surfaces)
    return [s for s in candidates if text[s.start:s.end] in confirmed]
