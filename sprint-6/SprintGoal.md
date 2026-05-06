# Sprint Goal — Sprint 6

## Cilj sprinta

U Sprintu 6 fokus je na tome da administrator dobije potpunu kontrolu nad podacima u sistemu. Nakon što je Sprint 5 postavio temelje kroz prijavu korisnika i osnovni unos transkripata, ovaj sprint gradi na tom temelju i zatvara ključne praznine koje su postojale: transkripti su se mogli unijeti, ali ne i mijenjati ili brisati; korisnici su postojali u sistemu, ali njima nije moglo biti upravljano; dashboard je prikazivao podatke, ali ne i stvarne. Sprint 6 rješava sve to i uvodi validaciju koja osigurava da podaci koji ulaze u sistem budu ispravnog formata od samog početka, što je preduvjet za ispravan rad pipeline obrade u kasnijim sprintovima.

Na kraju ovog sprinta, administrator ima funkcionalan i upotrebljiv administratorski panel — može pregledati, urediti i obrisati transkripte, pretražiti ih po ključnoj riječi, datumu ili agentu, upravljati korisničkim nalozima i ulogama, te na dashboardu odmah vidjeti stvarno stanje sistema bez potrebe za prelaskom na zasebne module.

---

## Šta ovaj sprint isporučuje

**Upravljanje transkriptima** je u ovom sprintu dobilo sve funkcionalnosti koje nedostaju za svakodnevni rad. Administrator sada može otvoriti postojeći transkript, izmijeniti sadržaj ili metapodatke i sačuvati izmjene, ali i trajno obrisati transkript uz obaveznu potvrdu koja sprečava slučajno brisanje. Uz to, uvedena je pretraga i filtriranje — po ključnoj riječi, vremenskom periodu i identifikatoru agenta — što omogućava brzo pronalaženje relevantnih zapisa u sistemu koji će s vremenom imati sve više podataka.

**Validacija formata transkripata** je tehnički važna stavka ovog sprinta. Sistem sada odbija svaki transkript koji ne prati propisanu strukturu `Agent: [tekst]` / `Korisnik: [tekst]` i prikazuje jasnu poruku greške s objašnjenjem ispravnog formata. Ovo važi i za upload fajla i za ručni unos. Bez ove validacije, pipeline obrada u kasnijim sprintovima bi primala nestrukturirane podatke koji bi narušili kvalitet baze znanja.

**Upravljanje korisnicima** je nova funkcionalnost ovog sprinta. Administrator može pregledati listu svih registrovanih korisnika s njihovim podacima i ulogama, dodijeliti ili promijeniti ulogu, te obrisati korisnički nalog uz potvrdu. Promjena uloge stupa na snagu odmah — korisnik gubi ili dobija pristup odgovarajućim dijelovima sistema bez odlaganja.

**Dashboard s aktuelnim podacima** je zatvorio jedan vidljiv problem iz prethodnog sprinta — prikaz hardkodiranih vrijednosti zamijenjen je stvarnim agregatima iz baze podataka. Administrator sada na prvom ekranu vidi tačan broj transkripata, korisnika i interakcija s chatbotom.

---

## Stavke uključene u sprint

| ID | Naziv | Prioritet |
|----|-------|-----------|
| PB-33 | Pregled unesenih transkripata | High |
| PB-34 | Pregled postavljenih pitanja i odgovora | High |
| PB-38 | Uređivanje postojećih transkripata | High |
| PB-39 | Brisanje transkripata s potvrdom akcije | High |
| PB-40 | Filtriranje i pretraga transkripata | High |
| PB-41 | Dodjela i upravljanje ulogama korisnika | High |
| PB-42 | Pregled i brisanje korisnika | High |
| PB-43 | Dashboard s aktuelnim podacima | Medium |
| PB-44 | Validacija formata transkripata | High |

---

## Kriterij uspjeha

Sprint se smatra uspješnim ako:

- administrator može urediti i obrisati transkript uz obaveznu potvrdu, bez greške u sistemu
- pretraga i filtriranje vraćaju tačne rezultate za sve podržane filtere (ključna riječ, datum, agent)
- promjena uloge korisnika odmah stupa na snagu i ograničava ili proširuje pristup u sistemu
- dashboard prikazuje stvarne podatke iz baze koji se mijenjaju s promjenama u sistemu
- unos transkripata koji ne slijedi `Agent:` / `Korisnik:` format biva odbijen s jasnom i razumljivom porukom greške, za oba načina unosa (upload i ručni unos)
