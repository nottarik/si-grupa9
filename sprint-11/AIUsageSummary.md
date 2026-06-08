# Final AI Usage Summary

Završni sažetak korištenja AI alata na projektu. Cilj je **transparentno i kritičko** prikazivanje:
za šta je AI korišten, šta je prihvaćeno, izmijenjeno i odbačeno, koje greške je AI pravio, te koji
dijelovi sistema su razvijani uz AI pomoć i zahtijevaju posebno razumijevanje.

> Detaljni hronološki zapisi po sprintovima nalaze se u `sprint-5` … `sprint-10` (`AIUsageLog.md`,
> `DecisionLog.md`). Ovaj dokument je konsolidovani pregled.

---

## 1. Koji AI alat je korišten

**Claude Code** (Anthropic) — kroz cijeli razvoj, kao asistent pri implementaciji, refaktoringu,
pisanju testova, deployment konfiguraciji i dokumentaciji. AI nije korišten kao autonomni autor —
svaki prijedlog je tim pregledao, prilagodio projektu i selektivno prihvatao.

Pored toga, sistem **u runtime-u** koristi AI servise (Groq LLM i Whisper, sentence-transformers
embedding) kao dio same funkcionalnosti — to je opisano u `ArchitectureOverview.md` i razlikuje se od
korištenja AI-a u razvoju koje opisuje ovaj dokument.

---

## 2. Za šta je AI korišten (po oblastima)

| Oblast | Primjeri korištenja |
|---|---|
| Backend autentifikacija | Registracija/prijava, hashiranje lozinki, JWT, obrada grešaka |
| Frontend | Login/register forme, chat komponenta, dashboard, navigacija, prevodi, landing |
| API integracija | Organizacija Axios modula, error/loading stanja, povezivanje sa backendom |
| Transcript pipeline | Tok obrade, segmentacija, statusi, validacija formata |
| Preprocessing refaktoring | Razdvajanje monolita na module (`normalize`, `speakers`, `chunking`, `pii/*`, `audit`) |
| PII maskiranje | Regex/checksum za JMBG/telefon/email/IBAN/SSN, Fernet token mapa, no-leak garancije |
| LLM speaker labeling | Fallback labelovanje govornika uz strogi privacy boundary (samo maskirani tekst) |
| RAG logika | Retrieval prije generisanja, pragovi pouzdanosti, fallback, klasifikacija namjere |
| Baza znanja | CRUD, kuriranje, dedup, čišćenje PII placeholdera (LLM scrubber + regex safety net) |
| Eskalacija / WebSocket | Queue logika, ConnectionManager, real-time tokovi |
| Testiranje | Unit/integracijski testovi, fixture-i, mockovi za Groq, CI konfiguracija |
| DevOps / deployment | Docker optimizacija (CPU-only torch, cache), `azd`/Bicep, GitHub Actions |
| Dokumentacija | Sprint dokumenti, README, ovaj set završne dokumentacije |

---

## 3. Šta je tim prihvatio

- Osnovne obrasce implementacije (auth tok, RAG tok, pipeline orkestracija, WS ConnectionManager).
- Modularnu podjelu preprocessing-a sa jasnim odgovornostima i dataclass modelima.
- Sigurnosne principe: PII se maskira prije obrade; LLM uvijek prima samo maskirani tekst; Fernet enkripcija token mape; checksum za JMBG.
- Strukturu i obrazac testova (sekcije po modulu, fixture sa validnim PII, no-leak asercije, mock Groq).
- Docker/CI optimizacije (CPU-only torch layer, cache mount) i `azd`/Bicep single-click deployment.

## 4. Šta je tim izmijenio

- Nazive, strukturu i format usklađene sa postojećim modelima i konvencijama projekta.
- Validacije i poruke grešaka prilagođene pravilima projekta i **bosanskom jeziku**.
- Regex za telefon proširen na bosanske/regionalne formate; validaciju rola u LLM odgovorima.
- Pragove pouzdanosti i strukturu odgovora usklađene sa stvarnim ponašanjem i frontend prikazom.
- Pojednostavljene prijedloge koji su bili preopširni za stvarni obim sprinta.

## 5. Šta je tim odbacio

- Generičke dijelove koda koji nisu odgovarali postojećoj strukturi.
- Nepotrebne dodatne biblioteke (npr. **Presidio** za PII — pretežak za obim; korištena vlastita regex+checksum implementacija) i eksternu enkripcijsku uslugu (u korist lokalnog Fernet-a).
- Prekompleksan state management i suvišne UI efekte/animacije.
- Property-based testiranje (hypothesis) i testove koji zahtijevaju stvarni Groq API ključ.
- Apstrakcije/plugin arhitekture nepotrebne za trenutni obim; streaming LLM odgovore i keširanje gdje nisu potrebni.

---

## 6. Koje greške je AI pravio

- Generisao kod koji prolazi sintaksno, ali **ne provjerava stvarnu poslovnu logiku** (testovi koji „prolaze" bez vrijednosti) — tim je dorađivao asercije.
- Predlagao **previše generičke** strukture koje nisu odgovarale postojećem modelu baze/imenima.
- Uvodio **suvišne zavisnosti** i kompleksnost koja nije bila tražena.
- Povremeno predlagao rješenja koja **nisu uzimala u obzir stanje** (npr. reset transkripta bez provjere statusa).
- Sigurnosno „funkcionalan" kod koji **nije dovoljno siguran bez ručne provjere** (autentikacija, PII rubni slučajevi).
- Kod refaktoringa rizik da nenamjerno utiče na već funkcionalne dijelove — zahtijevalo ručnu regresijsku provjeru.

---

## 7. Koji dijelovi su razvijani uz AI pomoć i moraju se posebno znati objasniti

Tim je u stanju objasniti i odbraniti sve navedeno; sljedeći dijelovi su najosjetljiviji:

1. **PII maskiranje i token mapa** (`services/preprocessing/pii/`): JMBG checksum, konzistentni placeholderi, Fernet enkripcija, posljedica promjene `TOKEN_MAP_KEY`-a.
2. **RAG tok** (`services/ai/rag_service.py`): klasifikacija namjere, pragovi (`HIGH=0.5–0.55`, `LOW=0.35`, `OFFTOPIC=0.5`), query rewriting, kada se eskalira, kako se loguje anomalija.
3. **Privacy boundary prema LLM-u**: garancija da Groq prima isključivo maskirani tekst (transkripcija, speaker labeling, scrub).
4. **Čišćenje baze znanja** od PII placeholdera (LLM scrubber + deterministička regex sigurnosna mreža).
5. **Deployment kao kod** (`infra/main.bicep`, `azure.yaml`, `azure-dev.yml`): šta se provisionira, kako se injektuju secrets, zašto je 1 uvijek-topla replika, zašto se image buildi lokalno.
6. **Self-heal pri startu** (`app/main.py`): zašto postoji i koje stanje popravlja.

---

## 8. Kritički osvrt

AI je značajno ubrzao implementaciju rutinskih i ponavljajućih dijelova (CRUD, forme, testovi,
konfiguracija), ali je **svaki sigurnosno i poslovno osjetljiv dio zahtijevao ručnu provjeru i
doradu**. Najveća vrijednost ostvarena je tamo gdje je tim imao jasne kriterije ispravnosti (testovi,
privacy boundary, deployment provjere); najveći rizik bio je u prividno ispravnom kodu koji ne hvata
stvarnu logiku ili sigurnosne rubne slučajeve. Korištenje AI-a je bilo transparentno dokumentovano po
sprintovima i konsolidovano ovdje.
