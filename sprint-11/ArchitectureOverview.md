# Architecture / Technical Overview

Kratki tehnički pregled sistema namijenjen osobi koja **prvi put gleda projekat** i treba razumjeti
njegovu strukturu, glavne komponente, kako one komuniciraju, gdje se nalazi ključni kod i koje su
najvažnije sigurnosne odluke.

---

## 1. Šta je sistem

**Call Centar Chatbot** je RAG-zasnovan (Retrieval-Augmented Generation) AI asistent za podršku
call centru telekom/ISP operatera. Sistem:

1. prima transkripte poziva (audio ili tekst),
2. obrađuje ih kroz pipeline (normalizacija → maskiranje PII → detekcija govornika → chunking →
   ekstrakcija Q&A parova → embedding → pohrana u vektorsku bazu),
3. odgovara na pitanja korisnika kroz chat, koristeći retrieval nad bazom znanja + LLM,
4. eskalira na živog agenta kada nije siguran ili kad korisnik to eksplicitno traži.

UI tekstovi i domenski dokumenti su na bosanskom; identifikatori u kodu su na engleskom.

---

## 2. Komponente na visokom nivou

```
            ┌──────────────────────────────────────────────────────────────┐
            │                        KRAJNJI KORISNICI                       │
            │     korisnik (chat)   ·   agent (panel)   ·   admin (panel)    │
            └───────────────┬───────────────────────────┬──────────────────┘
                            │  HTTPS / WSS               │
                            ▼                            ▼
        ┌───────────────────────────┐      ┌──────────────────────────────┐
        │   FRONTEND (Vite SPA)     │      │   (isti SPA, role-routane     │
        │   React 18 + TS + Tailwind│      │    stranice /admin /agent)    │
        │   Azure Static Web App    │      └──────────────────────────────┘
        └─────────────┬─────────────┘
                      │  REST (Axios)  +  WebSocket (chat/escalation)
                      ▼
        ┌───────────────────────────────────────────────────────────────┐
        │                  BACKEND — FastAPI (Python 3.12)               │
        │                  Azure Container App (1 vCPU / 2 GiB)          │
        │                                                               │
        │   api/v1/routes  →  auth · chat · knowledge · transcripts     │
        │                     escalation · schedule · users ·           │
        │                     announcements · internal                  │
        │   services/ai           RagService, EmbeddingService,         │
        │                         LLMService, VectorStoreService        │
        │   services/preprocessing  normalize, PII mask, chunk, QA      │
        │   services/transcript     Groq Whisper transkripcija          │
        │   services/escalation     queue + agent routing              │
        │   services/ws             WebSocket ConnectionManager        │
        │   services/schedule       in-process Drive auto-import loop   │
        │   services/storage        Supabase Storage + Google Drive    │
        └───┬───────────────┬───────────────┬───────────────┬──────────┘
            │               │               │               │
            ▼               ▼               ▼               ▼
   ┌─────────────┐  ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
   │ PostgreSQL  │  │  Qdrant      │ │  Groq API   │ │ Supabase     │
   │ 16 (Supabase│  │  Cloud       │ │ LLM +       │ │ Storage      │
   │ + asyncpg)  │  │ (vektori)    │ │ Whisper     │ │ (fajlovi)    │
   └─────────────┘  └──────────────┘ └─────────────┘ └──────────────┘
                                          ▲
                                          │ (batch import)
                                    ┌─────────────┐
                                    │ Google Drive│
                                    └─────────────┘
```

---

## 3. Frontend, backend, baza i vanjski servisi

### Frontend (`projekat/frontend/`)
- **React 18 + TypeScript + Vite 5 + Tailwind CSS**, state/data preko **React Query**, HTTP preko **Axios**, routing preko **react-router-dom 6**.
- Stranice: `LandingPage`, `LoginPage`, `ChatPage`, `HomePage`, `AdminPage`, `AgentPage`.
- Pristup zaštićen `ProtectedRoute` komponentom (role-checked): `/admin` (admin), `/agent` (admin/agent), `/chat` i `/home` (svaki autentifikovan korisnik).
- API moduli po domeni (`src/api/*.ts`), hookovi (`useAuth`, `useChat`, `useEscalation`).
- Build je statički (`dist/`), servira se kao Azure Static Web App; SPA fallback definisan u `staticwebapp.config.json`.

### Backend (`projekat/backend/app/`)
- **FastAPI 0.111**, **SQLAlchemy 2.0 (async)**, **Pydantic v2**, **Alembic** migracije, **uvicorn** server.
- Slojevi:
  - `api/v1/routes/` — tanke rute (HTTP/WS handleri).
  - `services/` — poslovna logika (AI/RAG, preprocessing, transcript, escalation, ws, schedule, storage, auth).
  - `db/models/` — SQLAlchemy ORM modeli; `schemas/` — Pydantic request/response modeli; `core/` — konfiguracija i sigurnost.
  - `tasks/` — asinhroni poslovi pokrenuti kroz **FastAPI BackgroundTasks** (nema Celery-ja).

### Baza i vanjski servisi
- **PostgreSQL 16 (Supabase)** preko `asyncpg` — relacioni podaci.
- **Qdrant Cloud** — vektorska baza (kolekcija `knowledge_base`, 384-dim vektori).
- **Groq API** — `llama-3.3-70b-versatile` (generisanje/klasifikacija) i `whisper-large-v3` (transkripcija audija).
- **sentence-transformers `all-MiniLM-L6-v2`** — embedding model, izvršava se **lokalno na CPU** unutar backenda.
- **Supabase Storage** (bucket `supabucket`) — pohrana uploadovanih fajlova.
- **Google Drive API** (service account) — batch import transkripata.

---

## 4. Glavni moduli / odgovornosti (gdje se nalazi ključni kod)

| Modul | Putanja | Odgovornost |
|---|---|---|
| RAG odgovaranje | `services/ai/rag_service.py` | Klasifikacija namjere, retrieval, generisanje, eskalacija, perzistencija sesije |
| Embedding | `services/ai/embedding_service.py` | `all-MiniLM-L6-v2` embeddinzi (CPU) |
| LLM | `services/ai/llm_service.py` | Groq pozivi: `classify_intent`, `rewrite_query`, `generate`, `generate_without_context` |
| Vektorska baza | `services/ai/vector_store.py` | Qdrant: `ensure_collection`, `search`, upsert |
| KB indeksiranje | `services/ai/kb_indexing.py` | `embed_pending` (self-heal embedding) |
| Preprocessing pipeline | `services/preprocessing/pipeline.py` | `run_pipeline()` — orkestracija obrade transkripta |
| PII maskiranje | `services/preprocessing/pii/` | Detekcija + maskiranje (JMBG/telefon/email/IBAN/SSN), Fernet token mapa |
| Transkripcija | `services/transcript/transcription_service.py` | Groq Whisper API |
| Eskalacija | `services/escalation/service.py` | Queue, dodjela agenta, prioriteti, statusi |
| WebSocket | `services/ws/connection_manager.py` | Real-time veze korisnik↔agent |
| Scheduler | `services/schedule/scheduler.py` | In-process loop za Drive auto-import |
| Auth/sigurnost | `core/security.py`, `services/auth/` | JWT, hashiranje lozinki, RBAC |
| Konfiguracija | `core/config.py` | Sve env varijable (Pydantic Settings) |

---

## 5. Kako komponente komuniciraju

1. **Korisnik → backend (REST):** SPA šalje `POST /api/v1/chat/ask` sa pitanjem i kratkom historijom. Axios klijent dodaje JWT u `Authorization` header.
2. **Backend → AI servisi:** `RagService.answer()` paralelno klasificira namjeru (Groq) i embeduje pitanje (lokalni model), zatim radi cosine pretragu u Qdrant-u (top-K=5) i, ako je pouzdanost dovoljna, generiše odgovor kroz Groq LLM s injektovanim kontekstom.
3. **Perzistencija:** svaka interakcija upisuje `ChatSesija` → `Poruka` → `Odgovor` (sa `metoda_generisanja`, `skor_pouzdanosti`, `latencija_ms`); slabe/promašene se loguju kao `Anomalija`.
4. **Eskalacija (WebSocket):** ako je potrebna eskalacija, kreira se `Eskalacija` zapis i agentima se preko `ConnectionManager`-a broadcastuje `queue_update`. Korisnik i dodijeljeni agent dalje razmjenjuju poruke real-time preko `/api/v1/escalation/ws/chat/{session_id}` i `/ws/escalation`.
5. **Transcript pipeline:** upload → fajl u Supabase Storage → (audio) Groq Whisper transkripcija → `run_pipeline()` (normalizacija, PII maskiranje, chunking, ekstrakcija Q&A, embedding, upsert u Qdrant + `unos_baze_znanja`). Pokreće se kroz **BackgroundTasks**; napredak po fazama prikazuje se u admin panelu.
6. **Self-heal pri startu:** na startu backend dovršava neembedovane odobrene KB unose i ponovo procesira transkripte zaglavljene u statusu „Sirovi".

---

## 6. Pregled API površine (v1, prefix `/api/v1`)

- **auth:** `POST /auth/register`, `POST /auth/login`, `GET/PATCH /auth/me`, `DELETE /auth/me/history`, `DELETE /auth/me`
- **chat:** `POST /chat/ask`, `POST /chat/feedback`, `GET /chat/ratings`, `GET /chat/logs`, `GET /chat/sessions`, `GET /chat/sessions/{id}/messages`, `POST /chat/sessions/{id}/close|rate`, `DELETE /chat/sessions/{id}`, `GET/PATCH/DELETE /chat/issues...`, `POST /chat/logs/bulk-delete`, `POST /chat/issues/bulk-delete`
- **knowledge:** `GET /knowledge/pending|approved|categories|search|debug`, `POST /knowledge/manual`, `PUT/DELETE /knowledge/{id}`, `POST /knowledge/{id}/approve|reject`, `POST /knowledge/reindex`
- **transcripts:** `POST /transcripts/upload|manual|transcribe-preview|confirm-audio|import-drive|bulk-delete`, `GET /transcripts/|active|drive-folder|{id}`, `PATCH/DELETE /transcripts/{id}`
- **escalation:** `GET /escalation/`, `GET /escalation/agent-statuses|my-stats|my-history|{id}`, `PATCH /escalation/agent-status`, `POST /escalation/request|cancel|{id}/accept|release|resolve`, WS `/escalation/ws/chat/{session_id}`, WS `/escalation/ws/escalation`
- **schedule:** `GET/PUT /schedule/drive`, `POST /schedule/drive/cancel`
- **users:** `GET /users`, `PATCH /users/{id}/role`, `DELETE /users/{id}`
- **announcements:** `GET /announcements/active`, `GET/POST /announcements`, `PATCH/DELETE /announcements/{id}`
- **internal** (zaštićeno `INTERNAL_API_KEY`): `POST /internal/reconcile-transcripts|sync-drive|cleanup-raw-text`
- **health:** `GET /health`, `GET /heartbeat`

Interaktivna dokumentacija dostupna je na `/docs` (Swagger UI) kad backend radi.

---

## 7. Model podataka (PostgreSQL)

| Tabela | Svrha |
|---|---|
| `korisnik` | Korisnici (UUID PK, ime/prezime/email, `uloga` enum, `auth_user_id`) |
| `kategorija` | Kategorije (samoreferencirajuća hijerarhija) |
| `transkript` | Uploadovani transkripti (format, status, jezik, kvalitet) |
| `segment` | Chunkovi transkripta (tip_segmenta, pouzdanost_score, status) |
| `baza_znanja` | Verzije baze znanja |
| `unos_baze_znanja` | **RAG unosi** — pitanje/odgovor, `vector_id` (Qdrant), status odobravanja, verzionisanje |
| `chat_sesija` | Chat sesije (kanal_pristupa, status, broj_poruka) |
| `poruka` | Poruke (tip: korisnik / chatbot) |
| `odgovor` | Odgovori (metoda_generisanja, skor_pouzdanosti, latencija_ms) |
| `feedback` | Ocjene 1–5 po odgovoru / sesiji |
| `anomalija` | Događaji niske pouzdanosti / bez odgovora / negativan feedback |
| `eskalacija`, `status_agenta` | Eskalacijski red i status agenata |
| `announcement` | Sistemske obavijesti (baner) |
| `drive_schedule` | Konfiguracija scheduled Drive importa |
| `token_map` | Enkriptovana (Fernet) mapa PII → originalna vrijednost |

**Traceability:** `transkript` → `segment` → `unos_baze_znanja` (izvor); `chat_sesija` → `poruka` → `odgovor` → `unos_baze_znanja` → `feedback`/`anomalija`. Svaki odgovor je sljediv natrag do originalnog transkripta.

Migracije: `alembic/versions/` (001 token map, 002 escalation, 003 anomalija, 004 session feedback, 005 drive schedule).

---

## 8. Najvažnije sigurnosne odluke

- **JWT autentifikacija (stateless):** tokeni potpisani `SECRET_KEY`-em, istek `ACCESS_TOKEN_EXPIRE_MINUTES` (60 min). Lozinke hashirane **bcrypt**-om.
- **RBAC u servisnom sloju:** uloge `admin`, `manager`, `agent`, `user`; provjera prava se radi u servisima/dependency-jima, ne samo na rutama.
- **PII maskiranje prije obrade:** imena, telefoni, JMBG, email, IBAN, SSN se detektuju i zamjenjuju placeholderima **prije** embeddinga i prije bilo kakvog slanja LLM-u. JMBG ima checksum validaciju (manje lažnih pozitiva).
- **Privacy boundary prema LLM-u:** Groq-u (transkripcija, speaker labeling, scrub) šalje se **isključivo maskirani tekst**.
- **Enkriptovana token mapa:** originalne PII vrijednosti čuvaju se Fernet-enkriptovane (`TOKEN_MAP_KEY`); placeholderi se uklanjaju iz odgovora prije nego stignu korisniku.
- **Prompt-injection zaštita:** ulazi koji odgovaraju injection obrascima se odbijaju prije ikakvog retrievala.
- **Secrets van koda:** svi ključevi su env varijable; u Azure-u su Container App secrets, lokalno su u `.env` (koji se ne commit-uje).
- **CORS:** `ALLOWED_ORIGINS` ograničava dozvoljene originе; u produkciji je to domena Static Web App-a.
- **HTTPS svuda:** Azure Static Web App i Container App ingress serviraju isključivo HTTPS/WSS.

---

## 9. Tehnološki stack (sažeto)

- **Frontend:** React 18, TypeScript, Vite 5, Tailwind CSS, React Query, Axios, react-router-dom 6
- **Backend:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), Alembic, python-jose (JWT), bcrypt, FastAPI BackgroundTasks
- **AI:** Groq (`llama-3.3-70b-versatile`, `whisper-large-v3`), sentence-transformers (`all-MiniLM-L6-v2`), LangChain, spaCy (NER), Qdrant client
- **Podaci:** PostgreSQL 16 (Supabase), Qdrant Cloud, Supabase Storage
- **Infra:** Docker, Azure Container Apps + Static Web Apps, Azure Developer CLI (`azd`), Bicep, GitHub Actions
