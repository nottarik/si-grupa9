# Završni izvještaj o radu tima (Dokumentovanje rada)

Konkretan završni izvještaj o razvoju sistema **Call Centar Chatbot**. Izvještaj je vezan za stvarnu
implementaciju projekta i prati strukturu traženu u zadatku zadnjeg sprinta.

---

## 1. Svrha projekta

Cilj projekta je izgraditi **RAG-zasnovani AI asistent za podršku call centru** telekom/ISP operatera
koji iz stvarnih transkripata poziva gradi pretraživu bazu znanja i na osnovu nje daje tačne,
izvor-sljedive odgovore kroz chat. Sistem treba smanjiti opterećenje agenata, ubrzati dolazak do
odgovora i osigurati da se korisnik bez pouzdanog odgovora glatko prebaci na živog agenta.

## 2. Problem koji sistem rješava

- **Znanje je zaključano u transkriptima poziva** — agenti ponavljaju iste odgovore, a novi agenti
  teško dolaze do provjerenih informacija.
- Klasična pretraga ne razumije prirodni jezik niti kontekst razgovora.
- Osjetljivi lični podaci (PII) u transkriptima ne smiju procuriti u bazu znanja ni u odgovore.

Sistem rješava ovo tako što transkripte automatski obrađuje (uz **maskiranje PII**), pretvara ih u
Q&A bazu znanja i koristi **retrieval-augmented generation** da odgovori na pitanja — a kad nije
siguran, **eskalira na agenta** umjesto da nagađa.

## 3. Glavne korisničke uloge

| Uloga | Opis |
|---|---|
| **Korisnik (user)** | Postavlja pitanja chatbotu, ocjenjuje odgovore, eskalira na agenta, vodi vlastitu historiju. |
| **Agent** | Preuzima eskalirane razgovore, vodi live chat, pretražuje bazu znanja, predlaže Q&A parove. |
| **Administrator (admin)** | Upravlja transkriptima, bazom znanja, korisnicima, ocjenama, issues-ima, obavijestima i automatskim importom. |
| **Manager** | Uloga sa pravima pregleda nivoa administracije (bez zasebnog panela). |

## 4. Glavne implementirane funkcionalnosti

- **RAG chat** — klasifikacija namjere, cosine pretraga (top-K=5) nad Qdrant-om, generisanje odgovora kroz Groq LLM uz kontekst, napomena o nesigurnosti, fallback i eskalacija.
- **Eskalacija na agenta** — automatska (niska pouzdanost) i na eksplicitan zahtjev; red čekanja, prioriteti, live chat preko WebSocket-a, resolve.
- **Transcript pipeline** — upload (tekst/audio), Groq Whisper transkripcija, normalizacija, **maskiranje PII**, detekcija govornika, chunking, ekstrakcija Q&A parova, embedding, pohrana u Qdrant; asinhrono uz live status po fazama.
- **Baza znanja** — ručni unos, kuriranje (approve/reject), prevencija duplikata, verzionisanje, traceability do izvornog transkripta.
- **Admin i agent paneli** — dashboard, transkripti, baza znanja, korisnici, chat logovi, ocjene, issues, obavijesti; agent live queue + KB lookup + historija.
- **Automatizacija podataka** — batch import sa Google Drive-a i scheduled pipeline (hourly/daily/weekly).
- **Sigurnost** — JWT autentifikacija, RBAC u servisnom sloju, privacy boundary prema LLM-u, Fernet enkripcija PII token mape, prompt-injection zaštita.
- **Cloud deployment** — single-click na Azure (`azd` + Bicep), automatizovan kroz GitHub Actions.

## 5. Pregled rada kroz sprintove

| Sprint | Fokus | Glavni ishodi |
|---|---|---|
| **1** | Istraživanje i vizija | Domena, stakeholderi, Product Vision, Team Charter, početni backlog |
| **2** | Zahtjevi | User Stories, Acceptance Criteria, NFR, sprint backlog/goal |
| **3** | Arhitektura i plan | Architecture Overview, Domain Model, Use Case, Risk Register, Test Strategy |
| **4** | Setup i plan isporuke | Definition of Done, tehnički setup, initial release plan |
| **5** | MVP jezgro | Auth, chat UI, transcript obrada, baza znanja, RAG, prvi testovi |
| **6** | Stabilizacija | Dorada uploada/validacije, dashboard/navigacija, report issues, CI testovi |
| **7** | Preprocessing & PII | Refaktoring pipeline-a u module, PII detekcija/maskiranje (Fernet), LLM speaker labeling, granularni testovi |
| **8** | Audio & glasovni unos | Groq Whisper transkripcija, audio preview, glasovni unos u chatu |
| **9** | Kvalitet i UX | Ocjene sesije, obavijesti, ručni unos KB, kuriranje, performanse, E2E/regresijski testovi, user settings |
| **10** | Automatizacija & cloud | Batch Drive import, scheduled pipeline, live progress, single-click Azure deploy, build optimizacija, dedup, bulk delete, korisničke poruke o greškama |
| **11** | Završna isporuka | Stabilizacija + kompletna dokumentacija, deployment procedura, CD pipeline, user manual, finalni backlog, release notes, QA, arhitektura, AI summary, known issues |

## 6. Šta je završeno, djelimično završeno ili nije završeno

**Završeno (Done):** sve numerisane backlog stavke PB-1 – PB-72 — kompletan MVP plus naknadno
planirane funkcionalnosti (vidi `ProductBacklog.md`). Sistem je deployovan i live.

**Nije završeno / odgođeno (Not Done / Deferred):**
- Automatizovani frontend test suite u CI (validacija ručna + lint).
- Horizontalno autoscaliranje i Redis na Azure produkciji.
- Cloud (ACR Tasks) build backend image-a — free-trial ograničenje.
- Mjerenje test coverage % i višejezičnost van BS/EN.

Razlozi za svaku nezavršenu stavku navedeni su u `ProductBacklog.md` i `KnownIssues.md`.

## 7. Glavne tehničke odluke

| Odluka | Obrazloženje |
|---|---|
| **RAG umjesto fine-tuninga** | Jeftinije, ažurno, izvor-sljedivo; baza znanja se mijenja bez retreniranja modela. |
| **Groq kao LLM/Whisper provider** | Brzi inference (`llama-3.3-70b-versatile`, `whisper-large-v3`) uz free tier. |
| **Lokalni embedding (`all-MiniLM-L6-v2`)** | Bez eksternog troška/latencije za embedding; 384-dim dovoljno za domenu. |
| **Qdrant Cloud** | Namjenska vektorska baza sa cosine pretragom. |
| **Vlastita PII implementacija (regex+checksum+NER) umjesto Presidio** | Lakša zavisnost, kontrola nad formatima (BS telefon, JMBG checksum). |
| **Fernet enkripcija token mape** | Reverzibilno maskiranje bez eksterne enkripcijske usluge. |
| **Privacy boundary** | LLM uvijek prima samo maskirani tekst — zaštita PII na nivou arhitekture. |
| **FastAPI BackgroundTasks + self-heal umjesto Celery** | Jednostavnije za free-tier (jedna replika); self-heal pokriva prekide. |
| **Azure Container Apps + Static Web Apps preko `azd`/Bicep** | Single-click, ponovljiv deployment; infrastruktura kao kod. |
| **Jedna uvijek-topla replika** | Izbjegava cold-start učitavanja modela i dvostruko okidanje schedulera. |

## 8. Najveći problemi tokom razvoja i način rješavanja

| Problem | Rješenje |
|---|---|
| **PII curenje rizik** (osjetljivi podaci u bazi/odgovorima) | Maskiranje prije obrade, privacy boundary prema LLM-u, scrubber + regex safety net na izlazu, no-leak testovi |
| **Lažno pozitivno maskiranje imena** | Dorada NER/recognizer logike (Sprint 10) + čišćenje placeholdera iz baze znanja |
| **Pogrešna klasifikacija rubnih upita** | Uvođenje `OFFTOPIC` praga i fallback na eskalaciju umjesto pogrešnog odgovora |
| **Spori Docker buildovi (>25 min)** | CPU-only torch u zasebnom layeru + BuildKit cache mount → cached rebuild u sekundama (Sprint 10) |
| **ACR Tasks blokirani na free-trial** | Lokalni Docker build pa push na ACR (dokumentovano u deployment proceduri) |
| **Prekid obrade pri padu procesa** (nema durable queue) | Self-heal pri startu — ponovna obrada „Sirovih" transkripata + dovršavanje embeddinga |
| **Duplikati u bazi znanja** | Dedup na svim ulazima (ručni unos, transkript, batch, eskalacija) — Sprint 10 |
| **Nestabilnost eksternih servisa** | Graceful degradacija, retry pri startu (Qdrant), eskalacija kao sigurnosna mreža |
| **Sirove tehničke greške korisniku** | Korisnički prilagođene, konzistentne poruke o greškama (Sprint 10) |

## 9. Šta bi tim unaprijedio da se projekat nastavlja

1. **Automatizovani frontend testovi** (Vitest/RTL) integrisani u CI + mjerenje coverage %.
2. **Skalabilnost:** prelazak na horizontalno skaliranje (eksterni durable queue/Celery umjesto in-process schedulera) i Redis za cache/rate-limit u produkciji.
3. **Robusniji PII sloj** sa formalnom evaluacijom (precision/recall) i širom pokrivenošću formata.
4. **Mjerenje kvaliteta RAG-a** (ground-truth set, metrika tačnosti/relevantnosti, A/B pragova).
5. **Produkcijsko otvrdnjavanje:** rate-limiting, audit logovi, monitoring/alerting, backup strategija baze.
6. **Manager panel** i finija RBAC prava po sekcijama.
7. **Cloud build pipeline** (kada to pretplata dozvoli) da se ukloni lokalni Docker preduvjet.

---

## 10. Zaključak

Projekat je isporučio funkcionalno kompletan, deployovan RAG chatbot za podršku call centru, sa punim
tokom od transkripta do odgovora, eskalacijom na agenta, administracijom i automatizacijom uvoza
podataka. Sistem je razvijan inkrementalno kroz 11 sprintova, sa transparentnim korištenjem AI alata i
jasno dokumentovanim ograničenjima. Uz pripadajuću dokumentaciju (deployment, CD pipeline, user manual,
arhitektura, QA, release notes, known issues), projekat se može **pokrenuti, deployati, koristiti,
testirati i evaluirati bez dodatnih neformalnih objašnjenja tima**.
