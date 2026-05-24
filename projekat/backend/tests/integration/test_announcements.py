import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _admin_token(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    return resp.json()["access_token"]


async def _user_token(client: AsyncClient) -> str:
    import uuid
    email = f"ann_user_{uuid.uuid4().hex[:8]}@test.com"
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pass123", "full_name": "Ann User", "role": "user"},
    )
    resp = await client.post("/api/v1/auth/login", json={"email": email, "password": "pass123"})
    return resp.json()["access_token"]


async def _create_announcement(client: AsyncClient, token: str, tekst: str = "Sistemska obavijest.") -> int:
    resp = await client.post(
        "/api/v1/announcements",
        json={"naslov": "Test obavijest", "tekst": tekst},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


# ── List active ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_active_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/announcements/active")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_active_as_authenticated_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _user_token(client)
        resp = await client.get(
            "/api/v1/announcements/active",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── List all (admin only) ──────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_all_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _user_token(client)
        resp = await client.get(
            "/api/v1/announcements",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_all_as_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get(
            "/api/v1/announcements",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ── Create ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_announcement_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _user_token(client)
        resp = await client.post(
            "/api/v1/announcements",
            json={"tekst": "Neka obavijest"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_create_announcement_as_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.post(
            "/api/v1/announcements",
            json={"naslov": "Planirana obustava", "tekst": "Sistem će biti nedostupan u subotu od 02:00 do 04:00."},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 201
    body = resp.json()
    assert "id" in body
    assert body["aktivna"] is True
    assert body["tekst"] == "Sistem će biti nedostupan u subotu od 02:00 do 04:00."


@pytest.mark.asyncio
async def test_create_announcement_without_naslov():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.post(
            "/api/v1/announcements",
            json={"tekst": "Obavijest bez naslova."},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 201
    body = resp.json()
    assert body["naslov"] is None
    assert body["tekst"] == "Obavijest bez naslova."


# ── Update ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_announcement():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        ann_id = await _create_announcement(client, token, "Originalni tekst.")
        resp = await client.patch(
            f"/api/v1/announcements/{ann_id}",
            json={"tekst": "Ažurirani tekst.", "aktivna": False},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["tekst"] == "Ažurirani tekst."
    assert body["aktivna"] is False


@pytest.mark.asyncio
async def test_update_announcement_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.patch(
            "/api/v1/announcements/999999",
            json={"tekst": "Nepostojeća obavijest."},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


# ── Delete ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_announcement():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        ann_id = await _create_announcement(client, token, "Brisati ću ovo.")
        resp = await client.delete(
            f"/api/v1/announcements/{ann_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_announcement_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.delete(
            "/api/v1/announcements/999999",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


# ── Lifecycle: create → appears in active → deactivate → not in active ─────────

@pytest.mark.asyncio
async def test_active_list_reflects_deactivation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        ann_id = await _create_announcement(client, token, "Vidljiva samo kad je aktivna.")

        active_before = await client.get(
            "/api/v1/announcements/active",
            headers={"Authorization": f"Bearer {token}"},
        )
        ids_before = [a["id"] for a in active_before.json()]
        assert ann_id in ids_before

        await client.patch(
            f"/api/v1/announcements/{ann_id}",
            json={"aktivna": False},
            headers={"Authorization": f"Bearer {token}"},
        )

        active_after = await client.get(
            "/api/v1/announcements/active",
            headers={"Authorization": f"Bearer {token}"},
        )
        ids_after = [a["id"] for a in active_after.json()]
        assert ann_id not in ids_after
