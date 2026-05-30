# Call Centar Chatbot

A RAG-based AI assistant for ISP/telecom call center support. Agents upload call transcripts; the system processes them into a searchable knowledge base, and end users get accurate, source-traced answers through a chat interface. Admins review and manage everything through a dedicated dashboard.

## How it works

**Transcript → Knowledge Base**

When a transcript is uploaded (audio or text), it goes through a preprocessing pipeline: text normalization, PII masking (names, phone numbers, IDs are replaced with encrypted tokens), speaker detection, and chunking. The pipeline then uses an LLM to extract Q&A pairs from the conversation — if that fails, it falls back to a pattern-matching approach that pairs user questions with agent answers. Every Q&A pair is embedded with `all-MiniLM-L6-v2` (384-dim vectors) and stored in Qdrant.

**Chat → Answer**

When a user sends a question, the system classifies intent first: domain question, small talk, escalation request, or out-of-scope. For domain questions it embeds the query and runs a cosine similarity search against Qdrant (top-K=5). If the top hit scores above threshold, context is injected into a Groq LLM prompt (`llama-3.3-70b-versatile`) to generate a grounded answer. Below a low-confidence threshold the system routes to a human agent instead. Short or context-dependent questions are rewritten using conversation history before retrieval.

There are two confidence thresholds: `RAG_CONFIDENCE_THRESHOLD` (0.55) for a clean answer, and `RAG_CONFIDENCE_THRESHOLD_LOW` (0.35) — anything in between gets answered with an uncertainty note appended. Below the low threshold triggers escalation and logs an anomaly.

Prompt injection patterns are detected and rejected before any retrieval happens.

## Tech stack

**Backend** — Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic v2, Celery  
**AI** — Groq API (`llama-3.3-70b-versatile`), faster-whisper (audio transcription), sentence-transformers (`all-MiniLM-L6-v2`), LangChain  
**Data** — PostgreSQL 16 (Supabase), Qdrant (vector DB), Redis 7  
**Frontend** — React 18, TypeScript, Vite, Tailwind CSS, React Query, Axios  
**Infra** — Docker Compose (7 services), Nginx, Azure + Render + Supabase + Qdrant free tiers, GitHub Actions

## Running locally

```bash
# Prerequisites: Docker, Docker Compose

cd projekat
docker-compose up
```

This starts the backend (`:8000`), frontend (`:5173`), PostgreSQL, Redis, Qdrant, Celery worker, and Nginx reverse proxy.

**Backend only:**
```bash
cd projekat/backend
pip install -r requirements.txt
uvicorn app.main:app --reload                             # API on :8000
celery -A app.workers.celery_app worker --loglevel=info  # Async worker
```

**Frontend only:**
```bash
cd projekat/frontend
npm install
npm run dev  # Dev server on :5173
```

**Database migrations:**
```bash
cd projekat/backend
alembic upgrade head
```

## Configuration

All settings are environment variables. Copy `backend/.env.example` and fill in:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | JWT signing key |
| `GROQ_API_KEY` | Groq API key for LLM |
| `DATABASE_URL` | `postgresql+asyncpg://...` |
| `QDRANT_URL` | Qdrant instance URL |
| `REDIS_URL` | Redis connection string |
| `WHISPER_MODEL` | `base` / `small` / `medium` / `large-v3` |
| `TOKEN_MAP_KEY` | Fernet key for PII token encryption |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | For Google Drive batch import |
| `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` | Supabase file storage |

## Features

**Admin dashboard** — upload transcripts, monitor pipeline progress in real time (per-stage status via WebSocket), approve or reject Q&A entries before they enter the knowledge base, manually add KB entries, manage users, review escalation queue, view chat logs and ratings, post announcements.

**Agent shell** — agents see their escalation queue, handle live escalated chats (WebSocket), look up the knowledge base directly, and review their conversation history.

**Chat interface** — users chat with the AI assistant, can rate responses, and get seamlessly handed off to a human agent when the system can't answer confidently or when they explicitly ask for one.

**RAG pipeline** — intent classification routes each message before any retrieval happens. Query rewriting handles follow-up questions that reference prior context. PII tokens are stripped from answers before they reach the user.

**Self-healing startup** — on restart, the backend automatically re-embeds any approved KB entries that weren't indexed yet and re-processes any transcripts stuck in a raw state from a previous crash.

**Google Drive batch import** — one-click pipeline run that pulls transcripts from a configured Drive folder, processes them all, and updates the knowledge base.

## Project structure

```
projekat/
├── backend/
│   └── app/
│       ├── api/v1/routes/      # auth, chat, knowledge, transcripts, escalation
│       ├── services/
│       │   ├── ai/             # RagService, EmbeddingService, LLMService, VectorStore
│       │   ├── preprocessing/  # normalize, PII masking, chunking, QA extraction
│       │   ├── transcript/     # audio transcription (Whisper)
│       │   ├── escalation/     # agent routing
│       │   └── ws/             # WebSocket connection manager
│       ├── db/models/          # SQLAlchemy ORM (korisnik, transkript, unos_baze_znanja, …)
│       ├── schemas/            # Pydantic v2 request/response models
│       ├── tasks/              # Celery async jobs
│       └── core/               # config, security (JWT, RBAC)
└── frontend/
    └── src/
        ├── pages/              # ChatPage, AdminPage, AgentPage, LoginPage, HomePage
        ├── components/
        │   ├── chat/           # ChatWindow, MessageBubble, RatingModal
        │   ├── admin/          # TranscriptUpload, PipelineMonitor, KnowledgeApprovedList, …
        │   └── agent/          # AgentShell, AgentQueue, KbLookup
        ├── api/                # Axios modules per domain
        └── hooks/              # useAuth, useChat
```

## Auth & roles

JWT-based (stateless). Four roles: `admin`, `manager`, `agent`, `user`. RBAC is enforced in the service layer, not just the routes. Admins manage everything; agents handle escalations; regular users can only chat.

## Database schema

Core tables: `korisnik` (users), `transkript` (uploaded files), `segment` (text chunks), `unos_baze_znanja` (Q&A KB entries with Qdrant `vector_id`), `chat_sesija`, `poruka`, `odgovor`, `feedback`, `anomalija`, `baza_znanja`. Full traceability from an answer back through the KB entry → segment → original transcript.
