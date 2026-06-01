import asyncio
import json
import logging

from groq import Groq

logger = logging.getLogger(__name__)

# Only name/location masks are fallible; structural PII (JMBG, card, phone, …)
# is matched by deterministic regexes and is never second-guessed here.
_FALLIBLE_TYPES = ("PERSON", "LOKACIJA")

_SYSTEM_PROMPT = """\
You are a PII filter for a Bosnian/English call center transcript.
You receive a JSON list of words or phrases that an automatic detector flagged as
possible person names or place names. The detector is noisy and often flags ordinary
capitalized words (e.g. sentence-initial adverbs like "Simply").

Return ONLY the items that are genuinely the personal name of an individual or a
specific geographic location (real PII). Exclude everything else: common words,
verbs, adverbs, greetings, generic nouns, job titles, and company/product/brand names.

Return ONLY valid JSON in this exact format: {"pii": ["<item>", ...]}
Each returned string must be copied exactly from the input list. If none qualify,
return {"pii": []}.\
"""


def _placeholder_type(placeholder: str) -> str:
    # "[PERSON_1]" -> "PERSON"
    return placeholder[1:-1].rsplit("_", 1)[0]


async def _confirmed_pii(surfaces: list[str]) -> set[str]:
    """Ask the LLM which candidate strings are genuine name/location PII.

    Fails safe toward masking: on a missing key or any error, treats every
    candidate as PII (keep masking) so nothing is wrongly unmasked.
    """
    from app.core.config import settings

    if not settings.GROQ_API_KEY:
        return set(surfaces)

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
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
        by_norm = {s.strip().casefold(): s for s in surfaces}
        result: set[str] = set()
        for c in confirmed:
            if isinstance(c, str):
                original = by_norm.get(c.strip().casefold())
                if original is not None:
                    result.add(original)
        return result
    except Exception as exc:
        logger.warning("Name verification failed; keeping all masks. %s", exc)
        return set(surfaces)


async def drop_false_positive_names(
    masked_text: str, token_map: dict[str, str]
) -> tuple[str, dict[str, str]]:
    """Restore name/location placeholders whose original value is not real PII.

    The noisy NER model masks ordinary capitalized words (e.g. "Simply" -> [PERSON_1]).
    Using the token_map originals, the LLM confirms which are genuine names/locations;
    the rest are restored to their original text and dropped from the token_map.
    """
    candidates = {
        ph: orig for ph, orig in token_map.items()
        if _placeholder_type(ph) in _FALLIBLE_TYPES
    }
    if not candidates:
        return masked_text, token_map

    keep = await _confirmed_pii(list(set(candidates.values())))

    restored = masked_text
    new_map = dict(token_map)
    for ph, orig in candidates.items():
        if orig not in keep:
            restored = restored.replace(ph, orig)
            new_map.pop(ph, None)
    return restored, new_map
