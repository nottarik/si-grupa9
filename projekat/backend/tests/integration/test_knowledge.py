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
    email = f"kb_user_{uuid.uuid4().hex[:8]}@test.com"
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "pass123", "full_name": "KB User", "role": "user"},
    )
    resp = await client.post("/api/v1/auth/login", json={"email": email, "password": "pass123"})
    return resp.json()["access_token"]


async def _create_manual_qa(client: AsyncClient, token: str) -> int:
    resp = await client.post(
        "/api/v1/knowledge/manual",
        json={
            "pitanje": "Kako se aktivira internet banking?",
            "odgovor": "Internet banking se aktivira posjetom najbliže poslovnice ili putem mobilne aplikacije.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    return resp.json()["id"]


# ═══════════════════════════════════════════════════════════════════════════════
# PENDING APPROVALS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_list_pending_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _user_token(client)
        resp = await client.get(
            "/api/v1/knowledge/pending",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_pending_as_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get("/api/v1/knowledge/pending", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORIES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_list_categories_as_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get(
            "/api/v1/knowledge/categories",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


# ═══════════════════════════════════════════════════════════════════════════════
# MANUAL Q&A ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_create_manual_qa_as_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.post(
            "/api/v1/knowledge/manual",
            json={
                "pitanje": "Koji su uslovi za stambeni kredit?",
                "odgovor": "Za stambeni kredit potrebna je lična karta, potvrda o zaposlenju i izvod sa žiro računa.",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert "id" in body
    assert "message" in body


@pytest.mark.asyncio
async def test_create_manual_qa_requires_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _user_token(client)
        resp = await client.post(
            "/api/v1/knowledge/manual",
            json={"pitanje": "Neko pitanje ovdje?", "odgovor": "Neki odgovor ovdje."},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_create_manual_qa_too_short_rejected():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.post(
            "/api/v1/knowledge/manual",
            json={"pitanje": "Kratko?", "odgovor": "Da."},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_manual_qa_without_category():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.post(
            "/api/v1/knowledge/manual",
            json={
                "pitanje": "Kako podnijeti reklamaciju na uslugu?",
                "odgovor": "Reklamaciju možete podnijeti putem call centra ili pisanim putem na adresu kompanije.",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200


# ═══════════════════════════════════════════════════════════════════════════════
# APPROVED LIST
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_list_approved_as_admin():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get(
            "/api/v1/knowledge/approved",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    if body:
        first = body[0]
        assert "id" in first
        assert "question" in first
        assert "answer" in first
        assert "source_type" in first


# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE ITEM
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_update_kb_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        item_id = await _create_manual_qa(client, token)
        resp = await client.put(
            f"/api/v1/knowledge/{item_id}",
            json={
                "pitanje": "Kako aktivirati internet banking na novi način?",
                "odgovor": "Posjetite poslovnicu ili nazovite call centar za aktivaciju internet bankinga.",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert "message" in resp.json()


@pytest.mark.asyncio
async def test_update_kb_item_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.put(
            "/api/v1/knowledge/999999",
            json={
                "pitanje": "Nepostojeće pitanje za update?",
                "odgovor": "Nepostojeći odgovor za update teste.",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


# ═══════════════════════════════════════════════════════════════════════════════
# APPROVE / REJECT
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_approve_pending_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        item_id = await _create_manual_qa(client, token)
        resp = await client.post(
            f"/api/v1/knowledge/{item_id}/approve",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert "message" in resp.json()


@pytest.mark.asyncio
async def test_reject_pending_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        item_id = await _create_manual_qa(client, token)
        resp = await client.post(
            f"/api/v1/knowledge/{item_id}/reject",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert "message" in resp.json()


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE ITEM
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_delete_kb_item():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        item_id = await _create_manual_qa(client, token)
        resp = await client.delete(
            f"/api/v1/knowledge/{item_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert "message" in resp.json()


# ═══════════════════════════════════════════════════════════════════════════════
# SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_search_knowledge_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/knowledge/search?q=kredit")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_search_knowledge_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get(
            "/api/v1/knowledge/search?q=kredit",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
