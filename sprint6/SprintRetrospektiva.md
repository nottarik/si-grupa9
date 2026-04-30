# Sprint Retrospektiva

**Datum:** 30. april 2026


---

## Što smo naučili

Ovaj sprint bio je temeljan, uspostavili smo autentifikaciju, unos i pregled transkripata te log infrastrukturu. Isporuka je bila potpuna i to je vrijedno pohvale. Međutim, retrospektiva nije samo o tome što smo završili, već o tome kako smo radili i što možemo raditi bolje.

---

## Što je išlo dobro

- Sve planirane stavke su zatvorene unutar sprinta bez prenošenja.
- UI rješenje za pregled transkripata je kvalitetno i vizualno poliran — to je standard kojeg treba zadržati.
- Tim je funkcionisao koordinisano i bez blokatora koji bi zaustavili isporuku.

---

## Što trebamo popraviti

### Navigacija — Back dugme ne vraća na Home
U većini slučajeva Back dugme ne vraća korisnika na početni ekran kako bi se očekivalo. Ovo narušava osnovni tok kretanja kroz aplikaciju i zbunjuje korisnika. Navigacijska logika treba biti dosljedna na svim ekranima — ovo je visoki prioritet za sljedeći sprint.

### Listing transkripata — nedostaje tip fajla
U tabeli pregleda transkripata trenutno nedostaje kolona s tipom fajla (npr. PDF, MP3, DOCX). Korisnik ne može na prvi pogled raspoznati s kakvim sadržajem radi. Dodavanje ovog podatka je mala izmjena s vidljivim efektom na upotrebljivost.

### Settings — Account sekcija ne reaguje na klik
Klik na Account u Settings ekranu ne pokreće nikakvu akciju. Ovo je broken flow koji ostavlja korisnika u slijepoj ulici. Treba provjeriti je li u pitanju nedovršena implementacija ili bag u rutiranju, te zatvoriti tu stavku što prije.

---

## Refleksija na tim i proces

Kapacitet je iskorišten dobro, ali uočavamo obrazac: funkcionalne stavke se zatvaraju, no UI/UX detalji i rubni slučajevi ostaju nedovoljno testirani prije review-a. Back navigacija i nepovezan Settings nisu sitni propusti — to su stvari koje korisnik primijeti u prvoj minuti korišćenja.

Za sljedeći sprint vrijedi uvesti kratki korak pred zatvaranje svake stavke: proći kroz osnovne korisničke tokove i provjeriti radi li navigacija dosledno. Ne radi se o formalnom QA procesu, već o navici koja štedi vrijeme na retrospektivi.

---

## Akcije za sljedeći sprint

| # | Akcija | Odgovornost | Prioritet |
|---|--------|-------------|-----------|
| 1 | Popraviti Back navigaciju na svim ekranima | Frontend | High |
| 2 | Dodati kolonu tipa fajla u listing transkripata | Frontend | Medium |
| 3 | Implementirati ili zakrpiti Account u Settings | Frontend / Backend | High |
| 4 | Uspostaviti kratki navigacijski smoke test pred zatvaranje stavke | Cijeli tim | Medium |

---

## Zaključak

Temelji su postavljeni, tim funkcioniše, isporuka je bila kompletna. Ono što sad trebamo je podići standard na detalje, jer u call centar kontekstu, korisnici rade s alatom svaki dan i svaki broken flow im troši vrijeme. Sljedeći sprint je prilika da pokažemo da možemo isporučivati i kvantitativno i kvalitativno.
