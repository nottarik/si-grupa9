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

\---

## 1\. Branching strategija — GitHub Flow

Odabrali smo **GitHub Flow** zbog jednostavnosti i prilagođenosti timovima koji rade kontinuirani razvoj bez kompleksnih release ciklusa. Strategija je linearna, pregledna i svim članovima tima odmah razumljiva.

### Grane

|Grana|Namjena|
|-|-|
|`main`|Uvijek stabilan, direktno deployabilan kod|
|`feature/naziv-stavke`|Svaka backlog stavka = jedna grana|
|`fix/naziv-buga`|Ispravke grešaka|

### Konvencija commit poruka

```
\[feat]     nova funkcionalnost
\[fix]      ispravka greške
\[refactor] refaktorisanje
\[docs]     dokumentacija
\[test]     testovi
\[chore]    build, konfiguracija
```

### Tok rada

1. Kreirati granu iz `main`: `git checkout -b feature/budget-planning`
2. Razviti funkcionalnost uz redovne commitove
3. Otvoriti Pull Request prema `main`
4. Minimalno jedan član tima radi code review
5. Nakon odobrenja — merge u `main` i brisanje feature grane

\---

## 2\. Pregled stacka

|Sloj|Tehnologija|
|-|-|
|Frontend|React 18 + Vite + Tailwind CSS|
|Backend|Python 3.12 + FastAPI|
|Auth|python-jose + passlib/bcrypt|
|AI / RAG pipeline|Groq API (Llama 3.3) + direktna implementacija (bez LangChain)|
|Audio transkripcija|Groq Whisper API (whisper-large-v3, cloud)|
|Embeddinzi|sentence-transformers all-MiniLM-L6-v2 (lokalno)|
|Pozadinska obrada|FastAPI BackgroundTasks|
|Relacijska baza|PostgreSQL 16 + SQLAlchemy + Alembic (Supabase cloud)|
|File storage|Supabase Storage|
|Vektorska baza|Qdrant Cloud|
|Tunel / proxy|Cloudflare Tunnel (cloudflared)|
|Kontejnerizacija|Docker + Docker Compose|
|Hosting|Cloudflare Tunnel (backend) + Cloudflare Pages (frontend) + Supabase + Qdrant Cloud|

\---

## 3\. Programski jezik i runtime

### Python 3.12

Cijeli backend pišemo u Pythonu jer ima najbolju i najzreliju podršku za AI i RAG ekosistem (Hugging Face, sentence-transformers, Qdrant klijenti), što omogućava bržu i jednostavniju implementaciju modela, embeddinga i retrieval logike. Node.js nije odabran jer, iako je dobar za web i real-time aplikacije, ima slabiju i manje razvijenu AI/ML podršku, pa bi razvoj RAG sistema bio kompleksniji i manje efikasan.

\---

## 4\. Frontend

### React 18 + Vite + Tailwind CSS

**React** ima najveću bazu developera i bogat ekosistem UI biblioteka relevantnih za ovaj projekat (react-markdown, react-virtuoso). Vue i Svelte su tehnički odlični, ali manji ekosistem znači manje gotovih rješenja za chat interfejs i admin panel.

**Vite** zamjenjuje Create React App zbog brzine – dev server startuje za ispod sekunde umjesto 10–30 s, a produkcijski build je optimizovaniji zahvaljujući Rollup-u.

**Tailwind** daje punu kontrolu nad dizajnom bez override-anja tuđeg vizualnog jezika kao što nameću Bootstrap ili Material UI. Utility klase drže stilove uz markup, što ubrzava razvoj responsive komponenti.

### Axios + React Query

**Axios** umjesto nativnog fetch-a zbog interceptora – JWT token se dodaje jednom globalno, ne po svakom pozivu. **React Query** zamjenjuje Redux za server state: caching, refetching i error handling u nekoliko linija, bez boilerplatea.

\---

## 5\. Backend servisi

### FastAPI

Odabran umjesto Djanga (previše funkcionalnosti koje ne koristimo – ORM, template engine, admin panel) i Flaska (sinhroni po defaultu, nema automatsku validaciju). FastAPI ključne prednosti:

* Automatski Swagger UI na `/docs` bez konfiguracije
* Pydantic validacija ulaznih podataka i jasne error poruke
* Native `async/await` – endpoint ne blokira server dok čeka LLM odgovor (5–10 s)

### SQLAlchemy 2.0 + Alembic

Najzreliji Python ORM s najboljom PostgreSQL podrškom. SQLAlchemy 2.0 uvodi async session support. Alembic generiše revizionalne migration skripte s rollback podrškom.

\---

## 6\. AI i RAG komponente

### Groq API (Llama 3.3 70B)

Groq koristi vlastite LPU čipove i odgovara za manje od sekunde. Model `llama-3.3-70b-versatile` donosi poboljšanja u tačnosti i slijeđenju instrukcija u odnosu na Llamu 3.1. Besplatni tier: 14.400 zahtjeva/dan, 500.000 tokena/min – dovoljno za razvoj i testiranje. Lokalni pristup (Ollama) je besplatan ali zahtijeva 8+ GB RAM-a samo za model i 30–60 s po odgovoru bez GPU-a.

### sentence-transformers – `all-MiniLM-L6-v2`

Embedding model koji radi lokalno bez API troška. Optimizovan za semantičku sličnost i brze cosine pretrage, veličina \~90 MB, radi na CPU-u. Podržava engleski i latinske jezike; za Bosnian/Serbian/Croatian tekst daje dovoljno dobre rezultate za MVP fazu.

### Groq Whisper API (whisper-large-v3)

Transkripcija audio fajlova vrši se putem Groq cloud API-ja (`whisper-large-v3`), što eliminira potrebu za lokalnim pokretanjem modela i smanjuje RAM footprint backend servera. Odgovor stiže za nekoliko sekundi bez GPU-a na serveru. Prethodni pristup (faster-whisper lokalno) zahtijevao je dodatne Docker resurse i \~30–60 s po minuti audia na CPU-u.

### RAG pipeline — direktna implementacija

RAG pipeline je implementiran direktno bez LangChain apstrakcijskog sloja. Retrieval se vrši Qdrant klijentom, embeddinzi se generišu sentence-transformers bibliotekom, a Groq SDK se koristi direktno za pozive LLM-u. Ovo smanjuje broj zavisnosti i daje punu kontrolu nad svakim korakom pipeline-a.

\---

## 7\. Pozadinska obrada

### FastAPI BackgroundTasks

Transkripcija i generisanje embeddinga su dugotrajne operacije koje se izvršavaju asinhorno kako ne bi blokirale HTTP odgovor. Koristi se FastAPI ugrađeni `BackgroundTasks` mehanizam: endpoint odmah vraća `transcript\_id`, a obrada (Groq Whisper → preprocessing → embedding → Qdrant) se nastavlja u pozadini iste serverske instance. Ovaj pristup je dovoljan za trenutne obime opterećenja bez potrebe za eksternim brokerom. Celery + Redis ostaje opcija za horizontalno skaliranje kada obim zahtijeva distribuirane workere na više instanci.

\---

## 8\. Baze podataka i storage

### PostgreSQL 16 (Supabase)

Bolji JSON support (`jsonb`), bolji full-text search i stroža SQL conformance u poređenju s MySQL-om. Baza je hostovana na **Supabase** (managed PostgreSQL cloud), što eliminira potrebu za administracijom servera, automatski pruža SSL i backup, a besplatni tier pokriva MVP fazu. SQLite nije opcija za produkciju zbog file-based lockinga.

### Supabase Storage

Koristi se za čuvanje uploadovanih audio i tekstualnih fajlova transkripta. Integrisan s istim Supabase projektom kao i PostgreSQL, što pojednostavljuje autentifikaciju i smanjuje broj eksternih servisa.

### Qdrant Cloud

Vektorska baza hostovana na **Qdrant Cloud** (free tier). Pinecone nema self-hosted opciju i limitira besplatni tier na 100k vektora. pgvector nema HNSW indeksiranje, što znači znatno sporije pretrage pri 10k+ embeddinga. Qdrant podržava payload filtere (pretraga unutar određenog transkript ID-a ili datumskog raspona). Cloud hosting smanjuje operativni overhead u odnosu na self-hosted Docker varijantu.

\---

## 9\. Infrastruktura i deployment

### Cloudflare Tunnel + Cloudflare Pages + managed cloud servisi

|Servis|Provider|Tier|
|-|-|-|
|Backend (FastAPI)|Cloudflare Tunnel (cloudflared)|Free|
|Frontend (React)|Cloudflare Pages|Free|
|PostgreSQL + Storage|Supabase|Free|
|Vektorska baza|Qdrant Cloud|Free (1GB)|

**Cloudflare Tunnel** izlaže lokalno pokrenuti backend na internet bez otvorenih portova, bez statičke IP adrese i bez potrebe za reverse proxyjem. `cloudflared` kontejner uspostavlja outbound tunel prema Cloudflare mreži i generiše javni URL. Ovo eliminiše potrebu za Nginxom, SSL certifikatima i Oracle/Render hostingom — backend može raditi na bilo kojoj mašini iza NAT-a. Sve managed cloud komponente (Supabase, Qdrant Cloud) automatski pružaju SSL, backup i monitoring.

### Docker + Docker Compose

Garantuje identično okruženje lokalno i na serveru. Nov developer klonira repo i pokreće `docker compose up` – sistem je gore za dvije minute. Kubernetes je prevelika kompleksnost za MVP fazu; granice između servisa su već jasno postavljene kontejnerima, što migraciju čini pravolinijskom kad za to dođe potreba.

Kontejneri (lokalni razvoj — `docker-compose.yml`):

```
backend               → FastAPI servis (port 8000)
db                    → PostgreSQL 16 (lokalna kopija, port 5432)
qdrant                → Qdrant (lokalna kopija, port 6333)
```

Produkcija (docker-compose.tunnel.yml):

```
backend               → FastAPI servis (expose :8000, bez javnog porta)
cloudflared           → Cloudflare Tunnel — izlaže backend:8000 na internet
```

Svi eksterni podaci (DB, Qdrant) su u cloudu — nema lokalnih db/qdrant kontejnera u produkciji.

**GitHub Actions** za CI/CD: svaki push na `main` builda i deployuje frontend na Cloudflare Pages automatski.

### SSL i proxy

U aktualnom produkcijskom setupu (Cloudflare Tunnel) nema potrebe za Nginxom ni Let's Encrypt certifikatima — SSL i proxying rješava Cloudflare automatski na svojoj mreži. Nginx i Certbot postoje jedino u starijem `docker-compose.prod.yml` koji je korišten za Oracle Cloud hosting i trenutno nije aktivan.

\---

## 10\. Rezime – sve tehnologije

### Runtime i jezik

|Alat|Verzija|Namjena|
|-|-|-|
|Python|3.12|Runtime za sve backend servise|

### Frontend

|Alat|Namjena|Odabran umjesto|
|-|-|-|
|React 18|UI framework|Vue, Svelte|
|Vite|Build alat i dev server|Create React App|
|Tailwind CSS|Stilizacija|Bootstrap, Material UI|
|Axios|HTTP klijent|native fetch|
|React Query|Server state management|Redux|

### Backend

|Alat|Namjena|Odabran umjesto|
|-|-|-|
|FastAPI|HTTP framework za sve servise|Django, Flask|
|Pydantic v2|Validacija podataka|ručna validacija|
|python-jose|JWT generisanje i verifikacija|PyJWT|
|passlib + bcrypt|Hashiranje passworda|—|
|SQLAlchemy 2.0|ORM za PostgreSQL|Tortoise ORM|
|Alembic|Migracije baze podataka|—|

### AI i obrada

|Alat|Namjena|Odabran umjesto|
|-|-|-|
|Groq API (Llama 3.3 70B)|LLM za generisanje odgovora|Claude API, GPT-4o|
|Groq Whisper API (whisper-large-v3)|Audio transkripcija (cloud)|faster-whisper lokalno|
|sentence-transformers (all-MiniLM-L6-v2)|Embeddinzi lokalno|OpenAI embedding API|
|FastAPI BackgroundTasks|Pozadinska asinhorna obrada|Celery + Redis|

### Baze i storage

|Alat|Namjena|Odabran umjesto|
|-|-|-|
|PostgreSQL 16 (Supabase)|Relacijska baza (cloud)|MySQL, SQLite|
|Supabase Storage|File storage za transkripte|S3, lokalni disk|
|Qdrant Cloud|Vektorska baza (cloud)|Pinecone, pgvector|

### Infrastruktura

|Alat|Namjena|Odabran umjesto|
|-|-|-|
|Docker|Kontejnerizacija|direktna instalacija|
|Docker Compose|Orkestracija kontejnera|Kubernetes|
|Cloudflare Tunnel (cloudflared)|Backend izlaganje na internet (bez otvoren porta)|Nginx + certbot, ngrok, Render|
|Cloudflare Pages|Frontend hosting (CDN)|Netlify, Vercel|
|GitHub Actions|CI/CD pipeline|Jenkins, GitLab CI|

\---

## Napomena: Prelaz na produkciju

Ukoliko projekat preraste studentsku fazu, plaćene alternative su direktna zamjena bez refaktoringa:

|Komponenta|Studentska verzija|Produkcijska verzija|
|-|-|-|
|LLM|Groq (besplatno, Llama 3.3)|Claude API / GPT-4o|
|Embeddinzi|sentence-transformers (lokalno)|OpenAI text-embedding-3-small|
|Audio|Groq Whisper API (besplatno)|OpenAI Whisper API|
|Hosting|Cloudflare Tunnel + Supabase + Qdrant Cloud (free)|VPS CPX31|

Zamjena LLM-a ili vektorske baze zahtijeva izmjenu odgovarajućeg servisa (`LLMService`, `VectorStoreService`), ali ostatak pipeline-a ostaje nepromijenjen.

