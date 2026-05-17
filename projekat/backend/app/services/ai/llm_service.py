from groq import Groq
from app.core.config import settings

_SYSTEM_WITH_CONTEXT = """
You are an AI assistant for a call center. Answer strictly based on the provided context.
If the context does not contain enough information, clearly state that you are not sure
and recommend the user contact an agent.
Keep answers short, clear, and helpful.
The context may contain masked placeholders such as [PERSON_1] or [ORGANIZACIJA_1] representing redacted private data.
Never include these bracket tokens in your answer. Write as if those specific values are unknown or irrelevant to the answer.
"""

_SYSTEM_REWRITE = """
You are a search query rewriter for a call center knowledge base.
Given a conversation history and the user's latest message, rewrite the latest message
into a single self-contained search query that can be understood without any context.
Output ONLY the rewritten query — no explanation, no punctuation outside the query itself.
If the latest message is already self-contained, return it unchanged.
"""

_SYSTEM_NO_CONTEXT = """
You are an AI assistant for a call center. You have no knowledge base entry for this question.
You may answer general, conversational, or common-knowledge questions (greetings, definitions,
general how-to) from your own knowledge.
For anything company-specific — policies, pricing, account details, procedures, product specifics —
do NOT guess. Instead tell the user you don't have that information and recommend they contact an agent.
Keep answers short, clear, and helpful.
"""

_SYSTEM_CLASSIFY = (
    "Classify the user's message with exactly one word. "
    "Reply \"conversational\" if it is a greeting, small talk, or a general-knowledge question "
    "unrelated to company services (e.g. \"hello\", \"how are you\", \"what is AI\"). "
    "Reply \"domain\" if it asks about company products, services, accounts, policies, "
    "procedures, pricing, or any support topic that requires company knowledge."
)


class LLMService:
    """Wraps Groq API for LLM completions."""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL

    def generate(self, question: str, context: str, history: list[dict] | None = None) -> str:
        messages: list[dict] = [{"role": "system", "content": _SYSTEM_WITH_CONTEXT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": f"Context:\n{context}\n\nUser question:\n{question}"})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=512,
            temperature=0.2,
        )
        return response.choices[0].message.content

    def rewrite_query(self, question: str, history: list[dict]) -> str:
        messages: list[dict] = [{"role": "system", "content": _SYSTEM_REWRITE}]
        messages.extend(history)
        messages.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=64,
            temperature=0.0,
        )
        return response.choices[0].message.content.strip()

    def generate_without_context(self, question: str, history: list[dict] | None = None) -> str:
        messages: list[dict] = [{"role": "system", "content": _SYSTEM_NO_CONTEXT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=256,
            temperature=0.1,
        )
        return response.choices[0].message.content

    def classify_intent(self, question: str) -> str:
        """Returns 'conversational' or 'domain'."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": _SYSTEM_CLASSIFY},
                {"role": "user", "content": question},
            ],
            max_tokens=5,
            temperature=0.0,
        )
        raw = response.choices[0].message.content.strip().lower()
        return "conversational" if "convers" in raw else "domain"
