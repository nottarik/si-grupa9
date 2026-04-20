from groq import Groq
from app.core.config import settings

SYSTEM_PROMPT = """
Ti si AI asistent za call centar. Odgovaraš isključivo na osnovu dostavljenog konteksta.
Ako kontekst ne sadrži dovoljno informacija, jasno naznači da nisi siguran i preporuči
korisnika da kontaktira agenta.
Odgovaraj kratko, jasno i ljubazno na bosanskom/srpskom/hrvatskom jeziku.
"""


class LLMService:
    """Wraps Groq API for LLM completions."""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_MODEL

    def generate(self, question: str, context: str) -> str:
        user_message = f"Kontekst:\n{context}\n\nPitanje korisnika:\n{question}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=512,
            temperature=0.2,
        )
        return response.choices[0].message.content
