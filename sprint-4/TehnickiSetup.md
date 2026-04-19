# Tehnički setup

## Sadržaj

1. [Pregled stacka](#1-pregled-stacka)
2. [Programski jezik i runtime](#2-programski-jezik-i-runtime)
3. [Frontend](#3-frontend)
4. [Backend servisi](#4-backend-servisi)
5. [AI i RAG komponente](#5-ai-i-rag-komponente)
6. [Asinhrona obrada](#6-asinhrona-obrada)
7. [Baze podataka](#7-baze-podataka)
8. [Infrastruktura i deployment](#8-infrastruktura-i-deployment)
9. [Rezime – sve tehnologije](#9-rezime--sve-tehnologije)

---

## 1. Pregled stacka

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

## 2. Programski jezik i runtime

### Python 3.12

Cijeli backend – glavni API, auth servis, audio servis, AI chatbot modul i processing pipeline – pišu se u **Pythonu 3.12**.

**Zašto Python, a ne Node.js:**

Node.js ima prednost jednog jezika kroz cijeli stack (frontend + backend u JavaScriptu), ali za ovaj sistem to nije presudna prednost jer frontend i backend ionako razvijaju isti timovi u odvojenim repozitorijima. Python je odabran zbog bolje podrške za AI biblioteke (LangChain, Hugging Face), koje su ključne za implementaciju RAG sistema u ovom projektu.


---

## 3. Frontend

### React 18

**Zašto React, a ne Vue ili Svelte:**

Vue i Svelte su tehnički odlični, ali React ima daleko veću bazu developera, više gotovih UI biblioteka kompatibilnih s chatbot interfejsima (react-markdown za renderovanje AI odgovora, react-virtuoso za virtualizaciju dugih lista poruka), i bolji TypeScript support. Za Admin Dashboard s tabelama, filterima i uploadom fajlova – React ekosistem ima gotova rješenja za svaki od tih zahtjeva.

### Vite

**Zašto Vite, a ne Create React App:**

Create React App se rjeđe koristi u novim projektima, jer Webpack koji koristi ispod haube je spor (cold start od 10-30 sekundi na većim projektima). Vite koristi native ES module i esbuild, pa dev server startuje za manje od sekundu. Za produkciju koristi Rollup koji generiše optimiziranije bundle-ove. Vite je pogodniji izbor za novi projekat.

### Tailwind CSS

**Zašto Tailwind, a ne Bootstrap ili Material UI:**

Bootstrap i Material UI nameću vlastiti vizualni jezik koji se teško mijenja. Tailwind je utility-first – gradiš vlastiti dizajn sistem bez override-anja tuđeg. Za call centar aplikaciju koja treba specifičan branding, Tailwind daje punu kontrolu bez borbe s gotovim komponentama.

**Zašto Tailwind, a ne čisti CSS:**

Čisti CSS zahtijeva konstantno prebacivanje između JSX i CSS fajlova i izmišljanje naziva klasa. Tailwind drži stilove direktno uz markup, što je brže za razvoj Chat UI komponenti – posebno za responsive dizajn gdje Tailwind-ovi sm:, md:, lg: prefiksi eliminišu pisanje media query-ja.

### Axios + React Query

**Axios** umjesto nativnog fetch API-ja zbog interceptora – automatsko dodavanje JWT tokena na svaki zahtjev piše se jednom, ne po svakom pozivnom mjestu.

**React Query** umjesto Reduxa za server state, jer je vrlo kompleksan. React Query rješava caching, background refetching i error stanja u nekoliko linija koda, što je sve što nam treba za Admin Dashboard i Chat UI.

---

## 4. Backend servisi

### FastAPI

**Zašto FastAPI, a ne Django ili Flask:**

Django je full-stack framework s ORM-om, admin panelom i template engineom – uključuje funkcionalnosti koje nisu potrebne u ovom projektu, jer imamo React frontend. Flask je minimalan kao FastAPI, ali je sinhroni po defaultu i nema automatsku validaciju podataka ni generisanje dokumentacije.

FastAPI je odabran jer::

- **Automatska API dokumentacija** – na /docs imaš Swagger UI odmah, bez konfiguracije. Svaki endpoint je testabilan iz browsera dok razvijaš.
- **Pydantic validacija** – definišeš model jednom, FastAPI automatski validira ulazne podatke i vraća jasne error poruke. Nema ručne validacije.
- **Nativna async podrška** – async def endpoint ne blokira server dok čeka LLM odgovor koji može trajati 5-10 sekundi.
- **Brz runtime** – benchmarci pokazuju FastAPI kao jedan od najbržih Python web frameworka, uporediv s Node.js Expressom.

### python-jose + passlib + bcrypt

- **python-jose** za JWT generisanje i verifikaciju – standard u Python ekosistemu
- **passlib + bcrypt** za hashiranje passworda (salt rounds: 12)

### SQLAlchemy + Alembic

**Zašto SQLAlchemy, a ne Tortoise ORM:**

SQLAlchemy je najzreliji Python ORM s najboljom PostgreSQL podrškom i najbogatijim query API-jem. SQLAlchemy 2.0 uvodi async session support koji pokriva iste slučajeve kao Tortoise. Alembic generiše revizionalne migration skripte s mogućnošću rollbacka.

---

## 5. AI i RAG komponente

### Groq API

**Groq** nudi besplatan API s pristupom moćnim open-source modelima:

- **Llama 3.1 70B** (Meta) – model usporediv s GPT-4o za zadatke odgovaranja na pitanja iz konteksta
- **Mixtral 8x7B** – odličan za duže kontekste kakve RAG pipeline proizvodi
- Besplatni tier: 14.400 zahtjeva dnevno, 500.000 tokena u minuti – više nego dovoljno za razvoj i testiranje

**Zašto Groq, a ne Ollama (lokalni LLM):**

Ollama pokreće modele lokalno na tvom računaru – besplatno, ali zahtijeva minimum 8 GB RAM-a samo za model, i na računarima bez dedicirane GPU-e odgovor traje 30-60 sekundi. Groq koristi vlastiti hardver (LPU čipovi) i odgovara za manje od sekunde čak i na besplatnom tieru. Za razvoj i demo, Groq je daleko praktičniji.

LangChain integracija postoji za oba, pa je prelazak na plaćeni model (Claude, GPT-4o) u budućnosti samo promjena jedne linije koda.

### sentence-transformers (lokalno)

**sentence-transformers** je Python biblioteka koja pokreće embedding modele lokalno, bez API troška.

Odabrani model: paraphrase-multilingual-MiniLM-L12-v2

- Podržava 50+ jezika uključujući bosanski, srpski i hrvatski
- Veličina modela: ~470 MB (preuzima se jednom pri prvom pokretanju)
- Radi na CPU-u bez GPU-a
- Kvalitet embeddinga dovoljan za semantičku pretragu call centar transkripata

**Zašto ovaj model, a ne veći multilingualni model:**

Veći modeli (npr. multilingual-e5-large) daju bolje rezultate, ali su 3-4× sporiji na CPU-u. Za MVP fazu MiniLM-L12-v2 pruža dobar balans brzine i kvaliteta, a zamjena modela je jedna linija koda u LangChain konfiguraciji.

### faster-whisper (lokalno)

**faster-whisper** je open-source reimplementacija Whisper modela koja radi na CPU-u i do 4× brže od originalne implementacije.

- Besplatno, bez API ključa, bez limita
- Odabrani model: small (244 MB) – dobar balans brzine i tačnosti za ex-Yu jezike
- Na prosječnom CPU-u: ~1 minuta audio ≈ 30-60 sekundi transkripcije
- Radi unutar Docker kontejnera bez GPU-a

**Zašto faster-whisper, a ne originalni openai-whisper paket:**

Originalni openai-whisper Python paket je sporiji i zahtijeva više memorije za isti model. faster-whisper koristi CTranslate2 engine koji daje identične rezultate ali znatno brže i s manjim RAM footprintom – što je važno jer Oracle Cloud Always Free instanca ima 24 GB RAM-a koji dijele svi kontejneri.

### LangChain

**Zašto LangChain, a ne direktni API pozivi:**

Direktni pozivi ka Groq API-ju su jednostavniji za trivijalne slučajeve, ali RAG pipeline zahtijeva: retrieval iz vektorske baze, formatiranje konteksta, prompt template management, output parsiranje i logovanje poziva. LangChain daje gotove apstrakcije za sve to i omogućava zamjenu bilo koje komponente (drugi LLM, druga vektorska baza) bez refaktoringa cijelog pipeline-a.

---

## 6. Asinhrona obrada

### Celery + Redis

Transkripcija audio fajla i generisanje embeddinga mogu trajati 30–120 sekundi (lokalno na CPU-u). Korisnik ne čeka – backend odmah vraća 202 Accepted, a posao ide u queue.

**Zašto Celery, a ne RQ ili dramatiq:**

RQ (Redis Queue) je jednostavniji od Celerya, ali nema ugrađeni retry mehanizam s exponential backoff koji je neophodan kad Groq API vrati rate limit grešku ili kad faster-whisper padne na oštećenom audio fajlu. Celery je industrijski standard za Python async taskove s najboljom dokumentacijom i **Flower** monitoring UI-jem za praćenje queue stanja.

**Zašto Redis kao broker, a ne RabbitMQ:**

Redis već koristimo za session cache, pa ga koristimo i kao Celery broker – jedan servis manje u Docker Compose stacku.

---

## 7. Baze podataka

### PostgreSQL 16

**Zašto PostgreSQL, a ne MySQL ili SQLite:**

SQLite nije opcija za produkciju s više concurrent korisnika (file-based locking). PostgreSQL ima superiorniji JSON support (jsonb tip kolone za metadata uz transkripte), bolji full-text search, i strožu SQL conformance. Sve besplatno i open-source.

### Qdrant

**Zašto Qdrant, a ne Pinecone, Weaviate ili pgvector:**

Pinecone je managed cloud servis bez self-hosted opcije – ima besplatni tier, ali s limitom od 100k vektora i jednim indexom, što je restriktivno. Weaviate ima veći footprint i kompleksniju konfiguraciju. pgvector nema HNSW indeksiranje – što znači znatno sporije pretrage pri većem broju embeddinga (10k+). Qdrant radi u Dockeru bez eksternih dependencija, besplatan je i open-source, ima odličan Python klijent, i podržava payload filtere (pretraga samo unutar određenog transkript ID-a ili datumskog raspona).

### Redis 7

**Zašto Redis, a ne Memcached:**

Memcached je čisti key-value cache bez persistence i bez podrške za kompleksne strukture. Redis podržava liste i sorted setove koje Celery koristi za queue implementaciju. Jedna instanca Redisa pokriva i task queue i session cache.
---

## 8. Infrastruktura i deployment

### Oracle Cloud Always Free

**Oracle Cloud Always Free** tier je trenutno najmoćnija besplatna cloud opcija na tržištu:

| Spec | Oracle Always Free (ARM) |
|---|---|
| vCPU | 4 ARM Ampere A1 |
| RAM | 24 GB |
| Storage | 200 GB block storage |
| Transfer | 10 TB/mj |

Ovo nije trial – Oracle Always Free nema vremenskog ograničenja. 4 ARM CPU jezgra i 24 GB RAM-a su dovoljni za pokretanje cijelog Docker Compose stacka uključujući faster-whisper i sentence-transformers koji rade lokalno.

**Zašto Oracle, a ne GitHub Pages, Render ili Railway:**

GitHub Pages servira samo statičke fajlove – bez backenda. Render i Railway imaju besplatne tierove, ali servisi se gase nakon 15 minuta neaktivnosti (cold start od 30+ sekundi pri prvom zahtjevu) i imaju stroge limite na CPU i memoriju. Oracle Always Free ne gasi servise i daje znatno više resursa.

**Registracija:** Potrebna je kreditna kartica za verifikaciju identiteta, ali se **ne naplaćuje ništa** dok se koriste Always Free resursi. Potrebno je odabrati region pri registraciji – preporučuje se eu-frankfurt-1 ili eu-amsterdam-1 zbog GDPR usklađenosti (EU data centar).

### Ubuntu 22.04 LTS

**Zašto Ubuntu, a ne Debian ili CentOS:**

CentOS je de facto ugašen (CentOS Stream nije isti produkt). Ubuntu 22.04 LTS ima podršku do April 2027, svi Docker tutoriali i Nginx konfiguracije su primarno pisani za Ubuntu, i Oracle Cloud nudi Ubuntu kao first-class image.

### Nginx

**Zašto Nginx, a ne Apache ili Caddy:**

Apache je stariji i teži web server s kompleksnijim konfiguracionim sistemom. Caddy automatski pribavlja SSL certifikate bez Certbota, ali nema tako bogatu dokumentaciju za specifičnije reverse proxy scenarije. Nginx je najrasprostranjeniji reverse proxy u produkcijskim okruženjima.

**Let's Encrypt + Certbot** za besplatne SSL/TLS certifikate koji se automatski obnavljaju svakih 90 dana.

### Docker + Docker Compose

**Zašto Docker, a ne direktna instalacija:**

Docker garantuje da isti kontejner koji radi lokalno radi identično na Oracle Cloud instanci. Docker Compose opisuje cijeli sistem u jednom docker-compose.yml fajlu – nov developer klonira repo i pokreće docker compose up, sistem je pokrenut za dvije minute.

**Zašto Docker Compose, a ne Kubernetes:**

Kubernetes je dizajniran za sisteme koji zahtijevaju automatsko skaliranje na klasteru više mašina. Za MVP fazu to je prevelika kompleksnost. Granice između servisa su jasno postavljene kontejnerima, što migraciju na Kubernetes čini pravolinijskom kad za to dođe stvarna potreba.


Kontejneri:
  frontend              → Nginx servira React build
  backend               → Glavni FastAPI servis
  auth-service          → Auth FastAPI servis
  audio-service         → faster-whisper transkripcija
  ai-chatbot-service    → RAG Chatbot (Groq + sentence-transformers)
  processing-pipeline   → Celery worker za obradu transkripata
  database              → PostgreSQL 16
  vector-db             → Qdrant
  redis                 → Redis 7
  nginx                 → Reverse proxy


**GitHub Actions** za CI/CD: svaki push na main branch automatski builda Docker image-ove i restarta servise na Oracle instanci via SSH – nema ručnog deployanja.

---

## 9. Rezime – sve tehnologije

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
| faster-whisper (small model) | Audio transkripcija lokalno | OpenAI Whisper API |
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
| Ubuntu 22.04 LTS | Serverski operativni sistem | Debian, CentOS |
| Oracle Cloud Always Free | Cloud hosting | Hetzner VPS, DigitalOcean, AWS |
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

LangChain apstrakcija osigurava da je svaka od ovih zamjena promjena jedne linije u konfiguraciji, ne refaktoring koda.

---

> **Napomena o performansama:** Lokalno pokretanje faster-whisper i sentence-transformers na Oracle ARM instanci je sporije nego API pozivi. Transkripcija minute audio zapisa traje 30-60 sekundi, generisanje embeddinga za jedan transkript 5-15 sekundi. Za studentski projekat i demo to je prihvatljivo – korisnici čekaju u pozadini dok Celery worker radi posao, a potvrda stiže notifikacijom kad je obrada gotova.
