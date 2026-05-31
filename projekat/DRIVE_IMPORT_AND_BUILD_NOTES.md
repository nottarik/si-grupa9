# Notes: Google Drive batch import + backend build speed-up

Two things landed together:

1. **Google Drive batch import** — admin pastes a Drive folder ID, the system
   pulls the supported files and runs them through the existing transcript
   pipeline (on-demand).
2. **Backend Docker build optimization** — cut the rebuild from ~20 min toward
   ~1–2 min on subsequent builds, without changing runtime behaviour.

---

## 1. Backend build speed-up

### Why it was slow
`backend/requirements.txt` includes `sentence-transformers`, which pulls in
`torch`. By default `pip install torch` resolves the **CUDA build**, dragging in
~2–3 GB of NVIDIA libraries (`nvidia-cuda-*`, `cudnn`, `cublas`, …) — even though
this app does **CPU-only** embedding (`EmbeddingService` calls
`SentenceTransformer.encode(...)` with no GPU anywhere).

On top of that, the whole pip layer was one `RUN` keyed on `requirements.txt`.
Any edit to that file (e.g. adding the two Google deps) invalidated the layer and
re-downloaded **everything** from scratch.

### What changed (`backend/Dockerfile`)
All changes preserve the exact runtime environment — same packages, same spacy
model, same `apt` packages, same start command.

| Change | Effect |
|---|---|
| **CPU-only torch in its own layer**, installed *before* `requirements.txt` via `--index-url https://download.pytorch.org/whl/cpu` | Skips the multi-GB CUDA download. `sentence-transformers` then sees torch already satisfied and does not pull the CUDA build. Helps even the first build. Layer stays cached across `requirements.txt` edits. |
| **BuildKit pip cache mount** (`RUN --mount=type=cache,target=/root/.cache/pip ...`) on both pip installs | Downloaded wheels persist between builds. Editing `requirements.txt` then re-downloads only the *changed* packages, not the whole set. |
| **`# syntax=docker/dockerfile:1`** directive | Enables the cache-mount syntax. |
| **`backend/.dockerignore`** (new) | Excludes `__pycache__`, caches, `.venv`, `*.db`, `.git`, `.env*` so a smaller context is sent to the daemon each build. |

### Why it is safe
- The container has no GPU; `SentenceTransformer` already ran on CPU. CPU torch
  produces an **identical** runtime — only the wasted CUDA payload is removed.
- `requirements.txt` is unchanged as the single source of truth for packages.
- `apt` packages, the spacy model download, and the `CMD` are byte-for-byte the same.

### Expected impact
- **First build after this change:** still downloads packages once (the pip cache
  starts empty), but CPU torch (~190 MB) instead of CUDA torch (~2.5 GB) already
  cuts it substantially.
- **Every rebuild after that:** wheels come from the cache; a `requirements.txt`
  edit only fetches the changed package(s). Minutes, not tens of minutes.

### Requirements / gotchas
- Needs **BuildKit**, which is the default in Docker Compose v2 (confirmed
  `v5.1.1` locally) and Docker 29. Build with `docker compose up --build`.
- If a build ever errors that `--mount` is unsupported, BuildKit was not active —
  set `DOCKER_BUILDKIT=1` (PowerShell: `$env:DOCKER_BUILDKIT=1`) before building.

> Not yet timed on a live daemon — the numbers above are expected, based on the
> standard BuildKit patterns used. Verify on the next real build.

---

## 2. Google Drive batch import

### What it does
An admin enters a Google Drive **folder ID**; the backend lists the supported
files in that folder, downloads each, and feeds them through the **same pipeline
already used by manual uploads** (`process_transcript`). On-demand only (a button);
no scheduling.

- Supported types: `.mp3`, `.wav`, `.m4a`, `.ogg`, `.txt`, `.pdf`
- Dedup: files already imported from a folder are skipped (idempotent re-runs).
- No DB migration, no new services, no Celery.

### How it works
1. `POST /api/v1/transcripts/import-drive` (admin) validates config, then fires a
   FastAPI **BackgroundTask** and returns immediately.
2. The task `import_drive_folder(folder_id, uploader_id)`:
   - lists the folder via `GoogleDriveService`,
   - preloads existing names (dedup) — naming scheme `gdrive:<folder_id>:<filename>`,
   - for each new file, reuses the exact `/upload` logic: audio → Supabase Storage,
     `.txt` → decode, `.pdf` → text extraction; creates a `Transkript` row
     (status `Sirovi`) and calls `process_transcript`.
   - per-file errors are caught so one bad file does not abort the batch.
3. New rows appear in the **Transcripts** list and move `Sirovi → Obradjeno` as the
   pipeline processes them.

### Files changed / added
**Backend**
- `app/services/transcript/file_utils.py` *(new)* — shared `classify_file`,
  `extract_pdf_text`, and the `ALLOWED_*` / `MAX_FILE_SIZE` constants, lifted out of
  the upload route so the route and the import task share one definition.
- `app/services/storage/google_drive_service.py` *(new)* — `GoogleDriveService`:
  service-account auth, paginated `list_files`, `download_file`. Google libs are
  imported lazily, so nothing loads them unless an import actually runs.
- `app/tasks/transcript_tasks.py` — new `import_drive_folder(...)`.
- `app/api/v1/routes/transcripts.py` — new `POST /transcripts/import-drive`; now
  imports the shared helpers instead of defining them locally.
- `app/schemas/transcript.py` — `DriveImportRequest` / `DriveImportResponse`.
- `app/core/config.py` — new `GOOGLE_SERVICE_ACCOUNT_JSON` setting (default `""`).
- `requirements.txt` — `google-api-python-client`, `google-auth`.

**Frontend**
- `src/api/transcripts.ts` — `importDriveTranscripts(folderId)`.
- `src/components/admin/sections/UploadSection.tsx` — new **☁️ Drive** tab with a
  folder-ID input, "Start Import" button, and status message.

### Configuration (one-time, manual)
1. Google Cloud: create a project, enable **Google Drive API**, create a
   **Service Account**, download its **JSON key**.
2. Share the target Drive folder with the service account's email (Viewer).
3. Put the whole JSON key as one line in `backend/.env`:
   ```
   GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":...}
   ```
   (Never commit this; `.env` is git-ignored and excluded from the image.)

If `GOOGLE_SERVICE_ACCOUNT_JSON` is unset, the endpoint returns **503** with a
clear message and the UI shows it — useful as a quick wiring check.

### How to test
- **Without Google setup:** open Admin → Upload → ☁️ Drive, enter anything, click
  Start Import → expect the 503 "not configured" message. That proves the full
  chain (UI → API → endpoint → admin auth → config guard) is wired.
- **With Google setup:** set the env var, restart the backend, paste a real folder
  ID, Start Import, then watch the Transcripts list fill in.

### Deliberately deferred (not built)
- **Scheduled runs:** would reuse the existing `/internal/*` + `INTERNAL_API_KEY`
  pattern plus a `schedule:` GitHub Actions workflow hitting the tunnel.
- **Other sources (S3, etc.):** would extract a small `RemoteSource` interface and
  add an `S3Source`; the pipeline stays untouched.
