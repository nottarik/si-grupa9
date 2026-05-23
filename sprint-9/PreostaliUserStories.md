# Preostali User Stories — Sprint 9 i Sprint 10



## Pregled user storija

| ID | Naziv | Sprint | Prioritet | Poslovna vrijednost |
|----|-------|--------|-----------|---------------------|
| 56.1 | Poboljšanje maskiranja PII podataka | 9 | High | Osigurava pouzdanu zaštitu privatnosti korisnika i sprečava curenje osjetljivih podataka u odgovorima chatbota |
| 56.2 | Poboljšanje ekstrakcije Q&A parova iz transkripata | 9 | High | Poboljšava kvalitet baze znanja eliminacijom pogrešno ekstrahiranih parova koji degradiraju relevantnost odgovora chatbota |
| 57.1 | Prikaz forme za ocjenu na kraju razgovora | 9 | High | Prikuplja relevantnu i promišljenu povratnu informaciju umjesto impulsivnih reakcija po svakoj poruci |
| 58.1 | Prikaz banera o poznatim problemima ili planiranom održavanju | 9 | Medium | Proaktivno informiše korisnike o problemima, smanjuje frustraciju i broj nepotrebnih eskalacija |
| 59.1 | Ručni unos Q&A para direktno u bazu znanja bez transkripata | 10 | High | Omogućava administratorima da odmah dodaju provjerene informacije bez potrebe za kreiranjem cijelog transkripata |
| 60.1 | Pregled i uklanjanje nevažećih unosa iz baze znanja | 10 | High | Osigurava da baza znanja sadrži isključivo provjerene i relevantne informacije |
| 60.2 | Kontinuirano poboljšanje baze znanja kroz kuriranje sadržaja | 10 | High | Osigurava da baza znanja ostane ažurna, tačna i relevantna kroz kontinuirani proces pregleda |
| 61.1 | Smanjenje latencije odgovora chatbota | 10 | High | Poboljšava korisničko iskustvo eliminacijom dugog čekanja na odgovor |
| 62.1 | Poboljšanje vizualnog dizajna Chat UI-a | 10 | Medium | Profesionalniji i intuitivniji izgled povećava povjerenje korisnika u sistem |
| 62.2 | Poboljšanje dizajna Admin panela | 10 | Medium | Čistiji admin panel smanjuje kognitivno opterećenje administratora i ubrzava svakodnevne zadatke |
| 63.1 | Puno funkcionalno testiranje kritičnih putanja | 10 | High | Garantuje stabilnost sistema pred produkciju i sprečava regresije |
| 63.2 | Regresijsko testiranje nakon ispravki grešaka | 10 | High | Sprečava ponovnu pojavu već riješenih grešaka i osigurava da nove ispravke ne narušavaju postojeću funkcionalnost |

---

## Sprint 9

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

## Sprint 10

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

### PB-62 — Dizajn i UX poboljšanja

#### User Story 62.1 — Poboljšanje vizualnog dizajna Chat UI-a

| Polje | Vrijednost |
|---|---|
| **ID** | 62.1 |
| **Naziv** | Poboljšanje vizualnog dizajna Chat UI-a |
| **Sprint** | 10 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Profesionalniji i intuitivniji izgled povećava povjerenje korisnika u sistem i smanjuje krivulju učenja za nove korisnike |

**Uloga:**
Kao korisnik, želim koristiti chatbot koji ima pregledan, moderan i konzistentan dizajn kako bi moje iskustvo bilo ugodno i profesionalno.

**Pretpostavke i otvorena pitanja:**
Poboljšanja obuhvataju: Chat UI, Admin panel i stranica za prijavu. Otvoreno pitanje: Da li je definisan branding (logo, boje) koji treba biti primijenjen?

**Veze sa drugim storyjima ili zavisnostima:**
Vezano za PB-22 Chat UI. Zavisi od Sign In (PB-36).

**Acceptance Criteria:**
- Chat UI mora imati konzistentnu paletu boja i tipografiju kroz sve komponente
- Poruke korisnika i chatbota moraju biti vizualno jasno razlikovane (pozicija, boja mjehurića)
- Dugmad i interaktivni elementi moraju imati hover/active stanje i vidljive fokus indikatore
- Dizajn mora biti responzivan i upotrebljiv na mobilnim uređajima (minimalna širina 375px)
- Stranica za prijavu mora biti vizualno konzistentna s ostatkom aplikacije
- Sve izmjene moraju proći vizualnu provjeru na Chrome, Firefox i Edge

---

#### User Story 62.2 — Poboljšanje dizajna Admin panela

| Polje | Vrijednost |
|---|---|
| **ID** | 62.2 |
| **Naziv** | Poboljšanje dizajna Admin panela |
| **Sprint** | 10 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Čistiji admin panel smanjuje kognitivno opterećenje administratora i ubrzava svakodnevne zadatke upravljanja sistemom |

**Uloga:**
Kao administrator, želim da admin panel ima preglednu navigaciju i konzistentan vizualni jezik kako bih efikasno upravljao sistemom.

**Pretpostavke i otvorena pitanja:**
Fokus na: sidebar navigacija, tabele s podacima, forme za unos i status indikatori. Otvoreno pitanje: Da li uvesti dark mode?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-43 Dashboard s aktuelnim podacima. Zavisi od Sign In (PB-36).

**Acceptance Criteria:**
- Sidebar navigacija mora jasno prikazivati aktivnu sekciju i grupirati srodne stavke
- Tabele s podacima moraju imati konzistentan stil (zebra stripe, hover highlight, sortabilni naslovi)
- Forme za unos moraju imati jasne labele, placeholder tekstove i vizualne indikatore validacije
- Status badge-evi (Pending, Processing, Completed, Failed) moraju biti konzistentno obojeni kroz cijeli admin panel
- Dizajn mora biti konzistentan s Chat UI-em (iste boje, isti komponenti)

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
