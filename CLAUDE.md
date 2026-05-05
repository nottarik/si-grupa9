# CLAUDE.md

RAG-based AI chatbot for call center support. Ingests call transcripts, builds a vector knowledge base, and answers agent queries via retrieval-augmented generation. Chat UI + admin dashboard. UI text and domain docs are in Bosnian; code identifiers are English.

## Commands

### Frontend (`projekat/frontend/`)
```bash
npm run dev       # Dev server on port 5173
npm run build     # Production build
npm run lint      # ESLint (strict, max-warnings 0)
```

### Backend (`projekat/backend/`)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload                              # Dev server on port 8000
celery -A app.workers.celery_app worker --loglevel=info   # Async task worker
pytest                                                     # Run all tests
pytest tests/path/to/test_file.py                         # Run single test file
```

### Full Stack (from `projekat/`)
```bash
docker-compose up     # Start all 7 services
docker-compose down
```

### Database Migrations (from `projekat/backend/`)
```bash
alembic upgrade head
alembic revision --autogenerate -m "description"
```

## Architecture

### Backend (`projekat/backend/app/`)
- **`api/v1/`** — Thin route handlers: `auth`, `chat`, `knowledge`, `transcripts`
- **`services/ai/`** — `RagService`, `EmbeddingService` (sentence-transformers), `LLMService` (Groq), `VectorStoreService` (Qdrant)
- **`services/transcript/`** — `TranscriptionService` (faster-whisper)
- **`services/pipeline/`** — `PipelineService`: normalize → mask PII → embed → store in Qdrant
- **`services/auth/`** — JWT generation, RBAC enforcement
- **`db/`** — SQLAlchemy ORM models; **`schemas/`** — Pydantic v2; **`tasks/`** — Celery jobs; **`core/`** — config + security

### Frontend (`projekat/frontend/src/`)
- **`api/`** — Axios modules per domain; **`components/`** — `ChatWindow`, `TranscriptUpload`, `Layout`
- **`pages/`** — `ChatPage`, `LoginPage`, `AdminPage`; **`hooks/`** — `useAuth`, `useChat`
- **`App.tsx`** — Router with role-checked protected routes

### Infrastructure
Docker Compose: `frontend`, `backend`, `celery_worker`, `db` (PostgreSQL 16), `redis`, `qdrant`, `nginx` (SSL).

### RAG Pipeline
1. Transcript uploaded → `PipelineService` normalizes, masks PII, chunks text
2. Chunks embedded via `all-MiniLM-L6-v2` (384-dim) → stored in Qdrant collection `knowledge_base`
3. On `/ask`: question embedded → cosine search (top-K=5) → context injected into Groq `llama-3.1-70b-versatile` → answer + confidence score
4. Confidence threshold 0.6 — below triggers fallback message

### Auth & Roles
JWT (stateless). Roles: `admin`, `agent`, `user`, `manager`. RBAC enforced in service layer.

## Key Configuration

All settings via env vars (`app/core/config.py`):
- `GROQ_API_KEY`, `SECRET_KEY`
- `DATABASE_URL` — `postgresql+asyncpg://...`
- `QDRANT_URL`, `QDRANT_COLLECTION_NAME`
- `REDIS_URL`
- `WHISPER_MODEL_SIZE` — `small` | `base` | `medium` | `large`
- `RAG_TOP_K`, `RAG_CONFIDENCE_THRESHOLD`

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Axios, React Query
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, python-jose, passlib/bcrypt
- **AI:** LangChain, Groq API (`llama-3.1-70b-versatile`), faster-whisper, sentence-transformers, Celery
- **Data:** PostgreSQL 16 (Supabase), Qdrant (vector DB), Redis 7
- **Infra:** Docker Compose, Nginx, Let's Encrypt, Ubuntu 22.04, Render + Supabase + Qdrant free tiers, GitHub Actions

## Database (Supabase)

| Table | Purpose |
|---|---|
| `korisnik` | Users (UUID PK, ime/prezime/email, uloga enum, auth_user_id) |
| `kategorija` | Categories (self-referencing hierarchy) |
| `transkript` | Uploaded transcripts (format, status, jezik, kvalitet) |
| `segment` | Transcript chunks (tip_segmenta, pouzdanost_score, status) |
| `baza_znanja` | Knowledge base versions (status, id_administratora) |
| `unos_baze_znanja` | **RAG entries** — pitanje/odgovor, vector_id (Qdrant), approval status, versioning |
| `chat_sesija` | Chat sessions (kanal_pristupa, status, broj_poruka) |
| `poruka` | Messages (tip: user/chatbot) |
| `odgovor` | Responses (metoda_generisanja, skor_pouzdanosti, latencija_ms) |
| `feedback` | Ratings 1–5 per response |
| `anomalija` | Low-confidence / no-answer events |

**Key relationships:** `transkript` → `segment` → `unos_baze_znanja` (source trace); `chat_sesija` → `poruka` → `odgovor` → `unos_baze_znanja` (retrieval ref) → `feedback`/`anomalija`.

**RAG:** retrieval runs against Qdrant using `vector_id`; results map back to `unos_baze_znanja`, traceable to originating `segment` and `transkript`.
