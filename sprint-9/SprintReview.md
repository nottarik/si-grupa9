# Sprint Review Summary

Sprint 9

---

## Pregled sprinta

Cilj Sprinta 9 bio je stabilizacija sistema, unapređenje kvaliteta podataka i priprema aplikacije za produkcijsko okruženje. Fokus sprinta bio je na poboljšanju baze znanja, kvalitetnijem maskiranju osjetljivih podataka, optimizaciji performansi chatbota, unapređenju korisničkog iskustva te provođenju završnog funkcionalnog i regresijskog testiranja.

---

## Isporučene stavke

| ID | Naziv stavke | Prioritet | Status |
|----|--------------|-----------|--------|
| PB-56 | Poboljšanje maskiranja PII podataka i ekstrakcije Q&A parova | High | Završeno |
| PB-57 | Ocjena razgovora po završetku sesije | High | Završeno |
| PB-58 | Sistemske obavijesti u chatbotu | Medium | Završeno |
| PB-59 | Mogućnost ručnog unosa Q&A para direktno u bazu znanja | High | Završeno |
| PB-60 | Pregled i kuriranje sadržaja baze znanja | High | Završeno |
| PB-61 | Optimizacija performansi chatbota | High | Završeno |
| PB-62 | Prikaz komentara uz ocjene razgovora u admin i agent panelu | Medium | Završeno |
| PB-63 | End-to-end i regresijsko testiranje sistema | High | Završeno |
| PB-64 | User Settings | Medium | Završeno |
| PB-65 | Brisanje pojedinačnog chata iz historije | Medium | Završeno |

---

## Šta je završeno?

Tokom Sprinta 9 uspješno su realizovane sve planirane funkcionalnosti. Poboljšano je maskiranje osjetljivih podataka i unaprijeđena ekstrakcija Q&A parova kako bi sadržaj pohranjen u bazi znanja bio kvalitetniji i relevantniji za chatbot odgovore.

Administratorima je omogućeno ručno upravljanje bazom znanja kroz dodavanje novih Q&A parova, pregled postojećeg sadržaja i uklanjanje nevažećih unosa. Na taj način omogućena je bolja kontrola nad kvalitetom informacija koje chatbot koristi prilikom odgovaranja korisnicima.

Implementirana je mogućnost ocjenjivanja razgovora po završetku sesije zajedno sa prikazom komentara koje korisnici ostavljaju uz ocjene. Dodane su sistemske obavijesti u chatbotu, User Settings funkcionalnosti te mogućnost brisanja pojedinačnih razgovora iz historije.

Izvršena je optimizacija performansi chatbota, a kompletan sistem prošao je end-to-end i regresijsko testiranje kako bi se osigurala stabilnost i spremnost za produkcijsko okruženje.

---

## Šta nije završeno?

Sve planirane stavke Sprinta 9 su uspješno završene i uspješno demonstrirane tokom sastanka.

---

## Demonstrirane funkcionalnosti ili artefakti

- Poboljšano maskiranje PII podataka
- Unaprijeđena ekstrakcija Q&A parova
- Ručni unos Q&A parova u bazu znanja
- Pregled i kuriranje sadržaja baze znanja
- Ocjenjivanje razgovora po završetku sesije
- Prikaz komentara uz ocjene razgovora
- Sistemske obavijesti u chatbotu
- User Settings
- Brisanje pojedinačnog razgovora iz historije
- Optimizovane performanse chatbota
- Rezultati end-to-end i regresijskog testiranja

---

## Glavni problemi i blokeri

Najveći izazov tokom sprinta bio je osigurati visok kvalitet podataka koji ulaze u bazu znanja. Posebna pažnja posvećena je testiranju različitih formata osjetljivih podataka i validaciji generisanih Q&A parova kako bi se smanjila mogućnost pojave neispravnih ili nepotpunih informacija.

Dodatni izazov predstavljalo je provođenje regresijskog testiranja velikog broja funkcionalnosti implementiranih u prethodnim sprintovima kako bi se osiguralo da nove izmjene ne uzrokuju probleme u postojećim dijelovima sistema.

---

## Ključne odluke donesene u sprintu

- Omogućeno je ručno upravljanje sadržajem baze znanja od strane administratora.
- Sistem ocjenjivanja razgovora proširen je komentarima korisnika.
- Sistemske obavijesti implementirane su kao centralizovani mehanizam komunikacije prema korisnicima.
- Optimizacija performansi provedena je prije završnog testiranja sistema.
- Regresijsko testiranje postavljeno je kao obavezna aktivnost prije produkcijske isporuke.

---

## Povratna informacija Product Ownera

Product Owner je pozitivno ocijenio unapređenja vezana za kvalitet baze znanja, stabilnost sistema i poboljšanja korisničkog iskustva.

Kao preporuku za naredni period predloženo je implementiranje dodatnih user storija kako bi aplikacija postala još više automatizirana i zahtijevala manje ručnih aktivnosti od strane korisnika i administratora.

Posebno su istaknute sljedeće ideje za budući razvoj:

- Batch procesiranje fajlova sa web lokacija (S3, Google Drive i slični izvori) kroz on-demand i scheduled obradu.
- Potpuno automatizovan pipeline za transkripciju, prečišćavanje podataka, kreiranje i unapređenje baze znanja uz vidljiv napredak obrade u chatbotu.
- Single-click deployment rješenje za cloud platforme kao što su Azure ili AWS.

---

## Zaključak za naredni sprint

Sprint 9 uspješno je unaprijedio kvalitet podataka, administraciju baze znanja, performanse sistema i korisničko iskustvo. Završene funkcionalnosti dodatno su približile aplikaciju produkcijskoj spremnosti.

U narednom periodu fokus će biti na daljoj automatizaciji procesa, unapređenju infrastrukture i implementaciji novih funkcionalnosti koje će pojednostaviti upravljanje sistemom i povećati efikasnost rada aplikacije.