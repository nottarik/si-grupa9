import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@example.com", "password": "wrong"},
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_requires_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_valid_credentials():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "admin123"},
        )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_missing_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={},
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_wrong_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "pogresna"},
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_duplicate_email():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@test.com",
                "password": "admin123",
                "full_name": "Test User",
                "role": "agent",
            },
        )
    assert response.status_code == 400


# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE PROFILE (PATCH /auth/me)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_update_me_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.patch("/api/v1/auth/me", json={"full_name": "Novo Ime"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_update_me():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "update_me@test.com", "password": "pass123", "full_name": "Staro Ime", "role": "user"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "update_me@test.com", "password": "pass123"},
        )
        token = login.json()["access_token"]
        resp = await client.patch(
            "/api/v1/auth/me",
            json={"full_name": "Novo Ime Prezime"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Novo Ime Prezime"


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE CHAT HISTORY (DELETE /auth/me/history)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_delete_history_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete("/api/v1/auth/me/history")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_delete_history():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "del_hist@test.com", "password": "pass123", "full_name": "Del Hist", "role": "user"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "del_hist@test.com", "password": "pass123"},
        )
        token = login.json()["access_token"]
        resp = await client.delete(
            "/api/v1/auth/me/history",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE ACCOUNT (DELETE /auth/me)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_delete_account_requires_auth():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete("/api/v1/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_delete_account():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "del_account@test.com", "password": "pass123", "full_name": "Del Account", "role": "user"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "del_account@test.com", "password": "pass123"},
        )
        token = login.json()["access_token"]
        resp = await client.delete(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
