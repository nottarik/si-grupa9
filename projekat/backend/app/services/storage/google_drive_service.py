"""Read-only Google Drive access for batch importing transcript source files.

Authenticates with a service account (no OAuth user flow). The admin shares the
target Drive folder with the service account's email; this service lists and
downloads the supported files from that folder.
"""
import io
import json
import logging

from app.core.config import settings
from app.services.transcript.file_utils import (
    ALLOWED_AUDIO_TYPES,
    ALLOWED_PDF_TYPES,
    ALLOWED_TEXT_TYPES,
)

logger = logging.getLogger(__name__)

_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
_SUPPORTED_MIME_TYPES = ALLOWED_AUDIO_TYPES | ALLOWED_TEXT_TYPES | ALLOWED_PDF_TYPES


class GoogleDriveService:
    """Wrapper around the Google Drive API for listing and downloading files."""

    def __init__(self):
        self._service = None

    def _client(self):
        if self._service is None:
            if not settings.GOOGLE_SERVICE_ACCOUNT_JSON:
                raise RuntimeError(
                    "GOOGLE_SERVICE_ACCOUNT_JSON is not configured."
                )
            # Imported lazily so the dependency is only required when Drive import is used.
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            try:
                info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
            except json.JSONDecodeError as exc:
                raise RuntimeError(
                    f"GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON: {exc}"
                ) from exc

            creds = service_account.Credentials.from_service_account_info(
                info, scopes=_SCOPES
            )
            self._service = build("drive", "v3", credentials=creds, cache_discovery=False)
        return self._service

    def list_files(self, folder_id: str) -> list[dict]:
        """Return [{id, name, mimeType, modifiedTime}] for supported, non-trashed files."""
        service = self._client()
        query = f"'{folder_id}' in parents and trashed = false"
        files: list[dict] = []
        page_token: str | None = None
        while True:
            response = (
                service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
                    pageToken=page_token,
                    pageSize=100,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )
            for f in response.get("files", []):
                if f.get("mimeType") in _SUPPORTED_MIME_TYPES:
                    files.append(f)
            page_token = response.get("nextPageToken")
            if not page_token:
                break
        return files

    def download_file(self, file_id: str) -> bytes:
        """Download a Drive file's raw bytes."""
        from googleapiclient.http import MediaIoBaseDownload

        service = self._client()
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return buffer.getvalue()
