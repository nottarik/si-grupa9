import asyncio
import json
import logging

from groq import Groq

from .models import Turn

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are labeling a call center transcript between a support agent and a customer.
The text may already contain line breaks or may be one continuous block.
PII has been replaced with placeholders like [PERSON_1], [TELEFON_1], [JMBG_1] — preserve them exactly.

Split the text into speaker turns and assign each a role.
Return ONLY valid JSON in this exact format:
{"turns": [{"role": "agent", "text": "..."}, {"role": "user", "text": "..."}, ...]}

Role assignment rules:
- "agent": greets the caller, confirms details, asks clarifying questions, explains procedures, offers help
- "user": states a problem, requests help, provides personal details, asks questions about a service
- If genuinely ambiguous use "unknown"

Do not add, change, or remove any words from the original text.
Do not include explanations outside the JSON.\
"""

_VALID_ROLES = {"agent", "user", "unknown"}


async def label_speakers_llm(masked_text: str) -> list[Turn]:
    """
    Ask Groq to segment and label speakers in a masked transcript.
    Returns [] on any failure so the caller can fall back gracefully.
    Only call this with already-masked text — never raw.
    """
    from app.core.config import settings

    if not settings.GROQ_API_KEY:
        return []

    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": masked_text},
            ],
            response_format={"type": "json_object"},
            max_tokens=4096,
            temperature=0.0,
        )
        raw = response.choices[0].message.content
        data = json.loads(raw)
        turns_data = data.get("turns", [])

        turns: list[Turn] = []
        for i, t in enumerate(turns_data):
            role = t.get("role", "unknown")
            text = t.get("text", "").strip()
            if not text:
                continue
            if role not in _VALID_ROLES:
                role = "unknown"
            turns.append(Turn(role=role, text=text, position=i))

        return turns

    except Exception as exc:
        logger.warning(
            "LLM speaker labeling failed; falling back to pattern detection. %s", exc
        )
        return []
