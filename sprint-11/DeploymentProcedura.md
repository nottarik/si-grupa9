# Deployment Procedura

Detaljan i provjeriv vodič kojim **druga osoba može pokrenuti sistem prateći napisane korake** —
lokalno (za razvoj) i u produkciji na Azure-u. Ako negdje zapne, pogledaj sekciju
[10. Najčešći problemi](#10-najčešći-problemi-pri-pokretanju-i-rješenja).

---

## 1. Naziv aplikacije i kratak opis arhitekture

**Call Centar Chatbot** — RAG-zasnovan AI asistent za podršku call centru.

- **Frontend:** React 18 + TypeScript + Vite SPA (servira se kao Azure Static Web App).
- **Backend:** FastAPI (Python 3.12) REST + WebSocket API (Azure Container App).
- **Podaci:** PostgreSQL 16 (Supabase), Qdrant Cloud (vektori), Supabase Storage (fajlovi).
- **AI:** Groq API (LLM + Whisper), sentence-transformers embedding (lokalno na CPU).

Detaljan tehnički pregled: vidi `ArchitectureOverview.md`.

> **Produkcija se hostuje na Azure free tieru.** Cloud deployment je opisan u sekciji 8, a
> automatizovani CD pipeline u `CD-Pipeline.md`.

---

## 2. Tehnologije koje se koriste

| Sloj | Tehnologija |
|---|---|
| Frontend | React 18, TypeScript, Vite 5, Tailwind CSS, React Query, Axios |
| Backend | Python 3.12, FastAPI 0.111, SQLAlchemy 2.0 (async), Pydantic v2, Alembic, uvicorn |
| AI | Groq (`llama-3.3-70b-versatile`, `whisper-large-v3`), sentence-transformers (`all-MiniLM-L6-v2`), spaCy, LangChain |
| Baza / storage | PostgreSQL 16 (Supabase), Qdrant Cloud, Supabase Storage |
| Infra | Docker + Docker Compose, Azure Container Apps, Azure Static Web Apps, Azure Developer CLI (`azd`), Bicep, GitHub Actions |

---

## 3. Potrebni alati i verzije

| Alat | Verzija | Za šta |
|---|---|---|
| Git | bilo koja novija | kloniranje repozitorija |
| Docker + Docker Compose | Docker 24+ | najlakši lokalni start (preporučeno) |
| Python | 3.12 | backend bez Dockera |
| Node.js | 20.x | frontend bez Dockera |
| Azure Developer CLI (`azd`) | 1.x | cloud deployment |
| Azure CLI (`az`) | novija | login/diagnostika (opciono) |
| Azure pretplata | free tier | hosting |

---

## 4. Sve potrebne environment varijable

### Backend (`projekat/backend/.env`)

| Varijabla | Obavezno | Opis |
|---|---|---|
| `APP_ENV` | ne | `development` / `production` / `test` (default `development`) |
| `SECRET_KEY` | **da** | ključ za potpisivanje JWT tokena |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ne | trajanje tokena (default 60) |
| `TOKEN_MAP_KEY` | **da** (prod) | Fernet ključ za enkripciju PII token mape. Generisanje: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`. **Ne mijenjati nakon prvog deploya** — promjena čini već maskirane podatke nedekriptabilnim. |
| `DATABASE_URL` | **da** | `postgresql+asyncpg://...` (Supabase) |
| `REDIS_URL` | ne | opcioni cache/rate-limit; ako nije postavljen, koristi se default i Redis se preskače |
| `QDRANT_URL` | **da** | URL Qdrant instance |
| `QDRANT_API_KEY` | **da** (Cloud) | API ključ za Qdrant Cloud |
| `QDRANT_COLLECTION_NAME` | ne | default `knowledge_base` |
| `GROQ_API_KEY` | **da** | Groq API ključ (LLM + Whisper) |
| `EMBEDDING_MODEL` | ne | default `all-MiniLM-L6-v2` |
| `LLM_MODEL` | ne | default `llama-3.3-70b-versatile` |
| `WHISPER_MODEL` | ne | default `whisper-large-v3` |
| `RAG_TOP_K` | ne | broj rezultata pretrage (default 5) |
| `RAG_CONFIDENCE_THRESHOLD` | ne | prag „čistog" odgovora (0.5–0.55) |
| `RAG_CONFIDENCE_THRESHOLD_LOW` | ne | ispod ovoga → eskalacija (default 0.35) |
| `RAG_OFFTOPIC_THRESHOLD` | ne | stroži prag za off-topic upite (default 0.5) |
| `SUPABASE_URL` | **da** | Supabase projekt URL |
| `SUPABASE_SERVICE_KEY` | **da** | Supabase service role ključ |
| `SUPABASE_BUCKET` | ne | bucket za fajlove (prod: `supabucket`) |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | ne | service account JSON (Drive import) |
| `GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID` | ne | default folder za „Run complete pipeline" |
| `INTERNAL_API_KEY` | ne | štiti `/internal/*` endpointe |
| `ALLOWED_ORIGINS` | **da** (prod) | CORS lista, npr. `https://purple-field-0d55d8003.7.azurestaticapps.net` |

> Šablon: `projekat/backend/.env.example`. **Stvarni `.env` se ne commit-uje.**

### Frontend (`projekat/frontend/.env`)

| Varijabla | Opis |
|---|---|
| `VITE_API_URL` | bazni URL backenda. Lokalno: `http://localhost:8000`. U Azure deployu se **automatski injektuje** iz `main.bicep` outputa (FQDN backend Container App-a) tokom `azd` builda. |

> Napomena: `frontend/.env.production` u repou još pokazuje na raniji Render backend; za Azure
> produkciju ta vrijednost je irelevantna jer `azd` postavlja `VITE_API_URL` u build koraku.

---

## 5. Lokalno pokretanje — Docker Compose (preporučeno)

Najjednostavniji način: jedna komanda diže backend, frontend, lokalni Postgres, Redis, Qdrant i nginx.

```bash
git clone <repo-url>
cd projekat

# 1) Pripremi backend .env
cp backend/.env.example backend/.env
# popuni GROQ_API_KEY, QDRANT_URL/API_KEY, SUPABASE_*, SECRET_KEY, TOKEN_MAP_KEY, DATABASE_URL

# 2) Digni cijeli stack
docker-compose up
```

Servisi nakon `docker-compose up` (uz `docker-compose.override.yml` koji se auto-učitava):

| Servis | Port |
|---|---|
| backend (FastAPI) | http://localhost:8000 (Swagger: `/docs`) |
| frontend (Vite dev) | http://localhost:5173 |
| nginx reverse proxy | http://localhost:80 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |
| Qdrant | localhost:6333 |

Zaustavljanje: `docker-compose down` (dodaj `-v` da obrišeš volumene/podatke).

---

## 6. Lokalno pokretanje backenda (bez Dockera)

```bash
cd projekat/backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
python -m spacy download xx_ent_wiki_sm   # NER model za PII detekciju

# .env mora postojati u projekat/backend/
uvicorn app.main:app --reload              # API na :8000
```

Provjera: otvori <http://localhost:8000/health> → `{"status":"ok","env":"development"}`.

---

## 7. Lokalno pokretanje frontenda (bez Dockera)

```bash
cd projekat/frontend
npm install
# .env sa VITE_API_URL=http://localhost:8000
npm run dev        # http://localhost:5173
```

Produkcijski build (statički fajlovi u `dist/`):

```bash
npm run build
npm run preview    # lokalni pregled builda
```

Lint (strict, max-warnings 0): `npm run lint`.

---

## 8. Migracije i seed podaci

Baza se nalazi u Supabase-u (cloud) i dijeljena je između lokalnog razvoja i produkcije.

```bash
cd projekat/backend
alembic upgrade head                              # primijeni sve migracije
alembic revision --autogenerate -m "opis"         # nova migracija (pri promjeni modela)
```

**Seed / demo nalozi** (vidi `UserManual.md`):

| Uloga | Email | Lozinka |
|---|---|---|
| Admin | `admin@test.com` | `admin123` |
| Agent | `agent@test.com` | `Agent1234` |
| User | `user@test.com` | `User1234` |

Novi korisnik se može registrovati kroz `POST /api/v1/auth/register` ili LoginPage formu (default uloga `user`); ulogu mijenja admin u panelu (`PATCH /users/{id}/role`).

> Napomena: sistem nema poseban automatski seed skript — knowledge base se popunjava uploadom
> transkripata / ručnim unosom Q&A parova / Drive importom kroz aplikaciju. Pri startu backend radi
> **self-heal**: dovršava neembedovane odobrene unose i ponovo procesira zaglavljene transkripte.

---

## 9. Pokretanje testova

```bash
cd projekat/backend
pytest -q                                  # svih 223 testa
pytest tests/unit -v                       # samo unit testovi (bez baze/HTTP-a)
pytest tests/integration/test_chat_sessions.py -v   # pojedinačni fajl
```

Testovi koriste lokalni SQLite (`sqlite+aiosqlite`) i ne diraju produkcijsku bazu; PII/preprocessing
testovi rade potpuno offline. Detalji i očekivani rezultat: `TestSummary.md`.

---

## 10. Produkcijski / cloud deployment — Azure (`azd`)

Produkcija je na **Azure free tieru**. Infrastruktura je definisana u `projekat/infra/main.bicep`, a
deploy orkestrira **Azure Developer CLI** preko `projekat/azure.yaml`. Jedna komanda — `azd up` —
provisionira infrastrukturu, buildi oba Dockerfile-a / Vite app i deploya ih.

### 10.1 Šta se provisionira (`main.bicep`)

- Log Analytics workspace (observability)
- Azure Container Registry (Basic) + user-assigned identity sa `AcrPull` ulogom
- Container Apps managed environment
- **Container App `backend`** (FastAPI): 1 vCPU / 2 GiB, ingress na portu 8000, `transport: auto` (omogućava WSS za chat/escalation sockete), `minReplicas=1` (uvijek topla — nema cold-start učitavanja modela)
- **Static Web App `web`** (Free SKU) za frontend

Eksterni servisi (Supabase, Qdrant Cloud, Groq) ostaju van Azure-a; u Container App se injektuju kao **secrets**.

### 10.2 Preduvjeti

- Instaliran `azd` i Docker (image se buildi **lokalno** pa push na ACR — cloud/ACR-Tasks build je blokiran na free-trial pretplatama: „TasksOperationsNotAllowed").
- Prijava: `azd auth login`.
- Vrijednosti secret-a spremne: `DATABASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY`, `GROQ_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `TOKEN_MAP_KEY`, (opc.) `GOOGLE_SERVICE_ACCOUNT_JSON_BASE64`, `GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID`.

### 10.3 Koraci

```bash
cd projekat

azd auth login                 # prijava na Azure
azd env new chatbot            # kreiraj okruženje (jednom)

# Postavi tajne kao azd env varijable (primjeri):
azd env set DATABASE_URL "postgresql+asyncpg://...supabase..."
azd env set QDRANT_URL "https://...qdrant.io"
azd env set QDRANT_API_KEY "..."
azd env set GROQ_API_KEY "gsk_..."
azd env set SUPABASE_URL "https://....supabase.co"
azd env set SUPABASE_SERVICE_KEY "..."
azd env set TOKEN_MAP_KEY "<postojeći Fernet ključ — NE generisati novi>"
# Drive je opcionalno:
azd env set GOOGLE_SERVICE_ACCOUNT_JSON_BASE64 "<base64 service-account JSON>"
azd env set GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID "<folder id>"

azd up                         # provision + build + deploy (sve odjednom)
```

> `GOOGLE_SERVICE_ACCOUNT_JSON` se prosljeđuje **base64-enkodirano** jer sirovi JSON (navodnici/novi
> redovi) korumpira azd parametarski fajl; `main.bicep` ga dekodira nazad u JSON.

Po završetku `azd` ispisuje outpute:
- `WEB_URI` — URL frontenda (Static Web App)
- `BACKEND_URI` — URL backenda (Container App)
- `VITE_API_URL` — baked u frontend build (FQDN backenda)
- `AZURE_CONTAINER_REGISTRY_ENDPOINT` — gdje je image push-an

Frontend `VITE_API_URL` se postavlja automatski iz backend FQDN-a — **ne treba ručno editovati `.env.production`**.

### 10.4 Ažuriranje postojećeg deploya

```bash
azd deploy            # samo rebuild + redeploy aplikacije (bez ponovnog provisioninga)
azd provision         # samo infrastruktura
```

U CI/CD-u (push na `main`) ovo radi GitHub Actions automatski — vidi `CD-Pipeline.md`.

---

## 11. Link na deployment

- **Frontend (live):** <https://purple-field-0d55d8003.7.azurestaticapps.net/>
- **Backend:** Azure Container App FQDN (oblik `https://ca-backend-<token>.<region>.azurecontainerapps.io`), ispisan kao `BACKEND_URI` nakon `azd up`.

Provjera da je backend živ: `GET <BACKEND_URI>/health` → `{"status":"ok"}`.

---

## 12. Šta se tačno deploya, koje varijable / secrets koristi

- **Backend image** (iz `backend/Dockerfile`) → ACR → Container App `backend`. Env i secrets postavljeni u `main.bicep` (`DATABASE_URL`, `QDRANT_*`, `GROQ_API_KEY`, `SUPABASE_*`, `TOKEN_MAP_KEY`, `SECRET_KEY` (auto-generisan po deployu), `INTERNAL_API_KEY` (auto), `GOOGLE_*`, plus ne-secret postavke modela i `ALLOWED_ORIGINS` = domena Static Web App-a).
- **Frontend** (`npm run build`) → Static Web App `web`. Jedina build varijabla: `VITE_API_URL` (FQDN backenda).
- **Drive auto-import** nema poseban cron resurs — radi ga in-process scheduler u backendu (jedna uvijek-topla replika → nema dvostrukog okidanja). Manuelni trigger: `POST /api/v1/internal/sync-drive` (zaštićeno `INTERNAL_API_KEY`).

---

## 13. Poznata ograničenja deploymenta

- **Backend image se buildi lokalno** (Docker daemon obavezan) jer ACR Tasks nisu dozvoljeni na free-trial pretplati.
- **Uvijek-topla replika** (`min=max=1`): nema horizontalnog skaliranja; in-process scheduler zavisi od te jedne replike.
- **Eksterni servisi** (Supabase, Qdrant, Groq) imaju vlastite free-tier limite (rate/kvota) i nisu dio Azure provisioninga.
- **`TOKEN_MAP_KEY` mora ostati isti** kroz deployove — novi ključ čini ranije maskirane podatke nedekriptabilnim.
- **Redis nije provisioniran na Azure-u** — koristi se opciono (lokalno/Upstash). Aplikacija radi i bez njega.
- Detalji i ostala ograničenja: `KnownIssues.md`.

---

## 14. Gdje se provjerava rezultat deploymenta

1. Otvoriti `WEB_URI` (frontend) i prijaviti se demo nalogom.
2. `GET <BACKEND_URI>/health` i `/heartbeat` → status OK.
3. `<BACKEND_URI>/docs` → Swagger UI sa svim rutama.
4. Logovi backenda u **Log Analytics** workspace-u (Container Apps logovi).
5. Poslati test pitanje u chatu i provjeriti da stigne odgovor (end-to-end RAG put).

---

## 10. Najčešći problemi pri pokretanju i rješenja

| Problem | Uzrok | Rješenje |
|---|---|---|
| `azd up` ne može buildati image (`TasksOperationsNotAllowed`) | ACR Tasks blokirani na free-trial | Pokreni lokalni Docker daemon — image se buildi lokalno pa push na ACR |
| 401/403 na svim API pozivima | nedostaje/istekao JWT | ponovo se prijavi; provjeri `SECRET_KEY` (ako se rotirao, svi se moraju ponovo logovati) |
| CORS greška u browseru | `ALLOWED_ORIGINS` ne sadrži domenu frontenda | dodaj tačnu domenu Static Web App-a u `ALLOWED_ORIGINS` |
| Chatbot ne nalazi odgovore / sve eskalira | Qdrant nedostupan ili prazna kolekcija | provjeri `QDRANT_URL/API_KEY`; uploaduj transkripte ili `POST /knowledge/reindex` |
| PII se ne može dekriptovati nakon restarta | promijenjen ili prazan `TOKEN_MAP_KEY` | koristi isti Fernet ključ kroz sve deployove |
| Backend ne startuje lokalno (spaCy greška) | nedostaje NER model | `python -m spacy download xx_ent_wiki_sm` |
| `whisper`/LLM pozivi padaju | nevažeći/prekoračeni `GROQ_API_KEY` | provjeri ključ i Groq kvotu |
| Frontend gađa pogrešan backend | `VITE_API_URL` postavljen na staru vrijednost | postavi tačan URL (lokalno `.env`; na Azure-u `azd` to radi automatski) |
