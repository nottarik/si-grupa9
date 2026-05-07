import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app


# ─── Pomoćne funkcije ─────────────────────────────────────────────────────────

async def _get_auth_token(client: AsyncClient) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    return response.json()["access_token"]


async def _upload_txt(
    client: AsyncClient,
    token: str,
    content: bytes = b"Agent: Zdravo\nKorisnik: Kako mogu pomoci.",
    filename: str = "test.txt",
) -> int:
    with patch("app.api.v1.routes.transcripts.process_transcript", new=AsyncMock()):
        resp = await client.post(
            "/api/v1/transcripts/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": (filename, content, "text/plain")},
        )
    assert resp.status_code == 200
    return resp.json()["transcript_id"]


# ═══════════════════════════════════════════════════════════════════════════════
# UPLOAD
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_upload_transcript_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/transcripts/upload")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_unsupported_file_type():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        response = await client.post(
            "/api/v1/transcripts/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.exe", b"fake content", "application/octet-stream")},
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_txt_file():
    with patch("app.api.v1.routes.transcripts.process_transcript", new=AsyncMock()):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            token = await _get_auth_token(client)
            content = b"Korisnik: kako platiti racun?\nAgent: putem internet bankarstva."
            response = await client.post(
                "/api/v1/transcripts/upload",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("test.txt", content, "text/plain")},
            )
    assert response.status_code == 200
    assert "transcript_id" in response.json()


# ═══════════════════════════════════════════════════════════════════════════════
# LIST
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_list_transcripts_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/transcripts/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_transcripts_with_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        response = await client.get(
            "/api/v1/transcripts/",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ═══════════════════════════════════════════════════════════════════════════════
# GET ONE
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_get_transcript_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        response = await client.get(
            "/api/v1/transcripts/999999",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 404


# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE (PATCH)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_update_transcript_name():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        tid = await _upload_txt(client, token)
        resp = await client.patch(
            f"/api/v1/transcripts/{tid}",
            json={"naziv": "Preimenovan.txt"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["naziv"] == "Preimenovan.txt"


@pytest.mark.asyncio
async def test_update_transcript_processed_text():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        tid = await _upload_txt(client, token)
        resp = await client.patch(
            f"/api/v1/transcripts/{tid}",
            json={"processed_text": "Ažurirani sadržaj transkripta."},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    assert resp.json()["processed_text"] == "Ažurirani sadržaj transkripta."


@pytest.mark.asyncio
async def test_update_transcript_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        resp = await client.patch(
            "/api/v1/transcripts/999999",
            json={"naziv": "Novo ime.txt"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_transcript_unauthenticated():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.patch("/api/v1/transcripts/1", json={"naziv": "x.txt"})
    assert resp.status_code == 401


# ═══════════════════════════════════════════════════════════════════════════════
# DELETE
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_delete_transcript():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        tid = await _upload_txt(client, token, filename="to_delete.txt")
        resp = await client.delete(
            f"/api/v1/transcripts/{tid}",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_transcript_removes_from_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        tid = await _upload_txt(client, token, filename="to_delete_verify.txt")
        await client.delete(
            f"/api/v1/transcripts/{tid}",
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.get(
            "/api/v1/transcripts/",
            headers={"Authorization": f"Bearer {token}"},
        )
    ids = [t["id"] for t in resp.json()]
    assert tid not in ids


@pytest.mark.asyncio
async def test_delete_transcript_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        resp = await client.delete(
            "/api/v1/transcripts/999999",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_transcript_non_admin_forbidden():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        tid = await _upload_txt(client, token, filename="agent_cannot_delete.txt")
        await client.post(
            "/api/v1/auth/register",
            json={"email": "tr_delete_agent@test.com", "password": "pass123", "full_name": "Agent", "role": "agent"},
        )
        login = await client.post(
            "/api/v1/auth/login",
            json={"email": "tr_delete_agent@test.com", "password": "pass123"},
        )
        agent_token = login.json()["access_token"]
        resp = await client.delete(
            f"/api/v1/transcripts/{tid}",
            headers={"Authorization": f"Bearer {agent_token}"},
        )
    assert resp.status_code == 403


# ═══════════════════════════════════════════════════════════════════════════════
# SEARCH / FILTER
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_search_transcripts_by_keyword():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _get_auth_token(client)
        unique_keyword = "xyzuniqueterm987"
        await _upload_txt(
            client, token,
            content=f"Korisnik pita o {unique_keyword} usluzi.".encode(),
            filename="keyword_test.txt",
        )
        resp = await client.get(
            "/api/v1/transcripts/",
            params={"q": unique_keyword},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) >= 1