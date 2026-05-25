# Sprint Backlog — Sprint 9 

## Opis sprinta

Sprint 9 fokusira se na konsolidaciju sistema, poboljšanje kvaliteta podataka i isporuku završnih funkcionalnosti. Nakon što je Sprint 8 postavio end-to-end funkcionalan sistem, ovaj sprint ispravlja preostale tehničke nedostatke u obradi podataka, zaokružuje korisničko iskustvo kroz ocjenu razgovora i sistemske obavijesti, te uvodi upravljanje bazom znanja i optimizaciju performansi kao pripremu za produkcijsku isporuku.

Tokom ovog sprinta implementiraju se funkcionalnosti vezane za:

- poboljšanje maskiranja PII podataka — pokrivanje edge case formata JMBG-a i telefonskih brojeva koji nisu bili ispravno maskirani
- poboljšanje ekstrakcije Q&A parova iz transkripata — eliminacija pogrešno ekstrahiranih parova koji degradiraju bazu znanja
- ocjenu razgovora po završetku sesije — forma za numeričku ocjenu 1–5 umjesto thumbs-up/down po poruci
- sistemske obavijesti u chatbotu — baner koji administrator može aktivirati za obavještavanje korisnika
- ručni unos Q&A parova direktno u bazu znanja bez transkripata
- pregled, uklanjanje i kuriranje sadržaja baze znanja
- smanjenje latencije odgovora chatbota
- prikaz komentara uz ocjene razgovora u admin i agent panelu
- end-to-end i regresijsko testiranje sistema

---


## Pregled stavki sprinta

| ID | Naziv stavke | Kratak opis | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-------------|-----|-----------|-----------------|--------|
| PB-56 | Poboljšanje maskiranja PII podataka i ekstrakcije Q&A parova | Ispravka edge case formata maskiranja i poboljšanje ekstrakcije Q&A parova (US-56.1, US-56.2) | Bug Fix | High | 8 | Završeno |
| PB-57 | Ocjena razgovora po završetku sesije | Forma za numeričku ocjenu 1–5 prikazuje se korisniku na kraju chat sesije (US-57.1) | Feature | High | 5 | Završeno |
| PB-58 | Sistemske obavijesti u chatbotu | Administrator postavlja vidljivi baner s porukom koji se prikazuje pri otvaranju Chat UI-a (US-58.1) | Feature | Medium | 3 | Završeno |
| PB-59 | Mogućnost ručnog unosa Q&A para direktno u bazu znanja bez transkripata | Administrator direktno unosi validirane Q&A parove u bazu znanja (US-59.1) | Feature | High | 5 | Završeno |
| PB-60 | Pregled i kuriranje sadržaja baze znanja | Pregled, uklanjanje nevažećih unosa i odobravanje prijedloga za bazu znanja (US-60.1, US-60.2) | Feature | High | 8 | Završeno |
| PB-61 | Optimizacija performansi chatbota | Smanjenje latencije RAG upita ispod 3 s i LLM upita ispod 5 s (US-61.1) | Technical Task | High | 8 | Završeno |
| PB-62 | Prikaz komentara uz ocjene razgovora u admin i agent panelu | Admin vidi sve komentare uz ocjene, agent vidi samo komentare razgovora na koje je on odgovorio (US-62.1) | Feature | Medium | 5 | Završeno |
| PB-63 | End-to-end i regresijsko testiranje sistema | Pokrivenost testovima ≥ 80%, E2E testovi kritičnih putanja, regresijski testovi (US-63.1, US-63.2) | Technical Task | High | 13 | Završeno |
| PB-64 | User Settings | Promjena korisničkog imena, brisanje historije razgovora i brisanje naloga (US-64.1, US-64.2, US-64.3) | Feature | Medium | 5 | Završeno |
| PB-65 | Brisanje pojedinačnog chata iz historije | Korisnik može obrisati specifičan chat iz historije s potvrdom akcije (US-65.1) | Feature | Medium | 3 | Završeno |

---

## Sprint Backlog stavke

---

### PB-56 — Poboljšanje obrade podataka

#### User Story 56.1 — Poboljšanje maskiranja PII podataka

| Polje | Vrijednost |
|---|---|
| **ID** | 56.1 |
| **Naziv** | Poboljšanje maskiranja PII podataka |
| **Sprint** | 9 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava pouzdanu zaštitu privatnosti korisnika i sprečava curenje osjetljivih podataka u odgovorima chatbota |

**Uloga:**
Kao sistem, moram ispravno maskirati sve PII podatke (ime, telefon, JMBG) u svakom unosu kako bih garantovao zaštitu privatnosti bez izuzetaka.

**Pretpostavke i otvorena pitanja:**
Greške su identifikovane tokom testiranja: određeni formati JMBG-a i telefonskih brojeva nisu bili pokriveni regex patternima. Pretpostavlja se da je lista edge caseova dokumentovana.

**Veze sa drugim storyjima ili zavisnostima:**
Nadograđuje US-26.1 Detekcija i zamjena osjetljivih podataka. Preduvjet za pouzdan rad RAG pipeline-a.

**Acceptance Criteria:**
- Sistem mora maskirati JMBG u svim poznatim BH formatima (13 cifara, sa i bez razmaka/crtica)
- Sistem mora maskirati brojeve telefona u formatima: +387XXXXXXXX, 06XXXXXXXX, 065/XXX-XXX
- Sistem mora maskirati puna imena koja se pojavljuju u tekstu (ime + prezime u nizu)
- Nijedan testirani edge case s prethodnih sprintova ne smije proći bez maskiranja
- Sistem mora logirati svaki pokušaj maskiranja radi provjere
- Regresijski testovi za sve prethodno neispravno maskirane formate moraju biti zeleni

---

#### User Story 56.2 — Poboljšanje ekstrakcije Q&A parova iz transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 56.2 |
| **Naziv** | Poboljšanje ekstrakcije Q&A parova iz transkripata |
| **Sprint** | 9 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Poboljšava kvalitet baze znanja eliminacijom pogrešno ekstrahiranih parova koji degradiraju relevantnost odgovora chatbota |

**Uloga:**
Kao sistem, moram ispravno ekstrahovati Q&A parove iz transkripata kako bi baza znanja sadržavala smislene i korisne informacije.

**Pretpostavke i otvorena pitanja:**
Identifikovane greške: ekstrakcija krojih/nepotpunih parova, miješanje konteksta između segmenata, pogrešna dodjela govornika. Otvoreno pitanje: Da li minimalna dužina odgovora treba biti parametar konfiguracije?

**Veze sa drugim storyjima ili zavisnostima:**
Nadograđuje US-23.2 Razdvajanje transkripta po ulogama. Preduvjet za US-27.1 Generisanje embeddinga.

**Acceptance Criteria:**
- Svaki Q&A par mora sadržavati pitanje pripisano korisniku i odgovor pripisano agentu
- Par koji sadrži nepotpunu rečenicu (kraće od 10 znakova) ne smije biti pohranjen
- Susjedni segmenti istog govornika moraju biti spojeni u jedan segment prije ekstrakcije
- Sistem mora odbaciti parove gdje je pitanje ili odgovor samo whitespace ili interpunkcija
- Stopa ispravno ekstrahiranih parova na testnom skupu transkripata mora biti ≥ 90%
- Greške pri ekstrakciji moraju biti zabilježene u logu s identifikatorom transkripata

---

### PB-57 — Ocjena razgovora po završetku sesije

#### User Story 57.1 — Prikaz forme za ocjenu na kraju razgovora

| Polje | Vrijednost |
|---|---|
| **ID** | 57.1 |
| **Naziv** | Prikaz forme za ocjenu na kraju razgovora |
| **Sprint** | 9 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Prikuplja relevantnu i promišljenu povratnu informaciju umjesto impulsivnih reakcija po svakoj poruci, što daje tačniju sliku korisničkog iskustva |

**Uloga:**
Kao korisnik call centra, želim ocijeniti cijeli razgovor s chatbotom putem forme koja se pojavljuje na kraju sesije, a ne ocjenjivati svaku poruku posebno.

**Pretpostavke i otvorena pitanja:**
Forma se prikazuje kada korisnik zatvori chat ili klikne "Završi razgovor". Otvoreno pitanje: Da li se forma prikazuje i kod eskalacije na agenta? Skala ocjenjivanja: 1–5 zvjezdica ili numerička.

**Veze sa drugim storyjima ili zavisnostima:**
Zamjenjuje pristup thumbs-up/thumbs-down po poruci (US-15.1, US-15.2). Preduvjet za US-15.3 Pregled prosječne ocjene chatbota.

**Acceptance Criteria:**
- Kada korisnik završi razgovor ili zatvori chat, tada sistem mora prikazati formu za ocjenu sesije
- Forma mora sadržavati: numeričku ocjenu 1–5, opcionalno polje za komentar i dugme za potvrdu
- Forma se ne smije prikazivati ako razgovor nije sadržavao nijednu poruku korisnika
- Kada korisnik potvrdi ocjenu, tada sistem mora pohraniti ocjenu vezanu za tu chat sesiju
- Korisnik mora moći zatvoriti formu bez ocjenjivanja — sistem ne smije prisiljavati ocjenu
- Sistem ne smije prikazati formu više puta za isti razgovor
- Prethodni pristup (thumbs-up/down po poruci) mora biti uklonjen iz Chat UI-a

---

### PB-58 — Sistemske obavijesti u chatbotu

#### User Story 58.1 — Prikaz banera o poznatim problemima ili planiranom održavanju

| Polje | Vrijednost |
|---|---|
| **ID** | 58.1 |
| **Naziv** | Prikaz banera o poznatim problemima ili planiranom održavanju |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Proaktivno informiše korisnike o problemima u sistemu, smanjuje frustraciju i broj nepotrebnih eskalacija na agente |

**Uloga:**
Kao administrator, želim postaviti vidljivu obavijest na vrhu chatbota (npr. "Trenutno radimo na otklanjanju problema — molimo za strpljenje") kako bih pravovremeno informisao korisnike o poznatim poteškoćama.

**Pretpostavke i otvorena pitanja:**
Obavijest je opcionalna — prikazuje se samo kada je aktivirana od strane administratora. Otvoreno pitanje: Da li obavijest ima datum isteka ili administrator mora ručno deaktivirati?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Vezano za PB-22 Chat UI.

**Acceptance Criteria:**
- Administrator mora moći kreirati, izmijeniti i deaktivirati sistemsku obavijest iz admin panela
- Kada je obavijest aktivna, tada sistem mora prikazati baner s porukom na vrhu Chat UI-a pri svakom otvaranju chata
- Baner mora biti vizualno istaknut (npr. žuta/narandžasta boja) ali ne smije blokirati upotrebu chata
- Korisnik mora moći zatvoriti baner za trajanje sesije — pri sljedećem otvaranju chata baner se ponovo prikazuje dok je aktivan
- Kada obavijest nije aktivna, baner se ne smije prikazivati
- Sistem ne smije prikazati grešku pri učitavanju statusa obavijesti

---


### PB-59 — Mogućnost ručnog unosa Q&A para direktno u bazu znanja bez transkripata

#### User Story 59.1 — Ručni unos Q&A para direktno u bazu znanja bez transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 59.1 |
| **Naziv** | Ručni unos Q&A para direktno u bazu znanja bez transkripata |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava administratorima i agentima da odmah dodaju provjerene informacije u bazu znanja, bez potrebe za kreiranjem i obradom cijelog transkripata |

**Uloga:**
Kao administrator, želim direktno unijeti par pitanje/odgovor u bazu znanja kako bih brzo dodao validiranu informaciju koju chatbot može koristiti.

**Pretpostavke i otvorena pitanja:**
Unos se odmah uključuje u bazu znanja po odobrenju. Otvoreno pitanje: Da li ručno uneseni parovi imaju isti prioritet pri retrieval-u kao parovi izvučeni iz transkripata?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Preduvjet za US-60.2 Kontinuirano poboljšanje baze znanja.

**Acceptance Criteria:**
- Kada administrator otvori modul za bazu znanja, tada sistem mora prikazati opciju za ručni unos novog Q&A para
- Forma mora sadržavati: polje za pitanje, polje za odgovor i opcionalno polje za kategoriju
- Kada administrator unese validan par i potvrdi, tada sistem mora generisati embedding i pohraniti par u Qdrant
- Sistem mora odbiti unos ako je pitanje ili odgovor prazno ili kraće od 10 znakova
- Administrator mora moći pregledati, izmijeniti i obrisati ručno unesene parove
- Ručno uneseni parovi moraju biti jasno označeni kao "Ručni unos" u pregledu baze znanja
- Sistem mora prikazati potvrdu nakon uspješnog dodavanja para

---

### PB-60 — Upravljanje sadržajem baze znanja

#### User Story 60.1 — Pregled i uklanjanje nevažećih unosa iz baze znanja

| Polje | Vrijednost |
|---|---|
| **ID** | 60.1 |
| **Naziv** | Pregled i uklanjanje nevažećih unosa iz baze znanja |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava da baza znanja sadrži isključivo provjerene i relevantne informacije, čime se direktno poboljšava preciznost odgovora chatbota |

**Uloga:**
Kao administrator, želim pregledati sve unose u bazi znanja i ukloniti one koji su netačni, zastarjeli ili uneseni tokom testiranja kako bi chatbot korisnicima pružao isključivo tačne i validne informacije.

**Pretpostavke i otvorena pitanja:**
Uklanjanje unosa podrazumijeva brisanje iz PostgreSQL baze i iz Qdrant vektorske baze. Otvoreno pitanje: Da li je potrebna soft delete opcija s mogućnošću oporavka ili trajno uklanjanje?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Vezano za PB-27 Izgradnja baze znanja.

**Acceptance Criteria:**
- Administrator mora moći pregledati listu svih unosa u bazi znanja s prikazom pitanja, odgovora, izvora i datuma
- Administrator mora moći odabrati jedan ili više unosa za brisanje (bulk select)
- Kada administrator potvrdi brisanje, tada sistem mora ukloniti unos iz PostgreSQL i iz Qdrant vektorske baze
- Brisanje mora biti potvrđeno dijalogom kako bi se spriječilo slučajno uklanjanje podataka
- Sistem mora prikazati poruku potvrde s brojem obrisanih unosa
- Administrator mora imati opciju za pretragu i filtriranje unosa po ključnoj riječi, izvoru i datumu

---

#### User Story 60.2 — Kontinuirano poboljšanje baze znanja kroz kuriranje sadržaja

| Polje | Vrijednost |
|---|---|
| **ID** | 60.2 |
| **Naziv** | Kontinuirano poboljšanje baze znanja kroz kuriranje sadržaja |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava da baza znanja ostane ažurna, tačna i relevantna kroz kontinuirani proces pregleda i odobravanja sadržaja |

**Uloga:**
Kao administrator, želim imati centralizovani pregled prijedloga za dodavanje u bazu znanja (iz agentskih odgovora i ručnih unosa) kako bih mogao odobriti ili odbaciti svaki prijedlog prije nego što postane dio baze.

**Pretpostavke i otvorena pitanja:**
Prijedlozi dolaze iz: agentovih odgovora na neodgovorena pitanja (US-31.3) i ručnih unosa. Otvoreno pitanje: Da li se automatski generisani parovi iz transkripata također trebaju prolaziti kroz odobrenje?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-31.3 Upotreba agentovog odgovora za poboljšanje chatbota. Zavisi od US-59.1. Zavisi od Sign In.

**Acceptance Criteria:**
- Administrator mora imati pregled svih prijedloga na čekanju s datumom, izvorom i predloženim parom
- Kada administrator odobri prijedlog, tada sistem mora dodati par u aktivnu bazu znanja i generisati embedding
- Kada administrator odbaci prijedlog, tada sistem mora ukloniti prijedlog s jasnom oznakom "Odbačeno"
- Administrator mora moći izmijeniti sadržaj prijedloga prije odobravanja
- Sistem mora prikazati broj prijedloga na čekanju kao notifikaciju u admin panelu
- Sistem ne smije automatski dodavati sadržaj u bazu znanja bez administratorskog odobrenja

---

### PB-61 — Optimizacija performansi chatbota

#### User Story 61.1 — Smanjenje latencije odgovora chatbota

| Polje | Vrijednost |
|---|---|
| **ID** | 61.1 |
| **Naziv** | Smanjenje latencije odgovora chatbota |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Poboljšava korisničko iskustvo eliminacijom dugog čekanja na odgovor, što direktno povećava stepen zadovoljstva i korištenosti sistema |

**Uloga:**
Kao korisnik call centra, želim dobiti odgovor chatbota u razumnom roku (ispod 3 sekunde za tipičan upit) kako bih mogao efikasno koristiti sistem.

**Pretpostavke i otvorena pitanja:**
Trenutne bottleneck tačke: embedding generisanje pri queriju, Qdrant pretraga, Groq API latencija. Otvoreno pitanje: Da li uvesti streaming odgovora za duže generisane tekstove?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-27 Izgradnja baze znanja. Zavisi od PB-52 RAG retrieval i LLM klasifikacija.

**Acceptance Criteria:**
- Prosječno vrijeme odgovora za RAG upite mora biti ispod 3 sekunde od slanja poruke
- Prosječno vrijeme odgovora za LLM-only upite mora biti ispod 5 sekundi
- Sistem mora prikazati indikator učitavanja dok se odgovor generišta
- Embedding za upit mora biti keširan unutar sesije ako se isti upit ponovi
- Performanse moraju biti izmjerene i dokumentovane prije i nakon optimizacije
- Optimizacija ne smije narušiti tačnost ili relevantnost odgovora

---

### PB-62 — Prikaz komentara uz ocjene razgovora u admin i agent panelu

#### US-62.1 — Prikaz komentara uz ocjene razgovora

| Polje | Vrijednost |
|---|---|
| **ID** | 62.1 |
| **Naziv** | Prikaz komentara uz ocjene razgovora |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Daje administratorima i agentima uvid u tekstualne povratne informacije korisnika, što omogućava identifikaciju problema i kontinuirano poboljšanje kvaliteta usluge |


**Uloga:** Kao administrator, želim vidjeti sve komentare koje su korisnici ostavili uz ocjene razgovora, a kao agent, želim vidjeti samo komentare razgovora na koje sam ja odgovorio, kako bih mogao pratiti povratne informacije relevantne za moj rad.

**Pretpostavke:** Korisnici su u Sprintu 9 dobili mogućnost ostavljanja komentara uz ocjenu razgovora (US-57.1). Komentari su pohranjeni u bazi podataka i vezani za konkretnu chat sesiju i agenta koji je vodio razgovor.

**Veze i zavisnosti:** Zavisi od PB-57 Ocjena razgovora po završetku sesije. Zavisi od PB-36 Sign In. Zavisi od PB-51 Agent panel s Live Queue i pristupom bazi znanja.

**Acceptance Criteria:**

- Kada administrator otvori pregled ocjena razgovora, tada sistem mora prikazati sve komentare svih korisnika za sve razgovore
- Kada agent otvori pregled ocjena u svom panelu, tada sistem mora prikazati samo komentare vezane za razgovore na koje je taj agent odgovorio
- Agent ne smije vidjeti komentare razgovora koje su vodili drugi agenti
- Svaki komentar mora biti prikazan uz odgovarajuću numeričku ocjenu, datum razgovora i korisnika koji je ostavio ocjenu
- Kada razgovor nema komentar, sistem ne smije prikazati prazno polje — stavka bez komentara se prikazuje samo s ocjenom
- Sistem ne smije prikazati grešku pri učitavanju komentara

---


### PB-63 — End-to-end testiranje sistema

#### User Story 63.1 — Puno funkcionalno testiranje kritičnih putanja

| Polje | Vrijednost |
|---|---|
| **ID** | 63.1 |
| **Naziv** | Puno funkcionalno testiranje kritičnih putanja |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Garantuje stabilnost sistema pred produkciju, sprečava regresije i daje tim uvid u pokrivenost testovima |

**Uloga:**
Kao tim, želimo pokriti sve kritične putanje sistema automatizovanim i manuelnim testovima kako bismo pouzdano mogli isporučiti produkcijsku verziju.

**Pretpostavke i otvorena pitanja:**
Kritične putanje: prijava/odjava, upload transkripata + pipeline obrada, chat (RAG i LLM), eskalacija na agenta, ocjena razgovora, admin CRUD operacije. Otvoreno pitanje: Da li uvesti Playwright za E2E testove frontenda?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od svih prethodnih user storija. Preduvjet za produkcijsku isporuku.

**Acceptance Criteria:**
- Backend: pokrivenost unit testovima ≥ 80% za `services/ai/`, `services/pipeline/` i `api/v1/`
- Backend: integracijski testovi za sve API endpointe moraju biti zeleni (`pytest`)
- Frontend: manuelni test plan mora biti izveden za sve kritične putanje s dokumentovanim rezultatima
- RAG pipeline: end-to-end test koji prati transkript od uploada do chatbot odgovora mora biti uspješan
- Svi testovi moraju biti zeleni u CI/CD pipelinu na main grani
- Identifikovane greške moraju biti klasifikovane po prioritetu (Critical / High / Medium) i dokumentovane
- Rješavanje Critical i High grešaka je preduvjet za produkcijsku isporuku

---

#### User Story 63.2 — Regresijsko testiranje nakon ispravki grešaka

| Polje | Vrijednost |
|---|---|
| **ID** | 63.2 |
| **Naziv** | Regresijsko testiranje nakon ispravki grešaka |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Sprečava ponovnu pojavu već riješenih grešaka i osigurava da nove ispravke ne narušavaju postojeću funkcionalnost |

**Uloga:**
Kao tim, želimo imati skup regresijskih testova koji se automatski izvršavaju pri svakom push-u kako bismo bili sigurni da ispravka jedne greške ne uvodi novu.

**Pretpostavke i otvorena pitanja:**
Fokus na greškama ispravljenim u Sprintu 9 (masking edge caseovi, QA ekstrakcija). Pretpostavlja se da CI/CD pipeline (GitHub Actions) već postoji.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-56.1 i US-56.2 (bug fixovi). Zavisi od US-63.1.

**Acceptance Criteria:**
- Za svaku grešku ispravljenu u Sprintu 9 mora postojati minimalno jedan automatizovani regresijski test
- Regresijski testovi moraju biti uključeni u GitHub Actions workflow i izvršavati se pri svakom PR-u
- Neuspješan regresijski test mora blokirati merge PR-a
- Testovi moraju biti opisno nazvani prema grešci koju pokrivaju
- Svi regresijski testovi moraju biti zeleni na main grani prije produkcijskog deploya

---

### PB-64 — User Settings

**Prioritet:** Medium

**Poslovna vrijednost:** Daje korisniku autonomiju nad vlastitim nalogom i podacima — može ažurirati ime, obrisati historiju razgovora ili trajno ukloniti nalog, bez potrebe za kontaktiranjem administratora.

**Pretpostavke:** Korisnik je prijavljen u sistem. Brisanje naloga i historije su trajne akcije.

**Veze i zavisnosti:** Zavisi od Sign In (PB-36). Zavisi od PB-49 Historija razgovora korisnika.

---

#### US-64.1 — Promjena korisničkog imena iz User Settings

| Polje | Vrijednost |
|---|---|
| **ID** | 64.1 |
| **Naziv** | Promjena korisničkog imena iz User Settings |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava korisniku ažuriranje vlastitog profila bez administratorske intervencije |

**Uloga:**
Kao korisnik, želim promijeniti svoje korisničko ime iz User Settings menija kako bih ažurirao podatke svog naloga.

**Pretpostavke i otvorena pitanja:**
Korisnik pristupa User Settings klikom na avatar u gornjem desnom uglu. Otvoreno pitanje: Da li novo ime mora biti jedinstveno u sistemu?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36).

**Acceptance Criteria:**
- Kada korisnik otvori User Settings i klikne "Change name", tada sistem mora prikazati polje za unos novog imena
- Kada korisnik unese novo ime i potvrdi, tada sistem mora sačuvati promjenu i odmah je prikazati u UI-u
- Sistem ne smije dozvoliti spremanje praznog imena
- Nakon uspješne promjene sistem mora prikazati potvrdu

---

#### US-64.2 — Brisanje cijele historije razgovora

| Polje | Vrijednost |
|---|---|
| **ID** | 64.2 |
| **Naziv** | Brisanje cijele historije razgovora |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Daje korisniku kontrolu nad vlastitim podacima i privatnošću |

**Uloga:**
Kao korisnik, želim obrisati cijelu svoju historiju razgovora iz User Settings kako bih uklonio sve prethodne interakcije.

**Pretpostavke i otvorena pitanja:**
Brisanje historije je trajno i ne može se oporaviti.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-49 Historija razgovora korisnika.

**Acceptance Criteria:**
- Kada korisnik klikne "Delete all history", tada sistem mora prikazati dijalog za potvrdu akcije
- Kada korisnik potvrdi, tada sistem mora trajno obrisati sve razgovore vezane za taj nalog
- Nakon brisanja historija mora biti prazna s odgovarajućom porukom
- Sistem ne smije obrisati historiju bez eksplicitne potvrde korisnika

---

#### US-64.3 — Brisanje korisničkog naloga

| Polje | Vrijednost |
|---|---|
| **ID** | 64.3 |
| **Naziv** | Brisanje korisničkog naloga |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava korisniku trajno uklanjanje naloga i svih asociranih podataka |

**Uloga:**
Kao korisnik, želim trajno obrisati vlastiti nalog iz User Settings kako bih uklonio sve svoje podatke iz sistema.

**Pretpostavke i otvorena pitanja:**
Brisanje naloga je trajno. Otvoreno pitanje: Da li se brišu i svi razgovori tog korisnika ili ostaju u sistemu bez vlasnika?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Zavisi od US-64.2.

**Acceptance Criteria:**
- Kada korisnik klikne "Delete account", tada sistem mora prikazati dijalog za potvrdu s jasnim upozorenjem da je akcija trajna
- Kada korisnik potvrdi, tada sistem mora obrisati nalog, sve sesije i preusmjeriti korisnika na stranicu za prijavu
- Sistem ne smije dozvoliti brisanje naloga bez eksplicitne potvrde
- Nakon brisanja korisnik ne smije moći pristupiti sistemu s istim kredencijalima

---

### PB-65 — Brisanje pojedinačnog chata iz historije

**Prioritet:** Medium

**Poslovna vrijednost:** Korisnik može selektivno ukloniti određene razgovore iz historije bez brisanja svih podataka, što daje finiju kontrolu nad privatnošću.

**Pretpostavke:** Korisnik je prijavljen i ima barem jedan razgovor u historiji.

**Veze i zavisnosti:** Zavisi od PB-49 Historija razgovora korisnika. Zavisi od PB-36 Sign In.

---

#### US-65.1 — Brisanje pojedinačnog chata iz historije

| Polje | Vrijednost |
|---|---|
| **ID** | 65.1 |
| **Naziv** | Brisanje pojedinačnog chata iz historije |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Korisnik može selektivno ukloniti određene razgovore bez brisanja cijele historije |

**Uloga:**
Kao korisnik, želim obrisati specifičan chat iz historije razgovora kako bih uklonio samo određene interakcije koje više ne trebam.

**Pretpostavke i otvorena pitanja:**
Brisanje chata je trajno. Opcija "Delete chat" pojavljuje se na desni klik ili long press na chat u listi historije.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-49 Historija razgovora korisnika. Zavisi od US-64.2.

**Acceptance Criteria:**
- Kada korisnik desnim klikom (ili long press) odabere chat iz historije, tada sistem mora prikazati opciju "Delete chat"
- Kada korisnik klikne "Delete chat", tada sistem mora prikazati dijalog za potvrdu
- Kada korisnik potvrdi, tada sistem mora trajno obrisati taj razgovor i ukloniti ga iz liste historije
- Ostali razgovori moraju ostati nepromijenjeni
- Sistem ne smije obrisati chat bez eksplicitne potvrde korisnika
- Nakon brisanja sistem mora prikazati ažuriranu listu historije bez obrisanog chata

