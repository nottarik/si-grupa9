# Tehnički setup

## Sadržaj

1. [Branching strategija](#1-branching-strategija)
2. [Pregled stacka](#2-pregled-stacka)
3. [Programski jezik i runtime](#3-programski-jezik-i-runtime)
4. [Frontend](#4-frontend)
5. [Backend servisi](#5-backend-servisi)
6. [AI i RAG komponente](#6-ai-i-rag-komponente)
7. [Asinhrona obrada](#7-asinhrona-obrada)
8. [Baze podataka](#8-baze-podataka)
9. [Infrastruktura i deployment](#9-infrastruktura-i-deployment)
10. [Rezime – sve tehnologije](#10-rezime--sve-tehnologije)

---

## 1. Branching strategija — GitHub Flow

Odabrali smo **GitHub Flow** zbog jednostavnosti i prilagođenosti timovima koji rade kontinuirani razvoj bez kompleksnih release ciklusa. Strategija je linearna, pregledna i svim članovima tima odmah razumljiva.

### Grane

| Grana | Namjena |
|---|---|
| `main` | Uvijek stabilan, direktno deployabilan kod |
| `feature/naziv-stavke` | Svaka backlog stavka = jedna grana |
| `fix/naziv-buga` | Ispravke grešaka |

### Konvencija commit poruka

```
feat:     nova funkcionalnost
fix:      ispravka greške
refactor: refaktorisanje bez promjene funkcionalnosti
docs:     izmjene dokumentacije
test:     dodavanje ili izmjena testova
chore:    build, konfiguracija, dependencies
```

### Tok rada

1. Kreirati granu iz `main`: `git checkout -b feature/budget-planning`
2. Razviti funkcionalnost uz redovne commitove
3. Otvoriti Pull Request prema `main`
4. Minimalno jedan član tima radi code review
5. Nakon odobrenja — merge u `main` i brisanje feature grane

---

## 2. Pregled stacka

| Sloj | Tehnologija |
|---|---|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend (svi servisi) | Python 3.12 + FastAPI |
| Auth | python-jose + passlib/bcrypt |
| AI / RAG pipeline | LangChain + Groq API (Llama 3.1) |
| Audio transkripcija | faster-whisper (lokalno, CPU) |
| Embeddinzi | sentence-transformers (lokalno) |
| Asinhroni taskovi | Celery + Redis |
| Relacijska baza | PostgreSQL 16 + SQLAlchemy + Alembic |
| Vektorska baza | Qdrant |
| Cache / Queue broker | Redis |
| Reverse proxy | Nginx |
| Kontejnerizacija | Docker + Docker Compose |
| Operativni sistem | Ubuntu 22.04 LTS |
| Hosting | Oracle Cloud Always Free |

---

## 3. Programski jezik i runtime

### Python 3.12

Cijeli backend pišemo u Pythonu zbog superiorne podrške za AI biblioteke (LangChain, Hugging Face, sentence-transformers) koje su ključne za RAG sistem. Node.js bi omogućio jedan jezik kroz cijeli stack, ali frontend i backend ionako razvijaju odvojeni timovi – ta prednost ovdje ne dolazi do izražaja.

---

## 4. Frontend

### React 18 + Vite + Tailwind CSS

**React** ima najveću bazu developera i bogat ekosistem UI biblioteka relevantnih za ovaj projekat (react-markdown, react-virtuoso). Vue i Svelte su tehnički odlični, ali manji ekosistem znači manje gotovih rješenja za chat interfejs i admin panel.

**Vite** zamjenjuje Create React App zbog brzine – dev server startuje za ispod sekunde umjesto 10–30 s, a produkcijski build je optimizovaniji zahvaljujući Rollup-u.

**Tailwind** daje punu kontrolu nad dizajnom bez override-anja tuđeg vizualnog jezika kao što nameću Bootstrap ili Material UI. Utility klase drže stilove uz markup, što ubrzava razvoj responsive komponenti.

### Axios + React Query

**Axios** umjesto nativnog fetch-a zbog interceptora – JWT token se dodaje jednom globalno, ne po svakom pozivu. **React Query** zamjenjuje Redux za server state: caching, refetching i error handling u nekoliko linija, bez boilerplatea.

---

## 5. Backend servisi

### FastAPI

Odabran umjesto Djanga (previše funkcionalnosti koje ne koristimo – ORM, template engine, admin panel) i Flaska (sinhroni po defaultu, nema automatsku validaciju). FastAPI ključne prednosti:

- Automatski Swagger UI na `/docs` bez konfiguracije
- Pydantic validacija ulaznih podataka i jasne error poruke
- Native `async/await` – endpoint ne blokira server dok čeka LLM odgovor (5–10 s)

### SQLAlchemy 2.0 + Alembic

Najzreliji Python ORM s najboljom PostgreSQL podrškom. SQLAlchemy 2.0 uvodi async session support. Alembic generiše revizionalne migration skripte s rollback podrškom.

---

## 6. AI i RAG komponente

### Groq API (Llama 3.1 70B)

Groq koristi vlastite LPU čipove i odgovara za manje od sekunde. Besplatni tier: 14.400 zahtjeva/dan, 500.000 tokena/min – dovoljno za razvoj i testiranje. Lokalni pristup (Ollama) je besplatan ali zahtijeva 8+ GB RAM-a samo za model i 30–60 s po odgovoru bez GPU-a.

### sentence-transformers – `paraphrase-multilingual-MiniLM-L12-v2`

Embedding model koji radi lokalno bez API troška. Podržava 50+ jezika (uključujući ex-Yu), veličina ~470 MB, radi na CPU-u. Veći modeli (npr. multilingual-e5-large) daju bolje rezultate ali su 3–4× sporiji na CPU-u – za MVP fazu MiniLM nudi dobar balans. Zamjena je jedna linija u LangChain konfiguraciji.

### faster-whisper (small model)

Open-source Whisper reimplementacija koja radi do 4× brže od originalnog `openai-whisper` paketa zahvaljujući CTranslate2 engineu, uz manji RAM footprint. Radi lokalno unutar Dockera bez GPU-a. ~1 min audia ≈ 30–60 s transkripcije na prosječnom CPU-u.

### LangChain

RAG pipeline zahtijeva retrieval, formatiranje konteksta, prompt template management i logovanje – direktni Groq API pozivi su previše rudimentarni za to. LangChain daje apstrakcije za sve komponente i omogućava zamjenu LLM-a ili vektorske baze bez refaktoringa cijelog koda.

---

## 7. Asinhrona obrada

### Celery + Redis

Transkripcija i embedding generisanje traju 30–120 s. Backend odmah vraća `202 Accepted`, posao ide u queue. Odabran umjesto RQ-a zbog ugrađenog retry mehanizma s exponential backoff (neophodan za Groq rate limit greške) i **Flower** monitoring UI-ja. Redis koristimo i kao Celery broker jer ga već imamo u stacku – jedan servis manje.

---

## 8. Baze podataka

### PostgreSQL 16

Superioran JSON support (`jsonb`), bolji full-text search i stroža SQL conformance u poređenju s MySQL-om. SQLite nije opcija za produkciju zbog file-based lockinga.

### Qdrant

Self-hosted, open-source, bez eksternih dependencija – radi u Dockeru. Pinecone nema self-hosted opciju i limitira besplatni tier na 100k vektora. pgvector nema HNSW indeksiranje, što znači znatno sporije pretrage pri 10k+ embeddinga. Qdrant podržava payload filtere (pretraga unutar određenog transkript ID-a ili datumskog raspona).

### Redis 7

Pokriva i Celery task queue i session cache u jednoj instanci. Memcached ne podržava persistence ni kompleksne strukture podataka koje Celery koristi.

---

## 9. Infrastruktura i deployment

### Oracle Cloud Always Free

| Spec | Oracle Always Free (ARM) |
|---|---|
| vCPU | 4 ARM Ampere A1 |
| RAM | 24 GB |
| Storage | 200 GB |
| Transfer | 10 TB/mj |

Bez vremenskog ograničenja, servisi se nikad ne gase. Render i Railway imaju besplatne tierove, ali gase servise nakon 15 min neaktivnosti i imaju stroge CPU/RAM limite. Za registraciju je potrebna kreditna kartica (verifikacija identiteta), ali se ne naplaćuje ništa dok se koriste Always Free resursi. Preporučeni region: `eu-frankfurt-1` ili `eu-amsterdam-1` (GDPR).

### Docker + Docker Compose

Garantuje identično okruženje lokalno i na serveru. Nov developer klonira repo i pokreće `docker compose up` – sistem je gore za dvije minute. Kubernetes je prevelika kompleksnost za MVP fazu; granice između servisa su već jasno postavljene kontejnerima, što migraciju čini pravolinijskom kad za to dođe potreba.

Kontejneri:
```
frontend              → Nginx servira React build
backend               → Glavni FastAPI servis
auth-service          → Auth FastAPI servis
audio-service         → faster-whisper transkripcija
ai-chatbot-service    → RAG Chatbot (Groq + sentence-transformers)
processing-pipeline   → Celery worker
database              → PostgreSQL 16
vector-db             → Qdrant
redis                 → Redis 7
nginx                 → Reverse proxy
```

**GitHub Actions** za CI/CD: svaki push na `main` automatski builda Docker image-ove i restarta servise na Oracle instanci via SSH.

### Nginx + Let's Encrypt

Nginx kao reverse proxy zbog rasprostranjene dokumentacije i produkcijske dokazanosti. Caddy automatski pribavlja SSL ali ima manje resursa za specifičnije proxy scenarije. Let's Encrypt + Certbot za besplatne SSL/TLS certifikate koji se automatski obnavljaju svakih 90 dana.

---

## 10. Rezime – sve tehnologije

### Runtime i jezik

| Alat | Verzija | Namjena |
|---|---|---|
| Python | 3.12 | Runtime za sve backend servise |

### Frontend

| Alat | Namjena | Odabran umjesto |
|---|---|---|
| React 18 | UI framework | Vue, Svelte |
| Vite | Build alat i dev server | Create React App |
| Tailwind CSS | Stilizacija | Bootstrap, Material UI |
| Axios | HTTP klijent | native fetch |
| React Query | Server state management | Redux |

### Backend

| Alat | Namjena | Odabran umjesto |
|---|---|---|
| FastAPI | HTTP framework za sve servise | Django, Flask |
| Pydantic v2 | Validacija podataka | ručna validacija |
| python-jose | JWT generisanje i verifikacija | PyJWT |
| passlib + bcrypt | Hashiranje passworda | — |
| SQLAlchemy 2.0 | ORM za PostgreSQL | Tortoise ORM |
| Alembic | Migracije baze podataka | — |

### AI i obrada

| Alat | Namjena | Odabran umjesto |
|---|---|---|
| LangChain | RAG pipeline orkestracija | direktni API pozivi |
| Groq API (Llama 3.1 70B) | LLM za generisanje odgovora | Claude API, GPT-4o |
| faster-whisper (small) | Audio transkripcija lokalno | OpenAI Whisper API |
| sentence-transformers (MiniLM) | Embeddinzi lokalno | OpenAI embedding API |
| Celery | Asinhroni task queue | RQ, dramatiq |

### Baze i storage

| Alat | Namjena | Odabran umjesto |
|---|---|---|
| PostgreSQL 16 | Relacijska baza | MySQL, SQLite |
| Qdrant | Vektorska baza | Pinecone, pgvector |
| Redis 7 | Queue broker + cache | RabbitMQ, Memcached |

### Infrastruktura

| Alat | Namjena | Odabran umjesto |
|---|---|---|
| Docker | Kontejnerizacija | direktna instalacija |
| Docker Compose | Orkestracija kontejnera | Kubernetes |
| Nginx | Reverse proxy + SSL | Apache, Caddy |
| Let's Encrypt + Certbot | SSL/TLS certifikati | plaćeni certifikati |
| Ubuntu 22.04 LTS | Serverski OS | Debian, CentOS |
| Oracle Cloud Always Free | Cloud hosting | Render, Railway, DigitalOcean |
| GitHub Actions | CI/CD pipeline | Jenkins, GitLab CI |

---

## Napomena: Prelaz na produkciju

Kad projekat preraste studentsku fazu, plaćene alternative su direktna zamjena bez refaktoringa:

| Komponenta | Studentska verzija | Produkcijska verzija |
|---|---|---|
| LLM | Groq (besplatno) | Claude API / GPT-4o |
| Embeddinzi | sentence-transformers (lokalno) | OpenAI text-embedding-3-small |
| Audio | faster-whisper (lokalno, sporije) | OpenAI Whisper API |
| Hosting | Oracle Always Free | Hetzner VPS CPX31 (~17 €/mj) |

LangChain apstrakcija osigurava da je svaka zamjena promjena jedne linije u konfiguraciji, ne refaktoring koda.
