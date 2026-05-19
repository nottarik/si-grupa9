# User Stories

**Projekat:** Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra

---

> **Promjene**
> - Svaki user story je sada povezan sa odgovarajućom stavkom iz Product Backloga (PB).
> - Izvršena preraspodjela user stories po sprintovima.

---

## Sprint 5

---

### PB 18 — Upload i unos transkripata

#### User Story 18.1 — Upload transkripata putem fajla

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

#### User Story 18.2 — Ručni unos transkripata

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

#### User Story 18.3 — Validacija unesenih transkripata

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
Zavisi od Upload transkripata putem fajla (18.1). Zavisi od Ručni unos transkripata (18.2).

**Acceptance Criteria:**
- Kada administrator pokuša pohraniti nepotpun transkript, tada sistem mora prikazati odgovarajuću poruku greške
- Sistem ne smije dozvoliti pohranivanje transkripata koji ne zadovoljavaju validaciona pravila
- Sistem mora jasno naznačiti koje polje sadrži grešku

---

### PB 22 — Chat UI

#### User Story 22.1 — Postavljanje pitanja chatbotu tekstom

| Polje | Vrijednost |
|---|---|
| **ID** | 4 |
| **Naziv** | Postavljanje pitanja chatbotu tekstom |
| **Sprint** | 5 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osnovna funkcionalnost — omogućava korisnicima da komuniciraju sa chatbotom |

**Uloga:**
Kao korisnik call centra, želim upisati pitanje chatbotu kako bih dobio odgovor na svoj upit.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je chatbot aktivan i dostupan.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Ocjena odgovora chatbota (15.x).

**Acceptance Criteria:**
- Kada korisnik otvori sučelje chatbota, tada sistem mora prikazati polje za unos pitanja
- Kada korisnik unese pitanje i potvrdi slanje, tada sistem mora prikazati odgovor chatbota
- Sistem ne smije prikazati grešku pri slanju validnog pitanja
- Sistem ne smije dozvoliti slanje praznog polja

---

### PB 36 — Prijava u sistem

| Polje | Vrijednost |
|---|---|
| **ID** | 5 |
| **Naziv** | Prijava u sistem |
| **Sprint** | 5 |
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

### PB 37 — Odjava iz sistema

| Polje | Vrijednost |
|---|---|
| **ID** | 6 |
| **Naziv** | Odjava iz sistema |
| **Sprint** | 5 |
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

---

## Sprint 6

---

### PB 33 — Pregled unesenih transkripata

#### User Story 33.1 — Lista svih unesenih transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 7 |
| **Naziv** | Lista svih unesenih transkripata |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Daje administratoru centralizovan pregled svih pohranjenih transkripata |

**Uloga:**
Kao administrator, želim vidjeti listu svih unesenih transkripata kako bih imao pregled dostupnih podataka.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je barem jedan transkript pohranjen u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Upload i unos transkripata (18.x). Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori modul za transkripate, tada sistem mora prikazati listu svih transkripata
- Kada ne postoji nijedan transkript, tada sistem mora prikazati poruku 'Nema unesenih transkripata'
- Sistem ne smije prikazati grešku prilikom učitavanja liste

---

#### User Story 33.2 — Detaljan pregled pojedinačnog transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 8 |
| **Naziv** | Detaljan pregled pojedinačnog transkripata |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava dublju analizu sadržaja konkretnog razgovora |

**Uloga:**
Kao administrator, želim otvoriti detalje pojedinog transkripata kako bih vidio kompletan zapis razgovora.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da transkript postoji u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih unesenih transkripata (33.1).

**Acceptance Criteria:**
- Kada administrator klikne na transkript iz liste, tada sistem mora prikazati kompletan sadržaj razgovora
- Prikaz mora sadržavati datum, identifikator agenta i sav sadržaj razgovora
- Sistem ne smije prikazati grešku prilikom učitavanja detalja

### PB-38 — Uređivanje postojećih transkripata

#### User Story 38.1 — Uređivanje sadržaja transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 38.1 |
| **Naziv** | Uređivanje sadržaja transkripata |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava ispravku grešaka u unesenim transkriptima bez potrebe za ponovnim uploadom |

**Uloga:**
Kao administrator, želim urediti sadržaj postojećeg transkripata kako bih ispravio greške nastale pri unosu.

**Pretpostavke i otvorena pitanja:**
Transkript mora postojati u sistemu. Samo administrator i agent imaju pravo uređivanja.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-33.1 Lista svih unesenih transkripata. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori detalje transkripata, tada sistem mora prikazati opciju za uređivanje
- Kada administrator klikne "Uredi", tada sistem mora otvoriti formu s prethodno unesenim podacima
- Kada administrator spremi izmjene, tada sistem mora pohraniti ažurirani transkript i prikazati potvrdu
- Sistem ne smije izgubiti originalni sadržaj ako administrator odustane od uređivanja
- Sistem ne smije dozvoliti spremanje praznog sadržaja transkripata

---

#### User Story 38.2 — Uređivanje metapodataka transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 38.2 |
| **Naziv** | Uređivanje metapodataka transkripata |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava tačnost evidencije transkripata bez potrebe za brisanjem i ponovnim unosom |

**Uloga:**
Kao administrator, želim ažurirati metapodatke transkripata (datum, identifikator agenta) kako bi evidencija bila tačna.

**Pretpostavke i otvorena pitanja:**
Format datuma mora biti konzistentan s ostatkom sistema.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-33.1. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator uredi metapodatke i spremi, tada sistem mora pohraniti izmjene i odmah ih reflektovati u listi
- Sistem mora validirati metapodatke pri uređivanju (format datuma, neprazni identifikator agenta)
- Sistem ne smije prikazati grešku pri ispravnom unosu metapodataka

---

### PB-39 — Brisanje transkripata s potvrdom akcije

#### User Story 39.1 — Brisanje pojedinačnog transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 39.1 |
| **Naziv** | Brisanje pojedinačnog transkripata |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava uklanjanje netačnih ili zastarjelih transkripata uz zaštitu od slučajnog brisanja |

**Uloga:**
Kao administrator, želim obrisati transkript iz sistema kako bih uklonio netačne ili zastarjele podatke.

**Pretpostavke i otvorena pitanja:**
Brisanje je trajno i ne može se oporaviti. Otvoreno pitanje: Da li brisanje treba kaskadirati na Q&A parove izvučene iz tog transkripata?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-33.1 Lista svih unesenih transkripata. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator odabere opciju brisanja, tada sistem mora prikazati dijalog za potvrdu akcije
- Kada administrator potvrdi brisanje, tada sistem mora trajno ukloniti transkript i ažurirati listu
- Kada administrator odustane od brisanja, tada sistem mora zatvoriti dijalog bez ikakve izmjene
- Sistem ne smije dozvoliti brisanje bez eksplicitne potvrde korisnika
- Nakon uspješnog brisanja sistem mora prikazati odgovarajuću poruku potvrde

---

### PB-40 — Filtriranje i pretraga transkripata

#### User Story 40.1 — Pretraga transkripata po ključnoj riječi

| Polje | Vrijednost |
|---|---|
| **ID** | 40.1 |
| **Naziv** | Pretraga transkripata po ključnoj riječi |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Smanjuje vrijeme pronalaska relevantnih transkripata u sistemu s velikim brojem zapisa |

**Uloga:**
Kao administrator, želim pretraživati transkripate po ključnoj riječi kako bih pronašao specifične razgovore.

**Pretpostavke i otvorena pitanja:**
Pretraga se vrši po sadržaju i nazivu transkripata.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-33.1 Lista svih unesenih transkripata.

**Acceptance Criteria:**
- Kada administrator unese ključnu riječ u polje za pretragu, tada sistem mora prikazati transkripate čiji sadržaj ili naziv odgovara unesenoj riječi
- Kada nema rezultata, tada sistem mora prikazati poruku "Nema rezultata za uneseni pojam"
- Kada administrator obriše ključnu riječ, tada sistem mora prikazati kompletnu listu transkripata

---

#### User Story 40.2 — Filtriranje transkripata po datumu i agentu

| Polje | Vrijednost |
|---|---|
| **ID** | 40.2 |
| **Naziv** | Filtriranje transkripata po datumu i agentu |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava brzu navigaciju kroz transkripate prema vremenskom periodu ili konkretnom agentu |

**Uloga:**
Kao administrator, želim filtrirati transkripate po datumu i identifikatoru agenta kako bih brzo pronašao relevantne zapise.

**Pretpostavke i otvorena pitanja:**
Filter po datumu podržava odabir raspona (od–do). Filter po agentu podržava parcijalni unos.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-33.1. Zavisi od US-40.1.

**Acceptance Criteria:**
- Kada administrator primijeni filter po datumu, tada sistem mora prikazati samo transkripate unutar odabranog vremenskog perioda
- Kada administrator primijeni filter po agentu, tada sistem mora prikazati samo transkripate tog agenta
- Kada administrator resetuje filtere, tada sistem mora prikazati sve transkripate
- Sistem ne smije prikazati grešku pri primjeni filtera

---

### PB-41 — Dodjela i upravljanje ulogama korisnika

#### User Story 41.1 — Dodjela uloge korisniku

| Polje | Vrijednost |
|---|---|
| **ID** | 41.1 |
| **Naziv** | Dodjela uloge korisniku |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava da korisnici imaju pristup isključivo funkcionalnostima koje odgovaraju njihovoj ulozi |

**Uloga:**
Kao administrator, želim dodijeliti ulogu korisniku kako bi korisnik imao odgovarajući nivo pristupa sistemu.

**Pretpostavke i otvorena pitanja:**
Dostupne uloge: Administrator, Supervizor, CallCentarAgent, KrajnjiKorisnik.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-42.1 Pregled liste svih korisnika. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori profil korisnika, tada sistem mora prikazati trenutnu ulogu i opciju za izmjenu
- Kada administrator odabere novu ulogu i potvrdi, tada sistem mora odmah primijeniti promjenu
- Sistem mora prikazati poruku potvrde nakon uspješne dodjele uloge
- Sistem ne smije dozvoliti postavljanje nepostojeće uloge

---

#### User Story 41.2 — Izmjena postojeće uloge korisnika

| Polje | Vrijednost |
|---|---|
| **ID** | 41.2 |
| **Naziv** | Izmjena postojeće uloge korisnika |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava da promjena radnih odgovornosti bude odmah reflektovana u sistemu |

**Uloga:**
Kao administrator, želim promijeniti ulogu korisnika kada se promijene njegove radne odgovornosti.

**Pretpostavke i otvorena pitanja:**
Promjena uloge stupa na snagu odmah. Otvoreno pitanje: Da li korisnik treba dobiti obavijest o promjeni uloge?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-41.1. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator promijeni ulogu, tada sistem mora odmah ažurirati pristup tog korisnika u skladu s novom ulogom
- Ako je korisnik trenutno prijavljen, tada mora biti preusmjeren na prijavu pri narednoj akciji koja zahtijeva staru ulogu
- Sistem mora evidentirati promjenu uloge s datumom i identifikatorom administratora koji je napravio izmjenu

---

### PB-42 — Pregled i brisanje korisnika

#### User Story 42.1 — Pregled liste svih korisnika

| Polje | Vrijednost |
|---|---|
| **ID** | 42.1 |
| **Naziv** | Pregled liste svih korisnika |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Daje administratoru centralizovan pregled svih naloga u sistemu |

**Uloga:**
Kao administrator, želim pregledati listu svih registrovanih korisnika kako bih imao pregled naloga u sistemu.

**Pretpostavke i otvorena pitanja:**
Administrator mora biti prijavljen.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za US-41.1 i US-42.2.

**Acceptance Criteria:**
- Kada administrator otvori modul za korisnike, tada sistem mora prikazati listu svih registrovanih korisnika
- Svaki red mora prikazivati ime, prezime, email, ulogu i datum kreiranja naloga
- Kada nema registrovanih korisnika, tada sistem mora prikazati poruku "Nema registrovanih korisnika"
- Sistem ne smije prikazati grešku prilikom učitavanja liste

---

#### User Story 42.2 — Brisanje korisničkog naloga

| Polje | Vrijednost |
|---|---|
| **ID** | 42.2 |
| **Naziv** | Brisanje korisničkog naloga |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava administratoru uklanjanje neaktivnih ili neovlaštenih korisnika |

**Uloga:**
Kao administrator, želim obrisati korisnički nalog kako bih uklonio neaktivne ili neovlaštene korisnike.

**Pretpostavke i otvorena pitanja:**
Brisanje je trajno. Otvoreno pitanje: Šta se dešava s transkriptima koje je taj korisnik uploadovao?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-42.1 Pregled liste svih korisnika. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator odabere brisanje korisnika, tada sistem mora prikazati dijalog za potvrdu
- Kada administrator potvrdi brisanje, tada sistem mora ukloniti korisnički nalog i sve s njim povezane sesije
- Administrator ne smije moći obrisati vlastiti nalog
- Sistem ne smije dozvoliti brisanje bez eksplicitne potvrde
- Nakon uspješnog brisanja sistem mora prikazati odgovarajuću poruku potvrde

---

### PB-43 — Dashboard s aktuelnim podacima

#### User Story 43.1 — Prikaz aktuelnih statistika na dashboardu

| Polje | Vrijednost |
|---|---|
| **ID** | 43.1 |
| **Naziv** | Prikaz aktuelnih statistika na dashboardu |
| **Sprint** | 6 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Pruža administratoru brz pregled trenutnog stanja sistema bez prelaška na zasebne module |

**Uloga:**
Kao administrator, želim da admin dashboard prikazuje stvarne podatke o sistemu kako bih imao brz pregled trenutnog stanja.

**Pretpostavke i otvorena pitanja:**
Podaci se učitavaju pri otvaranju dashboarda. Otvoreno pitanje: Da li je potreban auto-refresh podataka?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-33, PB-34, PB-42. Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori dashboard, tada sistem mora prikazati aktuelni broj unesenih transkripata
- Dashboard mora prikazivati aktuelni broj registrovanih korisnika
- Dashboard mora prikazivati broj interakcija s chatbotom
- Svi prikazani podaci moraju odgovarati stvarnom stanju u bazi podataka — ne smiju biti statični/hardkodirani
- Sistem ne smije prikazati grešku pri učitavanju dashboarda

---

### PB-44 — Validacija formata transkripata

#### User Story 44.1 — Provjera Agent:/Korisnik: strukture pri unosu

| Polje | Vrijednost |
|---|---|
| **ID** | 44.1 |
| **Naziv** | Provjera Agent:/Korisnik: strukture pri unosu |
| **Sprint** | 6 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Sprečava unos nevalidnih transkripata koji bi narušili rad pipeline obrade i degradirali kvalitet baze znanja |

**Uloga:**
Kao sistem, želim provjeriti da li uneseni transkript slijedi propisanu strukturu (svaka linija mora počinjati s "Agent:" ili "Korisnik:") kako bih spriječio pohranu nevalidnih podataka.

**Pretpostavke i otvorena pitanja:**
Provjera se primjenjuje pri ručnom unosu i uploadovanju TXT/PDF fajla. Otvoreno pitanje: Da li linije koje ne počinju nijednim prefiksom trebaju biti upozorenje ili greška?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-18.1 Upload transkripata putem fajla. Zavisi od US-18.2 Ručni unos transkripata. Nadograđuje US-18.3 Validacija unesenih transkripata.

**Acceptance Criteria:**
- Kada administrator pokuša pohraniti transkript koji ne sadrži nijednu liniju s prefiksom "Agent:" ili "Korisnik:", tada sistem mora odbiti unos i prikazati jasnu poruku greške
- Poruka greške mora objasniti da transkript mora biti u formatu "Agent: [tekst]" i "Korisnik: [tekst]"
- Sistem ne smije pohraniti transkript koji ne zadovoljava strukturalni format
- Kada transkript sadrži barem jednu ispravno formatiranu liniju, tada sistem mora nastaviti s obradom
- Validacija mora raditi i za upload fajla (TXT/PDF) i za ručni unos teksta

---

## Sprint 7

---

### PB 23 — Priprema za obradu transkripata

#### User Story 23.1 — Normalizacija teksta transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 9 |
| **Naziv** | Normalizacija teksta transkripata |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava konzistentan format podataka za dalju obradu i treniranje modela |

**Uloga:**
Kao administrator, želim da sistem automatski normalizuje tekst transkripata kako bi podaci bili spremni za dalju obradu i pohranu.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da transkripti mogu sadržavati nekonzistentan format (velika/mala slova, specijalni znakovi). Otvoreno pitanje: Da li primijeniti naprednu jezičku korekciju ili samo osnovnu normalizaciju?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Upload i unos transkripata (18.x). Preduvjet za Razdvajanje po ulogama (23.2) i Detekcija i zamjena osjetljivih podataka (26.1).

**Acceptance Criteria:**
- Kada sistem primi transkript, tada mora ukloniti nepotrebne razmake i standardizovati tekst
- Sistem mora konvertovati tekst u definisani format (npr. mala slova ili standardizovana kapitalizacija)
- Sistem mora ukloniti ili zamijeniti nevalidne znakove
- Sistem ne smije promijeniti semantičko značenje teksta

---

#### User Story 23.2 — Razdvajanje transkripta po ulogama (agent/korisnik)

| Polje | Vrijednost |
|---|---|
| **ID** | 10 |
| **Naziv** | Razdvajanje transkripta po ulogama (agent/korisnik) |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava strukturiranje razgovora i kvalitetnije treniranje AI modela |

**Uloga:**
Kao administrator, želim da sistem automatski razdvoji transkript po ulogama (agent i korisnik) kako bi razgovor bio jasno strukturiran.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da transkript sadrži indikatore govornika (npr. "Agent:", "Korisnik:"). Otvoreno pitanje: Kako postupati kada oznake govornika nisu jasno definisane?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Normalizacija teksta transkripata (23.1). Preduvjet za Detekcija i zamjena osjetljivih podataka (26.1).

**Acceptance Criteria:**
- Kada sistem obradi transkript, tada mora identificirati govornike u razgovoru
- Sistem mora označiti svaki segment teksta odgovarajućom ulogom (agent ili korisnik)
- Kada oznake nisu jasno definisane, sistem mora pokušati inferirati uloge ili označiti segment kao nepoznat
- Sistem ne smije pogrešno dodijeliti uloge kada su oznake jasno definisane

---

### PB 26 — Maskiranje osjetljivih podataka

#### User Story 26.1 — Detekcija i zamjena osjetljivih podataka (ime, telefon, JMBG)

| Polje | Vrijednost |
|---|---|
| **ID** | 11 |
| **Naziv** | Detekcija i zamjena osjetljivih podataka (ime, telefon, JMBG) |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Štiti privatnost korisnika automatskim maskiranjem ličnih podataka prije obrade od strane chatbota |

**Uloga:**
Kao korisnik call centra, želim da sistem automatski detektuje i zamijeni moje osjetljive podatke (ime, telefon, JMBG) prije nego što se moj upit obradi, kako bi moja privatnost bila zaštićena.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su definisani obrasci za detekciju osjetljivih podataka (regex ili NLP model). Otvorena pitanja: Da li korisnik treba biti obaviješten o zamjeni podataka? Da li se original čuva ili trajno briše?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Postavljanje pitanja chatbotu tekstom (22.1).

**Acceptance Criteria:**
- Kada korisnik unese poruku koja sadrži ime, broj telefona ili JMBG, tada sistem mora detektovati i maskirati te podatke prije slanja chatbotu
- Sistem mora prikazati korisniku obavijest da su osjetljivi podaci zamijenjeni radi zaštite privatnosti
- Sistem mora podržati detekciju bh. formata JMBG (13 cifara), brojeva telefona i najčešćih obrazaca imena
- Zamjena se mora izvršiti transparentno — odgovor chatbota mora i dalje biti razumljiv korisniku
- Sistem ne smije slati originalne (nemaskirane) podatke chatbotu ili ih pohranjivati u logovima

---

### PB 27 — Izgradnja baze znanja

#### User Story 27.1 — Generisanje embeddinga iz transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 27.1 |
| **Naziv** | Generisanje embeddinga iz transkripata |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava semantičko razumijevanje sadržaja transkripata i predstavlja temelj za RAG pretragu chatbota |

**Uloga:**
Kao administrator, želim da sistem generiše embeddinge iz obrađenih transkripata kako bi chatbot mogao koristiti semantičku pretragu.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su transkripti prethodno normalizovani i validirani kroz pipeline (PB-23, PB-26). Otvoreno pitanje: Koji embedding model će biti korišten za generisanje vektora?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-23 Priprema za obradu transkripata (US-23.1, US-23.2). Zavisi od PB-26 Maskiranje osjetljivih podataka (US-26.1). Preduvjet za US-27.2 Pohrana embeddinga u vektorsku bazu.

**Acceptance Criteria:**
- Kada sistem obradi transkript, tada mora generisati embeddinge za tekstualne segmente
- Sistem mora evidentirati greške tokom generisanja embeddinga
- Sistem ne smije preskočiti validne tekstualne segmente
- Generisani embedding mora biti povezan s odgovarajućim segmentom transkripata

---

#### User Story 27.2 — Pohrana embeddinga u vektorsku bazu

| Polje | Vrijednost |
|---|---|
| **ID** | 27.2 |
| **Naziv** | Pohrana embeddinga u vektorsku bazu |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Čini embeddinge dostupnim za RAG pretragu i omogućava chatbotu korištenje baze znanja izgrađene iz transkripata |

**Uloga:**
Kao administrator, želim da sistem pohrani embeddinge u vektorsku bazu kako bi chatbot mogao koristiti relevantne informacije pri odgovaranju na pitanja.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je vektorska baza (Qdrant) pokrenuta i dostupna. Otvoreno pitanje: Da li će se koristiti Qdrant, Pinecone ili druga vektorska baza?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-27.1 Generisanje embeddinga iz transkripata. Preduvjet za US-27.3 Retrieval mehanizam za semantičku pretragu.

**Acceptance Criteria:**
- Kada embedding bude generisan, tada sistem mora pohraniti embedding u vektorsku bazu
- Embedding mora biti povezan s originalnim transkriptom
- Sistem mora prikazati grešku ako pohrana nije uspješna
- Sistem ne smije pohraniti duplirane embeddinge za isti segment

---

#### User Story 27.3 — Retrieval mehanizam za semantičku pretragu

| Polje | Vrijednost |
|---|---|
| **ID** | 27.3 |
| **Naziv** | Retrieval mehanizam za semantičku pretragu |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Poboljšava relevantnost odgovora chatbota pronalaženjem semantički najsličnijeg sadržaja iz baze znanja |

**Uloga:**
Kao korisnik chatbot sistema, želim da sistem pronađe semantički relevantne informacije kako bih dobio tačne odgovore na svoja pitanja.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da embeddingi postoje u vektorskoj bazi. Otvoreno pitanje: Koliko najrelevantnijih rezultata treba vratiti chatbotu? Koji je prag sličnosti ispod kojeg sistem smatra da nema relevantnog rezultata?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-27.2 Pohrana embeddinga u vektorsku bazu. Zavisi od PB-22 Chat UI (US-22.1).

**Acceptance Criteria:**
- Kada korisnik pošalje pitanje, tada sistem mora izvršiti semantičku pretragu nad vektorskom bazom
- Upit se pretvara u embedding prije pretrage
- Sistem mora vratiti najrelevantnije rezultate rangirane po semantičkoj sličnosti
- Rezultati moraju biti proslijeđeni chatbotu za generisanje odgovora
- Sistem ne smije prikazati grešku pri uspješnoj pretrazi

---

### PB 45 — Account Settings

#### User Story 45.1 — Promjena korisničkog imena

| Polje | Vrijednost |
|---|---|
| **ID** | 45.1 |
| **Naziv** | Promjena korisničkog imena |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava korisnicima ažuriranje podataka naloga bez potrebe za administratorskom intervencijom |

**Uloga:**
Kao registrovani korisnik, želim promijeniti svoje korisničko ime kako bih ažurirao podatke svog naloga.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da korisnik ima aktivan nalog i da je prijavljen u sistem. Otvoreno pitanje: Da li korisničko ime mora biti jedinstveno na nivou cijelog sistema?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36).

**Acceptance Criteria:**
- Kada korisnik otvori Account Settings, tada sistem mora prikazati trenutno korisničko ime
- Kada korisnik unese novo korisničko ime i potvrdi izmjenu, tada sistem mora sačuvati izmjene
- Sistem ne smije dozvoliti unos već postojećeg korisničkog imena
- Nakon uspješne izmjene sistem mora prikazati potvrdu

---

#### User Story 45.2 — Promjena lozinke

| Polje | Vrijednost |
|---|---|
| **ID** | 45.2 |
| **Naziv** | Promjena lozinke |
| **Sprint** | 7 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Povećava sigurnost korisničkih naloga omogućavanjem redovne promjene lozinke |

**Uloga:**
Kao registrovani korisnik, želim promijeniti svoju lozinku kako bih zaštitio svoj nalog.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je korisnik autentifikovan i da poznaje trenutnu lozinku. Otvoreno pitanje: Da li sistem treba zahtijevati periodičnu promjenu lozinke?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Zavisi od US-45.1.

**Acceptance Criteria:**
- Kada korisnik unese trenutnu i novu lozinku, tada sistem mora validirati podatke
- Nova lozinka mora zadovoljiti sigurnosna pravila (minimum 8 znakova)
- Kada trenutna lozinka nije ispravna, tada sistem mora prikazati poruku greške
- Nakon uspješne promjene sistem mora prikazati potvrdu
- Sistem ne smije prikazati lozinku u čitljivom obliku
- Sistem ne smije dozvoliti postavljanje iste lozinke kao prethodne

---

#### User Story 45.3 — Ažuriranje profilnih podataka

| Polje | Vrijednost |
|---|---|
| **ID** | 45.3 |
| **Naziv** | Ažuriranje profilnih podataka |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Osigurava da informacije na korisničkom nalogu budu uvijek tačne i ažurne |

**Uloga:**
Kao registrovani korisnik, želim ažurirati svoje profilne podatke kako bi moj nalog sadržavao tačne informacije.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da korisnik ima pristup svom profilu. Otvoreno pitanje: Koji podaci mogu biti izmijenjeni (ime, prezime, email, profilna slika)?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Zavisi od US-45.1.

**Acceptance Criteria:**
- Kada korisnik izmijeni profilne podatke, tada sistem mora sačuvati izmjene
- Sistem mora validirati obavezna polja — polja ne smiju biti prazna
- Nakon spremanja izmjene moraju odmah biti prikazane u profilu
- Sistem ne smije dozvoliti unos nevalidnog email formata

---

### PB 46 — Prikaz statusa obrade transkripata

#### User Story 46.1 — Pregled statusa obrade transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 46.1 |
| **Naziv** | Pregled statusa obrade transkripata |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Daje administratoru uvid u tok procesiranja podataka i omogućava pravovremenu reakciju na probleme u pipeline obradi |

**Uloga:**
Kao administrator, želim vidjeti status obrade transkripata kako bih mogao pratiti proces obrade podataka.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da sistem vodi evidenciju statusa obrade svakog transkripata u bazi podataka. Otvoreno pitanje: Da li status treba biti automatski osvježavan u realnom vremenu?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Upload i unos transkripata (PB-18). Zavisi od PB-23 Priprema za obradu transkripata. Zavisi od PB-27 Izgradnja baze znanja.

**Acceptance Criteria:**
- Sistem mora prikazati status svakog transkripata u administratorskom pregledu
- Status može biti: `Pending`, `Processing`, `Completed` ili `Failed`
- Sistem ne smije prikazati grešku pri učitavanju statusa
- Status mora biti vidljiv u administratorskom pregledu transkripata

---

#### User Story 46.2 — Prikaz grešaka pri obradi transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 46.2 |
| **Naziv** | Prikaz grešaka pri obradi transkripata |
| **Sprint** | 7 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava administratoru brzu identifikaciju i rješavanje problema u obradi podataka |

**Uloga:**
Kao administrator, želim vidjeti greške tokom obrade transkripata kako bih mogao reagovati na probleme.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da sistem evidentira logove i greške tokom obrade. Otvoreno pitanje: Da li administrator može ponovo pokrenuti obradu nakon greške?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-46.1 Pregled statusa obrade transkripata.

**Acceptance Criteria:**
- Kada obrada ne uspije, tada sistem mora prikazati poruku greške sa statusom `Failed`
- Administrator mora moći identificirati problematični transkript
- Sistem mora evidentirati razlog greške
- Sistem ne smije prikazati tehničke detalje greške krajnjim korisnicima

---


## Sprint 8

---

### PB 13 — Konvertovanje iz audio zapisa u transkript

#### User Story 13.1 — Konverzija audio zapisa u transkript

| Polje | Vrijednost |
|---|---|
| **ID** | 12 |
| **Naziv** | Konverzija audio zapisa u transkript |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Automatizuje proces pretvaranja snimljenih poziva u tekstualne transkripate, eliminišući potrebu za ručnim prepisivanjem |

**Uloga:**
Kao administrator, želim uploadati audio zapis poziva kako bi sistem automatski generisao transkript razgovora i pohranio ga u sistem.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su podržani uobičajeni audio formati (MP3, WAV). Otvorena pitanja: Koji su maksimalni dozvoljeni veličina i trajanje audio fajla? Da li sistem treba podržavati više govornika (diarizacija)? Da li se obrađuje samo bosanski/hrvatski/srpski jezik ili i ostali?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Pregled unesenih transkripata (33.x). Zavisi od Validacija unesenih transkripata (18.3).

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

### PB 22 — Chat UI (nastavak)

#### User Story 22.2 — Postavljanje pitanja chatbotu glasovnim unosom (Dictate)

| Polje | Vrijednost |
|---|---|
| **ID** | 13 |
| **Naziv** | Postavljanje pitanja chatbotu glasovnim unosom (Dictate) |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Poboljšava dostupnost i brzinu unosa, posebno za korisnike koji preferiraju glasovnu interakciju |

**Uloga:**
Kao korisnik call centra, želim izgovoriti pitanje putem mikrofona kako bih komunikaciju s chatbotom učinio bržom i jednostavnijom.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da uređaj korisnika ima funkcionalan mikrofon i da su dodijeljene dozvole. Otvoreno pitanje: Da li sistem treba podržavati više jezika pri glasovnom unosu?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Postavljanje pitanja chatbotu tekstom (22.1).

**Acceptance Criteria:**
- Kada korisnik klikne na dugme za glasovni unos, tada sistem mora aktivirati prepoznavanje govora
- Kada korisnik završi govor, tada sistem mora pretvoriti govor u tekst i prikazati ga u polju za unos
- Kada korisnik potvrdi pitanje, tada sistem mora poslati pitanje chatbotu
- Sistem mora prikazati odgovarajuću poruku ako mikrofon nije dostupan
- Sistem ne smije prikazati grešku ako korisnik nije izgovorio ništa — umjesto toga mora ostati na čekanju

---

### PB 48 — Escalation Queue u admin panelu

#### User Story 48.1 — Prikaz eskaliranih upita u admin panelu

| Polje | Vrijednost |
|---|---|
| **ID** | 48.1 |
| **Naziv** | Prikaz eskaliranih upita u admin panelu |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava agentu da vidi sve upite korisnika koji nisu riješeni chatbotom i zahtijevaju ljudsku intervenciju |

**Uloga:**
Kao agent, želim vidjeti listu eskaliranih korisničkih upita u admin panelu kako bih mogao prihvatiti razgovor i pomoći korisniku.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je chatbot već pokušao odgovoriti i uputio korisnika na agenta. Otvoreno pitanje: Da li se eskalacija može dodijeliti specifičnom agentu?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-52 RAG retrieval i LLM klasifikacija. Zavisi od PB-54 WebSocket komunikacija. Preduvjet za PB-50 Automatska odjava agenta.

**Acceptance Criteria:**
- Kada korisnik pristane na povezivanje s agentom, tada sistem mora dodati upit u escalation queue u admin panelu
- Queue mora prikazivati korisnički upit, vrijeme čekanja i status
- Kada agent prihvati upit, tada sistem mora ukloniti upit iz queue-a i otvoriti live chat s korisnikom
- Sistem ne smije prikazati grešku pri učitavanju escalation queue-a
- Kada nema eskaliranih upita, sistem mora prikazati odgovarajuću poruku

---

#### User Story 48.2 — Prihvatanje eskaliranog upita i otvaranje live chata

| Polje | Vrijednost |
|---|---|
| **ID** | 48.2 |
| **Naziv** | Prihvatanje eskaliranog upita i otvaranje live chata |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava direktnu real-time komunikaciju između agenta i korisnika koji čeka pomoć |

**Uloga:**
Kao agent, želim prihvatiti eskalirani upit i ući u live chat s korisnikom kako bih mu direktno pomogao.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je WebSocket konekcija aktivna za oba učesnika.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-48.1. Zavisi od PB-54 WebSocket komunikacija.

**Acceptance Criteria:**
- Kada agent klikne "Prihvati", tada sistem mora otvoriti live chat prozor s historijom razgovora korisnika s chatbotom
- Agent i korisnik moraju moći razmjenjivati poruke u realnom vremenu
- Korisnik mora dobiti obavijest da je agent preuzeo razgovor
- Sistem ne smije dozvoliti da dva agenta prihvate isti upit istovremeno

---

### PB 49 — Historija razgovora korisnika

#### User Story 49.1 — Pregled vlastite historije razgovora

| Polje | Vrijednost |
|---|---|
| **ID** | 49.1 |
| **Naziv** | Pregled vlastite historije razgovora |
| **Sprint** | 8 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava korisniku pregled prethodnih interakcija s chatbotom i agentima radi lakšeg snalaženja i praćenja vlastitih upita |

**Uloga:**
Kao korisnik, želim pregledati historiju svojih razgovora s chatbotom i agentima kako bih mogao pratiti prethodne upite i odgovore.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su razgovori pohranjeni u bazi podataka i vezani za korisnički nalog.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Zavisi od PB-22 Chat UI.

**Acceptance Criteria:**
- Kada korisnik otvori "My History", tada sistem mora prikazati listu svih prethodnih razgovora s datumom i prvom porukom
- Kada korisnik klikne na razgovor, tada sistem mora prikazati kompletan sadržaj tog razgovora
- Kada nema historije, sistem mora prikazati odgovarajuću poruku
- Sistem ne smije prikazati razgovore koji ne pripadaju prijavljenom korisniku
- Sistem ne smije prikazati grešku pri učitavanju historije

---

### PB 50 — Automatsko obavještavanje agenta o završetku korisničke sesije

#### User Story 50.1 — Automatska diskoneksija agenta kada korisnik završi razgovor

| Polje | Vrijednost |
|---|---|
| **ID** | 50.1 |
| **Naziv** | Automatska diskoneksija agenta kada korisnik završi razgovor |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Sprečava da agent ostane u aktivnoj sesiji bez korisnika i osigurava čisto zatvaranje razgovora s obje strane |

**Uloga:**
Kao agent, želim biti automatski obaviješten i diskonektovan kada korisnik izađe iz razgovora kako bih znao da je sesija završena.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da sistem prati status konekcije korisnika putem WebSocketa.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-54 WebSocket komunikacija. Zavisi od PB-48 Escalation queue.

**Acceptance Criteria:**
- Kada korisnik izađe iz chata ili se odjavi, tada sistem mora automatski diskonektovati agenta iz te sesije
- Agentu mora biti prikazana poruka "Korisnik je završio konverzaciju"
- Razgovor mora biti automatski označen kao završen
- Sistem ne smije ostaviti agenta u aktivnoj sesiji nakon što je korisnik izašao

---

### PB 51 — Agent panel s Live Queue i pristupom bazi znanja

#### User Story 51.1 — Agent Live Queue — prikaz upita specifičnih za agenta

| Polje | Vrijednost |
|---|---|
| **ID** | 51.1 |
| **Naziv** | Agent Live Queue |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Agentima pruža personalizovan prikaz samo njihovih aktivnih sesija i upita, odvojen od globalnog admin pogleda |

**Uloga:**
Kao agent, želim vidjeti samo moje aktivne upite i sesije u Live Queue-u kako bih se fokusirao na vlastiti rad bez suvišnih informacija.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je agent prijavljen s ulogom CallCentarAgent.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Zavisi od PB-48 Escalation queue. Preduvjet za PB-50.

**Acceptance Criteria:**
- Kada agent otvori panel, tada sistem mora prikazati samo upite i sesije dodijeljene tom agentu
- Live Queue se mora ažurirati u realnom vremenu bez reload-a stranice
- Agent ne smije vidjeti upite dodijeljene drugim agentima
- Sistem ne smije prikazati grešku pri učitavanju Live Queue-a

---

#### User Story 51.2 — Pretraga baze znanja iz agentovog panela

| Polje | Vrijednost |
|---|---|
| **ID** | 51.2 |
| **Naziv** | Pretraga baze znanja iz agentovog panela |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Agentima omogućava brzo pronalaženje relevantnih informacija iz baze znanja tokom razgovora s korisnikom |

**Uloga:**
Kao agent, želim pretraživati bazu znanja direktno iz svog panela kako bih brzo pronašao odgovore tokom live razgovora s korisnikom.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da baza znanja sadrži Q&A parove iz obrađenih transkripata.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-27 Izgradnja baze znanja. Zavisi od US-51.1.

**Acceptance Criteria:**
- Kada agent unese ključnu riječ, tada sistem mora prikazati relevantne Q&A parove iz baze znanja
- Rezultati moraju biti sortirani po relevantnosti
- Kada nema rezultata, sistem mora prikazati odgovarajuću poruku
- Sistem ne smije prikazati grešku pri pretrazi

---

### PB 52 — RAG retrieval i LLM klasifikacija upita

#### User Story 52.1 — Klasifikacija upita — RAG ili LLM

| Polje | Vrijednost |
|---|---|
| **ID** | 52.1 |
| **Naziv** | Klasifikacija upita — RAG ili LLM |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava da korisnik dobije najtačniji odgovor — iz baze znanja kada postoji relevantan sadržaj, ili od LLM-a za opća pitanja |

**Uloga:**
Kao korisnik, želim da sistem automatski odabere najprikladniji način odgovaranja na moje pitanje kako bih dobio tačan i relevantan odgovor.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su embeddinzi pohranjeni u Qdrantu i da je LLM API dostupan.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-27 Izgradnja baze znanja. Zavisi od PB-22 Chat UI.

**Acceptance Criteria:**
- Kada korisnik postavi pitanje, tada sistem mora klasificirati upit kao RAG ili LLM upit
- Kada upit odgovara sadržaju u bazi znanja, tada sistem mora koristiti RAG retrieval za generisanje odgovora
- Kada upit nije pokriven bazom znanja, tada LLM mora generisati odgovor na osnovu općeg znanja
- Sistem ne smije pomiješati izvore odgovora za isti upit
- Klasifikacija mora biti transparentna u logu ali ne mora biti vidljiva korisniku

---

#### User Story 52.2 — RAG retrieval — pronalaženje relevantnih odgovora

| Polje | Vrijednost |
|---|---|
| **ID** | 52.2 |
| **Naziv** | RAG retrieval — pronalaženje relevantnih odgovora |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Chatbot daje odgovore utemeljene na stvarnim podacima call centra, a ne izmišljenim informacijama |

**Uloga:**
Kao korisnik, želim da chatbot odgovori na moje pitanje koristeći informacije iz baze znanja call centra kako bih dobio tačan i relevantan odgovor.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da baza znanja sadrži dovoljno podataka za pokrivanje čestih upita.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-52.1. Zavisi od PB-27 Izgradnja baze znanja.

**Acceptance Criteria:**
- Kada sistem klasificira upit kao RAG, tada mora pretražiti vektorsku bazu i pronaći najrelevantnije segmente
- Sistem mora koristiti pronađene segmente kao kontekst za generisanje odgovora
- Kada sistem ne pronađe relevantan sadržaj s dovoljnom sigurnošću, tada mora uputiti korisnika na agenta
- Sistem ne smije izmišljati informacije koje ne postoje u bazi znanja

---

### PB 53 — Obrada osnovne komunikacije sa LLM

#### User Story 53.1 — Odgovaranje na općenita pitanja i pozdrave

| Polje | Vrijednost |
|---|---|
| **ID** | 53.1 |
| **Naziv** | Odgovaranje na općenita pitanja i pozdrave |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Poboljšava korisničko iskustvo prirodnom konverzacijom za upite koji nisu vezani za domenu call centra, bez nepotrebnog opterećivanja agenata |

**Uloga:**
Kao korisnik, želim da chatbot prirodno odgovori na pozdrave i pitanja koja nisu vezana za usluge call centra, kako bi interakcija bila ugodna i tečna.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da LLM može prepoznati razliku između upita vezanih za domenu call centra i općenitih pitanja koja ne zahtijevaju intervenciju agenta.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-52.1 Klasifikacija upita. Zavisi od PB-22 Chat UI.

**Acceptance Criteria:**
- Kada korisnik pošalje pozdrav (npr. "Hej", "Hello"), tada sistem mora prirodno odgovoriti bez eskalacije na agenta
- Kada korisnik postavi pitanje koje nije vezano za domenu call centra, tada sistem mora ljubazno odgovoriti ili objasniti svoja ograničenja
- Sistem ne smije eskalirati na agenta za pozdrave i pitanja izvan domene
- Sistem mora minimizovati broj nepotrebnih eskalacija na agenta

---

#### User Story 53.2 — Usmjeravanje na agenta kada chatbot ne može odgovoriti

| Polje | Vrijednost |
|---|---|
| **ID** | 53.2 |
| **Naziv** | Usmjeravanje na agenta kada chatbot ne može odgovoriti |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava da korisnik uvijek dobije odgovarajuću pomoć čak i kada chatbot nema dovoljno informacija za pouzdan odgovor |

**Uloga:**
Kao korisnik, želim biti upućen na agenta kada chatbot nije u stanju odgovoriti na moj upit, kako bih dobio potrebnu pomoć.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su agenti dostupni u sistemu. Otvoreno pitanje: Kako sistem postupa kada nema dostupnih agenata?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-52.1. Zavisi od PB-48 Escalation queue.

**Acceptance Criteria:**
- Kada chatbot ne može generisati pouzdan odgovor, tada mora korisniku ponuditi opciju povezivanja s agentom
- Kada korisnik pristane, tada sistem mora dodati upit u escalation queue
- Kada korisnik odbije, tada sistem mora nastaviti konverzaciju bez eskalacije
- Sistem mora jasno i razumljivo objasniti korisniku razlog preusmjeravanja na agenta
---

### PB 54 — WebSocket komunikacija između korisnika i agenta

#### User Story 54.1 — Real-time razmjena poruka između korisnika i agenta

| Polje | Vrijednost |
|---|---|
| **ID** | 54.1 |
| **Naziv** | Real-time razmjena poruka između korisnika i agenta |
| **Sprint** | 8 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava neposrednu dvosmjernu komunikaciju bez kašnjenja, što je ključno za kvalitetnu korisničku podršku |

**Uloga:**
Kao korisnik, želim razmjenjivati poruke s agentom u realnom vremenu kako bih dobio brzu i direktnu pomoć.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da backend podržava WebSocket konekcije. Otvoreno pitanje: Koliko dugo se čuva WebSocket konekcija pri neaktivnosti?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-48 Escalation queue. Preduvjet za PB-50 Automatska odjava agenta.

**Acceptance Criteria:**
- Kada agent prihvati upit, tada sistem mora uspostaviti WebSocket konekciju između korisnika i agenta
- Poruke moraju biti isporučene u realnom vremenu bez potrebe za refreshom stranice
- Kada konekcija padne, sistem mora pokušati automatski se reconnectati
- Sistem mora prikazati indikator kada druga strana tipka poruku
- Sistem ne smije izgubiti poruke pri privremenom prekidu konekcije

---

### PB 55 — Resolving chatova

#### User Story 55.1 — Označavanje razgovora kao riješenog

| Polje | Vrijednost |
|---|---|
| **ID** | 55.1 |
| **Naziv** | Označavanje razgovora kao riješenog |
| **Sprint** | 8 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava čisto zatvaranje sesija i praćenje riješenih slučajeva, što poboljšava organizaciju rada agenata |

**Uloga:**
Kao agent, želim označiti razgovor kao riješen kako bih zatvorio aktivnu sesiju i oslobodio kapacitet za nove upite.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da razgovor mora biti aktivan da bi se mogao označiti kao riješen. Otvoreno pitanje: Da li korisnik dobija obavijest kada agent označi razgovor kao riješen?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-48 Escalation queue. Zavisi od PB-54 WebSocket komunikacija.

**Acceptance Criteria:**
- Kada agent klikne "Resolve", tada sistem mora označiti razgovor kao riješen i zatvoriti aktivnu sesiju
- Korisnik mora biti obaviješten da je razgovor zatvoren
- Riješeni razgovor mora biti vidljiv u historiji s odgovarajućim statusom
- Sistem ne smije dozvoliti slanje novih poruka u riješenom razgovoru
- Sistem ne smije prikazati grešku pri označavanju razgovora kao riješenog

---

## Sprint 9

---

### PB 15 — Ocjena odgovora chatbota

#### User Story 15.1 — Ocjena pojedinačnog odgovora

| Polje | Vrijednost |
|---|---|
| **ID** | 14 |
| **Naziv** | Ocjena pojedinačnog odgovora |
| **Sprint** | 9 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava prikupljanje povratnih informacija o kvalitetu odgovora chatbota |

**Uloga:**
Kao korisnik call centra, želim ocijeniti odgovor koji mi je chatbot dao kako bih pomogao u poboljšanju kvaliteta usluge.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je korisnik postavio pitanje i dobio odgovor od chatbota. Otvoreno pitanje: Da li ocjena treba biti binarna (palac gore / palac dolje) ili numerička (1–5)?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Preduvjet za Prijava netačnog odgovora (28.x).

**Acceptance Criteria:**
- Kada chatbot vrati odgovor, tada sistem mora prikazati opciju za ocjenu odgovora
- Kada korisnik odabere ocjenu, tada sistem mora sačuvati ocjenu i vezati je za konkretan odgovor
- Sistem ne smije dozvoliti slanje ocjene bez prethodno prikazanog odgovora
- Kada je ocjena uspješno sačuvana, tada sistem mora prikazati potvrdu korisniku

---

#### User Story 15.2 — Dodavanje opcionog komentara uz ocjenu

| Polje | Vrijednost |
|---|---|
| **ID** | 15 |
| **Naziv** | Dodavanje opcionog komentara uz ocjenu |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Pruža dublji kontekst uz ocjenu i olakšava analizu slabih odgovora |

**Uloga:**
Kao korisnik call centra, želim uz ocjenu dodati kratak komentar kako bih preciznije obrazložio zašto odgovor nije bio zadovoljavajući.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da korisnik već ima mogućnost ocjenjivanja. Otvoreno pitanje: Da li je komentar obavezan samo uz negativnu ocjenu?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Ocjena pojedinačnog odgovora (15.1).

**Acceptance Criteria:**
- Kada korisnik odabere negativnu ocjenu, tada sistem mora prikazati opcionalno polje za komentar
- Kada korisnik unese komentar i potvrdi, tada sistem mora sačuvati komentar vezan za tu ocjenu
- Sistem ne smije dozvoliti unos praznog komentara ako je polje otvoreno
- Sistem ne smije prikazati grešku prilikom slanja komentara

---

### PB 28 — Prijava netačnog odgovora

#### User Story 28.1 — Prijava netačnog odgovora chatbota

| Polje | Vrijednost |
|---|---|
| **ID** | 16 |
| **Naziv** | Prijava netačnog odgovora chatbota |
| **Sprint** | 9 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava identifikaciju i korekciju slabih mjesta u bazi znanja chatbota |

**Uloga:**
Kao korisnik call centra, želim prijaviti netačan ili neprimjeren odgovor chatbota kako bih pomogao u poboljšanju sistema.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je korisnik dobio odgovor od chatbota. Otvoreno pitanje: Da li korisnik mora biti prijavljen da bi mogao prijaviti problem?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Ocjena pojedinačnog odgovora (15.1). Preduvjet za Pregled prijavljenih problema (35.x).

**Acceptance Criteria:**
- Kada korisnik odabere opciju 'Prijavi problem', tada sistem mora prikazati formu za prijavu
- Kada korisnik popuni formu i potvrdi slanje, tada sistem mora pohraniti prijavu i vezati je za konkretan odgovor chatbota
- Sistem mora prikazati potvrdu korisniku da je prijava uspješno poslana
- Sistem ne smije dozvoliti slanje prazne prijave

---

#### User Story 28.2 — Kategorizacija prijavljenog problema

| Polje | Vrijednost |
|---|---|
| **ID** | 17 |
| **Naziv** | Kategorizacija prijavljenog problema |
| **Sprint** | 9 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Olakšava analizu i prioritizaciju grešaka u odgovorima chatbota |

**Uloga:**
Kao korisnik call centra, želim odabrati vrstu greške pri prijavi problema kako bi administrator lakše razumio prirodu problema.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su kategorije grešaka unaprijed definisane (npr. netačna informacija, nerelevantni odgovor, tehnička greška).

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Prijava netačnog odgovora chatbota (28.1).

**Acceptance Criteria:**
- Kada korisnik otvori formu za prijavu, tada sistem mora prikazati listu kategorija grešaka
- Kada korisnik odabere kategoriju, tada sistem mora vezati tu kategoriju za prijavljeni problem
- Sistem ne smije dozvoliti slanje prijave bez odabrane kategorije

---

## Sprint 10

---

### PB 15 — Ocjena odgovora chatbota (nastavak)

#### User Story 15.3 — Pregled prosječne ocjene chatbota

| Polje | Vrijednost |
|---|---|
| **ID** | 18 |
| **Naziv** | Pregled prosječne ocjene chatbota |
| **Sprint** | 10 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Daje administratoru uvid u ukupni kvalitet chatbota kroz agregirane metrike |

**Uloga:**
Kao administrator, želim vidjeti prosječnu ocjenu chatbota po vremenskom periodu kako bih pratio trendove kvaliteta.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoje sačuvane ocjene korisnika. Otvoreno pitanje: Koji vremenski period je podrazumijevani (sedmica, mjesec)?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Ocjena pojedinačnog odgovora (15.1). Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori pregled ocjena, tada sistem mora prikazati prosječnu ocjenu za odabrani period
- Kada nema ocjena za odabrani period, tada sistem mora prikazati poruku 'Nema dostupnih ocjena'
- Sistem mora omogućiti filtriranje po vremenskom periodu
- Sistem ne smije prikazati grešku prilikom učitavanja statistike

---

### PB 33 — Pregled unesenih transkripata (nastavak)

#### User Story 33.3 — Pretraga i filtriranje transkripata

| Polje | Vrijednost |
|---|---|
| **ID** | 19 |
| **Naziv** | Pretraga i filtriranje transkripata |
| **Sprint** | 10 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Smanjuje vrijeme pretrage i olakšava pronalazak relevantnih transkripata |

**Uloga:**
Kao administrator, želim pretraživati i filtrirati transkripate po ključnim riječima, datumu i agentu kako bih brzo pronašao relevantne zapise.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da transkripati postoje u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih unesenih transkripata (33.1).

**Acceptance Criteria:**
- Kada administrator unese ključnu riječ ili primijeni filter, tada sistem mora prikazati odgovarajuće transkripate
- Kada nema rezultata, tada sistem mora prikazati poruku 'Nema rezultata'
- Kada administrator resetuje filtere, tada sistem mora prikazati sve transkripate

---

### PB 34 — Pregled postavljenih pitanja i odgovora

#### User Story 34.1 — Pregled svih pitanja i odgovora — administratorski prikaz

| Polje | Vrijednost |
|---|---|
| **ID** | 20 |
| **Naziv** | Pregled svih pitanja i odgovora — administratorski prikaz |
| **Sprint** | 10 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Pruža administratoru uvid u česta pitanja i kvalitet odgovora radi unapređenja baze znanja |

**Uloga:**
Kao administrator, želim pregledati sva pitanja koja su korisnici postavili chatbotu, zajedno s odgovorima, kako bih identificirao najčešća pitanja i eventualne slabosti sistema.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su interakcije korisnika sačuvane i dostupne administratoru.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Zavisi od Postavljanje pitanja chatbotu tekstom (22.1).

**Acceptance Criteria:**
- Kada administrator otvori pregled, tada sistem mora prikazati sve zabilježene interakcije s pitanjima i odgovorima
- Administrator mora moći filtrirati prikaz po datumu, korisniku i ocjeni odgovora
- Sistem mora prikazati poruku 'Nema zabilježenih interakcija' ako je lista prazna
- Sistem ne smije prikazati grešku pri učitavanju liste

---

### PB 35 — Pregled prijavljenih problema

#### User Story 35.1 — Lista svih prijavljenih problema

| Polje | Vrijednost |
|---|---|
| **ID** | 21 |
| **Naziv** | Lista svih prijavljenih problema |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Daje administratoru centralizovan pregled svih grešaka chatbota koje su korisnici prijavili |

**Uloga:**
Kao administrator, želim vidjeti listu svih prijavljenih problema kako bih imao pregled netačnih odgovora chatbota.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoji barem jedna prijavljena greška.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Prijava netačnog odgovora chatbota (28.1). Zavisi od Sign In.

**Acceptance Criteria:**
- Kada administrator otvori modul za prijavljene probleme, tada sistem mora prikazati listu svih prijava
- Svaka prijava mora sadržavati: originalno pitanje, odgovor chatbota, kategoriju greške i datum prijave
- Kada nema prijavljenih problema, tada sistem mora prikazati poruku 'Nema prijavljenih problema'
- Sistem ne smije prikazati grešku pri učitavanju liste

---

#### User Story 35.2 — Detaljan pregled pojedinačne prijave

| Polje | Vrijednost |
|---|---|
| **ID** | 22 |
| **Naziv** | Detaljan pregled pojedinačne prijave |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava administratoru dubinsku analizu svake prijave radi korekcije baze znanja |

**Uloga:**
Kao administrator, želim otvoriti detalje pojedinačne prijave kako bih vidio sve informacije vezane za prijavljenu grešku.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da prijava postoji u sistemu.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih prijavljenih problema (35.1).

**Acceptance Criteria:**
- Kada administrator klikne na prijavu iz liste, tada sistem mora prikazati sve detalje te prijave
- Prikaz mora sadržavati: pitanje korisnika, odgovor chatbota, kategoriju greške, komentar korisnika i datum
- Sistem ne smije prikazati grešku pri učitavanju detalja

---

## Sprint 11

---

### PB 31 — Odgovor kada nema sigurnog responsea

#### User Story 31.1 — Pregled pitanja bez odgovora chatbota — agentski prikaz

| Polje | Vrijednost |
|---|---|
| **ID** | 23 |
| **Naziv** | Pregled pitanja bez odgovora chatbota — agentski prikaz |
| **Sprint** | 11 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava agentu da identificira i preuzme pitanja na koja chatbot nije bio u stanju odgovoriti, smanjujući broj neuspješnih korisničkih interakcija |

**Uloga:**
Kao agent call centra, želim vidjeti listu pitanja na koja chatbot nije mogao odgovoriti kako bih mogao intervenirati i dati ispravan odgovor korisniku.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da sistem bilježi sve interakcije gdje chatbot nije pronašao odgovarajući odgovor. Otvoreno pitanje: Koji je kriterij za klasifikaciju odgovora kao 'nije mogao odgovoriti' (prazni odgovor, niska pouzdanost, eksplicitna oznaka)?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In. Zavisi od Postavljanje pitanja chatbotu tekstom (22.1).

**Acceptance Criteria:**
- Kada agent otvori modul za neodgovorena pitanja, tada sistem mora prikazati listu svih pitanja na koja chatbot nije dao odgovor
- Svaki zapis mora sadržavati: originalno pitanje korisnika, datum i vrijeme, te status (Čeka odgovor / Odgovoreno)
- Kada nema neodgovorenih pitanja, tada sistem mora prikazati poruku 'Nema pitanja koja čekaju odgovor'
- Sistem ne smije prikazati grešku pri učitavanju liste

---

#### User Story 31.2 — Unos agentovog odgovora na neodgovoreno pitanje

| Polje | Vrijednost |
|---|---|
| **ID** | 24 |
| **Naziv** | Unos agentovog odgovora na neodgovoreno pitanje |
| **Sprint** | 11 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava kontinuitet korisničke podrške kada chatbot ne može pružiti odgovor |

**Uloga:**
Kao agent call centra, želim unijeti odgovor na pitanje koje chatbot nije mogao riješiti kako bih korisniku pružio tačnu informaciju.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da agent ima uvid u pitanje i kontekst korisnika. Otvoreno pitanje: Da li agentov odgovor treba biti prikazan korisniku u realnom vremenu ili uz vremenski odmak?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Pregled pitanja bez odgovora chatbota — agentski prikaz (31.1).

**Acceptance Criteria:**
- Kada agent klikne na neodgovoreno pitanje, tada sistem mora prikazati detalje pitanja i polje za unos odgovora
- Kada agent unese odgovor i potvrdi slanje, tada sistem mora pohraniti odgovor i promijeniti status pitanja u 'Odgovoreno'
- Korisnik mora biti obaviješten da je agent odgovorio na njegovo pitanje
- Sistem ne smije dozvoliti slanje praznog odgovora
- Sistem ne smije prikazati grešku pri uspješnom slanju odgovora

---

## Sprint 12

---

### PB 22 — Chat UI (nastavak)

#### User Story 22.3 — Pregled istorije pitanja i odgovora — korisnički prikaz

| Polje | Vrijednost |
|---|---|
| **ID** | 25 |
| **Naziv** | Pregled istorije pitanja i odgovora — korisnički prikaz |
| **Sprint** | 12 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Omogućava korisnicima uvid u prethodne interakcije s chatbotom |

**Uloga:**
Kao korisnik call centra, želim pregledati historiju mojih pitanja i odgovora chatbota kako bih se mogao referirati na prethodne interakcije.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su prethodne interakcije sačuvane u sistemu. Otvoreno pitanje: Koliko dugo se čuva istorija razgovora?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Postavljanje pitanja chatbotu tekstom (22.1). Zavisi od Sign In.

**Acceptance Criteria:**
- Kada korisnik otvori historiju, tada sistem mora prikazati listu prethodnih pitanja i odgovora hronološkim redoslijedom
- Svaki zapis mora sadržavati datum i vrijeme interakcije
- Kada nema istorije, tada sistem mora prikazati poruku 'Nema prethodnih razgovora'
- Sistem ne smije prikazati grešku prilikom učitavanja istorije

---

#### User Story 22.4 — Brisanje pitanja iz istorije — korisnički prikaz

| Polje | Vrijednost |
|---|---|
| **ID** | 26 |
| **Naziv** | Brisanje pitanja iz istorije — korisnički prikaz |
| **Sprint** | 12 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Daje korisnicima kontrolu nad vlastitom istorijom interakcija i podržava pravo na brisanje podataka |

**Uloga:**
Kao korisnik call centra, želim moći izbrisati jedno ili više svojih prethodnih pitanja iz historije kako bih upravljao vlastitim podacima.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da korisnik ima pristup historiji pitanja i odgovora. Otvoreno pitanje: Da li brisanje treba biti trajno ili je moguć oporavak u određenom roku?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Pregled istorije pitanja i odgovora — korisnički prikaz (22.3).

**Acceptance Criteria:**
- Kada korisnik otvori historiju, tada sistem mora prikazati opciju za brisanje uz svaki zapis
- Kada korisnik odabere brisanje, tada sistem mora zatražiti potvrdu prije trajnog brisanja
- Kada korisnik potvrdi brisanje, tada sistem mora ukloniti zapis iz historije i odmah ažurirati prikaz
- Sistem mora podržati brisanje više zapisa odjednom (bulk delete)
- Sistem ne smije prikazati grešku pri uspješnom brisanju

---

### PB 31 — Odgovor kada nema sigurnog responsea (nastavak)

#### User Story 31.3 — Upotreba agentovog odgovora za poboljšanje chatbota

| Polje | Vrijednost |
|---|---|
| **ID** | 27 |
| **Naziv** | Upotreba agentovog odgovora za poboljšanje chatbota |
| **Sprint** | 12 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Kontinuirano unapređuje bazu znanja chatbota na osnovu stvarnih korisničkih pitanja i agentovih odgovora |

**Uloga:**
Kao administrator, želim da agentovi odgovori na neodgovorena pitanja budu iskorišteni za treniranje chatbota kako bih smanjio broj budućih neuspješnih interakcija.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoji mehanizam za označavanje odgovora kao pogodnih za uključivanje u bazu znanja. Otvoreno pitanje: Da li administrator treba ručno odobravati odgovore prije dodavanja u trening dataset?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Unos agentovog odgovora na neodgovoreno pitanje (31.2).

**Acceptance Criteria:**
- Kada agentov odgovor bude označen kao validan, tada sistem mora ponuditi opciju za dodavanje tog para (pitanje/odgovor) u bazu znanja za treniranje
- Administrator mora moći pregledati i odobriti ili odbaciti prijedloge za dodavanje u bazu znanja
- Sistem mora prikazati potvrdu kada je par uspješno dodan u trening dataset
- Sistem ne smije automatski dodavati odgovore u bazu znanja bez odobrenja

---

### PB 35 — Pregled prijavljenih problema (nastavak)

#### User Story 35.3 — Promjena statusa prijave

| Polje | Vrijednost |
|---|---|
| **ID** | 28 |
| **Naziv** | Promjena statusa prijave |
| **Sprint** | 12 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Omogućava praćenje procesa rješavanja prijavljenih grešaka |

**Uloga:**
Kao administrator, želim promijeniti status prijavljenog problema kako bih označio da je problem u obradi ili riješen.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su statusi prijave unaprijed definisani (npr. Nova, U obradi, Riješena).

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Detaljan pregled pojedinačne prijave (35.2).

**Acceptance Criteria:**
- Kada administrator otvori prijavu, tada sistem mora prikazati opciju za promjenu statusa
- Kada administrator promijeni status i potvrdi, tada sistem mora sačuvati promjenu i odmah je reflektovati u prikazu
- Sistem ne smije dozvoliti postavljanje nevalidnog statusa
- Sistem ne smije prikazati grešku pri promjeni statusa

---

#### User Story 35.4 — Filtriranje i pretraga prijavljenih problema

| Polje | Vrijednost |
|---|---|
| **ID** | 29 |
| **Naziv** | Filtriranje i pretraga prijavljenih problema |
| **Sprint** | 12 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Smanjuje vrijeme potrebno za pronalazak relevantnih prijava i prioritizaciju grešaka |

**Uloga:**
Kao administrator, želim filtrirati prijavljene probleme po statusu, kategoriji i datumu kako bih lakše upravljao prioritetima.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da postoje prijave s različitim statusima i kategorijama.

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Lista svih prijavljenih problema (35.1).

**Acceptance Criteria:**
- Kada administrator odabere filter kriterij, tada sistem mora prikazati samo odgovarajuće prijave
- Kada nema rezultata za odabrane filtere, tada sistem mora prikazati poruku 'Nema rezultata'
- Kada administrator resetuje filtere, tada sistem mora prikazati sve prijave
- Sistem ne smije prikazati grešku pri primjeni filtera
