# Sprint Retrospektiva
---
## Šta smo naučili
Ovaj sprint bio je temeljen, uspostavili smo autentifikaciju, unos i pregled transkripata te log infrastrukturu. Isporuka je bila potpuna i to je vrijedno pohvale. Međutim, retrospektiva nije samo o tome šta smo završili, već o tome kako smo radili i šta možemo raditi bolje.
---
## Šta je išlo dobro
- Sve planirane stavke su zatvorene unutar sprinta bez prenošenja.
- UI rješenje za pregled transkripata je kvalitetno i vizualno poliran — to je standard kojeg treba zadržati.
- Tim je funkcionisao koordinisano i bez blokatora koji bi zaustavili isporuku.
---
## Šta trebamo popraviti
### Navigacija — Back dugme ne vraća na Home
U većini slučajeva Back dugme ne vraća korisnika na početni ekran kako bi se očekivalo. Konkretno:
- Kada je korisnik u admin prikazu i klikne "Back", aplikacija treba zatvoriti/izaći iz stranice umjesto da prebacuje korisnika u korisnički prikaz.
- Kada je korisnik na stranici "Transkripti – pregled" i klikne "Back", treba se vratiti na glavnu stranicu Transkripti.
- Isto ponašanje treba primjeniti i na stranicama Issues i Chat Logs — povratak iz "view" stranica treba voditi na odgovarajuću listu, ne na login.

Navigacijska logika treba biti dosljedna na svim ekranima — ovo je visoki prioritet za sljedeći sprint.

### Listing transkripata — nedostaje kolona tipa fajla
U tabeli pregleda transkripata trenutno nedostaje kolona s tipom fajla (npr. PDF, MP3, DOCX). Korisnik ne može na prvi pogled raspoznati s kakvim sadržajem radi. Dodavanje ovog podatka je mala izmjena s vidljivim efektom na upotrebljivost.

### Settings — Account sekcija ne reaguje na klik
Klik na Account u Settings ekranu ne pokreće nikakvu akciju. Ovo je broken flow koji ostavlja korisnika u slijepoj ulici. Treba provjeriti je li u pitanju nedovršena implementacija ili bag u rutiranju, te zatvoriti tu stavku što prije.

### Sidebar — Ratings prikaz ne pokazuje stvarne podatke
Ratings widget u sidebaru prikazuje statične ili placeholder podatke umjesto stvarnih ocjena. Treba ga spojiti na pravi izvor podataka kako bi prikazivao tačne i ažurne vrijednosti.

### Issues — Search placeholder i ikona se preklapaju
Na stranici Issues, tekst u search polju ("Search issues...") i search ikona (SVG) se vizualno preklapaju. Potrebno je poravnati padding i pozicioniranje kako bi prikaz bio čist i čitljiv.

### Issues — Report Issue forma ne radi
Dugme "Report Issue" ne pokreće nikakvu akciju ili forma ne šalje podatke ispravno. Ova funkcionalnost treba biti u potpunosti implementirana i testirana.

### Training Set — Edit funkcionalnost ne radi
Edit opcija na stranici Training Set ne reaguje kako treba. Treba provjeriti i popraviti flow za uređivanje stavki u training setu.

---
## Refleksija na tim i proces
Kapacitet je iskorišten dobro, ali uočavamo obrazac: funkcionalne stavke se zatvaraju, no UI/UX detalji i rubni slučajevi ostaju nedovoljno testirani prije review-a. Back navigacija, nepovezan Settings, neispravni podaci u sidebaru i broken forme nisu sitni propusti — to su stvari koje korisnik primijeti u prvoj minuti korišćenja.

Za sljedeći sprint vrijedi uvesti kratki korak pred zatvaranje svake stavke: proći kroz osnovne korisničke tokove i provjeriti radi li navigacija dosljedno. Ne radi se o formalnom QA procesu, već o navici koja štedi vrijeme na retrospektivi.

---
## Akcije za sljedeći sprint
| # | Akcija | Odgovornost | Prioritet |
|---|--------|-------------|-----------|
| 1 | Popraviti Back navigaciju na svim ekranima (admin exit, transkripti, issues, chat logs) | Frontend | High |
| 2 | Dodati kolonu tipa fajla u listing transkripata | Frontend | Medium |
| 3 | Implementirati ili zakrpiti Account u Settings | Frontend / Backend | High |
| 4 | Spojiti Ratings widget u sidebaru na stvarne podatke | Frontend / Backend | High |
| 5 | Popraviti search placeholder/ikona overlap na Issues stranici | Frontend | Low |
| 6 | Implementirati Report Issue funkcionalnost | Frontend / Backend | High |
| 7 | Popraviti Edit na Training Set stranici | Frontend | High |
| 8 | Uspostaviti kratki navigacijski smoke test pred zatvaranje stavke | Cijeli tim | Medium |

---
## Zaključak
Temelji su postavljeni, tim funkcioniše, isporuka je bila kompletna. Ono što sad trebamo je podići standard na detalje, jer u call centar kontekstu, korisnici rade s alatom svaki dan i svaki broken flow im troši vrijeme. Sljedeći sprint je prilika da pokažemo da možemo isporučivati i kvantitativno i kvalitativno.