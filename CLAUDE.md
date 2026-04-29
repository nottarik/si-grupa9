# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG-based AI chatbot system for call center support. Ingests call transcripts, builds a knowledge base via vector embeddings, and answers agent queries using retrieval-augmented generation. Includes a chat UI and an admin dashboard.

## Commands

### Frontend (`projekat/frontend/`)
```bash
npm run dev       # Dev server on port 5173
npm run build     # Production build
npm run preview   # Preview production build
npm run lint      # ESLint (strict, max-warnings 0)
```

### Backend (`projekat/backend/`)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload          # Dev server on port 8000
celery -A app.workers.celery_app worker --loglevel=info  # Async task worker
pytest                                  # Run all tests
pytest tests/path/to/test_file.py      # Run a single test file
```

### Full Stack (Docker Compose, from `projekat/`)
```bash
docker-compose up     # Start all 7 services
docker-compose down   # Stop all services
```

### Database Migrations (from `projekat/backend/`)
```bash
alembic upgrade head        # Apply all migrations
alembic revision --autogenerate -m "description"  # Create new migration
```

## Architecture

### Backend (`projekat/backend/app/`)

Layered FastAPI application with async SQLAlchemy:

- **`api/v1/`** — Route handlers: `auth`, `chat`, `knowledge`, `transcripts`. Thin layer — delegates immediately to services.
- **`services/`** — All business logic:
  - `ai/` — `RagService` (retrieval + generation), `EmbeddingService` (sentence-transformers), `LLMService` (Groq API), `VectorStoreService` (Qdrant CRUD)
  - `transcript/` — `TranscriptionService` (faster-whisper speech-to-text)
  - `pipeline/` — `PipelineService` (normalize → mask PII → embed → store in Qdrant)
  - `auth/` — JWT generation, RBAC enforcement
- **`db/`** — SQLAlchemy ORM models: `User`, `KnowledgeItem`, `ChatInteraction`, `Feedback`, `Transcript`
- **`schemas/`** — Pydantic v2 request/response models (strict validation)
- **`tasks/`** — Celery task definitions for long-running work (transcription, bulk embedding)
- **`core/`** — `config.py` (all settings from `.env`), `security.py` (JWT + passlib)

### Frontend (`projekat/frontend/src/`)

React 18 + TypeScript + React Query:

- **`api/`** — Axios client modules per domain (`auth`, `chat`, `knowledge`, `transcripts`)
- **`components/`** — Reusable UI: `ChatWindow`, `TranscriptUpload`, `Layout`
- **`pages/`** — Route-level components: `ChatPage`, `LoginPage`, `AdminPage`
- **`hooks/`** — `useAuth`, `useChat` (wrap React Query calls)
- **`App.tsx`** — Router setup with protected routes (role-checked via `useAuth`)

### Infrastructure (`projekat/`)

Docker Compose orchestrates: `frontend`, `backend`, `celery_worker`, `db` (PostgreSQL 16), `redis` (broker + cache), `qdrant` (vector DB), `nginx` (reverse proxy with SSL).

### RAG Pipeline

1. Transcript uploaded → `PipelineService` normalizes text, masks PII, chunks content
2. Chunks embedded via `all-MiniLM-L6-v2` (384-dim vectors) → stored in Qdrant collection `knowledge_base`
3. On chat `/ask`: question embedded → cosine similarity search in Qdrant (top-K=5) → top results injected as context into Groq LLM (`llama-3.1-70b-versatile`) → answer returned with confidence score
4. Confidence threshold: 0.6 — responses below this get a fallback message

### Auth & Roles

JWT-based (stateless). Four roles: `admin`, `agent`, `user`, `manager`. RBAC enforced in service layer. Tokens issued on login, verified on every protected endpoint.

## Key Configuration

All backend settings via environment variables (see `app/core/config.py`):
- `GROQ_API_KEY` — required for LLM
- `DATABASE_URL` — PostgreSQL async URL (`postgresql+asyncpg://...`)
- `QDRANT_URL` / `QDRANT_COLLECTION_NAME`
- `REDIS_URL`
- `SECRET_KEY` — JWT signing secret
- `WHISPER_MODEL_SIZE` — `small` | `base` | `medium` | `large`
- `RAG_TOP_K` / `RAG_CONFIDENCE_THRESHOLD`

Frontend proxies API calls to `backend:8000` via Vite dev config and nginx in production.

## Tech Stack

### Runtime
- Python 3.12

### Frontend
- React 18, TypeScript, Vite (build/dev server)
- Tailwind CSS (styling)
- Axios (HTTP client), React Query (server state)

### Backend
- FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic
- python-jose (JWT), passlib + bcrypt (password hashing)

### AI & Processing
- LangChain (RAG pipeline orchestration)
- Groq API — `llama-3.1-70b-versatile` (LLM)
- faster-whisper `small` model (local audio transcription)
- sentence-transformers `all-MiniLM-L6-v2` (local embeddings)
- Celery (async task queue)

### Data Stores
- PostgreSQL 16 (relational) supabase, Qdrant (vector DB), Redis 7 (broker + cache)

### Infrastructure
- Docker + Docker Compose, Nginx (reverse proxy + SSL)
- Let's Encrypt / Certbot (TLS), Ubuntu 22.04 LTS
- supabase free tier and render free tier and qdrant free tier and GitHub Actions (CI/CD)

## Language Note

The application domain, UI text, and most documentation are written in Bosnian. Variable and function names in code are English.

## Database Structure in Supabase

korisnik

* id (UUID, PK)
* ime, prezime, email
* uloga (enum)
* datum_kreiranja, aktivan
* auth_user_id (link na Supabase auth)

kategorija

* id (PK)
* naziv, opis
* nadredjena_kategorija_id (self-reference)
* aktivan

transkript

* id (PK)
* naziv
* datum_poziva, trajanje_sec
* format (audio/tekst)
* status (Sirovi/Obradjeno/Odbacen)
* id_korisnika_upload
* datum_uploada
* jezik
* kvalitet

segment

* id (PK)
* tekst
* tip_segmenta (Pitanje/Odgovor/Kontekst)
* pozicija_u_transkriptu
* id_transkripta
* status (Validan/Nevalidan/NaCekanju)
* id_kategorije
* pouzdanost_score
* datum_ekstrakcije

baza_znanja

* id (PK)
* naziv, verzija
* datum_kreiranja
* status (Aktivna/Arhivirana/NaCekanju)
* id_administratora
* broj_unosa

unos_baze_znanja (GLAVNA tabela za RAG)

* id (PK)
* pitanje, odgovor
* id_baze_znanja
* id_kategorije
* id_segmenta (source trace)
* status_aprovacije
* datum_kreiranja, datum_azuriranja
* tezina_pouzdanosti
* aktivan
* verzija_broj
* prethodna_verzija_id
* vector_id (ID u vector DB)

chat_sesija

* id (PK)
* datum_pocetka, datum_zavrsetka
* id_korisnika
* kanal_pristupa (web/mobile/API)
* status
* broj_poruka

poruka

* id (PK)
* tekst
* tip (user/chatbot)
* timestamp_msg
* id_sesije
* id_odgovora (ako postoji)

odgovor

* id (PK)
* tekst_odgovora
* id_unosa_baze_znanja (retrieved source)
* metoda_generisanja (Retrieval/Generativno/Fallback)
* skor_pouzdanosti
* latencija_ms
* id_poruke

feedback

* id (PK)
* ocjena (1–5)
* komentar
* tip (user/admin)
* timestamp
* id_odgovora
* id_korisnika

anomalija

* id (PK)
* opis
* tip (npr. low confidence, no answer)
* nivo_ozbiljnosti
* status
* datum_kreiranja
* id_poruke
* id_odgovora

Relationships Summary

* transkript → segment (1:N)
* segment → unos_baze_znanja (optional source link)
* baza_znanja → unos_baze_znanja (1:N)
* unos_baze_znanja → Pinecone (1:1 preko pinecone_id)
* chat_sesija → poruka (1:N)
* poruka → odgovor (1:1 optional)
* odgovor → unos_baze_znanja (retrieval reference)
* odgovor → feedback (1:N)
* odgovor → anomalija (1:1 or 1:N depending usage)

RAG Usage

* Retrieval se radi nad Pinecone koristeći pinecone_id
* Nakon retrieval-a, mapira se nazad na unos_baze_znanja
* Chatbot odgovori koriste podatke iz unos_baze_znanja
* Svaki odgovor može biti trace-an nazad do segmenta i transkripta
