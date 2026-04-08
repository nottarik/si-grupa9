# User Stories

**Projekat:** Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra

---

## Upload i unos transkripata

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 1 |
| **Naziv** | Upload transkripata putem fajla |
| **Sprint** | 5 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Ubrzava unos podataka i smanjuje manuelni rad administratora |

**Uloga:**
Kao administrator, želim uploadati transkript razgovora iz fajla kako bih pohranio evidenciju razgovora u sistemu.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je fajl validnog formata (TXT, PDF). Otvoreno pitanje: Koji su maksimalni dozvoljeni formati i veličina fajla?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Pregled unesenih transkripata.

**Acceptance Criteria:**
- Kada administrator pristupi modulu za upload, tada sistem mora prikazati opciju za odabir fajla
- Kada administrator učita validan fajl, tada sistem mora pohraniti transkript i prikazati poruku o uspješnom uploadu
- Kada fajl nije validnog formata, tada sistem mora prikazati odgovarajuću poruku greške
- Sistem ne smije prikazati grešku pri uploadu validnog fajla

---

### User Story 2

| Polje | Vrijednost |
|---|---|
| **ID** | 2 |
| **Naziv** | Ručni unos transkripata |
| **Sprint** | 5 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava unos transkripata koji nisu dostupni u digitalnom formatu |

**Uloga:**
Kao administrator, želim ručno unijeti transkript razgovora putem forme kako bih pohranio razgovor koji nije bio digitalno snimljen.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da administrator ima pristup formi za unos. Otvoreno pitanje: Da li forma treba imati polja za strukturirani unos ili slobodan tekst?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Pregled unesenih transkripata.

**Acceptance Criteria:**
- Kada administrator otvori formu za ručni unos, tada sistem mora prikazati sva potrebna polja (datum, sadržaj razgovora, identifikator agenta)
- Kada administrator popuni sva obavezna polja i klikne 'Sačuvaj', tada sistem mora pohraniti transkript
- Kada polje ostane prazno, tada sistem mora vizualno označiti obavezna polja
- Sistem ne smije prikazati grešku prilikom unosa validnih podataka

---

### User Story 3

| Polje | Vrijednost |
|---|---|
| **ID** | 3 |
| **Naziv** | Validacija unesenih transkripata |
| **Sprint** | 5 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava integritet i konzistentnost podataka u bazi transkripata |

**Uloga:**
Kao administrator, želim da sistem provjeri ispravnost unesenih podataka kako bih spriječio pohranu nekompletnih ili nevalidnih transkripata.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su definisana validaciona pravila (obavezna polja, format datuma, minimalna dužina teksta).

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Upload transkripata putem fajla. Zavisi od Ručni unos transkripata.

**Acceptance Criteria:**
- Kada administrator pokuša pohraniti nepotpun transkript, tada sistem mora prikazati odgovarajuću poruku greške
- Sistem ne smije dozvoliti pohranivanje transkripata koji ne zadovoljavaju validaciona pravila
- Sistem mora jasno naznačiti koje polje sadrži grešku

---

### User Story 4

| Polje | Vrijednost |
|---|---|
| **ID** | 27 |
| **Naziv** | Konverzija audio zapisa u transkript |
| **Sprint** | 5 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Automatizuje proces pretvaranja snimljenih poziva u tekstualne transkripate, eliminišući potrebu za ručnim prepisivanjem |

**Uloga:**
Kao administrator, želim uploadati audio zapis poziva kako bi sistem automatski generisao transkript razgovora i pohranio ga u sistem.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su podržani uobičajeni audio formati (MP3, WAV). Otvorena pitanja: Koji su maksimalni dozvoljeni veličina i trajanje audio fajla? Da li sistem treba podržavati više govornika (diarizacija)? Da li se obrađuje samo bosanski/hrvatski/srpski jezik ili i ostali?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Pregled unesenih transkripata. Zavisi od Validacija unesenih transkripata.

**Acceptance Criteria:**
- Kada administrator pristupi modulu za upload, tada sistem mora prikazati opciju za odabir audio fajla
- Kada administrator učita validan audio fajl, tada sistem mora pokrenuti proces transkripcije i prikazati indikator napretka
- Kada transkripcija bude završena, tada sistem mora prikazati generisani transkript i omogućiti administratoru pregled i eventualne korekcije prije pohrane
- Kada administrator potvrdi transkript, tada sistem mora pohraniti transkript na isti način kao i ručno uneseni ili uploadani tekstualni transkript
- Kada audio fajl nije validnog formata ili je oštećen, tada sistem mora prikazati odgovarajuću poruku greške
- Sistem mora prikazati upozorenje ako je kvalitet audio zapisa prenizak za pouzdanu transkripciju
- Sistem ne smije pohraniti transkript bez eksplicitne potvrde administratora
- Sistem ne smije prikazati grešku pri obradi validnog audio fajla

---

## Pregled unesenih transkripata

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 4 |
| **Naziv** | Lista svih unesenih transkripata |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Daje administratoru centralizovan pregled svih pohranjenih transkripata |

**Uloga:**
Kao administrator, želim vidjeti listu svih unesenih transkripata kako bih imao pregled dostupnih podataka.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je barem jedan transkript pohranjen u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Upload i unos transkripata. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori modul za transkripate, tada sistem mora prikazati listu svih transkripata
- Kada ne postoji nijedan transkript, tada sistem mora prikazati poruku 'Nema unesenih transkripata'
- Sistem ne smije prikazati grešku prilikom učitavanja liste

---

### User Story 2

| Polje | Vrijednost |
|---|---|
| **ID** | 5 |
| **Naziv** | Detaljan pregled pojedinačnog transkripata |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava dublju analizu sadržaja konkretnog razgovora |

**Uloga:**
Kao administrator, želim otvoriti detalje pojedinog transkripata kako bih vidio kompletan zapis razgovora.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da transkript postoji u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih unesenih transkripata.

**Acceptance Criteria:**
- Kada administrator klikne na transkript iz liste, tada sistem mora prikazati kompletan sadržaj razgovora
- Prikaz mora sadržavati datum, identifikator agenta i sav sadržaj razgovora
- Sistem ne smije prikazati grešku prilikom učitavanja detalja

---

### User Story 3

| Polje | Vrijednost |
|---|---|
| **ID** | 6 |
| **Naziv** | Pretraga i filtriranje transkripata |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Smanjuje vrijeme pretrage i olakšava pronalazak relevantnih transkripata |

**Uloga:**
Kao administrator, želim pretraživati i filtrirati transkripate po ključnim riječima, datumu i agentu kako bih brzo pronašao relevantne zapise.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da transkripati postoje u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih unesenih transkripata.

**Acceptance Criteria:**
- Kada administrator unese ključnu riječ ili primijeni filter, tada sistem mora prikazati odgovarajuće transkripate
- Kada nema rezultata, tada sistem mora prikazati poruku 'Nema rezultata'
- Kada administrator resetuje filtere, tada sistem mora prikazati sve transkripate

---

## Pregled postavljenih pitanja i odgovora

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 7 |
| **Naziv** | Postavljanje pitanja chatbotu tekstom |
| **Sprint** | 5 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osnovna funkcionalnost — omogućava korisnicima da komuniciraju sa chatbotom |

**Uloga:**
Kao korisnik call centra, želim upisati pitanje chatbotu kako bih dobio odgovor na svoj upit.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je chatbot aktivan i dostupan.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Ocjena odgovora chatbota.

**Acceptance Criteria:**
- Kada korisnik otvori sučelje chatbota, tada sistem mora prikazati polje za unos pitanja
- Kada korisnik unese pitanje i potvrdi slanje, tada sistem mora prikazati odgovor chatbota
- Sistem ne smije prikazati grešku pri slanju validnog pitanja
- Sistem ne smije dozvoliti slanje praznog polja

---

### User Story 2

| Polje | Vrijednost |
|---|---|
| **ID** | 8 |
| **Naziv** | Detekcija i zamjena osjetljivih podataka (ime, telefon, JMBG) |
| **Sprint** | 5 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Štiti privatnost korisnika automatskim maskiranjem ličnih podataka prije obrade od strane chatbota |

**Uloga:**
Kao korisnik call centra, želim da sistem automatski detektuje i zamijeni moje osjetljive podatke (ime, telefon, JMBG) prije nego što se moj upit obradi, kako bi moja privatnost bila zaštićena.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su definisani obrasci za detekciju osjetljivih podataka (regex ili NLP model). Otvorena pitanja: Da li korisnik treba biti obaviješten o zamjeni podataka? Da li se original čuva ili trajno briše?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Postavljanje pitanja chatbotu tekstom.

**Acceptance Criteria:**
- Kada korisnik unese poruku koja sadrži ime, broj telefona ili JMBG, tada sistem mora detektovati i maskirati te podatke prije slanja chatbotu
- Sistem mora prikazati korisniku obavijest da su osjetljivi podaci zamijenjeni radi zaštite privatnosti
- Sistem mora podržati detekciju bh. formata JMBG (13 cifara), brojeva telefona i najčešćih obrazaca imena
- Zamjena se mora izvršiti transparentno — odgovor chatbota mora i dalje biti razumljiv korisniku
- Sistem ne smije slati originalne (nemaskirane) podatke chatbotu ili ih pohranjivati u logovima

---

### User Story 3

| Polje | Vrijednost |
|---|---|
| **ID** | 9 |
| **Naziv** | Postavljanje pitanja chatbotu glasovnim unosom (Dictate) |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Poboljšava dostupnost i brzinu unosa, posebno za korisnike koji preferiraju glasovnu interakciju |

**Uloga:**
Kao korisnik call centra, želim izgovoriti pitanje putem mikrofona kako bih komunikaciju s chatbotom učinio bržom i jednostavnijom.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da uređaj korisnika ima funkcionalan mikrofon i da su dodijeljene dozvole. Otvoreno pitanje: Da li sistem treba podržavati više jezika pri glasovnom unosu?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Postavljanje pitanja chatbotu tekstom.

**Acceptance Criteria:**
- Kada korisnik klikne na dugme za glasovni unos, tada sistem mora aktivirati prepoznavanje govora
- Kada korisnik završi govor, tada sistem mora pretvoriti govor u tekst i prikazati ga u polju za unos
- Kada korisnik potvrdi pitanje, tada sistem mora poslati pitanje chatbotu
- Sistem mora prikazati odgovarajuću poruku ako mikrofon nije dostupan
- Sistem ne smije prikazati grešku ako korisnik nije izgovorio ništa — umjesto toga mora ostati na čekanju

---

### User Story 4

| Polje | Vrijednost |
|---|---|
| **ID** | 10 |
| **Naziv** | Pregled istorije pitanja i odgovora — korisnički prikaz |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava korisnicima uvid u prethodne interakcije s chatbotom |

**Uloga:**
Kao korisnik call centra, želim pregledati historiju mojih pitanja i odgovora chatbota kako bih se mogao referirati na prethodne interakcije.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su prethodne interakcije sačuvane u sistemu. Otvoreno pitanje: Koliko dugo se čuva istorija razgovora?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Postavljanje pitanja chatbotu tekstom. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada korisnik otvori historiju, tada sistem mora prikazati listu prethodnih pitanja i odgovora hronološkim redoslijedom
- Svaki zapis mora sadržavati datum i vrijeme interakcije
- Kada nema istorije, tada sistem mora prikazati poruku 'Nema prethodnih razgovora'
- Sistem ne smije prikazati grešku prilikom učitavanja istorije

---

### User Story 5

| Polje | Vrijednost |
|---|---|
| **ID** | 11 |
| **Naziv** | Brisanje pitanja iz istorije — korisnički prikaz |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Daje korisnicima kontrolu nad vlastitom istorijom interakcija i podržava pravo na brisanje podataka |

**Uloga:**
Kao korisnik call centra, želim moći izbrisati jedno ili više svojih prethodnih pitanja iz historije kako bih upravljao vlastitim podacima.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da korisnik ima pristup historiji pitanja i odgovora. Otvoreno pitanje: Da li brisanje treba biti trajno ili je moguć oporavak u određenom roku?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Pregled istorije pitanja i odgovora — korisnički prikaz.

**Acceptance Criteria:**
- Kada korisnik otvori historiju, tada sistem mora prikazati opciju za brisanje uz svaki zapis
- Kada korisnik odabere brisanje, tada sistem mora zatražiti potvrdu prije trajnog brisanja
- Kada korisnik potvrdi brisanje, tada sistem mora ukloniti zapis iz historije i odmah ažurirati prikaz
- Sistem mora podržati brisanje više zapisa odjednom (bulk delete)
- Sistem ne smije prikazati grešku pri uspješnom brisanju

---

### User Story 6

| Polje | Vrijednost |
|---|---|
| **ID** | 12 |
| **Naziv** | Pregled svih pitanja i odgovora — administratorski prikaz |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Pruža administratoru uvid u česta pitanja i kvalitet odgovora radi unapređenja baze znanja |

**Uloga:**
Kao administrator, želim pregledati sva pitanja koja su korisnici postavili chatbotu, zajedno s odgovorima, kako bih identificirao najčešća pitanja i eventualne slabosti sistema.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su interakcije korisnika sačuvane i dostupne administratoru.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Zavisi od Postavljanje pitanja chatbotu tekstom.

**Acceptance Criteria:**
- Kada administrator otvori pregled, tada sistem mora prikazati sve zabilježene interakcije s pitanjima i odgovorima
- Administrator mora moći filtrirati prikaz po datumu, korisniku i ocjeni odgovora
- Sistem mora prikazati poruku 'Nema zabilježenih interakcija' ako je lista prazna
- Sistem ne smije prikazati grešku pri učitavanju liste

---

## Ocjena odgovora chatbota

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 13 |
| **Naziv** | Ocjena pojedinačnog odgovora |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava prikupljanje povratnih informacija o kvalitetu odgovora chatbota |

**Uloga:**
Kao korisnik call centra, želim ocijeniti odgovor koji mi je chatbot dao kako bih pomogao u poboljšanju kvaliteta usluge.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je korisnik postavio pitanje i dobio odgovor od chatbota. Otvoreno pitanje: Da li ocjena treba biti binarna (palac gore / palac dolje) ili numerička (1–5)?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Prijava netačnog odgovora.

**Acceptance Criteria:**
- Kada chatbot vrati odgovor, tada sistem mora prikazati opciju za ocjenu odgovora
- Kada korisnik odabere ocjenu, tada sistem mora sačuvati ocjenu i vezati je za konkretan odgovor
- Sistem ne smije dozvoliti slanje ocjene bez prethodno prikazanog odgovora
- Kada je ocjena uspješno sačuvana, tada sistem mora prikazati potvrdu korisniku

---

### User Story 2

| Polje | Vrijednost |
|---|---|
| **ID** | 14 |
| **Naziv** | Dodavanje opcionog komentara uz ocjenu |
| **Sprint** | 6 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Pruža dublji kontekst uz ocjenu i olakšava analizu slabih odgovora |

**Uloga:**
Kao korisnik call centra, želim uz ocjenu dodati kratak komentar kako bih preciznije obrazložio zašto odgovor nije bio zadovoljavajući.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da korisnik već ima mogućnost ocjenjivanja. Otvoreno pitanje: Da li je komentar obavezan samo uz negativnu ocjenu?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Ocjena pojedinačnog odgovora.

**Acceptance Criteria:**
- Kada korisnik odabere negativnu ocjenu, tada sistem mora prikazati opcionalno polje za komentar
- Kada korisnik unese komentar i potvrdi, tada sistem mora sačuvati komentar vezan za tu ocjenu
- Sistem ne smije dozvoliti unos praznog komentara ako je polje otvoreno
- Sistem ne smije prikazati grešku prilikom slanja komentara

---

### User Story 3

| Polje | Vrijednost |
|---|---|
| **ID** | 15 |
| **Naziv** | Pregled prosječne ocjene chatbota |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Daje administratoru uvid u ukupni kvalitet chatbota kroz agregirane metrike |

**Uloga:**
Kao administrator, želim vidjeti prosječnu ocjenu chatbota po vremenskom periodu kako bih pratio trendove kvaliteta.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoje sačuvane ocjene korisnika. Otvoreno pitanje: Koji vremenski period je podrazumijevani (sedmica, mjesec)?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Ocjena pojedinačnog odgovora. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori pregled ocjena, tada sistem mora prikazati prosječnu ocjenu za odabrani period
- Kada nema ocjena za odabrani period, tada sistem mora prikazati poruku 'Nema dostupnih ocjena'
- Sistem mora omogućiti filtriranje po vremenskom periodu
- Sistem ne smije prikazati grešku prilikom učitavanja statistike

---

## Prijava netačnog odgovora

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 16 |
| **Naziv** | Prijava netačnog odgovora chatbota |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava identifikaciju i korekciju slabih mjesta u bazi znanja chatbota |

**Uloga:**
Kao korisnik call centra, želim prijaviti netačan ili neprimjeren odgovor chatbota kako bih pomogao u poboljšanju sistema.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je korisnik dobio odgovor od chatbota. Otvoreno pitanje: Da li korisnik mora biti prijavljen da bi mogao prijaviti problem?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Ocjena pojedinačnog odgovora. Preduvjet za Pregled prijavljenih problema.

**Acceptance Criteria:**
- Kada korisnik odabere opciju 'Prijavi problem', tada sistem mora prikazati formu za prijavu
- Kada korisnik popuni formu i potvrdi slanje, tada sistem mora pohraniti prijavu i vezati je za konkretan odgovor chatbota
- Sistem mora prikazati potvrdu korisniku da je prijava uspješno poslana
- Sistem ne smije dozvoliti slanje prazne prijave

---

### User Story 2

| Polje | Vrijednost |
|---|---|
| **ID** | 17 |
| **Naziv** | Kategorizacija prijavljenog problema |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Olakšava analizu i prioritizaciju grešaka u odgovorima chatbota |

**Uloga:**
Kao korisnik call centra, želim odabrati vrstu greške pri prijavi problema kako bi administrator lakše razumio prirodu problema.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su kategorije grešaka unaprijed definisane (npr. netačna informacija, nerelevantni odgovor, tehnička greška).

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Prijava netačnog odgovora chatbota.

**Acceptance Criteria:**
- Kada korisnik otvori formu za prijavu, tada sistem mora prikazati listu kategorija grešaka
- Kada korisnik odabere kategoriju, tada sistem mora vezati tu kategoriju za prijavljeni problem
- Sistem ne smije dozvoliti slanje prijave bez odabrane kategorije

---

## Pregled prijavljenih problema

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 18 |
| **Naziv** | Lista svih prijavljenih problema |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Daje administratoru centralizovan pregled svih grešaka chatbota koje su korisnici prijavili |

**Uloga:**
Kao administrator, želim vidjeti listu svih prijavljenih problema kako bih imao pregled netačnih odgovora chatbota.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoji barem jedna prijavljena greška.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Prijava netačnog odgovora chatbota. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori modul za prijavljene probleme, tada sistem mora prikazati listu svih prijava
- Svaka prijava mora sadržavati: originalno pitanje, odgovor chatbota, kategoriju greške i datum prijave
- Kada nema prijavljenih problema, tada sistem mora prikazati poruku 'Nema prijavljenih problema'
- Sistem ne smije prikazati grešku pri učitavanju liste

---

### User Story 2

| Polje | Vrijednost |
|---|---|
| **ID** | 19 |
| **Naziv** | Detaljan pregled pojedinačne prijave |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava administratoru dubinsku analizu svake prijave radi korekcije baze znanja |

**Uloga:**
Kao administrator, želim otvoriti detalje pojedinačne prijave kako bih vidio sve informacije vezane za prijavljenu grešku.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da prijava postoji u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih prijavljenih problema.

**Acceptance Criteria:**
- Kada administrator klikne na prijavu iz liste, tada sistem mora prikazati sve detalje te prijave
- Prikaz mora sadržavati: pitanje korisnika, odgovor chatbota, kategoriju greške, komentar korisnika i datum
- Sistem ne smije prikazati grešku pri učitavanju detalja

---

### User Story 3

| Polje | Vrijednost |
|---|---|
| **ID** | 20 |
| **Naziv** | Promjena statusa prijave |
| **Sprint** | 8 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava praćenje procesa rješavanja prijavljenih grešaka |

**Uloga:**
Kao administrator, želim promijeniti status prijavljenog problema kako bih označio da je problem u obradi ili riješen.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su statusi prijave unaprijed definisani (npr. Nova, U obradi, Riješena).

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Detaljan pregled pojedinačne prijave.

**Acceptance Criteria:**
- Kada administrator otvori prijavu, tada sistem mora prikazati opciju za promjenu statusa
- Kada administrator promijeni status i potvrdi, tada sistem mora sačuvati promjenu i odmah je reflektovati u prikazu
- Sistem ne smije dozvoliti postavljanje nevalidnog statusa
- Sistem ne smije prikazati grešku pri promjeni statusa

---

### User Story 4

| Polje | Vrijednost |
|---|---|
| **ID** | 21 |
| **Naziv** | Filtriranje i pretraga prijavljenih problema |
| **Sprint** | 8 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Smanjuje vrijeme potrebno za pronalazak relevantnih prijava i prioritizaciju grešaka |

**Uloga:**
Kao administrator, želim filtrirati prijavljene probleme po statusu, kategoriji i datumu kako bih lakše upravljao prioritetima.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoje prijave s različitim statusima i kategorijama.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih prijavljenih problema.

**Acceptance Criteria:**
- Kada administrator odabere filter kriterij, tada sistem mora prikazati samo odgovarajuće prijave
- Kada nema rezultata za odabrane filtere, tada sistem mora prikazati poruku 'Nema rezultata'
- Kada administrator resetuje filtere, tada sistem mora prikazati sve prijave
- Sistem ne smije prikazati grešku pri primjeni filtera

---

## Odgovaranje na pitanja koje chatbot nije mogao riješiti

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 22 |
| **Naziv** | Pregled pitanja bez odgovora chatbota — agentski prikaz |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava agentu da identificira i preuzme pitanja na koja chatbot nije bio u stanju odgovoriti, smanjujući broj neuspješnih korisničkih interakcija |

**Uloga:**
Kao agent call centra, želim vidjeti listu pitanja na koja chatbot nije mogao odgovoriti kako bih mogao intervenirati i dati ispravan odgovor korisniku.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da sistem bilježi sve interakcije gdje chatbot nije pronašao odgovarajući odgovor. Otvoreno pitanje: Koji je kriterij za klasifikaciju odgovora kao 'nije mogao odgovoriti' (prazni odgovor, niska pouzdanost, eksplicitna oznaka)?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Zavisi od Postavljanje pitanja chatbotu tekstom.

**Acceptance Criteria:**
- Kada agent otvori modul za neodgovorena pitanja, tada sistem mora prikazati listu svih pitanja na koja chatbot nije dao odgovor
- Svaki zapis mora sadržavati: originalno pitanje korisnika, datum i vrijeme, te status (Čeka odgovor / Odgovoreno)
- Kada nema neodgovorenih pitanja, tada sistem mora prikazati poruku 'Nema pitanja koja čekaju odgovor'
- Sistem ne smije prikazati grešku pri učitavanju liste

---

### User Story 2

| Polje | Vrijednost |
|---|---|
| **ID** | 23 |
| **Naziv** | Unos agentovog odgovora na neodgovoreno pitanje |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava kontinuitet korisničke podrške kada chatbot ne može pružiti odgovor |

**Uloga:**
Kao agent call centra, želim unijeti odgovor na pitanje koje chatbot nije mogao riješiti kako bih korisniku pružio tačnu informaciju.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da agent ima uvid u pitanje i kontekst korisnika. Otvoreno pitanje: Da li agentov odgovor treba biti prikazan korisniku u realnom vremenu ili uz vremenski odmak?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Pregled pitanja bez odgovora chatbota — agentski prikaz.

**Acceptance Criteria:**
- Kada agent klikne na neodgovoreno pitanje, tada sistem mora prikazati detalje pitanja i polje za unos odgovora
- Kada agent unese odgovor i potvrdi slanje, tada sistem mora pohraniti odgovor i promijeniti status pitanja u 'Odgovoreno'
- Korisnik mora biti obaviješten da je agent odgovorio na njegovo pitanje
- Sistem ne smije dozvoliti slanje praznog odgovora
- Sistem ne smije prikazati grešku pri uspješnom slanju odgovora

---

### User Story 3

| Polje | Vrijednost |
|---|---|
| **ID** | 24 |
| **Naziv** | Upotreba agentovog odgovora za poboljšanje chatbota |
| **Sprint** | 8 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Kontinuirano unapređuje bazu znanja chatbota na osnovu stvarnih korisničkih pitanja i agentovih odgovora |

**Uloga:**
Kao administrator, želim da agentovi odgovori na neodgovorena pitanja budu iskorišteni za treniranje chatbota kako bih smanjio broj budućih neuspješnih interakcija.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoji mehanizam za označavanje odgovora kao pogodnih za uključivanje u bazu znanja. Otvoreno pitanje: Da li administrator treba ručno odobravati odgovore prije dodavanja u trening dataset?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Unos agentovog odgovora na neodgovoreno pitanje.

**Acceptance Criteria:**
- Kada agentov odgovor bude označen kao validan, tada sistem mora ponuditi opciju za dodavanje tog para (pitanje/odgovor) u bazu znanja za treniranje
- Administrator mora moći pregledati i odobriti ili odbaciti prijedloge za dodavanje u bazu znanja
- Sistem mora prikazati potvrdu kada je par uspješno dodan u trening dataset
- Sistem ne smije automatski dodavati odgovore u bazu znanja bez odobrenja

---

## Sign In

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 25 |
| **Naziv** | Prijava u sistem |
| **Sprint** | 4 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Prijava je preduvjet za sve ostale funkcionalnosti sistema |

**Uloga:**
Kao ovlašteni korisnik, želim unijeti svoje korisničke podatke kako bih pristupio funkcionalnostima prilagođenim mojoj ulozi.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da administrator unaprijed kreira korisničke račune i dodjeljuje uloge.

**Veze sa drugim storyjima ili zavisnostima:**
Preduvjet za sve ostale user storije.

**Acceptance Criteria:**
- Kada korisnik otvori aplikaciju, tada sistem mora prikazati stranicu za prijavu s poljima za e-mail i lozinku
- Kada korisnik unese ispravne podatke, tada sistem mora preusmjeriti korisnika na odgovarajući dashboard prema ulozi
- Kada korisnik unese neispravne podatke, tada sistem mora prikazati generičku poruku greške
- Sistem ne smije prikazati lozinku u čitljivom obliku
- Sistem ne smije dozvoliti direktan pristup zaštićenim stranicama bez prijave — korisnik mora biti preusmjeren na stranicu za prijavu

---

## Sign Out

### User Story 1

| Polje | Vrijednost |
|---|---|
| **ID** | 26 |
| **Naziv** | Odjava iz sistema |
| **Sprint** | 4 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Štiti osjetljive podatke call centra od neovlaštenog pristupa |

**Uloga:**
Kao prijavljeni korisnik, želim odjaviti se iz sistema kako bih zaštitio svoje podatke kada završim s radom.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je korisnik prethodno prijavljen. Otvoreno pitanje: Koliko dugo traje aktivna sesija prije automatske odjave?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In.

**Acceptance Criteria:**
- Kada je korisnik prijavljen, tada sistem mora prikazati vidljivu opciju Sign Out u navigaciji
- Kada korisnik klikne Sign Out, tada sistem mora prekinuti sesiju i preusmjeriti korisnika na stranicu za prijavu
- Kada se korisnik odjavi i pritisne dugme za povratak u pregledniku, tada sistem ne smije prikazati zaštićeni sadržaj
