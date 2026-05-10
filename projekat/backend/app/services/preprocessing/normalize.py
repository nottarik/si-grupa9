import re
import unicodedata


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.strip()
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    for smart, plain in (
        ("‘", "'"), ("’", "'"),
        ("“", '"'), ("”", '"'),
    ):
        text = text.replace(smart, plain)
    return text
