from .recognizers import Span, find_structural_pii
from .ner import find_named_entities


def _resolve(spans: list[Span]) -> list[Span]:
    """Remove overlapping spans, keeping longest. Sorts by position."""
    spans = sorted(spans, key=lambda s: (s.start, -(s.end - s.start)))
    result: list[Span] = []
    end = -1
    for span in spans:
        if span.start >= end:
            result.append(span)
            end = span.end
    return result


def mask(text: str) -> tuple[str, dict[str, str]]:
    """
    Returns (masked_text, token_map).
    token_map maps each placeholder to its original value, e.g. {"[PERSON_1]": "Tarik"}.
    Same original value always gets the same placeholder within one call.
    """
    all_spans = find_structural_pii(text) + find_named_entities(text)
    resolved = _resolve(all_spans)

    seen: dict[str, str] = {}      # original → placeholder
    counters: dict[str, int] = {}  # entity_type → count
    token_map: dict[str, str] = {} # placeholder → original

    parts: list[str] = []
    pos = 0
    for span in resolved:
        parts.append(text[pos:span.start])
        original = text[span.start:span.end]
        if original not in seen:
            counters[span.entity_type] = counters.get(span.entity_type, 0) + 1
            placeholder = f"[{span.entity_type}_{counters[span.entity_type]}]"
            seen[original] = placeholder
            token_map[placeholder] = original
        parts.append(seen[original])
        pos = span.end
    parts.append(text[pos:])

    return "".join(parts), token_map
