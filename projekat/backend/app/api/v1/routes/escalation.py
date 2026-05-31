import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user, require_admin_or_agent
from app.core.security import decode_token
from app.db.models.escalation import Eskalacija, StatusAgenta
from app.db.models.user import Korisnik, UlogaTip
from app.db.session import get_db
from app.schemas.escalation import AgentStatusUpdate, EscalationResolve
from app.schemas.escalation import EscalationInfo
from app.services.escalation import service as eskal_svc
from app.services.ws.connection_manager import manager

router = APIRouter(prefix="/escalation", tags=["escalation"])
logger = logging.getLogger(__name__)

# Grace period before an in-progress chat is auto-ended after the user drops off.
USER_GRACE_SECONDS = 15
# session_id → pending auto-end task (cancelled if the user reconnects in time).
_user_grace_tasks: dict[int, asyncio.Task] = {}


async def _grace_end_escalation(session_id: int, escalation_id: int) -> None:
    """After the grace window, if the user hasn't reconnected, end the escalation:
    notify the assigned agent, free them, and close the session."""
    try:
        await asyncio.sleep(USER_GRACE_SECONDS)
    except asyncio.CancelledError:
        return
    finally:
        _user_grace_tasks.pop(session_id, None)

    if manager.is_user_connected(session_id):
        return  # user came back

    try:
        from app.db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            eskal = await eskal_svc.expire_escalation(db, escalation_id)
            if not eskal:
                return
            await db.commit()
            if eskal.dodjeljeni_agent_id:
                await manager.send_to_agent(str(eskal.dodjeljeni_agent_id), {
                    "type": "user_timeout",
                    "session_id": session_id,
                    "escalation_id": eskal.id,
                })
            await _broadcast_queue(db)
    except Exception:
        logger.warning("Grace auto-end failed for escalation %s", escalation_id)


def _cancel_grace(session_id: int) -> None:
    task = _user_grace_tasks.pop(session_id, None)
    if task:
        task.cancel()


def _eskal_dict(
    e: Eskalacija, pos: int | None = None, agent_name: str | None = None
) -> dict:
    return {
        "id": e.id,
        "sesija_id": e.sesija_id,
        "korisnik_id": str(e.korisnik_id),
        "dodjeljeni_agent_id": str(e.dodjeljeni_agent_id) if e.dodjeljeni_agent_id else None,
        "agent_name": agent_name,
        "prioritet": e.prioritet,
        "status": e.status,
        "trigger_tip": e.trigger_tip,
        "tema": e.tema,
        "razgovor": e.razgovor or [],
        "datum_kreiranja": e.datum_kreiranja.isoformat() if e.datum_kreiranja else None,
        "datum_rjesavanja": e.datum_rjesavanja.isoformat() if e.datum_rjesavanja else None,
        "napomena_rjesavanja": e.napomena_rjesavanja,
        "queue_position": pos,
    }


async def _agent_names_for_queue(
    db: AsyncSession, items: List[Eskalacija]
) -> dict[uuid.UUID, str]:
    agent_ids = [e.dodjeljeni_agent_id for e in items if e.dodjeljeni_agent_id]
    if not agent_ids:
        return {}
    result = await db.execute(
        select(Korisnik.id, Korisnik.ime, Korisnik.prezime).where(Korisnik.id.in_(agent_ids))
    )
    return {
        row.id: f"{row.ime} {row.prezime or ''}".strip() for row in result.all()
    }


async def _broadcast_queue(db: AsyncSession) -> None:
    queue = await eskal_svc.get_queue(db)
    names = await _agent_names_for_queue(db, queue)
    await manager.broadcast_to_agents({
        "type": "queue_update",
        "data": [
            _eskal_dict(e, i + 1, agent_name=names.get(e.dodjeljeni_agent_id))
            for i, e in enumerate(queue)
        ],
    })


async def _persist_chat_message(db: AsyncSession, session_id: int, role: str, content: str) -> None:
    """Append a message to the razgovor JSON of the active escalation for this session."""
    result = await db.execute(
        select(Eskalacija).where(
            Eskalacija.sesija_id == session_id,
            Eskalacija.status == "UToku",
        )
    )
    eskal = result.scalar_one_or_none()
    if not eskal:
        return
    history = list(eskal.razgovor or [])
    history.append({"role": role, "content": content})
    eskal.razgovor = history
    await db.commit()


# ── HTTP endpoints ─────────────────────────────────────────────────────────


@router.get("/")
async def list_queue(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin_or_agent),
):
    items = await eskal_svc.get_queue(db)
    names = await _agent_names_for_queue(db, items)
    return [
        _eskal_dict(e, i + 1, agent_name=names.get(e.dodjeljeni_agent_id))
        for i, e in enumerate(items)
    ]


@router.get("/agent-statuses")
async def get_agent_statuses(
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin_or_agent),
):
    result = await db.execute(select(StatusAgenta))
    return [
        {
            "agent_id": str(s.agent_id),
            "status": s.status,
            "trenutna_eskalacija_id": s.trenutna_eskalacija_id,
            "zadnje_aktivno": s.zadnje_aktivno.isoformat() if s.zadnje_aktivno else None,
        }
        for s in result.scalars().all()
    ]


@router.patch("/agent-status")
async def update_agent_status(
    payload: AgentStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_admin_or_agent),
):
    if payload.status not in ("Online", "Zauzet", "Offline"):
        raise HTTPException(status_code=400, detail="Invalid status")
    row = await eskal_svc.upsert_agent_status(db, current_user.id, payload.status)
    await db.commit()
    return {"ok": True, "status": row.status}


class EscalationRequest(BaseModel):
    session_id: int
    conversation_history: list[dict] = []


@router.post("/request")
async def request_escalation(
    payload: EscalationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    """Any authenticated user can manually request an agent. One active entry per user."""
    # One live agent chat at a time: if the user already has an active escalation in a
    # different chat, tell them to finish that one first instead of silently reusing it.
    existing = await eskal_svc.get_active_for_user(db, current_user.id)
    if existing and existing.sesija_id != payload.session_id:
        raise HTTPException(
            status_code=409,
            detail="Već razgovarate sa agentom u drugom razgovoru. Završite taj razgovor da biste započeli novi.",
        )

    eskal = await eskal_svc.create_escalation(
        db,
        sesija_id=payload.session_id,
        korisnik_id=current_user.id,
        trigger="EksplicitanZahtjev",
        razgovor=payload.conversation_history,
    )
    pos = await eskal_svc.queue_position(db, eskal.id)
    await db.commit()

    await _broadcast_queue(db)

    return {
        "escalation": EscalationInfo(
            escalation_id=eskal.id,
            status=eskal.status,
            queue_position=pos,
            trigger_tip=eskal.trigger_tip or "EksplicitanZahtjev",
        )
    }


@router.post("/cancel")
async def cancel_my_escalation(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(get_current_user),
):
    """User cancels their own queue entry (e.g. on logout)."""
    eskal = await eskal_svc.cancel_escalation(db, current_user.id)
    if eskal:
        await db.commit()
        await manager.broadcast_to_agents({
            "type": "user_disconnected",
            "session_id": eskal.sesija_id,
            "escalation_id": eskal.id,
        })
        await _broadcast_queue(db)
    return {"ok": True}


@router.get("/my-stats")
async def get_my_stats(
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_admin_or_agent),
):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=6)
    month_start = today_start - timedelta(days=29)

    result = await db.execute(
        select(func.count()).select_from(Eskalacija).where(
            Eskalacija.dodjeljeni_agent_id == current_user.id,
            Eskalacija.status == "Rijesena",
            Eskalacija.datum_rjesavanja >= today_start,
        )
    )
    handled_today = result.scalar() or 0

    result = await db.execute(
        select(func.count()).select_from(Eskalacija).where(
            Eskalacija.dodjeljeni_agent_id == current_user.id,
            Eskalacija.status == "Rijesena",
            Eskalacija.datum_rjesavanja >= week_start,
        )
    )
    handled_week = result.scalar() or 0

    result = await db.execute(
        select(Eskalacija.datum_kreiranja, Eskalacija.datum_azuriranja).where(
            Eskalacija.dodjeljeni_agent_id == current_user.id,
            Eskalacija.status == "Rijesena",
            Eskalacija.datum_rjesavanja >= month_start,
        )
    )
    rows = result.all()
    if rows:
        diffs = [
            (r.datum_azuriranja - r.datum_kreiranja).total_seconds()
            for r in rows
            if r.datum_azuriranja and r.datum_kreiranja
        ]
        avg_response_seconds = sum(diffs) / len(diffs) if diffs else None
    else:
        avg_response_seconds = None

    return {
        "handled_today": handled_today,
        "handled_week": handled_week,
        "avg_response_seconds": avg_response_seconds,
    }


@router.get("/my-history")
async def get_my_history(
    limit: int = Query(default=20, le=50),
    offset: int = Query(default=0),
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_admin_or_agent),
):
    result = await db.execute(
        select(Eskalacija)
        .where(
            Eskalacija.dodjeljeni_agent_id == current_user.id,
            Eskalacija.status.in_(["Rijesena", "Napustena"]),
        )
        .order_by(Eskalacija.datum_kreiranja.desc())
        .limit(limit)
        .offset(offset)
    )
    items = result.scalars().all()

    from app.db.models.knowledge import Feedback
    output = []
    for e in items:
        d = _eskal_dict(e)
        fb = (await db.execute(
            select(Feedback.ocjena, Feedback.komentar)
            .where(
                Feedback.id_sesije == e.sesija_id,
                Feedback.komentar.isnot(None),
                Feedback.komentar != "",
            )
            .order_by(Feedback.timestamp.desc())
            .limit(1)
        )).first()
        d["sesija_feedback"] = {
            "rating": int(fb.ocjena) if fb and fb.ocjena is not None else None,
            "comment": fb.komentar if fb else None,
        } if fb else None
        output.append(d)
    return output


@router.get("/{escalation_id}")
async def get_escalation(
    escalation_id: int,
    db: AsyncSession = Depends(get_db),
    _: Korisnik = Depends(require_admin_or_agent),
):
    result = await db.execute(select(Eskalacija).where(Eskalacija.id == escalation_id))
    eskal = result.scalar_one_or_none()
    if not eskal:
        raise HTTPException(status_code=404, detail="Not found")
    return _eskal_dict(eskal)


@router.post("/{escalation_id}/accept")
async def accept(
    escalation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_admin_or_agent),
):
    eskal = await eskal_svc.accept_escalation(db, escalation_id, current_user.id)
    if not eskal:
        raise HTTPException(status_code=400, detail="Escalation unavailable or already claimed")
    await db.commit()

    agent_name = f"{current_user.ime} {current_user.prezime or ''}".strip()
    await manager.send_to_user(eskal.sesija_id, {
        "type": "agent_connected",
        "agent_name": agent_name,
        "escalation_id": escalation_id,
    })
    await _broadcast_queue(db)
    return {"ok": True, "escalation": _eskal_dict(eskal, agent_name=agent_name)}


@router.post("/{escalation_id}/release")
async def release(
    escalation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_admin_or_agent),
):
    """Owner agent releases the escalation back to the waiting queue."""
    eskal = await eskal_svc.release_escalation(db, escalation_id, current_user.id)
    if not eskal:
        raise HTTPException(status_code=400, detail="Cannot release — not assigned to you or not in progress")
    await db.commit()

    await manager.send_to_user(eskal.sesija_id, {
        "type": "agent_released",
        "message": "Agent je napustio razgovor. Ponovo ste u redu čekanja.",
    })
    await _broadcast_queue(db)
    return {"ok": True}


@router.post("/{escalation_id}/resolve")
async def resolve(
    escalation_id: int,
    payload: EscalationResolve,
    db: AsyncSession = Depends(get_db),
    current_user: Korisnik = Depends(require_admin_or_agent),
):
    eskal = await eskal_svc.resolve_escalation(
        db,
        escalation_id,
        current_user.id,
        submit_to_kb=payload.submit_to_kb,
        kb_unosi=[(e.pitanje, e.odgovor) for e in payload.kb_unosi] if payload.kb_unosi else None,
    )
    if not eskal:
        raise HTTPException(status_code=404, detail="Not found")
    await db.commit()

    await manager.send_to_user(eskal.sesija_id, {
        "type": "session_ended",
        "message": "Vaša sesija sa agentom je završena. Hvala što ste koristili naš servis.",
    })
    await _broadcast_queue(db)
    return {"ok": True}


# ── WebSocket: user receives agent messages ────────────────────────────────


@router.websocket("/ws/chat/{session_id}")
async def ws_user_chat(
    websocket: WebSocket,
    session_id: int,
    token: str = Query(...),
):
    try:
        payload = decode_token(token)
        if not payload.get("sub"):
            await websocket.close(code=4001)
            return
    except Exception:
        await websocket.close(code=4001)
        return

    await manager.connect_user(session_id, websocket)

    # On (re)connect, reconcile the user against the latest escalation for this session:
    #  - still live (UToku)  → re-send agent_connected + tell the agent the user re-entered
    #  - already ended by the agent (Rijesena/Napustena) while the user was away
    #                          → tell the user the session ended so a new request starts fresh
    try:
        from app.db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as fresh_db:
            r = await fresh_db.execute(
                select(Eskalacija)
                .where(Eskalacija.sesija_id == session_id)
                .order_by(Eskalacija.id.desc())
                .limit(1)
            )
            eskal = r.scalar_one_or_none()
            if eskal and eskal.status == "UToku" and eskal.dodjeljeni_agent_id:
                # User came back in time — cancel any pending auto-end.
                _cancel_grace(session_id)
                ar = await fresh_db.execute(
                    select(Korisnik).where(Korisnik.id == eskal.dodjeljeni_agent_id)
                )
                agent = ar.scalar_one_or_none()
                agent_name = f"{agent.ime} {agent.prezime or ''}".strip() if agent else "Agent"
                await websocket.send_text(json.dumps({
                    "type": "agent_connected",
                    "agent_name": agent_name,
                    "escalation_id": eskal.id,
                }))
                # Presence: live agent chat + a fresh connect = the user came back.
                await manager.send_to_agent(str(eskal.dodjeljeni_agent_id), {
                    "type": "user_entered",
                    "session_id": session_id,
                    "escalation_id": eskal.id,
                })
            elif eskal and eskal.status in ("Rijesena", "Napustena"):
                # The agent left the chat (resolve) while the user was away. Clear the
                # user's stale "connected" state — a later request is a brand-new call.
                await websocket.send_text(json.dumps({
                    "type": "session_ended",
                    "message": "Vaša sesija sa agentom je završena. Hvala što ste koristili naš servis.",
                }))
    except Exception:
        pass

    async def _keepalive():
        while True:
            await asyncio.sleep(25)
            try:
                await websocket.send_text('{"type":"ping"}')
            except Exception:
                break

    keepalive_task = asyncio.create_task(_keepalive())
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        keepalive_task.cancel()
        manager.disconnect_user(session_id)
        # Presence: if the escalation is still live (UToku), the user only dropped
        # the chat view (Home / refresh / network) rather than ending it — tell the
        # assigned agent the user left. Resolved/abandoned cases (Rijesena/Napustena)
        # have their own messaging, so they're skipped by the status check.
        try:
            from app.db.session import AsyncSessionLocal
            async with AsyncSessionLocal() as fresh_db:
                r = await fresh_db.execute(
                    select(Eskalacija).where(
                        Eskalacija.sesija_id == session_id,
                        Eskalacija.status == "UToku",
                    )
                )
                eskal = r.scalar_one_or_none()
                if eskal and eskal.dodjeljeni_agent_id:
                    await manager.send_to_agent(str(eskal.dodjeljeni_agent_id), {
                        "type": "user_left",
                        "session_id": session_id,
                        "escalation_id": eskal.id,
                    })
                    # Start the grace countdown: if the user doesn't reconnect, the
                    # chat is auto-ended and the agent is freed.
                    _cancel_grace(session_id)
                    _user_grace_tasks[session_id] = asyncio.create_task(
                        _grace_end_escalation(session_id, eskal.id)
                    )
        except Exception:
            pass


# ── WebSocket: agents receive queue updates and chat with users ────────────


@router.websocket("/ws/escalation")
async def ws_agent_queue(
    websocket: WebSocket,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_token(token)
        user_id_str = payload.get("sub")
        if not user_id_str:
            await websocket.close(code=4001)
            return
        result = await db.execute(
            select(Korisnik).where(Korisnik.id == uuid.UUID(user_id_str))
        )
        agent = result.scalar_one_or_none()
        if not agent or agent.uloga not in (
            UlogaTip.administrator, UlogaTip.call_centar_agent, UlogaTip.supervizor
        ):
            await websocket.close(code=4003)
            return
    except Exception:
        await websocket.close(code=4001)
        return

    agent_id_str = str(agent.id)
    await manager.connect_agent(agent_id_str, websocket)

    queue = await eskal_svc.get_queue(db)
    names = await _agent_names_for_queue(db, queue)
    await websocket.send_text(json.dumps({
        "type": "queue_sync",
        "data": [
            _eskal_dict(e, i + 1, agent_name=names.get(e.dodjeljeni_agent_id))
            for i, e in enumerate(queue)
        ],
    }))

    agent_name = f"{agent.ime} {agent.prezime or ''}".strip()

    async def _agent_keepalive():
        while True:
            await asyncio.sleep(25)
            try:
                await websocket.send_text('{"type":"ping"}')
            except Exception:
                break

    keepalive_task = asyncio.create_task(_agent_keepalive())
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                continue

            if msg.get("type") == "agent_message":
                sid = msg.get("session_id")
                content = msg.get("content", "").strip()
                if sid and content:
                    # Expire the ORM identity map so we read the latest committed
                    # state from the DB (the accept endpoint ran in a different
                    # session and updated status + dodjeljeni_agent_id there).
                    db.expire_all()
                    result = await db.execute(
                        select(Eskalacija).where(
                            Eskalacija.sesija_id == int(sid),
                            Eskalacija.status == "UToku",
                        )
                    )
                    eskal = result.scalar_one_or_none()
                    if not eskal or str(eskal.dodjeljeni_agent_id) != agent_id_str:
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "You are not the assigned agent for this chat.",
                        }))
                        continue

                    await manager.send_to_user(int(sid), {
                        "type": "agent_message",
                        "content": content,
                        "agent_name": agent_name,
                    })
                    await _persist_chat_message(db, int(sid), "agent", content)

                    await manager.broadcast_to_agents({
                        "type": "chat_message",
                        "session_id": int(sid),
                        "escalation_id": eskal.id,
                        "role": "agent",
                        "content": content,
                        "agent_name": agent_name,
                    }, exclude_agent_id=agent_id_str)

            if msg.get("type") == "typing":
                sid = msg.get("session_id")
                if sid:
                    await manager.send_to_user(int(sid), {
                        "type": "agent_typing",
                        "is_typing": msg.get("is_typing", False),
                    })
    except WebSocketDisconnect:
        pass
    finally:
        keepalive_task.cancel()
        manager.disconnect_agent(agent_id_str, websocket)
