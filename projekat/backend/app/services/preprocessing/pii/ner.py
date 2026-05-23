import logging
from typing import Any

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


def find_named_entities(text: str) -> list[Span]:
    """Detect person names, locations, and organizations via spaCy NER."""
    nlp = _get_nlp()
    if nlp is None:
        return []
    doc = nlp(text)
    spans = []
    for ent in doc.ents:
        if ent.label_ not in _LABEL_MAP:
            continue
        surface = ent.text
        # Drop very short tokens and common conversational words (xx model is noisy)
        if len(surface) <= 2:
            continue
        if surface.lower() in _COMMON_WORDS:
            continue
        spans.append(Span(ent.start_char, ent.end_char, _LABEL_MAP[ent.label_]))
    return spans
