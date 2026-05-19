import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app
from app.db.session import AsyncSessionLocal
from app.db.models.user import Korisnik, UlogaTip
from app.db.models.knowledge import ChatSesija
from app.core.security import get_password_hash


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _get_admin_token(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    return resp.json()["access_token"]


async def _register_and_login(client: AsyncClient, role: str = "user") -> str:
    email = f"inteskal_{uuid.uuid4().hex[:8]}@test.com"
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pass123", "full_name": "Test User", "role": role},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "pass123"},
    )
    return resp.json()["access_token"]


async def _create_session_in_db(user_id: uuid.UUID) -> int:
    async with AsyncSessionLocal() as db:
        sesija = ChatSesija(id_korisnika=user_id, kanal_pristupa="web", status="Aktivna")
        db.add(sesija)
        await db.commit()
        await db.refresh(sesija)
        return sesija.id


async def _get_user_id(token: str, client: AsyncClient) -> uuid.UUID:
    resp = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    return uuid.UUID(resp.json()["id"])


# ── List queue ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_queue_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/escalation/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_queue_requires_admin_or_agent_role():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _register_and_login(client, role="user")
        resp = await client.get(
            "/api/v1/escalation/",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_queue_returns_list_for_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.get(
            "/api/v1/escalation/",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── Agent statuses ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_agent_statuses_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/escalation/agent-statuses")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_agent_statuses_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.get(
            "/api/v1/escalation/agent-statuses",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── Agent status update ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_agent_status_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.patch("/api/v1/escalation/agent-status", json={"status": "Online"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_update_agent_status_valid():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.patch(
            "/api/v1/escalation/agent-status",
            json={"status": "Online"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
    assert resp.json()["status"] == "Online"


@pytest.mark.asyncio
async def test_update_agent_status_invalid_value():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.patch(
            "/api/v1/escalation/agent-status",
            json={"status": "Nepostoji"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 400


# ── Request escalation ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_request_escalation_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/escalation/request", json={"session_id": 1})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_request_escalation_creates_queue_entry():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        admin_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(admin_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            resp = await client.post(
                "/api/v1/escalation/request",
                json={"session_id": session_id},
                headers={"Authorization": f"Bearer {token}"},
            )

    assert resp.status_code == 200
    body = resp.json()
    assert "escalation" in body
    assert body["escalation"]["status"] == "Cekanje"
    assert body["escalation"]["queue_position"] >= 1


@pytest.mark.asyncio
async def test_request_escalation_idempotent():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _register_and_login(client, role="user")
        user_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(user_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            r1 = await client.post(
                "/api/v1/escalation/request",
                json={"session_id": session_id},
                headers={"Authorization": f"Bearer {token}"},
            )
            r2 = await client.post(
                "/api/v1/escalation/request",
                json={"session_id": session_id},
                headers={"Authorization": f"Bearer {token}"},
            )

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["escalation"]["escalation_id"] == r2.json()["escalation"]["escalation_id"]


# ── Cancel escalation ─────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cancel_escalation_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/escalation/cancel")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_cancel_escalation_when_no_active_returns_ok():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _register_and_login(client, role="user")
        resp = await client.post(
            "/api/v1/escalation/cancel",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_cancel_escalation_cancels_active():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _register_and_login(client, role="user")
        user_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(user_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            with patch("app.api.v1.routes.escalation.manager") as mock_mgr:
                mock_mgr.broadcast_to_agents = AsyncMock()
                await client.post(
                    "/api/v1/escalation/request",
                    json={"session_id": session_id},
                    headers={"Authorization": f"Bearer {token}"},
                )
                resp = await client.post(
                    "/api/v1/escalation/cancel",
                    headers={"Authorization": f"Bearer {token}"},
                )

    assert resp.status_code == 200
    assert resp.json()["ok"] is True


# ── Get single escalation ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_escalation_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.get(
            "/api/v1/escalation/999999",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_escalation_returns_data():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        admin_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(admin_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            create_resp = await client.post(
                "/api/v1/escalation/request",
                json={"session_id": session_id},
                headers={"Authorization": f"Bearer {token}"},
            )
        eskal_id = create_resp.json()["escalation"]["escalation_id"]

        resp = await client.get(
            f"/api/v1/escalation/{eskal_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 200
    assert resp.json()["id"] == eskal_id


# ── Accept / Release / Resolve ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_accept_escalation_transitions_to_utoku():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        admin_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(admin_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            with patch("app.api.v1.routes.escalation.manager") as mock_mgr:
                mock_mgr.send_to_user = AsyncMock(return_value=True)
                mock_mgr.broadcast_to_agents = AsyncMock()

                create_resp = await client.post(
                    "/api/v1/escalation/request",
                    json={"session_id": session_id},
                    headers={"Authorization": f"Bearer {token}"},
                )
                eskal_id = create_resp.json()["escalation"]["escalation_id"]

                accept_resp = await client.post(
                    f"/api/v1/escalation/{eskal_id}/accept",
                    headers={"Authorization": f"Bearer {token}"},
                )

    assert accept_resp.status_code == 200
    assert accept_resp.json()["ok"] is True
    assert accept_resp.json()["escalation"]["status"] == "UToku"


@pytest.mark.asyncio
async def test_accept_nonexistent_escalation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.post(
            "/api/v1/escalation/999999/accept",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_release_escalation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        admin_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(admin_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            with patch("app.api.v1.routes.escalation.manager") as mock_mgr:
                mock_mgr.send_to_user = AsyncMock(return_value=True)
                mock_mgr.broadcast_to_agents = AsyncMock()

                create_resp = await client.post(
                    "/api/v1/escalation/request",
                    json={"session_id": session_id},
                    headers={"Authorization": f"Bearer {token}"},
                )
                eskal_id = create_resp.json()["escalation"]["escalation_id"]

                await client.post(
                    f"/api/v1/escalation/{eskal_id}/accept",
                    headers={"Authorization": f"Bearer {token}"},
                )

                release_resp = await client.post(
                    f"/api/v1/escalation/{eskal_id}/release",
                    headers={"Authorization": f"Bearer {token}"},
                )

    assert release_resp.status_code == 200
    assert release_resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_release_not_assigned_returns_400():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        admin_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(admin_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            create_resp = await client.post(
                "/api/v1/escalation/request",
                json={"session_id": session_id},
                headers={"Authorization": f"Bearer {token}"},
            )
        eskal_id = create_resp.json()["escalation"]["escalation_id"]

        # Try to release while still in Cekanje (not accepted)
        resp = await client.post(
            f"/api/v1/escalation/{eskal_id}/release",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_resolve_escalation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        admin_id = await _get_user_id(token, client)
        session_id = await _create_session_in_db(admin_id)

        with patch("app.api.v1.routes.escalation._broadcast_queue", new=AsyncMock()):
            with patch("app.api.v1.routes.escalation.manager") as mock_mgr:
                mock_mgr.send_to_user = AsyncMock(return_value=True)
                mock_mgr.broadcast_to_agents = AsyncMock()

                create_resp = await client.post(
                    "/api/v1/escalation/request",
                    json={"session_id": session_id},
                    headers={"Authorization": f"Bearer {token}"},
                )
                eskal_id = create_resp.json()["escalation"]["escalation_id"]

                await client.post(
                    f"/api/v1/escalation/{eskal_id}/accept",
                    headers={"Authorization": f"Bearer {token}"},
                )

                resolve_resp = await client.post(
                    f"/api/v1/escalation/{eskal_id}/resolve",
                    json={"napomena": "Završeno", "submit_to_kb": False},
                    headers={"Authorization": f"Bearer {token}"},
                )

    assert resolve_resp.status_code == 200
    assert resolve_resp.json()["ok"] is True


@pytest.mark.asyncio
async def test_resolve_nonexistent_escalation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.post(
            "/api/v1/escalation/999999/resolve",
            json={"napomena": ""},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


# ── My stats / My history ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_my_stats_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/escalation/my-stats")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_my_stats_returns_counts():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.get(
            "/api/v1/escalation/my-stats",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert "handled_today" in body
    assert "handled_week" in body
    assert "avg_response_seconds" in body


@pytest.mark.asyncio
async def test_my_history_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/escalation/my-history")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_my_history_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.get(
            "/api/v1/escalation/my-history",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_my_history_limit_param():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_admin_token(client)
        resp = await client.get(
            "/api/v1/escalation/my-history?limit=5",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert len(resp.json()) <= 5
