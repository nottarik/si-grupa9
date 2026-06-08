# Release Notes — Finalna verzija 

**Datum:** 07.06.2026.
**Sprint:** 11 
**Live deployment:** <https://purple-field-0d55d8003.7.azurestaticapps.net/>

Ovaj dokument jasno razlikuje **šta je stvarno isporučeno** u finalnoj verziji od onoga što je
planirano ali nije dio finalne isporuke.

---

## 1. Šta je uključeno u finalnu verziju

Finalna verzija je kompletan, deployan RAG chatbot za podršku call centru sa tri korisničke uloge
(korisnik, agent, admin) i punim tokom od transkripta do odgovora.

**Glavni isporučeni moduli:**
- Chat sa RAG odgovaranjem (retrieval + Groq LLM), klasifikacija namjere i query rewriting.
- Eskalacija na živog agenta (automatska kod niske pouzdanosti i na eksplicitan zahtjev) preko WebSocket-a.
- Transcript pipeline: upload (tekst/audio), Groq Whisper transkripcija, normalizacija, **maskiranje PII**, detekcija govornika, chunking, ekstrakcija Q&A, embedding (`all-MiniLM-L6-v2`), pohrana u Qdrant.
- Baza znanja: ručni unos, kuriranje (approve/reject), prevencija duplikata, verzionisanje, traceability do izvornog transkripta.
- Admin panel: dashboard, transkripti, baza znanja, korisnici, chat logovi, ocjene, issues, obavijesti.
- Agent panel: live queue, vođenje razgovora, KB lookup, vlastita historija.
- Batch import sa Google Drive-a + scheduled pipeline sa live prikazom napretka.
- Autentifikacija (JWT) i RBAC (admin/manager/agent/user).
- Self-healing pri startu (dovršavanje embeddinga + ponovna obrada zaglavljenih transkripata).

---

## 2. Najvažnije funkcionalnosti

| Funkcionalnost | Opis |
|---|---|
| RAG chat | Cosine pretraga (top-K=5) + LLM generisanje sa kontekstom; napomena o nesigurnosti kod srednje pouzdanosti |
| Eskalacija | Red čekanja, prioriteti, dodjela agenta, live chat, resolve |
| PII zaštita | Detekcija + maskiranje (JMBG s checksumom, telefon, email, IBAN, SSN), Fernet token mapa, čišćenje placeholdera iz baze znanja |
| Pipeline obrada | Asinhrono (FastAPI BackgroundTasks) + live status po fazama |
| Drive import | On-demand i scheduled (hourly/daily/weekly), deduplikacija, robusnost na grešku pojedinog fajla |
| Cloud deployment | Single-click `azd up` / push na `main` → Azure Container App + Static Web App |
| Sigurnost | JWT, RBAC u servisnom sloju, prompt-injection zaštita, HTTPS/WSS, secrets van koda |

---

## 3. Poznata ograničenja

- **Skaliranje:** backend je fiksiran na 1 uvijek-toplu repliku (free tier + in-process scheduler) — nema autoscalinga.
- **Frontend testovi nisu u CI-u:** CI pokreće samo backend `pytest`; frontend se validira ručno + `npm run lint`.
- **Redis nije na Azure produkciji:** koristi se opciono; aplikacija radi i bez njega.
- **Backend image se builda lokalno** (ACR Tasks blokirani na free-trial).
- **Zavisnost o vanjskim servisima:** Groq/Qdrant/Supabase free-tier limiti mogu uticati na odziv.
- **`TOKEN_MAP_KEY` se ne smije mijenjati** nakon prvog deploya (inače PII postaje nedekriptabilan).
- Potpuna lista: `KnownIssues.md`.

---

## 4. Poznati bugovi

- Klasifikacija namjere može povremeno pogrešno označiti rubni upit (npr. kratko ili dvosmisleno pitanje); ublaženo `RAG_OFFTOPIC_THRESHOLD` pragom i fallbackom na eskalaciju.
- LLM speaker labeling može pogrešno labelovati govornika u vrlo kratkim audio transkriptima (graceful fallback, ne ruši pipeline).
- PII regex detekcija može propustiti nestandardne formate; checksum/validacija smanjuju, ali ne eliminišu rizik.
- Kratki prekidi Groq/Qdrant servisa privremeno povećavaju udio eskalacija/fallback odgovora.

Nijedan poznati bug ne blokira osnovne korisničke tokove.

---

## 5. Šta NIJE dio finalne isporuke (planirano, ali nezavršeno)

| Stavka | Status | Napomena |
|---|---|---|
| Automatizovani frontend test suite u CI | Deferred | Postoji ručna validacija + lint; integracija u CI nije urađena |
| Horizontalno autoscaliranje backenda | Deferred | Fiksirana 1 replika |
| Redis cache/rate-limit na Azure produkciji | Deferred | Nije provisioniran |
| Poseban manager UI | Partially Done | Uloga postoji; nema zaseban panel |
| Cloud (ACR Tasks) build backend image-a | Deferred | Free-trial ograničenje |
| Višejezičnost van BS/EN | Not Done | Van opsega |

---

## 6. Sažetak isporuke vs. plan

Sve numerisane backlog stavke (PB-1 – PB-72) su isporučene (pogledati `ProductBacklog.md`). Razlika između
isporučenog i planiranog odnosi se isključivo na nefunkcionalne/operativne stavke navedene u sekcijama
3 i 5, koje su svjesno odgođene i nisu prikazane kao završene.
