from .models import Turn

_PREFIXES: list[tuple[list[str], str]] = [
    (["agent:", "agentica:", "operator:", "operater:"], "agent"),
    (["korisnik:", "customer:", "klijent:", "caller:"], "user"),
]


def split_turns(text: str) -> list[Turn]:
    turns: list[Turn] = []
    position = 0
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        low = line.lower()
        role = "unknown"
        content = line
        for prefixes, r in _PREFIXES:
            for p in prefixes:
                if low.startswith(p):
                    role = r
                    content = line[len(p):].strip()
                    break
            else:
                continue
            break
        if content:
            turns.append(Turn(role=role, text=content, position=position))
            position += 1
    return turns
