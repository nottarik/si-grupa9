# Sprint Backlog – Sprint 5

## Opis sprinta

Sprint 5 se fokusira na implementaciju sistema autentifikacije (prijava i odjava korisnika), funkcionalnosti za upload i unos transkripata, te pregleda unesenih transkripata i postavljenih pitanja i odgovora. Ove stavke čine temelj sistema — bez prijave korisnici ne mogu pristupiti nijednoj funkcionalnosti, a upload transkripata direktno napaja bazu znanja chatbota.

---

## Pregled stavki sprinta

| ID | Naziv stavke | Kratak opis | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-------------|-----|-----------|-----------------|--------|
| PB-36 | Sign In | Sistem za autentifikaciju korisnika | Technical Task | High | 5 | Done |
| PB-37 | Sign Out | Odjava iz sistema | Technical Task | High | 5 | Done |
| PB-18 | Upload i unos transkripata | Prijem i pohrana transkripata  | Feature | High | 8 | Done |
| PB-33 | Pregled unesenih transkripata | Tabela s listom fajlova, datumom, statusom obrade | Feature | High | 3 | Done |
| PB-19 | AI Usage Log i Decision Log | Uspostava logova za praćenje korištenja AI alata i tehničkih odluka | Technical Task | Medium | — | Done |

---

## Sprint Backlog stavke

---

### PB-36: Sign In — Prijava u sistem

**Naziv:** Prijava u sistem  
**Prioritet:** High  
**Poslovna vrijednost:** Prijava je preduvjet za sve ostale funkcionalnosti sistema. Bez nje korisnici ne mogu pristupiti nijednoj zaštićenoj stranici ili modulu.  
**Pretpostavke:** Administrator unaprijed kreira korisničke račune i dodjeljuje uloge.  
**Veze i zavisnosti:** Preduvjet za sve ostale user storije u sprintu i sistemu.

---

#### US-36.1 — Prijava u sistem

**Uloga:** Kao ovlašteni korisnik, želim unijeti svoje korisničke podatke kako bih pristupio funkcionalnostima prilagođenim mojoj ulozi.

**Acceptance Criteria:**

- Kada korisnik otvori aplikaciju, tada sistem mora prikazati stranicu za prijavu s poljima za e-mail i lozinku
- Kada korisnik unese ispravne podatke, tada sistem mora preusmjeriti korisnika na odgovarajući dashboard prema ulozi
- Kada korisnik unese neispravne podatke, tada sistem mora prikazati generičku poruku greške
- Sistem ne smije prikazati lozinku u čitljivom obliku
- Sistem ne smije dozvoliti direktan pristup zaštićenim stranicama bez prijave — korisnik mora biti preusmjeren na stranicu za prijavu

---

### PB-37: Sign Out — Odjava iz sistema

**Naziv:** Odjava iz sistema  
**Prioritet:** High  
**Poslovna vrijednost:** Štiti osjetljive podatke call centra od neovlaštenog pristupa nakon završetka rada korisnika.  
**Pretpostavke:** Korisnik je prethodno prijavljen. Otvoreno pitanje: Koliko dugo traje aktivna sesija prije automatske odjave?  
**Veze i zavisnosti:** Zavisi od PB-36 Sign In.

---

#### US-37.1 — Odjava iz sistema

**Uloga:** Kao prijavljeni korisnik, želim odjaviti se iz sistema kako bih zaštitio svoje podatke kada završim s radom.

**Acceptance Criteria:**

- Kada je korisnik prijavljen, tada sistem mora prikazati vidljivu opciju Sign Out u navigaciji
- Kada korisnik klikne Sign Out, tada sistem mora prekinuti sesiju i preusmjeriti korisnika na stranicu za prijavu
- Kada se korisnik odjavi i pritisne dugme za povratak u pregledniku, tada sistem ne smije prikazati zaštićeni sadržaj

---

### PB-18: Upload i unos transkripata

**Naziv:** Upload i unos transkripata  
**Prioritet:** High  
**Poslovna vrijednost:** Omogućava administratoru unos transkripata razgovora u sistem, čime se gradi baza podataka za treniranje i rad chatbota.  
**Pretpostavke:** Podržani formati fajlova su TXT i PDF. Otvorena pitanja: Koji su maksimalni dozvoljeni formati i veličina fajla? Da li forma treba imati polja za strukturirani unos ili slobodan tekst?  
**Veze i zavisnosti:** Zavisi od PB-36 Sign In. Preduvjet za PB-33 Pregled unesenih transkripata.

---

#### US-18.1 — Upload transkripata putem fajla

**Uloga:** Kao administrator, želim uploadati transkript razgovora iz fajla kako bih pohranio evidenciju razgovora u sistemu.

**Acceptance Criteria:**

- Kada administrator pristupi modulu za upload, tada sistem mora prikazati opciju za odabir fajla
- Kada administrator učita validan fajl, tada sistem mora pohraniti transkript i prikazati poruku o uspješnom uploadu
- Kada fajl nije validnog formata, tada sistem mora prikazati odgovarajuću poruku greške
- Sistem ne smije prikazati grešku pri uploadu validnog fajla

---

#### US-18.2 — Ručni unos transkripata

**Uloga:** Kao administrator, želim ručno unijeti transkript razgovora putem forme kako bih pohranio razgovor koji nije bio digitalno snimljen.

**Acceptance Criteria:**

- Kada administrator otvori formu za ručni unos, tada sistem mora prikazati sva potrebna polja (datum, sadržaj razgovora, identifikator agenta)
- Kada administrator popuni sva obavezna polja i klikne "Sačuvaj", tada sistem mora pohraniti transkript
- Kada polje ostane prazno, tada sistem mora vizualno označiti obavezna polja
- Sistem ne smije prikazati grešku prilikom unosa validnih podataka

---


### PB-33: Pregled unesenih transkripata

**Naziv:** Pregled unesenih transkripata  
**Prioritet:** High  
**Poslovna vrijednost:** Daje administratoru centralizovan pregled svih pohranjenih transkripata s mogućnošću uvida u sadržaj pojedinog razgovora.  
**Pretpostavke:** Barem jedan transkript mora biti pohranjen u sistemu.  
**Veze i zavisnosti:** Zavisi od PB-18 Upload i unos transkripata. Zavisi od PB-36 Sign In.

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


### PB-19: AI Usage Log i Decision Log

**Naziv:** Uspostava AI Usage Loga i Decision Loga  
**Prioritet:** Medium  
**Poslovna vrijednost:** Omogućava transparentno praćenje korištenja AI alata i dokumentovanje tehničkih odluka tokom razvoja projekta, čime se povećava odgovornost tima i olakšava kasnija analiza i održavanje sistema.  
**Pretpostavke:** Svi članovi tima imaju pristup repozitoriju. Otvoreno pitanje: Da li postoji odgovorna osoba za provjeru logova?  
**Veze i zavisnosti:** Definisana struktura projektne dokumentacije u repozitoriju.

---

#### US-19.1 — Standardizovani unos u AI Usage Log

**Uloga:** Kao tim, želimo kreirati AI Usage Log u okviru projekta, kako bismo evidentirali korištenje AI alata tokom razvoja i osigurali transparentnost rada.

**Acceptance Criteria:**

- Kada tim kreira projektnu dokumentaciju, tada se kreira AI Usage Log fajl u repozitoriju
- Log mora imati definisanu strukturu unosa (datum, alat, svrha korištenja, opis)
- Kada član tima koristi AI alat, tada je dužan evidentirati korištenje u logu
- Log mora biti dostupan svim članovima tima u repozitoriju

---

#### US-19.2 — Standardizovani unos u Decision Log

**Uloga:** Kao tim, želimo voditi Decision Log kako bismo dokumentovali važne tehničke i arhitekturalne odluke tokom razvoja sistema.

**Acceptance Criteria:**

- Kada se donese važna tehnička odluka, tada se ona mora zapisati u Decision Log
- Decision Log mora sadržavati datum, opis odluke i obrazloženje
- Sve ključne odluke o arhitekturi i implementaciji moraju biti dokumentovane
- Log mora biti dostupan svim članovima tima u repozitoriju
