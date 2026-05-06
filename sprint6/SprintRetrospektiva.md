# Sprint Retrospektiva
---
## Šta smo naučili
Ovaj sprint bio je temeljan, uspostavili smo autentifikaciju, unos i pregled transkripata te log infrastrukturu. Isporuka je bila potpuna i to je vrijedno pohvale. Međutim, retrospektiva nije samo o tome što smo završili, već o tome kako smo radili i što možemo raditi bolje.
---
## Šta je išlo dobro
- Sve planirane stavke su zatvorene unutar sprinta bez prenošenja.
- UI rješenje za pregled transkripata je kvalitetno i vizualno poliran — to je standard kojeg treba zadržati.
- Tim je funkcionisao koordinisano i bez blokatora koji bi zaustavili isporuku.
---
## Šta trebamo popraviti
### Navigacija — Back dugme ne vraća na Home
U većini slučajeva Back dugme ne vraća korisnika na početni ekran kako bi se očekivalo. Ovo narušava osnovni tok kretanja kroz aplikaciju i zbunjuje korisnika. Navigacijska logika treba biti dosljedna na svim ekranima — ovo je visoki prioritet za sljedeći sprint.

Konkretno, identificovani su sljedeći problemi:
- Kada korisnik otvori **Transcripts – pregled** i klikne Back, aplikacija ga vraća na ekran za prijavu umjesto na glavnu stranicu transkripata.
- Isti problem postoji i na **Issues** i **Chat Logs** — povratak iz pregled stranice ne vraća na listu, već na neočekivanu lokaciju.

### Sidebar — Ratings prikazuje placeholder podatke
Ratings widget u sidebaru trenutno prikazuje statične ili lažne podatke umjesto stvarnih. Treba ga povezati sa stvarnim podacima iz sistema kako bi informacije bile relevantne i korisne.

### Issues — Problemi sa pretragom i akcijama
- Placeholder tekst u polju za pretragu Issues-a se preklapa sa ikonom lupe (SVG), što narušava vizualni izgled.
- Dugme **Report Issue** ne funkcioniše — treba implementirati ili zakrpiti ovu akciju.
- Dugme **Edit** u Training Set sekciji ne funkcioniše — treba provjeriti implementaciju i osigurati da radi ispravno.

---
## Refleksija na tim i proces
Kapacitet je iskorišten dobro, ali uočavamo obrazac: funkcionalne stavke se zatvaraju, no UI/UX detalji i rubni slučajevi ostaju nedovoljno testirani prije review-a. Back navigacija i neispravne akcije nisu sitni propusti — to su stvari koje korisnik primijeti u prvoj minuti korišćenja.

Za sljedeći sprint vrijedi uvesti kratki korak pred zatvaranje svake stavke: proći kroz osnovne korisničke tokove i provjeriti radi li navigacija dosledno. Ne radi se o formalnom QA procesu, već o navici koja štedi vrijeme na retrospektivi.

---
## Akcije za sljedeći sprint
| # | Akcija | Odgovornost | Prioritet |
|---|--------|-------------|-----------|
| 1 | Popraviti Back navigaciju na svim ekranima (Transcripts, Issues, Chat Logs) | Frontend | High |
| 2 | Povezati Ratings u sidebaru sa stvarnim podacima | Frontend / Backend | Medium |
| 3 | Popraviti preklapanje placeholdera i ikone u Issues pretrazi | Frontend | Low |
| 4 | Implementirati Report Issue funkcionalnost | Frontend / Backend | Medium |
| 5 | Popraviti Edit dugme u Training Set sekciji | Frontend | Medium |
| 6 | Uspostaviti kratki navigacijski smoke test pred zatvaranje stavke | Cijeli tim | Medium |

---
## Zaključak
Temelji su postavljeni, tim funkcioniše, isporuka je bila kompletna. Ono što sad trebamo je podići standard na detalje, jer u call centar kontekstu, korisnici rade s alatom svaki dan i svaki broken flow im troši vrijeme. Sljedeći sprint je prilika da pokažemo da možemo isporučivati i kvantitativno i kvalitativno.
