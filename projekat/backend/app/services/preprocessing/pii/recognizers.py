import re
from dataclasses import dataclass


@dataclass
class Span:
    start: int
    end: int
    entity_type: str  # JMBG | KARTICA | IBAN | EMAIL | TELEFON


_JMBG = re.compile(r"\b(\d{13})\b")
_CARD = re.compile(r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b")
_IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[\s\-]?\d{4}){2,5}\b")
_EMAIL = re.compile(r"\b[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}\b")
_SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")       # US Social Security Number (XXX-XX-XXXX)
_PHONES = [
    re.compile(r"\b(\+?387|0)\s?6[0-9][\s\-]?\d{3}[\s\-]?\d{3}\b"),
    re.compile(r"\b0[1-5]\d[\s\-]?\d{3}[\s\-]?\d{3}\b"),
    re.compile(r"\+[1-9]\d{0,2}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}\b"),
]


def _jmbg_valid(jmbg: str) -> bool:
    d = [int(c) for c in jmbg]
    r = (
        7 * (d[0] + d[6]) + 6 * (d[1] + d[7]) + 5 * (d[2] + d[8]) +
        4 * (d[3] + d[9]) + 3 * (d[4] + d[10]) + 2 * (d[5] + d[11])
    ) % 11
    k = 11 - r
    if k == 10:
        return False
    expected = 0 if k == 11 else k
    return d[12] == expected


def find_structural_pii(text: str) -> list[Span]:
    spans: list[Span] = []

    for m in _JMBG.finditer(text):
        if _jmbg_valid(m.group()):
            spans.append(Span(m.start(), m.end(), "JMBG"))

    for m in _CARD.finditer(text):
        spans.append(Span(m.start(), m.end(), "KARTICA"))

    for m in _IBAN.finditer(text):
        spans.append(Span(m.start(), m.end(), "IBAN"))

    for m in _EMAIL.finditer(text):
        spans.append(Span(m.start(), m.end(), "EMAIL"))

    for m in _SSN.finditer(text):
        spans.append(Span(m.start(), m.end(), "SSN"))

    for pat in _PHONES:
        for m in pat.finditer(text):
            spans.append(Span(m.start(), m.end(), "TELEFON"))

    return spans
