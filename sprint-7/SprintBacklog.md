# Sprint Backlog – Sprint 7

## Opis sprinta

Sprint 7 fokusira se na implementaciju pipeline obrade transkripata i izgradnju baze znanja koja je temelj AI funkcionalnosti sistema. Uvodi se normalizacija teksta i razdvajanje po ulogama, maskiranje osjetljivih podataka, generisanje embeddinga i pohrana u vektorsku bazu s retrieval mehanizmom za semantičku pretragu. Pored toga, sprint uključuje upravljanje korisničkim nalogom (Account Settings) i prikaz statusa obrade transkripata u administratorskom UI-u.

Tokom ovog sprinta implementiraju se funkcionalnosti vezane za:

- normalizaciju teksta i razdvajanje transkripata po ulogama Agent/Korisnik
- maskiranje osjetljivih podataka (JMBG, telefon, ime) prije obrade
- generisanje embeddinga iz obrađenih transkripata i pohranu u vektorsku bazu (Qdrant)
- retrieval mehanizam za semantičku pretragu kao osnovu RAG sistema
- upravljanje korisničkim nalogom — promjena korisničkog imena, lozinke i profilnih podataka
- prikaz statusa obrade transkripata s evidencijom grešaka u administratorskom UI-u

---

## Pregled stavki sprinta

| ID | Naziv stavke | Kratak opis | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-------------|-----|-----------|-----------------|--------|
| PB-23 | Priprema za obradu transkripata | Normalizacija teksta i razdvajanje po ulogama | Technical Task | High | 13 | Završeno |
| PB-26 | Maskiranje osjetljivih podataka | Detekcija i zamjena ličnih podataka prije obrade | Technical Task | High | 5 | Završeno |
| PB-27 | Izgradnja baze znanja | Generisanje embeddinga, pohrana u vektorsku bazu i retrieval mehanizam (US-27.1, US-27.2, US-27.3) | Feature | High | 13 | Završeno |
| PB-45 | Account Settings | Upravljanje korisničkim nalogom — promjena korisničkog imena, lozinke i profilnih podataka (US-45.1, US-45.2, US-45.3) | Feature | Medium | 5 | Završeno |
| PB-46 | Prikaz statusa obrade transkripata | Prikaz statusa obrade i grešaka u administratorskom UI-u (US-46.1, US-46.2) | Feature | Medium | 5 | Završeno |

---

## Sprint Backlog stavke

---

### PB-23: Priprema za obradu transkripata

**Prioritet:** High

**Poslovna vrijednost:** Osigurava konzistentan i strukturiran format podataka kao preduvjet za ispravno generisanje embeddinga i rad cijelog AI pipeline-a.

**Pretpostavke:** Transkripti su prethodno uneseni u sistem. Format transkripata može biti nekonzistentan.

**Veze i zavisnosti:** Zavisi od PB-18 Upload i unos transkripata. Preduvjet za PB-26 Maskiranje osjetljivih podataka i PB-27 Izgradnja baze znanja.

---

#### US-23.1 — Normalizacija teksta transkripata

**Uloga:** Kao administrator, želim da sistem automatski normalizuje tekst transkripata kako bi podaci bili spremni za dalju obradu i pohranu.

**Acceptance Criteria:**

- Kada sistem primi transkript, tada mora ukloniti nepotrebne razmake i standardizovati tekst
- Sistem mora konvertovati tekst u definisani format (standardizovana kapitalizacija)
- Sistem mora ukloniti ili zamijeniti nevalidne znakove
- Sistem ne smije promijeniti semantičko značenje teksta

---

#### US-23.2 — Razdvajanje transkripta po ulogama (agent/korisnik)

**Uloga:** Kao administrator, želim da sistem automatski razdvoji transkript po ulogama (agent i korisnik) kako bi razgovor bio jasno strukturiran.

**Acceptance Criteria:**

- Kada sistem obradi transkript, tada mora identificirati govornike u razgovoru
- Sistem mora označiti svaki segment teksta odgovarajućom ulogom (agent ili korisnik)
- Kada oznake nisu jasno definisane, sistem mora pokušati inferirati uloge ili označiti segment kao nepoznat
- Sistem ne smije pogrešno dodijeliti uloge kada su oznake jasno definisane

---

### PB-26: Maskiranje osjetljivih podataka

**Prioritet:** High

**Poslovna vrijednost:** Štiti privatnost korisnika automatskim maskiranjem ličnih podataka prije obrade od strane chatbota, u skladu s propisima o zaštiti podataka.

**Pretpostavke:** Definirani su obrasci za detekciju osjetljivih podataka. Maskiranje se primjenjuje prije slanja podataka chatbotu.

**Veze i zavisnosti:** Zavisi od US-23.1 i US-23.2 Priprema za obradu transkripata. Zavisi od PB-22 Chat UI. Preduvjet za PB-27 Izgradnja baze znanja.

---

#### US-26.1 — Detekcija i zamjena osjetljivih podataka (ime, telefon, JMBG)

**Uloga:** Kao korisnik call centra, želim da sistem automatski detektuje i zamijeni moje osjetljive podatke (ime, telefon, JMBG) prije nego što se moj upit obradi, kako bi moja privatnost bila zaštićena.

**Acceptance Criteria:**

- Kada korisnik unese poruku koja sadrži ime, broj telefona ili JMBG, tada sistem mora detektovati i maskirati te podatke prije slanja chatbotu
- Sistem mora prikazati korisniku obavijest da su osjetljivi podaci zamijenjeni radi zaštite privatnosti
- Sistem mora podržati detekciju bh. formata JMBG (13 cifara), brojeva telefona i najčešćih obrazaca imena
- Zamjena se mora izvršiti transparentno — odgovor chatbota mora i dalje biti razumljiv korisniku
- Sistem ne smije slati originalne (nemaskirane) podatke chatbotu ili ih pohranjivati u logovima

---

### PB-27: Izgradnja baze znanja

**Prioritet:** High

**Poslovna vrijednost:** Gradi semantičku bazu znanja iz transkripata koja chatbotu omogućava pronalaženje relevantnih informacija i generisanje tačnih odgovora — ovo je centralna AI funkcionalnost cijelog sistema.

**Pretpostavke:** Transkripti su prethodno normalizovani i maskirani. Vektorska baza (Qdrant) je pokrenuta i dostupna.

**Veze i zavisnosti:** Zavisi od PB-23 Priprema za obradu transkripata. Zavisi od PB-26 Maskiranje osjetljivih podataka. Preduvjet za PB-46 Prikaz statusa obrade transkripata.

---

#### US-27.1 — Generisanje embeddinga iz transkripata

**Uloga:** Kao administrator, želim da sistem generiše embeddinge iz obrađenih transkripata kako bi chatbot mogao koristiti semantičku pretragu.

**Acceptance Criteria:**

- Kada sistem obradi transkript, tada mora generisati embeddinge za tekstualne segmente
- Sistem mora evidentirati greške tokom generisanja embeddinga
- Sistem ne smije preskočiti validne tekstualne segmente
- Generisani embedding mora biti povezan s odgovarajućim segmentom transkripata

---

#### US-27.2 — Pohrana embeddinga u vektorsku bazu

**Uloga:** Kao administrator, želim da sistem pohrani embeddinge u vektorsku bazu kako bi chatbot mogao koristiti relevantne informacije pri odgovaranju na pitanja.

**Acceptance Criteria:**

- Kada embedding bude generisan, tada sistem mora pohraniti embedding u vektorsku bazu
- Embedding mora biti povezan s originalnim transkriptom
- Sistem mora prikazati grešku ako pohrana nije uspješna
- Sistem ne smije pohraniti duplirane embeddinge za isti segment

---

#### US-27.3 — Retrieval mehanizam za semantičku pretragu

**Uloga:** Kao korisnik chatbot sistema, želim da sistem pronađe semantički relevantne informacije kako bih dobio tačne odgovore na svoja pitanja.

**Acceptance Criteria:**

- Kada korisnik pošalje pitanje, tada sistem mora izvršiti semantičku pretragu nad vektorskom bazom
- Upit se pretvara u embedding prije pretrage
- Sistem mora vratiti najrelevantnije rezultate rangirane po semantičkoj sličnosti
- Rezultati moraju biti proslijeđeni chatbotu za generisanje odgovora
- Sistem ne smije prikazati grešku pri uspješnoj pretrazi

---

### PB-45: Account Settings

**Prioritet:** Medium

**Poslovna vrijednost:** Omogućava korisnicima samostalno upravljanje podacima svog naloga bez potrebe za administratorskom intervencijom, što povećava sigurnost i autonomiju korisnika.

**Pretpostavke:** Korisnik mora biti prijavljen u sistem. Definisani su sigurnosni kriteriji za lozinku (minimum 8 znakova).

**Veze i zavisnosti:** Zavisi od PB-36 Sign In.

---

#### US-45.1 — Promjena korisničkog imena

**Uloga:** Kao registrovani korisnik, želim promijeniti svoje korisničko ime kako bih ažurirao podatke svog naloga.

**Acceptance Criteria:**

- Kada korisnik otvori Account Settings, tada sistem mora prikazati trenutno korisničko ime
- Kada korisnik unese novo korisničko ime i potvrdi izmjenu, tada sistem mora sačuvati izmjene
- Sistem ne smije dozvoliti unos već postojećeg korisničkog imena
- Nakon uspješne izmjene sistem mora prikazati potvrdu

---

#### US-45.2 — Promjena lozinke

**Uloga:** Kao registrovani korisnik, želim promijeniti svoju lozinku kako bih zaštitio svoj nalog.

**Acceptance Criteria:**

- Kada korisnik unese trenutnu i novu lozinku, tada sistem mora validirati podatke
- Nova lozinka mora zadovoljiti sigurnosna pravila (minimum 8 znakova)
- Kada trenutna lozinka nije ispravna, tada sistem mora prikazati poruku greške
- Nakon uspješne promjene sistem mora prikazati potvrdu
- Sistem ne smije prikazati lozinku u čitljivom obliku
- Sistem ne smije dozvoliti postavljanje iste lozinke kao prethodne

---

#### US-45.3 — Ažuriranje profilnih podataka

**Uloga:** Kao registrovani korisnik, želim ažurirati svoje profilne podatke kako bi moj nalog sadržavao tačne informacije.

**Acceptance Criteria:**

- Kada korisnik izmijeni profilne podatke, tada sistem mora sačuvati izmjene
- Sistem mora validirati obavezna polja — polja ne smiju biti prazna
- Nakon spremanja izmjene moraju odmah biti prikazane u profilu
- Sistem ne smije dozvoliti unos nevalidnog email formata

---

### PB-46: Prikaz statusa obrade transkripata

**Prioritet:** Medium

**Poslovna vrijednost:** Daje administratoru uvid u tok procesiranja podataka i omogućava pravovremenu reakciju na probleme u pipeline obradi, što osigurava stabilnost baze znanja.

**Pretpostavke:** Sistem vodi evidenciju statusa obrade svakog transkripata u bazi podataka. Pipeline obrada (PB-23, PB-26, PB-27) je implementirana.

**Veze i zavisnosti:** Zavisi od PB-18 Upload i unos transkripata. Zavisi od PB-23 Priprema za obradu transkripata. Zavisi od PB-27 Izgradnja baze znanja. Zavisi od PB-36 Sign In.

---

#### US-46.1 — Pregled statusa obrade transkripata

**Uloga:** Kao administrator, želim vidjeti status obrade transkripata kako bih mogao pratiti proces obrade podataka.

**Acceptance Criteria:**

- Sistem mora prikazati status svakog transkripata u administratorskom pregledu
- Status može biti: `Pending`, `Processing`, `Completed` ili `Failed`
- Sistem ne smije prikazati grešku pri učitavanju statusa
- Status mora biti vidljiv u administratorskom pregledu transkripata

---

#### US-46.2 — Prikaz grešaka pri obradi transkripata

**Uloga:** Kao administrator, želim vidjeti greške tokom obrade transkripata kako bih mogao reagovati na probleme.

**Acceptance Criteria:**

- Kada obrada ne uspije, tada sistem mora prikazati poruku greške sa statusom `Failed`
- Administrator mora moći identificirati problematični transkript
- Sistem mora evidentirati razlog greške
- Sistem ne smije prikazati tehničke detalje greške krajnjim korisnicima
