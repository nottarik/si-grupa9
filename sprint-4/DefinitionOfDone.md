# Definition of Done
## Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra

Stavka se smatra završenom kada su ispunjeni sljedeći kriteriji.

---

## Osnovni kriteriji

| Kategorija | Kriterij |
|---|---|
| **Funkcionalnost** | Funkcionalnost je implementirana ili dokumentovana u skladu sa definisanim zahtjevima |
| **Funkcionalnost** | Svi definisani Acceptance Criteria su u potpunosti ispunjeni |
| **Funkcionalnost** | Funkcionalnost je usklađena sa odgovarajućim user story-jem, use case-om i poslovnim pravilima sistema |
| **Integracija** | Nova funkcionalnost je povezana sa relevantnim dijelovima sistema i ne narušava postojeće funkcionalnosti |
| **Uloge i pristup** | Autentifikacija, autorizacija i RBAC rade ispravno za odgovarajuće korisničke uloge |
| **Podaci** | Podaci se ispravno unose, validiraju, čuvaju, ažuriraju, brišu ili prikazuju, zavisno od prirode funkcionalnosti |
| **Validacija** | Pokriveni su osnovni pozitivni i negativni scenariji, uključujući neispravne unose, prazna polja i neautorizovan pristup |
| **Backend** | API endpointi i poslovna logika rade prema definisanoj specifikaciji, ako su primjenjivi |
| **Frontend / UI** | Korisnički interfejs odgovara funkcionalnim zahtjevima i podržava jasan tok korištenja, ako je primjenjivo |
| **UX** | Greške, upozorenja i prazna stanja prikazuju se korisniku na jasan i razumljiv način |
| **Testiranje** | Funkcionalnost je adekvatno testirana u skladu sa vrstom stavke i rizikom koji nosi |
| **Testiranje** | Ključni testni slučajevi i rezultati testiranja su evidentirani |
| **Kvalitet** | Nema kritičnih ni visokih bugova koji onemogućavaju osnovno korištenje funkcionalnosti |
| **Kvalitet** | Poznati problemi i ograničenja su dokumentovani, ako postoje |
| **Code Review** | Implementacija je pregledana od strane tima |
| **Code Review** | Pull request je odobren i svi relevantni komentari su riješeni |
| **Kod i build** | Kod je pushovan na repozitorij i build prolazi bez grešaka |
| **Dokumentacija** | Dokumentacija je ažurirana ako promjena utiče na API, bazu podataka, poslovna pravila, UI ili korisnički tok |
| **Artefakti** | Promjene su evidentirane u relevantnim projektnim artefaktima |
| **Backlog** | Product Backlog i Sprint Backlog reflektuju stvarno stanje stavke |
| **Odluke** | Važne tehničke i dizajnerske odluke su evidentirane u Decision Log-u, ako je primjenjivo |
| **Spremnost za isporuku** | Funkcionalnost se može pokrenuti i demonstrirati u predviđenom okruženju bez dodatnih ručnih prilagodbi |
| **Demo** | Funkcionalnost je spremna za demonstraciju u okviru sprint review-a |
| **Validacija** | Tim smatra da je stavka završena i spremna za prihvatanje od strane Product Ownera / supervizora |

---

## Dodatno za AI funkcionalnosti
Primjenjuje se samo na stavke koje uključuju chatbot, transkripte, obradu podataka, bazu znanja, fallback ili eskalaciju.

| Kategorija | Kriterij |
|---|---|
| **Sigurnost i privatnost** | Komunikacija između klijenta i servera odvija se putem sigurnih protokola u skladu sa definisanim sigurnosnim zahtjevima |
| **Sigurnost i privatnost** | Lični i osjetljivi podaci u transkriptima su uklonjeni ili maskirani prije dalje obrade, kada je to primjenjivo |
| **Sigurnost i privatnost** | Korištenje podataka za unapređenje sistema poštuje definisana pravila privatnosti i opt-out mehanizme |
| **AI ponašanje** | Chatbot daje odgovor na osnovu odobrenih i relevantnih izvora znanja predviđenih sistemom |
| **AI ponašanje** | Kada sistem nije dovoljno siguran u odgovor, korisniku jasno prikazuje nesigurnost ili fallback odgovor |
| **Fallback / eskalacija** | Eskalacija na ljudskog agenta radi ispravno i bez gubitka relevantnog konteksta, kada je predviđena funkcionalnošću |
| **Obrada transkripata** | Obrada transkripata je izvršena u skladu sa pravilima sistema, uključujući validaciju, pripremu i zaštitu podataka |
| **Baza znanja** | Novi ili izmijenjeni unosi u bazu znanja su pregledani, validirani i evidentirani prije upotrebe, kada je to primjenjivo |
| **Auditabilnost** | Relevantne AI interakcije, promjene i odluke su evidentirane u AI Usage Log-u ili drugim predviđenim zapisima |
| **Testiranje AI funkcija** | Testirani su ključni AI scenariji, uključujući netačan odgovor, fallback, eskalaciju i obradu transkripta, kada su primjenjivi |
| **Performanse i pouzdanost** | Funkcionalnost zadovoljava relevantne nefunkcionalne zahtjeve definisane za tu stavku |

---

## Napomena za primjenu

| Vrsta stavke | Primjena DoD-a |
|---|---|
| **Documentation / research stavke** | Primjenjuje se samo osnovni DoD, bez AI-specifičnih kriterija osim ako stavka direktno obrađuje AI logiku ili privatnost |
| **Technical task / feature** | Primjenjuje se osnovni DoD, a dodatni AI kriteriji samo ako stavka uključuje chatbot, transkripte, bazu znanja ili fallback |
| **AI funkcionalnosti** | Primjenjuju se i osnovni i dodatni AI kriteriji |