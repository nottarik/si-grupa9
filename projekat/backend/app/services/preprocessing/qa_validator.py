import asyncio
import json
import logging

from groq import Groq

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are a quality filter for a call center knowledge base.

You will receive a list of Q&A pairs extracted from a call transcript. PII has been
replaced with placeholders like [PERSON_1], [TELEFON_1].

For each pair, decide whether it is suitable as a standalone knowledge base entry.
Mark it TRUE only if ALL of the following hold:
- The question is self-contained and understandable without reading the transcript
- The answer provides concrete, actionable information useful to a support agent
- Placeholders do not make the meaning unrecoverable
  (e.g. "Contact [PERSON_1]" with no other info is unrecoverable — mark FALSE)
- The pair is not a greeting, small talk, or vague acknowledgement

Return ONLY valid JSON:
{"results": [true, false, ...]}

The array must have exactly the same number of elements as the input pairs.\
"""


async def validate_qa_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Return only pairs the LLM considers coherent, standalone KB entries.

    Fails open: if the LLM call errors or returns bad JSON, all pairs pass through.
    """
    if not pairs:
        return []

    from app.core.config import settings

    if not settings.GROQ_API_KEY:
        return pairs

    payload = [{"question": q, "answer": a} for q, a in pairs]
    user_content = json.dumps(payload, ensure_ascii=False)

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
            max_tokens=512,
            temperature=0.0,
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        results = data.get("results", [])

        if len(results) != len(pairs):
            logger.warning(
                "QA validator returned %d results for %d pairs; passing all through.",
                len(results),
                len(pairs),
            )
            return pairs

        return [pair for pair, keep in zip(pairs, results) if keep]

    except Exception as exc:
        logger.warning("QA validation failed; passing all pairs through. %s", exc)
        return pairs
