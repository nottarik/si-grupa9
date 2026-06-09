# Final AI Usage Summary

Završni sažetak korištenja AI alata na projektu **Call Centar Chatbot**. Dokument je pripremljen kao
konsolidovani pregled najvažnijih informacija iz sprintova u kojima je vođen AI Usage Log, s fokusom na
ključne primjene AI alata, njihov stvarni doprinos projektu, odluke koje je tim prihvatio ili odbacio i
dijelove sistema koje tim mora posebno znati objasniti.

> Detaljni hronološki zapisi nalaze se u sprint dokumentima (`AIUsageLog.md` i `DecisionLog.md`).
> Ovaj dokument nije zamjena za hronološki log, nego završni sažetak najvažnijih obrazaca korištenja AI-ja.

---

## 1. Koji AI alat je korišten

Tokom razvoja korišten je **Claude Code** kao razvojni asistent za analizu problema, prijedloge
implementacije, refaktoring, testiranje, deployment dokumentaciju i završnu dokumentaciju.

AI nije korišten kao autonomni autor rješenja. Tim je svaki prijedlog pregledao, prilagodio stvarnoj
strukturi projekta, uskladio sa poslovnim pravilima i tek onda prihvatao u kod ili dokumentaciju.

Važno je razlikovati dvije vrste AI-ja u projektu:

| Vrsta AI-ja | Uloga |
|---|---|
| **AI kao razvojni alat** | Claude Code je pomagao timu pri implementaciji, testovima, refaktoringu i dokumentaciji. |
| **AI kao dio proizvoda** | Groq LLM, Groq Whisper i lokalni embedding modeli koriste se u runtime-u sistema za RAG odgovore, transkripciju i semantičku pretragu. |

---

## 2. Najvažnije korištenje AI-ja po sprintovima

| Sprint | Ključna upotreba AI alata | Doprinos projektu |
|---|---|---|
| **Sprint 5** | Auth, početni frontend, chat UI, osnovni transcript pipeline, baza znanja i prvi RAG tok | AI je ubrzao izgradnju MVP jezgra: login/register, API povezivanje, prvi chat tok i početna obrada transkripata. |
| **Sprint 6** | Stabilizacija uploada, validacija transkripata, dashboard, navigacija, report issues i testovi | AI je korišten za otklanjanje bugova, usklađivanje frontend/backend validacija i pripremu CI/test dokaza. |
| **Sprint 7** | Refaktoring preprocessing pipeline-a, PII maskiranje, Fernet token mapa, LLM speaker labeling, granularni testovi | AI je najviše doprinio modularizaciji obrade transkripata i sigurnosnom sloju, ali su svi PII edge caseovi ručno provjeravani. |
| **Sprint 8** | Audio transkripcija, glasovni unos, escalation queue, WebSocket live chat, agent panel | AI je pomogao u dizajnu real-time komunikacije, statusnog modela eskalacija i integracije agentskog toka sa historijom razgovora. |
| **Sprint 9** | Ocjene sesije, sistemske obavijesti, ručni unos i kuriranje KB-a, User Settings, performance optimizacije | AI je korišten za proširenje administrativnih i korisničkih tokova, ali su validacije, RBAC i destruktivne akcije dodatno ručno ograničene. |
| **Sprint 10** | Google Drive batch import, scheduled sync, live progress, Azure deployment, build optimizacija, dedup i korisničke greške | AI je pomogao u automatizaciji podataka, deployment proceduri i optimizaciji builda, posebno kod Docker cache-a i `azd` toka. |
| **Sprint 11** | Završna dokumentacija, konsolidacija AI Usage Summary-ja i odluka iz Decision Loga | AI je korišten za sažimanje i strukturiranje dokumentacije, ali sadržaj je vezan za stvarno implementirane funkcionalnosti. |

---

## 3. Ključne oblasti u kojima je AI najviše doprinio

### 3.1. Backend i API tokovi

AI je korišten za prijedloge strukture backend ruta, servisnih funkcija, Pydantic šema i obradu grešaka.
Najviše je pomogao kod autentifikacije, transkripata, baze znanja, chat sesija, ocjena, korisničkih
postavki i admin pregleda.

**Doprinos:** brže kreiranje ponavljajućih CRUD/API obrazaca, lakše uočavanje rubnih slučajeva i brža
standardizacija odgovora prema frontend-u.

### 3.2. Transcript pipeline i PII sigurnost

AI je korišten za refaktoring pipeline-a u module (`normalize`, `speakers`, `chunking`, `pii/*`, `audit`),
za prijedloge regex pravila, JMBG checksum validacije, Fernet enkripcije token mape i no-leak testova.

**Doprinos:** sistematski sigurnosni sloj koji smanjuje rizik curenja ličnih podataka u bazu znanja,
logove ili LLM pozive.

### 3.3. RAG i baza znanja

AI je pomogao pri definisanju retrieval toka, pragova pouzdanosti, fallback ponašanja, deduplikacije
unosa i pravila da je baza znanja autoritativan izvor čak i kada intent klasifikator pogriješi.

**Doprinos:** chatbot ne odgovara samo generativno, nego koristi relevantne KB unose, a kada nema dovoljno
siguran odgovor koristi fallback ili eskalaciju.

### 3.4. Eskalacije i WebSocket komunikacija

AI je korišten za dizajn statusnog modela eskalacije (`Cekanje`, `UToku`, `Rijesena`, `Napustena`),
`ConnectionManager` logiku, queue prikaz, agent locking, keepalive i replay evente.

**Doprinos:** korisnik može preći sa bota na živog agenta bez gubitka konteksta, a agent dobija radni
panel sa historijom razgovora i pristupom bazi znanja.

### 3.5. Testiranje i regresijska provjera

AI je korišten za generisanje prijedloga unit, integracijskih i regresijskih testova, uključujući mockove
za eksterne servise, testne fixture-e i edge caseove za PII i WebSocket.

**Doprinos:** brže pokrivanje kritičnih tokova, posebno onih gdje je ručno testiranje skupo ili sklono
greškama.

### 3.6. DevOps, deployment i build optimizacija

AI je pomogao u pripremi Docker optimizacija, `BuildKit` cache pristupa, CPU-only Torch instalacije,
single-click Azure deploymenta i dokumentacije za `azd up`.

**Doprinos:** build proces je značajno ubrzan, a deployment procedura postala ponovljiva i provjeriva.

---

## 4. Šta je tim prihvatio

Tim je prihvatio AI prijedloge kada su bili usklađeni sa stvarnim potrebama projekta:

- modularni preprocessing pipeline sa jasnim odgovornostima po modulu;
- RAG pristup uz Qdrant, lokalne embeddinge i Groq LLM;
- Groq Whisper za audio transkripciju i Web Speech API za glasovni unos;
- Fernet enkripciju PII token mape;
- privacy boundary: LLM ne prima nemaskirani tekst;
- WebSocket kao osnovu live komunikacije korisnika i agenta;
- statusni model eskalacija i agent locking;
- ručni i batch tok dodavanja Q&A parova u bazu znanja;
- deduplikaciju identičnih pitanja kroz sve ulaze u KB;
- korisnički razumljive poruke o greškama kroz centralni helper;
- Docker build optimizacije i Azure deployment dokumentaciju;
- strukturu završnih dokumenata za Sprint 11.

---

## 5. Šta je tim izmijenio

AI prijedlozi su skoro uvijek prilagođavani prije prihvatanja:

- nazivi modela, polja i funkcija usklađeni su sa postojećom bazom i API konvencijama;
- validacije su prilagođene stvarnim pravilima projekta i domeni call centra;
- poruke grešaka su preformulisane na korisnički razumljiv jezik;
- regex pravila su proširena za bosanske/regionalne formate telefona i JMBG-a;
- pragovi RAG sigurnosti i off-topic pretrage prilagođeni su kroz testiranje;
- UI prijedlozi su pojednostavljeni da odgovaraju postojećem dizajnu;
- generički deployment savjeti pretvoreni su u konkretne korake za Azure, Supabase, Qdrant i Groq;
- dokumentacija je skraćena i fokusirana na stvarno implementirane funkcionalnosti, bez predstavljanja planiranog kao završenog.

---

## 6. Šta je tim odbacio

Tim je odbacio prijedloge koji bi povećali kompleksnost bez stvarne koristi za MVP:

- potpuno oslanjanje na direktan LLM odgovor bez RAG konteksta;
- automatsko ubacivanje svih transkriptnih Q&A parova u aktivnu KB bez kontrole;
- Presidio kao težu PII zavisnost za trenutni obim projekta;
- eksternu enkripcijsku uslugu umjesto lokalnog Fernet pristupa;
- Celery/Redis worker kao obaveznu infrastrukturu u ranoj fazi;
- Redis pub/sub za WebSocket komunikaciju dok aplikacija radi na jednoj instanci;
- property-based testiranje i stvarne Groq/Qdrant pozive u CI testovima;
- prekompleksan frontend state management i suvišne UI animacije;
- prikaz tehničkih HTTP/axios grešaka krajnjem korisniku;
- dokumentovanje neimplementiranih funkcionalnosti kao da su završene.

---

## 7. Greške i rizici koje je AI pravio

AI je bio koristan, ali nije bio dovoljan bez ručne provjere. Uočeni su sljedeći rizici:

| Rizik / greška | Kako je tim reagovao |
|---|---|
| AI je predlagao testove koji prolaze sintaksno, ali ne provjeravaju stvarnu poslovnu logiku | Testovi su ručno dorađeni konkretnim asercijama i edge caseovima. |
| Generički kod nije uvijek odgovarao postojećim modelima i nazivima u projektu | Prijedlozi su prilagođeni stvarnoj strukturi repozitorija. |
| AI je ponekad uvodio nepotrebne biblioteke ili kompleksniju arhitekturu | Tim je birao jednostavnija rješenja pogodna za free-tier i MVP. |
| Sigurnosno osjetljive funkcije mogle su izgledati ispravno, ali bez dovoljne zaštite | PII, auth, RBAC i destructive actions su dodatno ručno pregledani. |
| AI je ponekad predlagao automatsko dodavanje sadržaja u KB bez kontrole kvaliteta | Uvedeno je kuriranje, izbor Q&A parova i deduplikacija. |
| Deployment savjeti su često bili generički | Pretvoreni su u konkretne komande, env varijable i ograničenja za ovaj projekat. |

---

## 8. Dijelovi sistema koje tim mora posebno znati objasniti

Zbog korištenja AI pomoći, tim mora posebno razumjeti i odbraniti sljedeće dijelove:

1. **RAG tok** — klasifikacija namjere, query rewrite, Qdrant retrieval, pragovi pouzdanosti, off-topic threshold i fallback/eskalacija.
2. **PII maskiranje** — regex/checksum/NER logika, token mapa, Fernet enkripcija i posljedice promjene `TOKEN_MAP_KEY`.
3. **Privacy boundary** — zašto LLM ne smije dobiti originalni tekst sa ličnim podacima.
4. **LLM speaker labeling** — kada se koristi, šta se šalje Groq-u i šta se dešava ako API padne.
5. **Knowledge base lifecycle** — ručni unos, batch import, kuriranje, deduplikacija, publish iz resolve toka i Qdrant sinhronizacija.
6. **Eskalacije i WebSocket** — queue, agent locking, keepalive, replay eventa i ograničenja jedne backend instance.
7. **Scheduled Google Drive sync** — razlika između manualnog i scheduled importa, live progress i rizik višestrukih replika.
8. **Deployment i build** — Azure `azd`, Bicep, GitHub Actions, Docker cache, CPU-only Torch i zašto prvi build može trajati duže.
9. **Korisnički razumljive greške** — centralni `readableError` i odnos između backend `detail` poruka i fallback tekstova.

---

## 9. Zaključak

AI alati su značajno ubrzali razvoj projekta, posebno kod ponavljajućih backend/frontend obrazaca,
testiranja, refaktoringa, deployment dokumentacije i završnog strukturiranja dokumenata. Najveću vrijednost
AI je imao kada je tim već imao jasne kriterije ispravnosti: sigurnost PII podataka, RAG fallback ponašanje,
statusi eskalacije, acceptance kriteriji i testni scenariji.

Najvažniji zaključak je da AI nije zamijenio inženjersku odgovornost tima. Svi sigurnosno, poslovno i
arhitekturno važni prijedlozi su pregledani, izmijenjeni ili odbijeni prije prihvatanja. Finalna verzija
projekta zato pokazuje transparentno, kritičko i kontrolisano korištenje AI alata.
