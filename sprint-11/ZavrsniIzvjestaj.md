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

## 7. Glavne tehničke i organizacijske odluke

U nastavku su izdvojene najvažnije odluke iz Decision Log-a. Fokus je na odlukama koje su stvarno uticale
na arhitekturu, sigurnost, način rada tima, deployment i održavanje sistema.

| Oblast | Glavna odluka | Obrazloženje / uticaj na projekat |
|---|---|---|
| **Infrastruktura i baza** | Korišten je kombinovani free-tier/cloud pristup: Supabase PostgreSQL, Qdrant Cloud, Groq i Azure za finalni deployment. | Omogućeno je da tim razvije i demonstrira sistem bez čekanja na nedostupne Oracle instance, uz jasnu podjelu između relacione baze, vektorske baze i AI servisa. |
| **Relacijski podaci** | Supabase PostgreSQL je izabran za korisnike, transkripte, sesije, poruke, feedback, anomalije i bazu znanja. | PostgreSQL bolje odgovara modelu sa više povezanih entiteta od nerelacionih baza i olakšava timski rad kroz zajedničku cloud bazu. |
| **Vektorska pretraga** | Qdrant je izabran za RAG retrieval. | Odvaja semantičku pretragu od relacione baze i omogućava povezivanje pronađenog vektorskog rezultata sa konkretnim unosom baze znanja. |
| **AI arhitektura** | Odabran je RAG umjesto direktnog generativnog odgovaranja ili fine-tuninga. | Odgovori se zasnivaju na stvarnoj bazi znanja, mogu se povezati sa izvorom i ne zahtijevaju retreniranje modela pri svakoj izmjeni sadržaja. |
| **LLM i embedding** | Korišteni su lokalni embedding modeli, Groq LLM i Groq Whisper. | Lokalni embedding smanjuje troškove i zavisnost od eksternog API-ja, dok Groq omogućava brzo generisanje odgovora i transkripciju audio fajlova. |
| **Obrada transkripata** | Pipeline je razdvojen u module za normalizaciju, detekciju govornika, PII, chunking, audit i Q&A ekstrakciju. | Modularizacija je povećala testabilnost i smanjila rizik da promjena u jednom dijelu naruši cijeli tok obrade. |
| **PII sigurnost** | Uvedeno je maskiranje osjetljivih podataka i Fernet enkripcija token mape. | Lični podaci se ne čuvaju u čistom tekstu i ne šalju se LLM-u; reverzibilnost je moguća samo uz odgovarajući `TOKEN_MAP_KEY`. |
| **Privacy boundary** | LLM dobija samo maskirani tekst. | Odluka je ključna za sigurnost jer se eksternom AI servisu ne šalju originalni JMBG, telefon, email, IBAN ili drugi osjetljivi podaci. |
| **RAG ponašanje** | Knowledge base je autoritativan izvor, pa `out_of_scope` klasifikacija više ne prekida automatski retrieval. | Time je smanjen rizik da chatbot odbije odgovor iako KB sadrži relevantnu informaciju; prompt injection ostaje hard block. |
| **Eskalacije** | Uvedeni su eksplicitni statusi eskalacije i agent locking. | Sistem jasno razlikuje razgovore koji čekaju, koji su u toku, riješeni ili napušteni; tokom live sesije chatbot ne odgovara paralelno sa agentom. |
| **Real-time komunikacija** | WebSocket je odabran za komunikaciju korisnika i agenta, uz singleton `ConnectionManager`. | Omogućena je dvosmjerna live komunikacija bez reload-a stranice, ali je jasno dokumentovano ograničenje jedne backend instance. |
| **Agent/Admin organizacija** | Agent panel je odvojen od admin panela, uz role-based pristup. | Agenti vide samo relevantan queue i razgovore, dok admin zadržava širi pregled sistema, korisnika, transkripata, ocjena i baze znanja. |
| **Baza znanja** | Uveden je ručni unos, kuriranje, izbor Q&A parova pri resolve toku i sprečavanje duplikata kroz sve tokove. | KB ostaje kvalitetnija jer se ne dodaju identična pitanja, a zaposleni biraju koji odgovori stvarno vrijede za buduće korisnike. |
| **Automatizacija importa** | Google Drive batch import i scheduled sync koriste postojeći transcript pipeline. | Administrator može ručno ili zakazano pokretati obradu eksternih fajlova, a svi fajlovi prolaze isti tok transkripcije, čišćenja, Q&A ekstrakcije i KB ažuriranja. |
| **Live progress** | Pipeline prikazuje status importa i zadnji scheduled run. | Administrator vidi da se proces stvarno izvršava, koji se fajl obrađuje i kakav je bio rezultat posljednjeg zakazanog importa. |
| **Build i deployment** | Uveden je Azure `azd`/Bicep deployment i optimizovan Docker build kroz CPU-only Torch, BuildKit cache i pinovane dependency-je. | Deployment je ponovljiv i dokumentovan, a rebuild nakon inicijalnog cache-a je značajno brži jer se biblioteke ne skidaju svaki put. |
| **Korisničke greške** | Sve greške se prikazuju kroz korisnički razumljive poruke umjesto sirovih HTTP/axios poruka. | Krajnji korisnik, agent i admin dobijaju jasnu povratnu informaciju kada akcija ne uspije. |
| **Završna dokumentacija** | Sprint 11 je fokusiran na dokumentovanje stvarnog stanja projekta, a ne dodavanje velikog broja novih funkcionalnosti. | Pripremljeni dokumenti omogućavaju da druga osoba pokrene, testira, deploya, koristi i evaluira sistem bez neformalnih objašnjenja tima. |

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

Da se razvoj nastavlja nakon finalne isporuke, tim bi prioritet dao sljedećim unapređenjima:

1. **Poboljšati funkcionalnost prevođenja.**  
   Trenutni sistem je primarno prilagođen bosanskom i djelimično engleskom jeziku. Nastavak razvoja bi uključio
   kvalitetnije prevođenje UI tekstova, bolju podršku za više jezika u chat odgovorima i jasnije razdvajanje jezika
   korisničkog interfejsa od jezika baze znanja.

2. **Omogućiti unos `.zip` formata.**  
   Administrator bi mogao uploadovati jedan `.zip` fajl koji sadrži više transkripata, PDF dokumenata ili audio
   snimaka. Sistem bi raspakovao arhivu, validirao svaki fajl, prikazao rezultat po fajlu i obradio validne fajlove
   kroz postojeći pipeline.

3. **Dodati podršku za više tipova importa.**  
   Google Drive import je implementiran, ali bi sistem trebalo proširiti na druge izvore kao što su S3, Azure Blob
   Storage, OneDrive, SharePoint ili interni dokument-menadžment sistemi. Idealno rješenje bi bio generički
   `RemoteSource` interfejs sa adapterima po servisu.

4. **Uvesti robusniji job queue za pipeline.**  
   Scheduled import trenutno zavisi od backend instance i in-process scheduler-a. U nastavku bi bilo korisno preći na
   durable queue/worker arhitekturu (npr. Celery/RQ + Redis ili cloud-native queue) kako bi se lakše podržalo više
   replika, retry politika i bolji oporavak nakon pada procesa.

5. **Poboljšati semantičku deduplikaciju baze znanja.**  
   Trenutno se sprečavaju identična pitanja. Naredni korak bi bio prepoznavanje semantički istih pitanja napisanih
   drugačijim riječima, uz prijedlog administratoru da ažurira postojeći odgovor umjesto dodavanja novog unosa.

6. **Uvesti formalnu evaluaciju kvaliteta RAG-a.**  
   Tim bi pripremio ground-truth set pitanja i očekivanih odgovora, mjerio relevantnost retrieval-a, tačnost odgovora,
   stopu eskalacije i uticaj promjene pragova (`LOW`, `HIGH`, `OFFTOPIC`) na kvalitet sistema.

7. **Automatizovati frontend testove i mjerenje coverage-a.**  
   Backend testovi su pokriveni, ali bi frontend trebalo dodatno pokriti kroz Vitest/React Testing Library, posebno
   chat, admin panele, agent queue, upload/import tokove i destruktivne akcije.

8. **Ojačati monitoring, audit i sigurnost produkcije.**  
   Nastavak bi uključio detaljniji audit log, monitoring performansi, alerting, rate limiting, backup/restore
   procedure, politiku retencije podataka i jasniji pregled pristupa osjetljivim podacima.

9. **Razviti poseban Manager panel i finija RBAC prava.**  
   Manager uloga trenutno postoji, ali nema potpuno odvojen radni panel. U nastavku bi se mogla dodati analitika
   kvaliteta, pregled performansi agenata, trendovi ocjena, broj eskalacija i kontrolisani pristup sekcijama po
   pravima.

10. **Poboljšati UX za velike količine podataka.**  
    Kod većeg broja transkripata, KB unosa i chat logova trebalo bi dodati bolju paginaciju, napredne filtere,
    export izvještaja, bulk akcije sa potvrdom i pregled statusa velikih batch poslova po fajlu.

11. **Ukloniti lokalni Docker build kao preduvjet cloud deploymenta.**  
    Kada cloud pretplata dozvoli, image build treba prebaciti u cloud build pipeline kako bi deployment bio potpuno
    automatizovan bez lokalnog Docker Desktop preduvjeta.

12. **Dodatno unaprijediti mobilnu upotrebljivost.**  
    Admin i agent paneli su responzivni, ali bi nastavak razvoja mogao uključiti PWA pristup, bolje touch akcije,
    prilagođene bulk kontrole i optimizovan prikaz širokih tabela na manjim ekranima.

---

## 10. Zaključak

Projekat je isporučio funkcionalno kompletan, deployovan RAG chatbot za podršku call centru, sa punim
tokom od transkripta do odgovora, eskalacijom na agenta, administracijom i automatizacijom uvoza
podataka. Sistem je razvijan inkrementalno kroz 11 sprintova, sa transparentnim korištenjem AI alata i
jasno dokumentovanim ograničenjima. Uz pripadajuću dokumentaciju (deployment, CD pipeline, user manual,
arhitektura, QA, release notes, known issues), projekat se može **pokrenuti, deployati, koristiti,
testirati i evaluirati bez dodatnih neformalnih objašnjenja tima**.
