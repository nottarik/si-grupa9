"""Live state of the Drive importer, shared by the scheduler and the import task and
surfaced to the admin UI (so a run is visible while it happens).

In-memory is fine: the scheduler, the import task, and the API all run in one process
(single always-warm replica). Kept in its own tiny module so both the generic import
task and the scheduler can touch it without importing each other.
"""

_STATE: dict = {"running": False, "last_result": None, "cancelling": False, "files": []}


def mark_running() -> None:
    _STATE["running"] = True
    _STATE["cancelling"] = False  # clear any stale cancel from a previous run
    _STATE["files"] = []  # fresh per-file progress for this run


def mark_done(result: str | None = None) -> None:
    _STATE["running"] = False
    _STATE["cancelling"] = False
    if result is not None:
        _STATE["last_result"] = result


def set_files(names: list[str]) -> None:
    """Seed the live per-file list as soon as the folder is listed, so the UI can show
    the titles being imported right away (all start as ``pending``)."""
    _STATE["files"] = [{"name": n, "status": "pending"} for n in names]


def update_file(name: str, status: str) -> None:
    for f in _STATE["files"]:
        if f["name"] == name:
            f["status"] = status
            return


def request_cancel() -> bool:
    """Ask the running import to stop after the current file. Returns True if an
    import was actually running (nothing to cancel otherwise)."""
    if _STATE["running"]:
        _STATE["cancelling"] = True
        return True
    return False


def is_cancelling() -> bool:
    return _STATE["cancelling"]


def snapshot() -> dict:
    snap = dict(_STATE)
    snap["files"] = [dict(f) for f in _STATE["files"]]  # copy so callers can't mutate state
    return snap
