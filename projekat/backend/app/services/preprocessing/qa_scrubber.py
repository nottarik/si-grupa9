import asyncio
import json
import logging
import re

from groq import Groq

logger = logging.getLogger(__name__)

_PLACEHOLDER_RE = re.compile(r"\[[A-Z]+_\d+\]")

# Natural generic wording per entity type, used as the deterministic fallback
# when the LLM rewrite is unavailable so no raw tokens ever reach the KB.
_GENERIC_BY_TYPE = {
    "PERSON":       "korisnik",
    "LOKACIJA":     "lokacija",
    "ORGANIZACIJA": "organizacija",
    "TELEFON":      "broj telefona",
    "EMAIL":        "email adresa",
    "JMBG":         "JMBG",
    "KARTICA":      "broj kartice",
    "IBAN":         "IBAN broj",
    "SSN":          "matični broj",
}

_SYSTEM_PROMPT = """\
You rewrite call-center knowledge base Q&A pairs to remove automatic PII redaction tokens.
The text may contain tokens like [PERSON_1], [TELEFON_1], [EMAIL_1], [LOKACIJA_1].

Rewrite each question and answer so these tokens are gone, replaced by natural generic
wording (e.g. "[PERSON_1]" -> "korisnik" / "vlasnik računa", "[TELEFON_1]" -> "broj telefona").
Keep the original language (Bosnian or English), the meaning, and the formatting.
Do not invent facts. Do not leave any square-bracket tokens.

Return ONLY valid JSON: {"pairs": [{"question": "...", "answer": "..."}, ...]}
The array must have exactly the same number of elements, in the same order, as the input.\
"""


def _strip_generic(text: str) -> str:
    """Replace every [TYPE_n] token with its generic wording. No-op if none."""
    def repl(m: re.Match) -> str:
        etype = m.group()[1:-1].rsplit("_", 1)[0]
        return _GENERIC_BY_TYPE.get(etype, "podatak")
    return _PLACEHOLDER_RE.sub(repl, text)


async def _rewrite_llm(pairs: list[tuple[str, str]]) -> list[tuple[str, str]] | None:
    """Rewrite pairs via Groq. Returns None on any failure so the caller falls back."""
    from app.core.config import settings

    payload = [{"question": q, "answer": a} for q, a in pairs]
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            response_format={"type": "json_object"},
            max_tokens=2048,
            temperature=0.0,
        )
        data = json.loads(response.choices[0].message.content)
        out = data.get("pairs", [])
        if len(out) != len(pairs):
            logger.warning(
                "QA scrub returned %d pairs for %d; using deterministic fallback.",
                len(out), len(pairs),
            )
            return None

        result: list[tuple[str, str]] = []
        for item, (orig_q, orig_a) in zip(out, pairs):
            # Always pass output through _strip_generic as a safety net in case
            # the model echoed a token back; it's a no-op when none remain.
            q = _strip_generic(item.get("question", "").strip())
            a = _strip_generic(item.get("answer", "").strip())
            if not q or not a:
                q, a = _strip_generic(orig_q), _strip_generic(orig_a)
            result.append((q, a))
        return result

    except Exception as exc:
        logger.warning("QA scrub failed; using deterministic fallback. %s", exc)
        return None


async def scrub_placeholders(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Rewrite KB-bound Q&A so PII placeholders become natural wording.

    Only call this on knowledge-base text — never on segments, which must keep
    the reversible masked form. Pairs with no placeholders are returned unchanged
    with no LLM call. Falls back to deterministic generic substitution when the
    LLM is unavailable, so raw tokens never reach the knowledge base.
    """
    if not pairs:
        return []

    if not any(_PLACEHOLDER_RE.search(q) or _PLACEHOLDER_RE.search(a) for q, a in pairs):
        return pairs

    from app.core.config import settings
    if settings.GROQ_API_KEY:
        rewritten = await _rewrite_llm(pairs)
        if rewritten is not None:
            return rewritten

    return [(_strip_generic(q), _strip_generic(a)) for q, a in pairs]
