# Sprint Review Summary

**Datum pregleda:** 9. maj 2026


---

## Pregled sprinta

Sprint 6 je uspješno završen. Svih osam planiranih stavki isporučeno je u statusu Završeno, što predstavlja pun kapacitet sprinta u skladu s definicijom dovršenosti. Tim je u ovom sprintu zatvorio ključne funkcionalne praznine koje su ostale nakon Sprinta 5: transkripti sada imaju potpun životni ciklus (unos, pregled, uređivanje, pretraga, brisanje), administrator ima kontrolu nad korisničkim nalozima i ulogama, dashboard prikazuje stvarne podatke iz baze, a validacija formata osigurava integritet podataka koji ulaze u pipeline.

---

## Isporučene stavke

| ID | Naziv stavke | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-----|-----------|-----------------|--------|
| PB-34 | Pregled postavljenih pitanja i odgovora | Feature | High | 3 | Završeno |
| PB-38 | Uređivanje postojećih transkripata | Feature | High | 5 | Završeno |
| PB-39 | Brisanje transkripata s potvrdom akcije | Feature | High | 3 | Završeno |
| PB-40 | Filtriranje i pretraga transkripata | Feature | High | 5 | Završeno |
| PB-41 | Dodjela i upravljanje ulogama korisnika | Feature | High | 5 | Završeno |
| PB-42 | Pregled i brisanje korisnika | Feature | High | 5 | Završeno |
| PB-43 | Dashboard s aktuelnim podacima | Feature | Medium | 3 | Završeno |
| PB-44 | Validacija formata transkripata | Technical Task | High | 3 | Završeno |

---

## Istaknuta dostignuća

### Potpun životni ciklus transkripata (PB-38, PB-39, PB-40)
Upravljanje transkriptima dobilo je sve funkcionalnosti koje su nedostajale za svakodnevni rad. Implementirano je uređivanje sadržaja i metapodataka, trajno brisanje uz obaveznu potvrdu koja sprečava slučajno brisanje, te pretraga i filtriranje po ključnoj riječi. Ovo je zaokružilo tok koji je Sprint 5 otvorio s uploadom i pregledom.

### Upravljanje korisnicima i ulogama (PB-41, PB-42)
Implementirana je nova administratorska funkcionalnost: pregled liste svih registrovanih korisnika, dodjela i izmjena uloga te brisanje korisničkih naloga uz potvrdu. Promjena uloge stupa na snagu odmah — korisnik gubi ili dobija pristup bez odlaganja. Administrator ne može obrisati vlastiti nalog, što sprečava slučajno zaključavanje sistema.

### Dashboard s aktuelnim podacima (PB-43)
Hardkodirane vrijednosti na dashboardu zamijenjene su stvarnim agregatima iz baze podataka. Administrator sada na prvom ekranu vidi tačan broj transkripata, registrovanih korisnika i interakcija s chatbotom, bez potrebe za prelaskom na zasebne module.

### Validacija formata transkripata (PB-44)
Sistem sada odbija svaki transkript koji ne prati propisanu `Agent:` / `Korisnik:` strukturu i prikazuje jasnu poruku greške. Validacija radi i za upload fajla i za ručni unos. Ovo je tehnički preduvjet za ispravan rad pipeline obrade u kasnijim sprintovima.

---

## Zaključak

Tim je isporučio cijeli planirani opseg bez prenošenja stavki. Sprint 6 je zatvorio sve funkcionalne praznine administratorskog panela i postavio stabilnu osnovu za naredne sprintove koji se fokusiraju na AI pipeline i RAG funkcionalnost. Posebno se ističe dosljedno testiranje RBAC pravila — brisanje transkripata i upravljanje korisnicima ispravno je ograničeno na administratore, što je potvrđeno i automatizovanim testovima.

Sljedeći sprint gradi se na ovim temeljima s fokusom na preprocessing pipeline i obradu PII podataka.
