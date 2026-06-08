# Finalni Product Backlog — status (Sprint 11)

Ovaj dokument prikazuje **stvarno stanje projekta na kraju razvoja**, ne željeno stanje. Status svake
stavke je jedan od: **Done**, **Partially Done**, **Not Done**, **Deferred**. Za svaku nezavršenu ili
djelimično završenu stavku naveden je kratak razlog.

> **Napomena o usklađivanju:** tokom sprinteva 1–4 dio planskih/istraživačkih i dokumentacionih
> stavki vođen je oznakama „In Progress"/„Not Started" koje su s vremenom **zastarjele** — njihov
> rezultat je u međuvremenu isporučen (kao deliverable dokument ili kroz povezanu kasniju stavku).
> Finalni status u tabeli ispod usklađen je sa stvarno isporučenim sistemom (provjereno u kodu i
> sprint deliverable-ima), pa se za neke rane stavke razlikuje od oznake iz ranijih sprintova. Kolona
> „Napomena" objašnjava gdje je stavka realizovana.

Legenda: **Done** = isporučeno i provjereno · **Partially Done** = djelimično · **Not Done** =
nije implementirano · **Deferred** = svjesno ostavljeno za budući rad.

---

## Numerisane stavke (PB-1 – PB-72)

| ID | Naziv stavke | Tip | Finalni status | Napomena / razlog |
|----|--------------|-----|----------------|-------------------|
| 1 | Istraživanje domene | research | Done | Sprint 1 deliverable |
| 2 | Mapiranje stakeholdera | research | Done | `StakeholderMap.md` |
| 3 | Product Vision | documentation | Done | `ProductVision.md` |
| 4 | Team Charter | documentation | Done | `TeamCharter.md` |
| 5 | Istraživanje ulaznih formata | research | Done | Realizovano kroz format `Agent:`/`Korisnik:` + audio pipeline |
| 6 | Istraživanje RAG i LLM servisa | research | Done | Odabir Groq + sentence-transformers + Qdrant |
| 7 | Definisanje MVP opsega | documentation | Done | Dio Product Vision-a |
| 8 | Početni Product Backlog | documentation | Done | Ažuriran svaki sprint; finalna verzija ovaj dokument |
| 9 | User Stories | documentation | Done | `UserStories.md` (sprint 2/3) |
| 10 | Acceptance Criteria | documentation | Done | Uz user stories |
| 11 | Nefunkcionalni zahtjevi | documentation | Done | `Non-FunctionalRequirements.md` |
| 12 | Ažuriranje backloga | documentation | Done | Kontinuirano kroz sprinteve |
| 13 | Konvertovanje iz audio zapisa u transkript | research | Done | Implementirano kroz Groq Whisper |
| 14 | Plan baze podataka | technical | Done | Shema realizovana (PostgreSQL/Supabase); domain model u sprint-3 |
| 15 | Ocjena odgovora chatbota | research | Done | Realizovano kroz feedback/ocjene (PB-57) |
| 16 | Risk Register | documentation | Done | `RiskRegister.md` (sprint 3) |
| 17 | Use Case Model | documentation | Done | `UseCase.md` (sprint 3) |
| 18 | Upload i unos transkripata | feature | Done | Transcripts modul (upload/manual) |
| 19 | Osmisliti testne strategije | research | Done | `TestStrategy.md` (sprint 3) |
| 20 | Definition of Done | documentation | Done | `DefinitionOfDone.md` (sprint 4) |
| 21 | Osnovni skeleton projekta | technical | Done | Repo, struktura, Docker, CI |
| 22 | Chat UI | feature | Done | `ChatWindow`/`ChatPage` |
| 23 | Priprema za obradu transkripata | technical | Done | Preprocessing pipeline |
| 24 | Parser za razdvajanje uloga | technical | Done | `preprocessing/speakers.py` (+ LLM fallback) |
| 25 | Normalizacija teksta | technical | Done | `preprocessing/normalize.py` |
| 26 | Maskiranje osjetljivih podataka | technical | Done | `preprocessing/pii/` (JMBG/telefon/email/IBAN/SSN) |
| 27 | Izgradnja baze znanja | feature | Done | Embedding + Qdrant + retrieval |
| 28 | Prijava netačnog odgovora | technical | Done | `POST /chat/feedback` (`is_incorrect`) |
| 29 | Korisnička dokumentacija | documentation | Done | `UserManual.md` (ovaj sprint) |
| 30 | Izgradnja razvojnog okruženja | feature | Done | Docker Compose (backend, db, redis, qdrant, nginx) |
| 31 | Odgovor kada nema sigurnog responsea | feature | Done | Fallback poruka + eskalacija na agenta |
| 32 | Potvrda i obrada netačnog odgovora | technical | Done | Negativan feedback → `Anomalija` (Issue) |
| 33 | Pregled unesenih transkripata | feature | Done | Transcripts lista |
| 34 | Pregled postavljenih pitanja i odgovora | feature | Done | Knowledge pregledi |
| 35 | Pregled prijavljenih problema | feature | Done | Admin → Issues |
| 36 | Sign In | technical | Done | JWT login |
| 37 | Sign Out | technical | Done | UserMenu odjava |
| 38 | Uređivanje postojećih transkripata | feature | Done | `PATCH /transcripts/{id}` |
| 39 | Brisanje transkripata sa potvrdom akcije | feature | Done | `DELETE /transcripts/{id}` |
| 40 | Filtriranje i pretraga transkripata | feature | Done | Pretraga po ključnoj riječi/datumu |
| 41 | Dodjela i upravljanje ulogama korisnika | feature | Done | `PATCH /users/{id}/role` |
| 42 | Pregled i brisanje korisnika | feature | Done | Users sekcija |
| 43 | Dashboard s aktuelnim podacima | feature | Done | Admin Dashboard (stvarni agregati) |
| 44 | Validacija formata transkripata | technical | Done | Backend + frontend validacija |
| 45 | Account Settings | feature | Done | Implementirano kao PB-64 (User Settings) |
| 46 | Prikaz statusa obrade transkripata | feature | Done | Pipeline Monitor (statusi) |
| 47 | Agent queue — pregled i potvrđivanje Q&A parova | feature | Done | Agent pregled Pending Q&A |
| 48 | Escalation queue u admin panelu | feature | Done | Eskalacijski red + live chat |
| 49 | Historija razgovora korisnika | feature | Done | `GET /chat/sessions` + UI |
| 50 | Automatsko obavještavanje agenta o završetku korisničke sesije | feature | Done | WS auto-end |
| 51 | Agent panel s Live Queue i pristupom bazi znanja | feature | Done | `AgentShell`, `AgentQueue`, `KbLookup` |
| 52 | RAG retrieval i LLM klasifikacija upita | technical | Done | `RagService` + intent klasifikacija |
| 53 | Obrada osnovne komunikacije sa LLM | feature | Done | Smalltalk/generativni odgovori |
| 54 | WebSocket komunikacijia između korisnika i agenta | technical | Done | `ConnectionManager` + WS rute |
| 55 | Resolving chatova | feature | Done | `POST /escalation/{id}/resolve` |
| 56 | Poboljšanje maskiranja PII podataka i ekstrakcije Q&A parova | bug fix | Done | Sprint 9 |
| 57 | Ocjena razgovora po završetku sesije | feature | Done | `POST /chat/sessions/{id}/rate` |
| 58 | Sistemske obavijesti u chatbot-u | feature | Done | Announcements |
| 59 | Mogućnost ručnog unosa Q&A para direktno u bazu znanja bez transkripata | feature | Done | `POST /knowledge/manual` |
| 60 | Pregled i kuriranje sadrzaja baze znanja | feature | Done | Knowledge Pending/Approved |
| 61 | Optimizacija performansi chatbota | technical | Done | Paralelni intent+embed, prefetch vektor |
| 62 | Prikaz komentara uz ocjene razgovora u admin i agent panelu | feature | Done | Ratings/komentari |
| 63 | End-to-end i regresijsko testiranje sistema | technical | Done | 223 testa u CI (pogledati napomenu o pokrivenosti) |
| 64 | User Settings | feature | Done | Ime, brisanje historije/naloga |
| 65 | Brisanje pojedinačnog chata iz historije| feature | Done | `DELETE /chat/sessions/{id}` |
| 66 | Batch procesiranje fajlova iz eksternih izvora | feature | Done | Google Drive import + deduplikacija |
| 67 | Scheduled pipeline obrada i automatsko ažuriranje baze znanja | feature | Done | In-process scheduler, admin kontrola |
| 68 | Single-click cloud deployment | devops | Done | Azure (`azd` + Bicep) |
| 69 | Optimizacija build procesa i CI-CD performansi | technical | Done | Docker cache + CPU-only torch layer |
| 70 | Prevencija duplih unosa u bazu znanja | technical | Done | Deduplikacija na svim ulazima |
| 71 | Bulk brisanje razgovora iz Chat Logs, Transcripts i Issues) | feature | Done | Bulk-delete endpointi |
| 72 | Razumljive i korisnički prilagođene poruke o greškama | feature | Done | Sprint 10 |

**Sažetak:** 72/72 numerisanih stavki — **Done**.

---

## Stvarno stanje van numerisanih stavki 

Sljedeće **nije bilo zasebna backlog stavka**, ali se navodi radi  stvarnog stanja
projekta (videti i `KnownIssues.md`):

| Stavka | Status | Razlog |
|---|---|---|
| Automatizovani frontend testovi u CI | **Not Done / Deferred** | CI (`ci.yml`) pokreće samo backend `pytest`; frontend se validira ručno + `npm run lint`. Frontend test suite nije integrisan u CI. |
| Horizontalno skaliranje backenda | **Deferred** | Container App je fiksiran na 1 repliku (uvijek-topla) zbog free tiera i in-process schedulera; autoscaling nije konfigurisan. |
| Redis na Azure produkciji | **Deferred** | Redis nije provisioniran u `main.bicep`; koristi se opciono (lokalno/Upstash). Aplikacija radi i bez njega. |
| Manager-specifični UI | **Partially Done** | Uloga `manager` postoji u modelu i RBAC-u, ali nema poseban panel — koristi preglede nivoa admina. |
| Cloud build backend image-a (ACR Tasks) | **Deferred** | Blokirano na free-trial pretplati („TasksOperationsNotAllowed"); image se buildi lokalno pa push na ACR. |
| Višejezičnost van BS/EN | **Not Done** | Sistem cilja bosanski (UI/domena) i razumije engleski; drugi jezici nisu u opsegu. |

---

## Zaključak

Kompletan MVP i sve naknadno planirane funkcionalnosti (PB-1 – PB-72) su isporučene i provjerene.
Preostale stavke iz tabele „van numerisanih stavki" su svjesno odgođene ili djelimično realizovane i
**nisu prikazane kao završene**, u skladu sa zahtjevom da backlog pokazuje stvarno, a ne željeno
stanje.
