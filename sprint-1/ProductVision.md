# Product Vision

## Naziv projekta
**Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra**

---

## Problem koji sistem rješava
Sistem smanjuje potrebu za ljudskim resursima u call centrima u određenoj mjeri.  
Na taj način štede se resursi, povećava se skalabilnost jer broj poziva nije više ograničen na broj agenata.  
Također, vrijeme poziva postaje neograničeno, sistem je sposoban raditi 24/7.  
Na taj način rješava se problem zavisnosti biznisa od pojedinca.

---

## Ciljni korisnici
- **Agenti**  
  - Podrška klijentima; u slučaju da chatbot nije u stanju odgovoriti na pitanje, prebacuje se na agenta. 
  - Evidentiraju neuspjele odgovore chatbotova i šalju ih administratorima.
  
- **Administratori**  
  - Uploaduje transkript fajlove za treniranje chatbota, primaju neuspjele chatove od agenata, validiraju ih i spremaju za novo treniranje chatbot modela.
  
- **Klijenti**  
  - Korisnici koji koriste usluge call centra.

  - **Menadžment**  
  - Donose odluke i prate performanse sistema.
    
- **Developeri**  
  - Zaduženi za izgradnju, unapređivanje i održavanje sistema.

---

## Vrijednost sistema
- Stalna dostupnost jer ne zavisi od broja agenata ili trenutnih korisnika.  
- Smanjeni troškovi: manji broj agenata plaćen po satu, neovisno o kompleksnosti posla.  
- AI odgovara na osnovna pitanja, a stvarni agenti se fokusiraju na važnije zadatke poput zadržavanja korisnika i pronalaska novih.

---

## Scope MVP verzije
U početni scope ulazi:  
- Transkript, obrada i priprema transkripta za treniranje modela.  
- Implementacija interface-a za sva tri učesnika (agente, administratore, klijente).  
- Logika za prebacivanje sa AI agenta na pravog agenta.  
- Osnovna zaštita identiteta korisnika i osjetljivih podataka.  
- Mogućnost ostavljanja feedback-a od strane korisnika.

---

## Šta ne ulazi u MVP
- Podrška za više jezika.  
- Real-time treniranje modela – model se prvo trenira, pa tek onda pušta u produkciju. Dodatna treniranja i optimizacije se vrše nakon određenog broja prikupljenih podataka ili procjene administratora.  
- Analiza tona i emocije korisnika u realnom vremenu.
- Dictation mode na chatbotu.
- Treniranje AI modela od nule.

---

## Ključna ograničenja i pretpostavke
- **Pravna ograničenja:** radi se o osjetljivim podacima. Potrebno je obavijestiti korisnika da će njegovi privatni podaci korišteni u razgovoru bit zaštićeni.  
- Omogućiti korisniku opciju da njegovi podaci budu uklonjeni i da ne podliježu procesu treniranja modela.  
