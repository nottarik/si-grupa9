import asyncio
import json
import logging

from groq import Groq

from .models import Turn

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are extracting question-answer pairs from a call center transcript.
The transcript has been labeled with speaker roles: "user" (customer) and "agent" (support).

Extract Q&A pairs where:
- The question is a self-contained customer inquiry, request, or problem statement
- The answer is the agent's complete response or resolution
- Combine multi-turn exchanges about the same topic into a single Q&A pair
- Rephrase questions to be self-contained (avoid pronouns like "it" or "that" without context)
- Keep answers informative — include the procedure, resolution, or information the agent provided
- PII has been replaced with placeholders like [PERSON_1], [TELEFON_1] — preserve them exactly
- Skip greetings, small talk, and turns that don't contain actionable information

Return ONLY valid JSON in this exact format:
{"pairs": [{"question": "...", "answer": "..."}, ...]}

If no meaningful Q&A pairs can be extracted, return {"pairs": []}.\
"""


async def extract_qa_pairs_llm(turns: list[Turn]) -> list[tuple[str, str]]:
    from app.core.config import settings

    if not settings.GROQ_API_KEY:
        return []

    conversation = "\n".join(f"{t.role}: {t.text}" for t in turns)

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": conversation},
            ],
            response_format={"type": "json_object"},
            max_tokens=4096,
            temperature=0.0,
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        pairs_data = data.get("pairs", [])

        pairs: list[tuple[str, str]] = []
        for p in pairs_data:
            q = p.get("question", "").strip()
            a = p.get("answer", "").strip()
            if q and a:
                pairs.append((q, a))

        return pairs

    except Exception as exc:
        logger.warning("LLM Q&A extraction failed; falling back to pattern matching. %s", exc)
        return []
