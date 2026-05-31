"""Live state of the Drive importer, shared by the scheduler and the import task and
surfaced to the admin UI (so a run is visible while it happens).

In-memory is fine: the scheduler, the import task, and the API all run in one process
(single always-warm replica). Kept in its own tiny module so both the generic import
task and the scheduler can touch it without importing each other.
"""

_STATE: dict = {"running": False, "last_result": None}


def mark_running() -> None:
    _STATE["running"] = True


def mark_done(result: str | None = None) -> None:
    _STATE["running"] = False
    if result is not None:
        _STATE["last_result"] = result


def snapshot() -> dict:
    return dict(_STATE)
