# Known Issues / Limitations

Iskrena lista poznatih problema, ograničenja i pretpostavki sistema. Cilj nije prikriti nedostatke —
ova lista sama po sebi nije negativna. Problem bi bio **prikrivanje** ograničenja ili predstavljanje
nedovršenih funkcionalnosti kao završenih.

---

## 1. Poznati bugovi

| # | Problem | Uticaj | Status / ublažavanje |
|---|---|---|---|
| B1 | Klasifikacija namjere može pogrešno označiti rubni upit (kratak/dvosmislen) | Povremeno off-topic ili nepotrebna eskalacija | Ublaženo `RAG_OFFTOPIC_THRESHOLD` (0.5) + fallback na eskalaciju |
| B2 | LLM speaker labeling griješi na vrlo kratkim audio transkriptima | Pogrešno pripisana uloga u segmentu | Graceful fallback (prazan rezultat), ne ruši pipeline |
| B3 | PII regex može propustiti nestandardne formate | Rijedak rizik curenja nestandardnog PII | Checksum (JMBG) + prošireni regex; LLM scrubber + regex safety net na izlazu |
| B4 | Kratki prekidi Groq/Qdrant servisa | Privremeno više fallback/eskalacija odgovora | Retry pri startu (Qdrant), graceful degradacija; eskalacija na agenta |
| B5 | Lažno pozitivno maskiranje imena (npr. obična riječ kao `[PERSON_1]`) | Rijetko neprirodan tekst u izvoru | Ispravljano u Sprintu 10; scrubber čisti placeholdere iz baze znanja |

Nijedan poznati bug ne blokira osnovne korisničke tokove (chat, eskalacija, upload, kuriranje, deployment).

---

## 2. Tehnička ograničenja

- **Jedna uvijek-topla replika backenda** (`min=max=1`): nema horizontalnog skaliranja. In-process scheduler (Drive auto-import) ovisi o toj jednoj replici (namjerno — sprječava dvostruko okidanje).
- **Backend image se buildi lokalno** (Docker daemon obavezan) jer su ACR Tasks blokirani na free-trial pretplati („TasksOperationsNotAllowed").
- **Integracijski testovi koriste SQLite**, a produkcija PostgreSQL — rubni slučajevi specifični za Postgres nisu automatski pokriveni.
- **Embedding na CPU**: `all-MiniLM-L6-v2` se izvršava lokalno na CPU; veliki batch obrade je sporiji nego na GPU.
- **Asinhrona obrada preko FastAPI BackgroundTasks** (nema durable queue/Celery): ako se proces ugasi usred obrade, posao se ne nastavlja iz reda — oslanja se na **self-heal pri startu** (ponovna obrada zaglavljenih „Sirovih" transkripata + dovršavanje neembedovanih unosa).
- **Zavisnost o vanjskim free-tier servisima** (Groq, Qdrant Cloud, Supabase): njihovi rate/kvota limiti i dostupnost direktno utiču na sistem.
- **Frontend testovi nisu u CI-u**: validacija je ručna + `npm run lint`.

---

## 3. Sigurnosna ograničenja

- **`TOKEN_MAP_KEY` mora ostati nepromijenjen** kroz deployove — nova vrijednost čini ranije maskirane podatke nedekriptabilnim. Ako nije postavljen, koristi se efemerni ključ (samo dev — mape ne prežive restart).
- **PII zaštita je „best-effort"**: regex+checksum+NER smanjuju, ali ne garantuju 100% detekciju svih formata.
- **Prompt-injection zaštita je regex-zasnovana**: pokriva uobičajene obrasce, ali nije potpuna odbrana od svih napada.
- **Rotacija `SECRET_KEY`-a** odjavljuje sve korisnike (tokeni postaju nevažeći) — u Azure-u se generiše po deployu.
- **Demo nalozi** (`admin@test.com` itd.) imaju poznate lozinke — moraju se promijeniti prije stvarne upotrebe.
- **Redis (rate-limiting) nije aktivan na Azure produkciji** — nema distribuiranog rate-limita na nivou infrastrukture.

---

## 4. Nedovršene / djelimično završene funkcionalnosti

| Stavka | Status | Razlog |
|---|---|---|
| Automatizovani frontend test suite u CI | Not Done / Deferred | CI pokriva samo backend; frontend ručno + lint |
| Horizontalno autoscaliranje | Deferred | Free tier + in-process scheduler → 1 replika |
| Redis na Azure produkciji | Deferred | Nije provisioniran u Bicep-u; opciono |
| Poseban manager UI | Partially Done | Uloga postoji u RBAC-u; koristi preglede nivoa admina |
| Cloud (ACR Tasks) build | Deferred | Free-trial ograničenje |
| Mjerenje test coverage % u CI | Not Done | Pokrivenost argumentovana obuhvatom, ne brojkom |
| Višejezičnost van BS/EN | Not Done | Van opsega projekta |

---

## 5. Pretpostavke koje sistem pravi

- Tekstualni transkripti slijede format `Agent:` / `Korisnik:` (validacija prije obrade); jako nestandardni unosi mogu biti pogrešno segmentirani.
- Domena je telekom/ISP — pitanja van te domene se namjerno ne odgovaraju (poruka o opsegu).
- Korisnici i domenski sadržaj su pretežno na bosanskom; sistem razumije i engleski.
- Vanjski servisi (Groq/Qdrant/Supabase) su dostupni i konfigurisani ispravnim ključevima.
- Baza znanja je popunjena (uploadom/ručno/Drive importom) — prazna baza znači da gotovo sve eskalira.
- Jedna instanca backenda → nema potrebe za distribuiranom koordinacijom scheduler-a.

---

## 6. Dijelove sistema NE treba predstavljati kao potpuno završene

Radi poštene slike, sljedeće se **ne** smije predstavljati kao „gotovo i produkcijski očvrsnuto":

- **Skalabilnost i otpornost na opterećenje** — sistem je funkcionalno potpun, ali konfigurisan za demo/free-tier razmjeru (1 replika, bez autoscalinga, bez distribuiranog cache/queue).
- **Potpunost PII detekcije i prompt-injection odbrane** — robusno za uobičajene slučajeve, nije formalno verifikovano protiv svih napada/formata.
- **Frontend automatizovano testiranje** — pokriveno ručno, ne automatski.
- **Tačnost LLM odgovora/transkripcije** — zavisi od modela i baze znanja; nije formalno izmjerena metrikama.

---

## 7. Zaključak

Sistem je funkcionalno kompletan i deployovan, sa jasno navedenim operativnim i sigurnosnim
ograničenjima koja proizlaze pretežno iz **free-tier hosting konteksta** i svjesnih kompromisa obima.
Sva ograničenja iz ovog dokumenta konzistentna su sa `ReleaseNotes.md`, `ProductBacklog.md` i
`TestSummary.md`.
