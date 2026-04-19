# Definition of Done
## Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra

Skup kriterija koji moraju biti ispunjeni kako bi se određena stavka smatrala završenom.

---

## Template

Stavka se smatra završenom kada su ispunjeni sljedeći uslovi:

- Funkcionalnost je implementirana ili dokumentovana u skladu sa dogovorenim zahtjevima
- Svi definisani Acceptance Criteria su u potpunosti ispunjeni
- Implementacija je pregledana od strane tima
- Funkcionalnost je adekvatno testirana
- Promjene su evidentirane u relevantnim projektnim artefaktima
- Funkcionalnost je spremna za demonstraciju u okviru sprint review-a

---

## Kriteriji

### Implementacija i funkcionalnost

- Funkcionalnost je implementirana u skladu sa definisanim zahtjevima i user story-em
- Svi definisani Acceptance Criteria su u potpunosti ispunjeni
- Svi rubni slučajevi su pokriveni (npr. neispravni unosi, prazna polja, neautorizovan pristup, nevalidan format fajla)
- Nova funkcionalnost je integrisana sa ostatkom sistema i ne narušava postojeće funkcionalnosti
- Uloge korisnika su pravilno implementirane — Korisnik call centra, Agent call centra i Administrator imaju odgovarajuće nivoe pristupa (RBAC)
- Autentifikacija i autorizacija rade ispravno; sesija ističe nakon 30 minuta neaktivnosti, a nalog se blokira nakon 5 uzastopnih neuspjelih pokušaja prijave (NFR-2)

### Sigurnost i privatnost

- Sva komunikacija između klijenta i servera odvija se isključivo putem HTTPS/TLS protokola (minimalno TLS 1.2) (NFR-1)
- Lični podaci (ime, telefon, JMBG, email) su maskirani ili uklonjeni iz transkripata prije obrade i pohrane (NFR-3)
- Originalni nemaskirani transkripti se ne čuvaju duže od 24 sata od trenutka unosa (NFR-3)
- Korisnik ima mogućnost opt-out opcije za korištenje njegovih podataka u svrhu treniranja modela (NFR-4)
- Chatbot ne izlaže sirove transkripte krajnjem korisniku — odgovara isključivo na osnovu procesiranih unosa iz baze znanja

### Testiranje

- Unit testovi su napisani i uspješno prolaze; ciljna pokrivenost je minimalno 80% za poslovnu logiku (Jest / PyTest)
- Integracioni testovi pokrivaju ključne tokove (npr. upload transkripta → obrada → pohrana, postavljanje pitanja → odgovor chatbota → eskalacija na agenta)
- UI/E2E testovi potvrđuju ispravno ponašanje interfejsa za sve korisničke uloge (Playwright)
- Nema kritičnih ni visokih bugova koji sprečavaju osnovno korištenje sistema
- Poznati problemi su dokumentovani (ako postoje)
- Rezultati testiranja su evidentirani u strukturiranom formatu (ID testa, ulazni podaci, očekivani rezultat, stvarni rezultat, status PASS/FAIL)

### Specifično za AI komponente

- Chatbot generiše odgovor koristeći RAG pristup — isključivo na osnovu sadržaja baze znanja
- Ako je skor pouzdanosti odgovora ispod 70%, sistem jasno naznačuje nesigurnost i nudi eskalaciju na agenta (NFR-6)
- Fallback mehanizam je testiran — preusmjeravanje na agenta odvija se u roku od 10 sekundi bez gubitka konteksta razgovora (NFR-5)
- Svaka funkcionalnost koja koristi AI ima evidentiran unos u AI Usage Log

### Dokumentacija i evidencija

- Kod je komentarisan tamo gdje je to potrebno
- Product Backlog je ažuriran ako je bilo promjena u opsegu
- Sprint Backlog reflektuje stvarno stanje
- Sve važne tehničke i dizajnerske odluke su evidentirane u Decision Logu
- Svaka nova AI interakcija je evidentirana u AI Usage Logu

### Tehnička ispravnost

- Podaci se ispravno čuvaju i ažuriraju u bazi podataka
- API endpointi rade prema specifikaciji
- Validacija podataka je implementirana na backendu
- Forma validacije radi ispravno (obavezna polja, format email-a, format fajla)
- Greške se prikazuju korisniku na jasan i razumljiv način
- Kod je pushovan na repozitorij i build prolazi bez grešaka
- Nema očiglednih problema sa performansama (odziv ne prelazi 3 sekunde u 95% slučajeva) (NFR-7)

### Kvalitet i demonstracija

- Implementacija je pregledana od strane tima (code review)
- UI odgovara funkcionalnim zahtjevima i korisničkim ulogama
- Aplikacija je upotrebljiva za sve tri korisničke uloge bez dodatne obuke (NFR-10)
- Sistem se može pokrenuti bez problema na svim razvojnim okruženjima članova tima
- Funkcionalnost se može demonstrirati u predviđenom okruženju bez ručnih prilagodbi
