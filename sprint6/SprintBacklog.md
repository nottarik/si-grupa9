# Sprint Backlog – Sprint 6

## Opis sprinta

Sprint 6 fokusira se na proširenje funkcionalnosti upravljanja transkriptima (uređivanje, brisanje, filtriranje i validacija formata), uvođenje administratorskog upravljanja korisnicima i dodjelu uloga, te poboljšanje admin dashboarda s aktuelnim podacima. Pored novih funkcionalnosti, sprint uključuje i stavke prenesene iz Sprint 5 (PB-33, PB-34) koje su bile planirane ali se vežu uz funkcionalnosti ovog sprinta.

Tokom ovog sprinta implementiraju se funkcionalnosti vezane za:

- pregled, uređivanje i brisanje transkripata
- filtriranje i pretragu transkripata po ključnoj riječi, datumu i agentu
- validaciju formata transkripata (Agent:/Korisnik: struktura)
- upravljanje korisnicima i dodjelu uloga od strane administratora
- prikaz aktuelnih podataka na admin dashboardu

---

## Pregled stavki sprinta

| ID | Naziv stavke | Kratak opis | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-------------|-----|-----------|-----------------|--------|
| PB-33 | Pregled unesenih transkripata | Tabela s listom transkripata, datumom, statusom obrade | Feature | High | 3 | Završeno |
| PB-34 | Pregled postavljenih pitanja i odgovora | Prikaz svih interakcija za administratora | Feature | High | 3 | Završeno |
| PB-38 | Uređivanje postojećih transkripata | Izmjena sadržaja ili metapodataka transkripata | Feature | High | 5 | Završeno |
| PB-39 | Brisanje transkripata s potvrdom akcije | Trajno brisanje transkripata uz potvrdu | Feature | High | 3 | Završeno |
| PB-40 | Filtriranje i pretraga transkripata | Pretraga po ključnoj riječi, datumu i agentu | Feature | High | 5 | Završeno |
| PB-41 | Dodjela i upravljanje ulogama korisnika | Administrator mijenja uloge korisnika | Feature | High | 5 | Završeno |
| PB-42 | Pregled i brisanje korisnika | Administrator pregledava i briše korisničke naloge | Feature | High | 5 | Završeno |
| PB-43 | Dashboard s aktuelnim podacima | Stvarni agregati na admin dashboardu | Feature | Medium | 3 | Završeno |
| PB-44 | Validacija formata transkripata | Provjera Agent:/Korisnik: strukture s prikazom greške | Technical Task | High | 3 | Završeno |

---

## Sprint Backlog stavke

---

### PB-33: Pregled unesenih transkripata

**Prioritet:** High
**Poslovna vrijednost:** Daje administratoru centralizovan pregled svih pohranjenih transkripata i omogućava pristup detaljima svakog razgovora.
**Pretpostavke:** Barem jedan transkript mora biti pohranjen u sistemu.
**Veze i zavisnosti:** Zavisi od PB-18 Upload i unos transkripata. Zavisi od PB-36 Sign In. Preduvjet za PB-38, PB-39, PB-40.

---

#### US-33.1 — Lista svih unesenih transkripata

**Uloga:** Kao administrator, želim vidjeti listu svih unesenih transkripata kako bih imao pregled dostupnih podataka.

**Acceptance Criteria:**
- Kada administrator otvori modul za transkripate, tada sistem mora prikazati listu svih transkripata
- Kada ne postoji nijedan transkript, tada sistem mora prikazati poruku "Nema unesenih transkripata"
- Sistem ne smije prikazati grešku prilikom učitavanja liste

---

#### US-33.2 — Detaljan pregled pojedinačnog transkripata

**Uloga:** Kao administrator, želim otvoriti detalje pojedinog transkripata kako bih vidio kompletan zapis razgovora.

**Acceptance Criteria:**
- Kada administrator klikne na transkript iz liste, tada sistem mora prikazati kompletan sadržaj razgovora
- Prikaz mora sadržavati datum, identifikator agenta i sav sadržaj razgovora
- Sistem ne smije prikazati grešku prilikom učitavanja detalja

---

### PB-34: Pregled postavljenih pitanja i odgovora

**Prioritet:** High
**Poslovna vrijednost:** Omogućava administratoru nadzor nad svim interakcijama korisnika s chatbotom radi praćenja kvaliteta odgovora.
**Pretpostavke:** Korisnici su postavljali pitanja chatbotu i odgovori su pohranjeni u sistemu.
**Veze i zavisnosti:** Zavisi od PB-36 Sign In. Zavisi od PB-22 Chat UI.

---

#### US-34.1 — Pregled svih pitanja i odgovora — administratorski prikaz

**Uloga:** Kao administrator, želim pregledati sva pitanja koja su korisnici postavili chatbotu, zajedno s odgovorima, kako bih identificirao najčešća pitanja i eventualne slabosti sistema.

**Acceptance Criteria:**
- Kada administrator otvori pregled, tada sistem mora prikazati sve zabilježene interakcije s pitanjima i odgovorima
- Svaki zapis mora sadržavati pitanje korisnika, odgovor chatbota i datum interakcije
- Kada ne postoji nijedna interakcija, tada sistem mora prikazati odgovarajuću poruku
- Sistem ne smije prikazati grešku prilikom učitavanja liste

---

### PB-38: Uređivanje postojećih transkripata

**Prioritet:** High
**Poslovna vrijednost:** Omogućava ispravku grešaka u unesenim transkriptima bez potrebe za ponovnim uploadom cijelog fajla.
**Pretpostavke:** Transkript mora postojati u sistemu. Samo administrator i agent mogu uređivati transkripte.
**Veze i zavisnosti:** Zavisi od PB-33 Pregled unesenih transkripata. Zavisi od PB-36 Sign In.

---

#### US-38.1 — Uređivanje sadržaja transkripata

**Uloga:** Kao administrator, želim urediti sadržaj postojećeg transkripata kako bih ispravио greške nastale pri unosu.

**Acceptance Criteria:**
- Kada administrator otvori detalje transkripata, tada sistem mora prikazati opciju za uređivanje
- Kada administrator klikne "Uredi", tada sistem mora otvoriti formu s prethodno unesenim podacima
- Kada administrator spremi izmjene, tada sistem mora pohraniti ažurirani transkript i prikazati potvrdu
- Sistem ne smije izgubiti originalni sadržaj ako administrator odustane od uređivanja
- Sistem ne smije dozvoliti spremanje praznog sadržaja transkripata

---

#### US-38.2 — Uređivanje metapodataka transkripata

**Uloga:** Kao administrator, želim ažurirati metapodatke transkripata (datum, identifikator agenta) kako bi evidencija bila tačna.

**Acceptance Criteria:**
- Kada administrator uredi metapodatke i spremi, tada sistem mora pohraniti izmjene i odmah ih reflektovati u listi
- Sistem mora validirati metapodatke pri uređivanju (format datuma, neprazni identifikator agenta)
- Sistem ne smije prikazati grešku pri ispravnom unosu metapodataka

---

### PB-39: Brisanje transkripata s potvrdom akcije

**Prioritet:** High
**Poslovna vrijednost:** Omogućava uklanjanje netačnih ili zastarjelih transkripata uz zaštitu od slučajnog brisanja.
**Pretpostavke:** Transkript mora postojati u sistemu. Brisanje je trajno i ne može se oporaviti.
**Veze i zavisnosti:** Zavisi od PB-33 Pregled unesenih transkripata. Zavisi od PB-36 Sign In.

---

#### US-39.1 — Brisanje pojedinačnog transkripata

**Uloga:** Kao administrator, želim obrisati transkript iz sistema kako bih uklonio netačne ili zastarjele podatke.

**Acceptance Criteria:**
- Kada administrator odabere opciju brisanja, tada sistem mora prikazati dijalog za potvrdu akcije
- Kada administrator potvrdi brisanje, tada sistem mora trajno ukloniti transkript i ažurirati listu
- Kada administrator odustane od brisanja, tada sistem mora zatvoriti dijalog bez ikakve izmjene
- Sistem ne smije dozvoliti brisanje bez eksplicitne potvrde korisnika
- Nakon uspješnog brisanja sistem mora prikazati odgovarajuću poruku potvrde

---

### PB-40: Filtriranje i pretraga transkripata

**Prioritet:** High
**Poslovna vrijednost:** Smanjuje vrijeme potrebno za pronalazak relevantnih transkripata u sistemu s velikim brojem zapisa.
**Pretpostavke:** Lista transkripata mora biti dostupna. Podržani filteri su: ključna riječ, datum i identifikator agenta.
**Veze i zavisnosti:** Zavisi od PB-33 Pregled unesenih transkripata.

---

#### US-40.1 — Pretraga transkripata po ključnoj riječi

**Uloga:** Kao administrator, želim pretraživati transkripate po ključnoj riječi kako bih pronašao specifične razgovore.

**Acceptance Criteria:**
- Kada administrator unese ključnu riječ u polje za pretragu, tada sistem mora prikazati transkripate čiji sadržaj ili naziv odgovara unesenoj riječi
- Kada nema rezultata, tada sistem mora prikazati poruku "Nema rezultata za uneseni pojam"
- Kada administrator obriše ključnu riječ, tada sistem mora prikazati kompletnu listu transkripata

---

#### US-40.2 — Filtriranje transkripata po datumu i agentu

**Uloga:** Kao administrator, želim filtrirati transkripate po datumu i identifikatoru agenta kako bih brzo pronašao relevantne zapise.

**Acceptance Criteria:**
- Kada administrator primijeni filter po datumu, tada sistem mora prikazati samo transkripate unutar odabranog vremenskog perioda
- Kada administrator primijeni filter po agentu, tada sistem mora prikazati samo transkripate tog agenta
- Kada administrator resetuje filtere, tada sistem mora prikazati sve transkripate
- Sistem ne smije prikazati grešku pri primjeni filtera

---

### PB-41: Dodjela i upravljanje ulogama korisnika

**Prioritet:** High
**Poslovna vrijednost:** Osigurava da korisnici imaju pristup isključivo funkcionalnostima koje odgovaraju njihovoj ulozi u sistemu.
**Pretpostavke:** Korisnik mora imati kreiran nalog. Administrator mora biti prijavljen. Dostupne uloge su: Administrator, Supervizor, CallCentarAgent, KrajnjiKorisnik.
**Veze i zavisnosti:** Zavisi od PB-36 Sign In. Zavisi od PB-42 Pregled i brisanje korisnika.

---

#### US-41.1 — Dodjela uloge korisniku

**Uloga:** Kao administrator, želim dodijeliti ulogu novom korisniku kako bi korisnik imao odgovarajući nivo pristupa sistemu.

**Acceptance Criteria:**
- Kada administrator otvori profil korisnika, tada sistem mora prikazati trenutnu ulogu i opciju za izmjenu
- Kada administrator odabere novu ulogu i potvrdi, tada sistem mora odmah primijeniti promjenu
- Sistem mora prikazati poruku potvrde nakon uspješne dodjele uloge
- Sistem ne smije dozvoliti postavljanje nepostojeće uloge

---

#### US-41.2 — Izmjena postojeće uloge korisnika

**Uloga:** Kao administrator, želim promijeniti ulogu korisnika kada se promijene njegove radne odgovornosti.

**Acceptance Criteria:**
- Kada administrator promijeni ulogu, tada sistem mora odmah ažurirati pristup tog korisnika u skladu s novom ulogom
- Ako je korisnik trenutno prijavljen, tada mora biti preusmjeren na prijavu pri narednoj akciji koja zahtijeva staru ulogu
- Sistem mora evidentirati promjenu uloge s datumom i identifikatorom administratora koji je napravio izmjenu

---

### PB-42: Pregled i brisanje korisnika

**Prioritet:** High
**Poslovna vrijednost:** Daje administratoru kontrolu nad korisničkim nalogima i mogućnost uklanjanja neaktivnih ili neovlaštenih korisnika.
**Pretpostavke:** Administrator mora biti prijavljen. Brisanje korisnika je trajno.
**Veze i zavisnosti:** Zavisi od PB-36 Sign In. Preduvjet za PB-41 Dodjela i upravljanje ulogama korisnika.

---

#### US-42.1 — Pregled liste svih korisnika

**Uloga:** Kao administrator, želim pregledati listu svih registrovanih korisnika kako bih imao pregled naloga u sistemu.

**Acceptance Criteria:**
- Kada administrator otvori modul za korisnike, tada sistem mora prikazati listu svih registrovanih korisnika
- Svaki red mora prikazivati ime, prezime, email, ulogu i datum kreiranja naloga
- Kada nema registrovanih korisnika, tada sistem mora prikazati poruku "Nema registrovanih korisnika"
- Sistem ne smije prikazati grešku prilikom učitavanja liste

---

#### US-42.2 — Brisanje korisničkog naloga

**Uloga:** Kao administrator, želim obrisati korisnički nalog kako bih uklonio neaktivne ili neovlaštene korisnike.

**Acceptance Criteria:**
- Kada administrator odabere brisanje korisnika, tada sistem mora prikazati dijalog za potvrdu
- Kada administrator potvrdi brisanje, tada sistem mora ukloniti korisnički nalog i sve s njim povezane sesije
- Administrator ne smije moći obrisati vlastiti nalog
- Sistem ne smije dozvoliti brisanje bez eksplicitne potvrde
- Nakon uspješnog brisanja sistem mora prikazati odgovarajuću poruku potvrde

---

### PB-43: Dashboard s aktuelnim podacima

**Prioritet:** Medium
**Poslovna vrijednost:** Pruža administratoru brz pregled trenutnog stanja sistema bez potrebe za prelaskom na zasebne module.
**Pretpostavke:** Podaci o transkriptima, korisnicima i interakcijama moraju biti dostupni u bazi.
**Veze i zavisnosti:** Zavisi od PB-33, PB-34, PB-42. Zavisi od PB-36 Sign In.

---

#### US-43.1 — Prikaz aktuelnih statistika na dashboardu

**Uloga:** Kao administrator, želim da admin dashboard prikazuje stvarne podatke o sistemu kako bih imao brz pregled trenutnog stanja.

**Acceptance Criteria:**
- Kada administrator otvori dashboard, tada sistem mora prikazati aktuelni broj unesenih transkripata
- Dashboard mora prikazivati aktuelni broj registrovanih korisnika
- Dashboard mora prikazivati broj interakcija s chatbotom
- Svi prikazani podaci moraju odgovarati stvarnom stanju u bazi podataka — ne smiju biti statični/hardkodirani
- Sistem ne smije prikazati grešku pri učitavanju dashboarda

---

### PB-44: Validacija formata transkripata

**Prioritet:** High
**Poslovna vrijednost:** Osigurava da su svi uneseni transkriati u ispravnom formatu (Agent:/Korisnik: struktura) kako bi pipeline obrada mogla ispravno funkcionisati.
**Pretpostavke:** Validacija se primjenjuje i na upload fajla i na ručni unos. Format koji se očekuje je linije koje počinju s "Agent:" ili "Korisnik:".
**Veze i zavisnosti:** Zavisi od PB-18 Upload i unos transkripata (US-18.1, US-18.2, US-18.3).

---

#### US-44.1 — Provjera Agent:/Korisnik: strukture pri unosu

**Uloga:** Kao sistem, želim provjeriti da li uneseni transkript slijedi propisanu strukturu (svaka linija mora počinjati s "Agent:" ili "Korisnik:") kako bih spriječio pohranu nevalidnih podataka koji bi narušili rad pipeline obrade.

**Acceptance Criteria:**
- Kada administrator pokuša pohraniti transkript koji ne sadrži nijednu liniju s prefiksom "Agent:" ili "Korisnik:", tada sistem mora odbiti unos i prikazati jasnu poruku greške
- Poruka greške mora objasniti da transkript mora biti u formatu "Agent: [tekst]" i "Korisnik: [tekst]"
- Sistem ne smije pohraniti transkript koji ne zadovoljava strukturalni format
- Kada transkript sadrži barem jednu ispravno formatiranu liniju, tada sistem mora nastaviti s obradom
- Validacija mora raditi i za upload fajla (TXT/PDF) i za ručni unos teksta

---
