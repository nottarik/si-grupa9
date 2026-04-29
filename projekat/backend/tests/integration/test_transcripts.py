import pytest
import io
from httpx import AsyncClient, ASGITransport
from app.main import app


async def get_auth_token(client: AsyncClient) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "admin123"},
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_upload_transcript_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/transcripts/upload")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upload_unsupported_file_type():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await get_auth_token(client)
        response = await client.post(
            "/api/v1/transcripts/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.exe", b"fake content", "application/octet-stream")},
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_txt_file():
    from unittest.mock import patch, MagicMock
    mock_task = MagicMock()
    mock_task.id = "fake-task-id"
    with patch("app.api.v1.routes.transcripts.process_transcript_task.delay", return_value=mock_task):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            token = await get_auth_token(client)
            content = b"Korisnik: kako platiti racun?\nAgent: putem internet bankarstva."
            response = await client.post(
                "/api/v1/transcripts/upload",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": ("test.txt", content, "text/plain")},
            )
    assert response.status_code == 200
    assert "transcript_id" in response.json()

@pytest.mark.asyncio
async def test_list_transcripts_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/transcripts/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_transcripts_with_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await get_auth_token(client)
        response = await client.get(
            "/api/v1/transcripts/",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_transcript_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await get_auth_token(client)
        response = await client.get(
            "/api/v1/transcripts/999999",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 404