# Test Summary / QA izvještaj

Završni izvještaj o testiranju sistema. Cilj je konkretno i provjerljivo pokazati šta je testirano,
kako se testovi pokreću i kakav je rezultat — ne samo tvrdnja da „sve radi".

---

## 1. Koje vrste testova postoje

| Vrsta | Alat | Šta pokriva | Zavisnosti |
|---|---|---|---|
| **Unit** | `pytest`, `pytest-asyncio` | Izolovana logika: PII pipeline/preprocessing, WebSocket `ConnectionManager`, eskalacijski servis | Nema baze/HTTP-a; potpuno offline |
| **Integracijsko (HTTP)** | `httpx.AsyncClient` + `ASGITransport` | API rute: auth, transkripti, korisnici, eskalacija, obavijesti, chat sesije, baza znanja | SQLite test baza (`sqlite+aiosqlite`) |
| **Integracijsko (DB pipeline)** | `pytest` + SQLite | End-to-end `run_pipeline()` nad test bazom (segmenti, Q&A, token mapa, no-PII-leak) | SQLite test baza |
| **WebSocket** | `starlette.testclient.TestClient` | Real-time tokovi korisnik/agent | In-process |
| **CI provjera** | GitHub Actions (`ci.yml`) | Pokreće cijeli `pytest` na svaki push/PR prema `main` | SQLite + dummy env |
| **Ručno (E2E/UI)** | Aplikacija u browseru | UI tokovi i infrastrukturne stavke (vidi sekciju 4) | Live/lokalni sistem |

> Frontend nema automatizovani test suite u CI-u; validira se ručno kroz aplikaciju i `npm run lint`
> (strict, max-warnings 0). Vidi `KnownIssues.md`.

---

## 2. Kako se testovi pokreću

```bash
cd projekat/backend

pytest -q                      # svih 223 testa
pytest -v                      # detaljan ispis
pytest tests/unit -v           # samo unit (offline)
pytest tests/integration -v    # samo integracijski (SQLite)
pytest tests/unit/test_preprocessing.py -v -k "scrub"   # ciljani podskup
```

U CI-u se isto pokreće automatski (`.github/workflows/ci.yml`) sa test env varijablama
(`DATABASE_URL=sqlite+aiosqlite:///./test.db`, `GROQ_API_KEY=test-key`, …).

---

## 3. Koliko testova prolazi

| | |
|---|---|
| Ukupno testova | **223** |
| Prošlo | **223** |
| Nije prošlo | 0 |
| Greške / upozorenja | 0 |
| Trajanje (puni suite) | ~62 s |

**Raspodjela po fajlovima:**

| Fajl | Testova | Tip |
|---|---|---|
| `tests/unit/test_connection_manager.py` | 19 | Unit |
| `tests/unit/test_escalation_service.py` | 29 | Unit |
| `tests/unit/test_preprocessing.py` | 42 | Unit |
| `tests/unit/test_pipeline_integration.py` | 1 | Integracijsko (DB) |
| `tests/integration/test_auth.py` | 13 | Integracijsko |
| `tests/integration/test_transcripts.py` | 15 | Integracijsko |
| `tests/integration/test_users.py` | 12 | Integracijsko |
| `tests/integration/test_escalation.py` | 27 | Integracijsko |
| `tests/integration/test_websocket.py` | 14 | Integracijsko |
| `tests/integration/test_announcements.py` | 12 | Integracijsko |
| `tests/integration/test_chat_sessions.py` | 24 | Integracijsko |
| `tests/integration/test_knowledge.py` | 15 | Integracijsko |
| **Ukupno** | **223** | |

---

## 4. Šta je ručno testirano (E2E / UI)

Funkcionalnosti koje su pretežno UI ili infrastrukturne validirane su ručno kroz aplikaciju; backend
tokovi koje koriste pokriveni su gornjim automatskim testovima.

| Tok | Provjereno | Rezultat |
|---|---|---|
| Prijava/odjava (sve uloge) | Login → role-based redirect; zaštićene rute | Prošlo |
| Chat → odgovor | Pitanje → RAG odgovor; napomena o nesigurnosti | Prošlo |
| Chat → eskalacija | Niska pouzdanost i eksplicitan zahtjev → red čekanja | Prošlo |
| Agent live chat | Accept → WS razgovor → Resolve | Prošlo |
| Upload transkripta (tekst/audio) | Audio preview → potvrda → pipeline + live status | Prošlo |
| Kuriranje baze znanja | Pending → Approve/Reject; ručni unos; dedup | Prošlo |
| Drive import / scheduled | Folder ID → obrada, preskakanje duplikata, status | Prošlo |
| Admin pregledi | Dashboard, Users, Ratings, Issues, Announcements, bulk delete | Prošlo |
| Cloud deployment | `azd up` / push na `main` → live frontend + `/health` OK | Prošlo |

---

## 5. Koji ključni korisnički tokovi su provjereni

- **Korisnik:** postavljanje pitanja, ocjena odgovora, eskalacija, historija, postavke naloga.
- **Agent:** preuzimanje eskalacije, live chat, KB lookup, resolve.
- **Admin:** upload i obrada transkripta, kuriranje baze znanja, upravljanje korisnicima/ocjenama/issues, obavijesti, scheduled import.
- **Sistem:** PII maskiranje (no-leak), privacy boundary prema LLM-u, self-heal pri startu, deployment + health provjera.

---

## 6. Poznati testni propusti / ograničenja testiranja

- **Frontend nema automatizovane testove u CI-u** — pokriven ručno + lint.
- **Integracijski testovi koriste SQLite**, ne PostgreSQL — rubni slučajevi specifični za Postgres nisu pokriveni automatski.
- **Vanjski servisi se mockuju** (Groq, Qdrant) — testovi potvrđuju logiku i privacy boundary na nivou koda, ne stvarno ponašanje produkcijskih servisa.
- **Nema mjerenja pokrivenosti (coverage %)** u CI izvještaju — pokrivenost se argumentuje brojem i obuhvatom testova po modulu.
- LLM/Whisper kvalitet (tačnost odgovora/transkripcije) nije automatski mjeren — validiran ručno kroz E2E.

---

## 7. Dokaz rezultata (pytest output)

Skraćeni ispis posljednjeg punog pokretanja (puni log dostupan pokretanjem `pytest -v` lokalno ili u
CI logovima):

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.2.0, pluggy-1.6.0
asyncio: mode=Mode.AUTO
collected 223 items

tests/unit/test_connection_manager.py ...................            [ 19]
tests/unit/test_escalation_service.py .............................  [ 48]
tests/unit/test_preprocessing.py ..........................................  [ 90]
tests/unit/test_pipeline_integration.py .                            [ 91]
tests/integration/test_auth.py .............                         [104]
tests/integration/test_transcripts.py ...............                [119]
tests/integration/test_users.py ............                         [131]
tests/integration/test_escalation.py ...........................     [158]
tests/integration/test_websocket.py ..............                   [172]
tests/integration/test_announcements.py ............                 [184]
tests/integration/test_chat_sessions.py ........................     [208]
tests/integration/test_knowledge.py ...............                  [223]

======================== 223 passed, 0 warnings in 61.78s ======================
```

> Dokaz je provjerljiv: `cd projekat/backend && pytest -v` reproducira ovaj rezultat; CI status je
> vidljiv u GitHub Actions (`CI` workflow) na svakom push-u prema `main`.

---

## 8. Zaključak

Svih **223 automatska testa prolaze bez grešaka**. Pokrivene su sve ključne backend domene
(autentikacija, transkripti, korisnici, eskalacija, obavijesti, chat sesije, baza znanja, WebSocket,
PII pipeline, end-to-end procesiranje). UI i infrastrukturne stavke validirane su ručno kroz E2E
tokove. Testiranje je konkretno povezano s funkcionalnostima i ponovljivo; poznata ograničenja
testiranja navedena su otvoreno u sekciji 6.
