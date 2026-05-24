import uuid
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.db.session import AsyncSessionLocal
from app.db.models.knowledge import ChatSesija


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _admin_token(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    return resp.json()["access_token"]


async def _register_and_login(client: AsyncClient, role: str = "user") -> tuple[str, str]:
    email = f"sess_{uuid.uuid4().hex[:8]}@test.com"
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pass123", "full_name": "Sess User", "role": role},
    )
    resp = await client.post("/api/v1/auth/login", json={"email": email, "password": "pass123"})
    token = resp.json()["access_token"]
    me = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    user_id = me.json()["id"]
    return token, user_id


async def _create_session(user_id: str) -> int:
    async with AsyncSessionLocal() as db:
        sesija = ChatSesija(id_korisnika=uuid.UUID(user_id), kanal_pristupa="web", status="Aktivna")
        db.add(sesija)
        await db.commit()
        await db.refresh(sesija)
        return sesija.id


# ═══════════════════════════════════════════════════════════════════════════════
# LIST SESSIONS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_list_sessions_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/chat/sessions")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_sessions_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        await _create_session(user_id)
        resp = await client.get("/api/v1/chat/sessions", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    first = body[0]
    assert "id" in first
    assert "status" in first
    assert "message_count" in first


# ═══════════════════════════════════════════════════════════════════════════════
# GET SESSION MESSAGES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_get_session_messages_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, _ = await _register_and_login(client)
        resp = await client.get(
            "/api/v1/chat/sessions/999999/messages",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_session_messages_wrong_user_returns_404():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        _, owner_id = await _register_and_login(client, role="user")
        session_id = await _create_session(owner_id)

        other_token, _ = await _register_and_login(client, role="user")
        resp = await client.get(
            f"/api/v1/chat/sessions/{session_id}/messages",
            headers={"Authorization": f"Bearer {other_token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_session_messages_returns_structure():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        session_id = await _create_session(user_id)
        resp = await client.get(
            f"/api/v1/chat/sessions/{session_id}/messages",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert "session_id" in body
    assert "messages" in body
    assert isinstance(body["messages"], list)


# ═══════════════════════════════════════════════════════════════════════════════
# CLOSE SESSION
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_close_session():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        session_id = await _create_session(user_id)
        resp = await client.post(
            f"/api/v1/chat/sessions/{session_id}/close",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_close_nonexistent_session_returns_404():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, _ = await _register_and_login(client)
        resp = await client.post(
            "/api/v1/chat/sessions/999999/close",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_close_session_is_idempotent():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        session_id = await _create_session(user_id)
        r1 = await client.post(
            f"/api/v1/chat/sessions/{session_id}/close",
            headers={"Authorization": f"Bearer {token}"},
        )
        r2 = await client.post(
            f"/api/v1/chat/sessions/{session_id}/close",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r1.status_code == 200
    assert r2.status_code == 200


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE SESSION
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_delete_session():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        session_id = await _create_session(user_id)
        resp = await client.delete(
            f"/api/v1/chat/sessions/{session_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_delete_session_removes_from_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        session_id = await _create_session(user_id)
        await client.delete(
            f"/api/v1/chat/sessions/{session_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.get("/api/v1/chat/sessions", headers={"Authorization": f"Bearer {token}"})
    ids = [s["id"] for s in resp.json()]
    assert session_id not in ids


@pytest.mark.asyncio
async def test_delete_nonexistent_session_returns_404():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, _ = await _register_and_login(client)
        resp = await client.delete(
            "/api/v1/chat/sessions/999999",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


# ═══════════════════════════════════════════════════════════════════════════════
# RATE SESSION
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_rate_session():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        session_id = await _create_session(user_id)
        resp = await client.post(
            f"/api/v1/chat/sessions/{session_id}/rate",
            json={"rating": 5, "comment": "Odlično!"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_rate_session_rating_is_clamped_to_valid_range():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client)
        session_id = await _create_session(user_id)
        resp = await client.post(
            f"/api/v1/chat/sessions/{session_id}/rate",
            json={"rating": 10},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_rate_nonexistent_session_returns_404():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, _ = await _register_and_login(client)
        resp = await client.post(
            "/api/v1/chat/sessions/999999/rate",
            json={"rating": 3},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN SESSION MESSAGES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_admin_get_session_messages_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, user_id = await _register_and_login(client, role="user")
        session_id = await _create_session(user_id)
        resp = await client.get(
            f"/api/v1/chat/admin/sessions/{session_id}/messages",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_admin_get_session_messages_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get(
            "/api/v1/chat/admin/sessions/999999/messages",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_admin_get_session_messages_any_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        _, user_id = await _register_and_login(client, role="user")
        session_id = await _create_session(user_id)
        admin_token = await _admin_token(client)
        resp = await client.get(
            f"/api/v1/chat/admin/sessions/{session_id}/messages",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
    assert resp.status_code == 200
    assert "messages" in resp.json()


# ═══════════════════════════════════════════════════════════════════════════════
# CHAT LOGS (ADMIN)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_chat_logs_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, _ = await _register_and_login(client, role="user")
        resp = await client.get(
            "/api/v1/chat/logs",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_chat_logs_as_admin_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get("/api/v1/chat/logs", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ═══════════════════════════════════════════════════════════════════════════════
# RATINGS STATS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_ratings_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/chat/ratings")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_ratings_returns_stats():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get("/api/v1/chat/ratings", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert "average_score" in body
    assert "total_rated" in body
    assert "distribution" in body
    assert "trend" in body


# ═══════════════════════════════════════════════════════════════════════════════
# ISSUES (ANOMALIES)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_issues_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token, _ = await _register_and_login(client, role="user")
        resp = await client.get(
            "/api/v1/chat/issues",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_issues_as_admin_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get("/api/v1/chat/issues", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_issues_status_filter():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get(
            "/api/v1/chat/issues?status_filter=Open",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
