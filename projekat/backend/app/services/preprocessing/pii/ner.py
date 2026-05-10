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
    "ORG":    "ORGANIZACIJA",
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


def find_named_entities(text: str) -> list[Span]:
    """Detect person names, locations, and organizations via spaCy NER."""
    nlp = _get_nlp()
    if nlp is None:
        return []
    doc = nlp(text)
    return [
        Span(ent.start_char, ent.end_char, _LABEL_MAP[ent.label_])
        for ent in doc.ents
        if ent.label_ in _LABEL_MAP
    ]
