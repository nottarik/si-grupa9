"""
WebSocket integration tests.

Uses starlette.testclient.TestClient for synchronous WebSocket connections,
which is the standard approach for testing FastAPI/Starlette WebSocket routes.
"""
import json
import uuid
import threading
import time
import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from unittest.mock import patch, AsyncMock

from app.main import app
from app.db.session import AsyncSessionLocal
from app.db.models.user import Korisnik, UlogaTip
from app.db.models.knowledge import ChatSesija
from app.db.models.escalation import Eskalacija
from app.core.security import get_password_hash, create_access_token


# ── Sync DB helpers (run inside sync context via asyncio.run equivalent) ──────

def _run_async(coro):
    import asyncio
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


def _create_agent_user() -> tuple[uuid.UUID, str]:
    """Create a call-center agent in DB and return (id, token)."""
    async def _inner():
        async with AsyncSessionLocal() as db:
            agent = Korisnik(
                ime="WS", prezime="Agent",
                email=f"wsagent_{uuid.uuid4().hex[:8]}@test.com",
                hashed_password=get_password_hash("x"),
                uloga=UlogaTip.call_centar_agent,
                aktivan=True,
            )
            db.add(agent)
            await db.commit()
            await db.refresh(agent)
            return agent.id
    agent_id = _run_async(_inner())
    token = create_access_token(str(agent_id))
    return agent_id, token


def _create_regular_user() -> tuple[uuid.UUID, str]:
    """Create a regular user in DB and return (id, token)."""
    async def _inner():
        async with AsyncSessionLocal() as db:
            user = Korisnik(
                ime="WS", prezime="User",
                email=f"wsuser_{uuid.uuid4().hex[:8]}@test.com",
                hashed_password=get_password_hash("x"),
                uloga=UlogaTip.krajnji_korisnik,
                aktivan=True,
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user.id
    user_id = _run_async(_inner())
    token = create_access_token(str(user_id))
    return user_id, token


def _create_session_and_escalation(user_id: uuid.UUID, agent_id: uuid.UUID) -> tuple[int, int]:
    """Create a ChatSesija and UToku Eskalacija; return (session_id, escalation_id)."""
    async def _inner():
        async with AsyncSessionLocal() as db:
            sesija = ChatSesija(id_korisnika=user_id, kanal_pristupa="web", status="Aktivna")
            db.add(sesija)
            await db.flush()
            eskal = Eskalacija(
                sesija_id=sesija.id,
                korisnik_id=user_id,
                dodjeljeni_agent_id=agent_id,
                status="UToku",
                prioritet="Normalan",
                trigger_tip="NiskaPouz",
                razgovor=[],
            )
            db.add(eskal)
            await db.commit()
            await db.refresh(sesija)
            await db.refresh(eskal)
            return sesija.id, eskal.id
    return _run_async(_inner())


# ── User WebSocket ────────────────────────────────────────────────────────────

def test_user_ws_connects_with_valid_token():
    _, token = _create_regular_user()
    with TestClient(app) as client:
        with client.websocket_connect(f"/api/v1/escalation/ws/chat/100?token={token}") as ws:
            # Connected successfully — connection stays open until we exit
            pass


def test_user_ws_rejects_missing_token():
    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/escalation/ws/chat/1") as ws:
                ws.receive_text()


def test_user_ws_rejects_invalid_token():
    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect(
                "/api/v1/escalation/ws/chat/1?token=not.a.valid.jwt"
            ) as ws:
                ws.receive_text()


def test_user_ws_rejects_expired_token():
    from datetime import timedelta
    expired_token = create_access_token(str(uuid.uuid4()), expires_delta=timedelta(seconds=-1))
    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect(
                f"/api/v1/escalation/ws/chat/1?token={expired_token}"
            ) as ws:
                ws.receive_text()


def test_user_ws_different_sessions_are_independent():
    _, t1 = _create_regular_user()
    _, t2 = _create_regular_user()
    with TestClient(app) as client:
        with client.websocket_connect(f"/api/v1/escalation/ws/chat/201?token={t1}"):
            with client.websocket_connect(f"/api/v1/escalation/ws/chat/202?token={t2}"):
                pass  # Both open simultaneously without error


# ── Agent WebSocket ───────────────────────────────────────────────────────────

def test_agent_ws_connects_with_valid_agent_token():
    _, token = _create_agent_user()
    with TestClient(app) as client:
        with client.websocket_connect(f"/api/v1/escalation/ws/escalation?token={token}") as ws:
            data = ws.receive_json()
            assert data["type"] == "queue_sync"
            assert isinstance(data["data"], list)


def test_agent_ws_receives_queue_sync_on_connect():
    _, token = _create_agent_user()
    with TestClient(app) as client:
        with client.websocket_connect(f"/api/v1/escalation/ws/escalation?token={token}") as ws:
            msg = ws.receive_json()
    assert msg["type"] == "queue_sync"
    assert "data" in msg


def test_agent_ws_rejects_invalid_token():
    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect(
                "/api/v1/escalation/ws/escalation?token=garbage"
            ) as ws:
                ws.receive_text()


def test_agent_ws_rejects_regular_user_role():
    _, token = _create_regular_user()
    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect(
                f"/api/v1/escalation/ws/escalation?token={token}"
            ) as ws:
                ws.receive_text()


def test_agent_ws_rejects_missing_token():
    with TestClient(app) as client:
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/escalation/ws/escalation") as ws:
                ws.receive_text()


def test_agent_ws_admin_can_connect():
    """Administrator role is accepted by the agent WebSocket route."""
    import asyncio

    async def _get_admin_id():
        from sqlalchemy import select
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Korisnik).where(Korisnik.email == "admin@test.com")
            )
            return result.scalar_one().id

    admin_id = _run_async(_get_admin_id())
    token = create_access_token(str(admin_id))

    with TestClient(app) as client:
        with client.websocket_connect(f"/api/v1/escalation/ws/escalation?token={token}") as ws:
            msg = ws.receive_json()
    assert msg["type"] == "queue_sync"


# ── Agent sends message to user ───────────────────────────────────────────────

def test_agent_sends_message_to_connected_user():
    """Agent's 'agent_message' is forwarded to the user's WebSocket."""
    user_id, user_token = _create_regular_user()
    agent_id, agent_token = _create_agent_user()
    session_id, _ = _create_session_and_escalation(user_id, agent_id)

    received = []
    error = []

    with TestClient(app) as client:
        def user_thread():
            try:
                with client.websocket_connect(
                    f"/api/v1/escalation/ws/chat/{session_id}?token={user_token}"
                ) as ws:
                    try:
                        while True:
                            msg = ws.receive_json()
                            received.append(msg)
                    except Exception:
                        pass  # connection closed — stop collecting
            except Exception as e:
                error.append(e)

        t = threading.Thread(target=user_thread, daemon=True)
        t.start()
        time.sleep(0.5)  # allow user to connect first

        with client.websocket_connect(
            f"/api/v1/escalation/ws/escalation?token={agent_token}"
        ) as ws:
            ws.receive_json()  # consume queue_sync
            ws.send_json({
                "type": "agent_message",
                "session_id": session_id,
                "content": "Zdravo, kako mogu pomoći?",
            })
            time.sleep(0.5)  # allow message to propagate

    t.join(timeout=5)

    assert len(error) == 0, f"User thread raised: {error}"
    assert any(m.get("type") == "agent_message" for m in received)
    agent_msgs = [m for m in received if m.get("type") == "agent_message"]
    assert agent_msgs[0]["content"] == "Zdravo, kako mogu pomoći?"


def test_agent_receives_error_when_not_assigned():
    """Agent gets error when sending to a session they're not assigned to."""
    _, agent_token = _create_agent_user()
    # session_id 99999 has no active escalation
    with TestClient(app) as client:
        with client.websocket_connect(
            f"/api/v1/escalation/ws/escalation?token={agent_token}"
        ) as ws:
            ws.receive_json()  # consume queue_sync
            ws.send_json({
                "type": "agent_message",
                "session_id": 99999,
                "content": "Poruka u void",
            })
            msg = ws.receive_json()
    assert msg["type"] == "error"


# ── Typing indicator ──────────────────────────────────────────────────────────

def test_agent_typing_forwarded_to_user():
    """Typing indicator from agent is delivered to the connected user."""
    user_id, user_token = _create_regular_user()
    agent_id, agent_token = _create_agent_user()
    session_id, _ = _create_session_and_escalation(user_id, agent_id)

    received = []
    error = []

    with TestClient(app) as client:
        def user_thread():
            try:
                with client.websocket_connect(
                    f"/api/v1/escalation/ws/chat/{session_id}?token={user_token}"
                ) as ws:
                    try:
                        while True:
                            msg = ws.receive_json()
                            received.append(msg)
                    except Exception:
                        pass  # connection closed — stop collecting
            except Exception as e:
                error.append(e)

        t = threading.Thread(target=user_thread, daemon=True)
        t.start()
        time.sleep(0.5)

        with client.websocket_connect(
            f"/api/v1/escalation/ws/escalation?token={agent_token}"
        ) as ws:
            ws.receive_json()  # consume queue_sync
            ws.send_json({
                "type": "typing",
                "session_id": session_id,
                "is_typing": True,
            })
            time.sleep(0.5)

    t.join(timeout=5)

    assert len(error) == 0, f"User thread raised: {error}"
    typing_msgs = [m for m in received if m.get("type") == "agent_typing"]
    assert len(typing_msgs) >= 1
    assert typing_msgs[0]["is_typing"] is True
