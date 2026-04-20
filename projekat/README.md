# Call Centar Chatbot

RAG-based chatbot trained on call centre transcripts.  
Built with **FastAPI**, **React + Vite**, **LangChain**, **Groq (Llama 3.1)**, **Qdrant**, **PostgreSQL**, **Celery**.

---

## Brzi start (lokalni razvoj)

### 1. Kloniranje i konfiguracija

```bash
git clone https://github.com/your-org/projekat.git
cd projekat

# Backend env
cp backend/.env.example backend/.env
# Otvorite backend/.env i dodajte GROQ_API_KEY

# Frontend env
cp frontend/.env.example frontend/.env
```

### 2. Pokretanje sa Docker Compose

```bash
docker compose up --build
```

| Servis | URL |
|---|---|
| Frontend (Chat UI) | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| Qdrant dashboard | http://localhost:6333/dashboard |

### 3. Migracije baze podataka

```bash
docker compose exec backend alembic upgrade head
```

### 4. Kreiranje admin korisnika

```bash
docker compose exec backend python -c "
import asyncio
from app.db.session import AsyncSessionLocal
from app.db.models.user import User, UserRole
from app.core.security import get_password_hash

async def create_admin():
    async with AsyncSessionLocal() as db:
        user = User(
            email='admin@example.com',
            hashed_password=get_password_hash('admin123'),
            full_name='Admin',
            role=UserRole.admin
        )
        db.add(user)
        await db.commit()
        print('Admin kreiran: admin@example.com / admin123')

asyncio.run(create_admin())
"
```

---

## Struktura projekta

```
projekat/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── routes/         # auth, chat, transcripts, knowledge
│   │   │   ├── deps.py         # JWT + RBAC dependencies
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py       # Settings (pydantic-settings)
│   │   │   └── security.py     # JWT + bcrypt
│   │   ├── db/
│   │   │   ├── models/         # SQLAlchemy modeli
│   │   │   └── session.py      # AsyncEngine + get_db
│   │   ├── schemas/            # Pydantic request/response modeli
│   │   ├── services/
│   │   │   ├── ai/             # RAG, embeddings, LLM, Qdrant
│   │   │   ├── pipeline/       # Normalizacija, PII masking, Q&A ekstrakcija
│   │   │   └── transcript/     # Whisper transkripcija
│   │   ├── tasks/              # Celery taskovi
│   │   ├── workers/            # Celery app inicijalizacija
│   │   └── main.py
│   ├── alembic/                # DB migracije
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/                # Axios pozivi prema backendu
│   │   ├── components/
│   │   │   ├── chat/           # ChatWindow, MessageBubble
│   │   │   ├── admin/          # TranscriptUpload, KnowledgePendingList
│   │   │   └── common/         # Layout, ProtectedRoute
│   │   ├── hooks/              # useAuth, useChat
│   │   ├── pages/              # LoginPage, ChatPage, AdminPage
│   │   └── types/              # Globalni TypeScript tipovi
│   ├── Dockerfile
│   └── .env.example
│
├── nginx/
│   └── nginx.conf
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Arhitektura (kratak pregled)

```
Browser → Nginx → FastAPI Backend → PostgreSQL
                               ↘ Qdrant (vektori)
                               ↘ Celery Worker → Whisper (transkripcija)
                                               → PipelineService (obrada)
                               ↘ Groq API (LLM generisanje)
```

**RAG tok:**
1. Korisnik pita → embedding pitanja (sentence-transformers)
2. Semantička pretraga u Qdrant → top-k Q&A parova
3. Confidence scoring (cosine similarity)
4. Ako confidence ≥ prag → LLM generisanje odgovora uz kontekst
5. Ako confidence < prag → fallback poruka s uputom za kontakt agenta

---

## Testiranje

```bash
# Backend testovi
docker compose exec backend pytest tests/ -v

# Ili lokalno (uz aktiviran venv)
cd backend
pytest tests/ -v
```

---

## Produkcijski deployment

1. Postavite A record domene na server IP
2. Instalirajte Certbot i generirajte SSL certifikat:
   ```bash
   certbot certonly --standalone -d your-domain.com
   ```
3. Kopirajte certifikate u `nginx/certs/`
4. Odkomentirajte HTTPS blok u `nginx/nginx.conf`
5. Postavite `APP_ENV=production` u `backend/.env`
6. Pokrenite: `docker compose -f docker-compose.yml up -d`

---

## Tech stack

| Sloj | Tehnologija |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, React Query |
| Backend | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| Auth | JWT (python-jose), bcrypt (passlib) |
| AI/RAG | LangChain, Groq API (Llama 3.1 70B) |
| Embeddings | sentence-transformers (MiniLM, lokalno) |
| STT | faster-whisper (lokalno, small model) |
| Baze | PostgreSQL 16, Qdrant, Redis 7 |
| Async | Celery + Redis broker |
| Infra | Docker, Docker Compose, Nginx, GitHub Actions |
