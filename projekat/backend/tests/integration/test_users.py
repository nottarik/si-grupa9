import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.security import get_password_hash
from app.db.models.user import Korisnik, UlogaTip
from app.db.session import AsyncSessionLocal
from app.main import app


async def _admin_token(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    return resp.json()["access_token"]


async def _create_user(email: str, uloga: UlogaTip = UlogaTip.call_centar_agent) -> str:
    from sqlalchemy import select
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Korisnik).where(Korisnik.email == email))
        existing = result.scalar_one_or_none()
        if existing:
            return str(existing.id)
        user = Korisnik(
            ime="Test",
            prezime="User",
            email=email,
            hashed_password=get_password_hash("pass123"),
            uloga=uloga.value,
            aktivan=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return str(user.id)


@pytest.mark.asyncio
async def test_list_users_unauthenticated():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/users")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_users_as_non_admin_forbidden():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "list_agent@test.com", "password": "pass123", "full_name": "List Agent", "role": "agent"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "list_agent@test.com", "password": "pass123"},
        )
        token = login.json()["access_token"]
        resp = await client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_users_as_admin_returns_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    first = body[0]
    assert "id" in first
    assert "email" in first
    assert "role" in first
    assert "is_active" in first


@pytest.mark.asyncio
async def test_update_role_as_admin():
    user_id = await _create_user("role_update_target@test.com", UlogaTip.call_centar_agent)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.patch(
            f"/api/v1/users/{user_id}/role",
            json={"role": "manager"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["role"] == "manager"
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_update_role_non_admin_forbidden():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "role_noperm@test.com", "password": "pass123", "full_name": "No Perm", "role": "agent"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "role_noperm@test.com", "password": "pass123"},
        )
        agent_token = login.json()["access_token"]
        fake_id = str(uuid.uuid4())
        resp = await client.patch(
            f"/api/v1/users/{fake_id}/role",
            json={"role": "admin"},
            headers={"Authorization": f"Bearer {agent_token}"},
        )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_update_role_user_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.patch(
            f"/api/v1/users/{uuid.uuid4()}/role",
            json={"role": "agent"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_role_invalid_role_value():
    user_id = await _create_user("role_invalid@test.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.patch(
            f"/api/v1/users/{user_id}/role",
            json={"role": "superuser"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_delete_user_as_admin():
    user_id = await _create_user("delete_target@test.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.delete(
            f"/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_removes_from_list():
    user_id = await _create_user("delete_verify@test.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        await client.delete(f"/api/v1/users/{user_id}", headers={"Authorization": f"Bearer {token}"})
        resp = await client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    ids = [u["id"] for u in resp.json()]
    assert user_id not in ids


@pytest.mark.asyncio
async def test_delete_self_forbidden():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        me = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        admin_id = me.json()["id"]
        resp = await client.delete(
            f"/api/v1/users/{admin_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_delete_user_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _admin_token(client)
        resp = await client.delete(
            f"/api/v1/users/{uuid.uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_non_admin_forbidden():
    user_id = await _create_user("delete_noperm_target@test.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "delete_noperm@test.com", "password": "pass123", "full_name": "No Perm", "role": "agent"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "delete_noperm@test.com", "password": "pass123"},
        )
        agent_token = login.json()["access_token"]
        resp = await client.delete(
            f"/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
    assert resp.status_code == 403
