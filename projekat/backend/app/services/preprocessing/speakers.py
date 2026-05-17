from .models import Turn

_PREFIXES: list[tuple[list[str], str]] = [
    (["agent:", "agentica:", "operator:", "operater:"], "agent"),
    (["user:", "korisnik:", "customer:", "klijent:", "caller:"], "user"),
]


def split_turns(text: str) -> list[Turn]:
    raw_turns: list[Turn] = []
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
            raw_turns.append(Turn(role=role, text=content, position=position))
            position += 1

    if not raw_turns:
        return raw_turns

    merged: list[Turn] = [raw_turns[0]]
    for turn in raw_turns[1:]:
        prev = merged[-1]
        if turn.role == prev.role and turn.role != "unknown":
            merged[-1] = Turn(
                role=prev.role,
                text=f"{prev.text} {turn.text}",
                position=prev.position,
            )
        else:
            merged.append(Turn(role=turn.role, text=turn.text, position=len(merged)))

    return merged
