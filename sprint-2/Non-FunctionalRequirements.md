## Non-Functional Requirements (NFR)

| ID | Kategorija | Opis zahtjeva | Kako će se provjeriti | Prioritet | Napomena |
|----|------------|--------------|-----------------------|----------|----------|
| 1 | Sigurnost | Sva komunikacija između klijenta i servera mora biti šifrirana putem HTTPS/TLS protokola | Provjera SSL/TLS certifikata i testiranje da li su svi endpointi dostupni isključivo putem HTTPS-a | High | |
| 2 | Sigurnost | Administratorski dio sistema mora biti zaštićen i dostupan samo ovlaštenim korisnicima uz implementaciju autentifikacije i Role-Based Access Control (RBAC) | Pokušaji neautorizovanog pristupa i provjera kontrole pristupa za različite korisničke uloge | High | |
| 3 | Privatnost | Prije korištenja podataka za treniranje chatbot-a, potrebno je ukloniti ili maskirati sve lične podatke iz transkripata (npr. imena, brojeve telefona, email adrese) | Testiranje sa primjerima transkripata koji sadrže lične podatke i provjera da li su podaci uklonjeni ili maskirani u bazi | High | |
| 4 | Privatnost | Razgovori se mogu koristiti za unapređenje sistema, ali korisnik mora imati mogućnost da to odbije (opt-out) | Provjera kroz UI i testiranje opcije odjave, uključujući provjeru da se podaci tog korisnika više ne koriste za treniranje modela | High | |
| 5 | Pouzdanost | Ako chatbot ne može riješiti korisnički zahtjev ili dođe do greške u radu sistema, razgovor se mora automatski preusmjeriti na ljudskog agenta bez gubitka konteksta | Testiranje scenarija sa greškama i kompleksnim upitima i provjera da li se kontekst prenosi na agenta | High | |
| 6 | Pouzdanost | Chatbot ne smije generisati izmišljene ili netačne informacije; u slučaju nesigurnosti mora jasno naznačiti da nema pouzdan odgovor | Testiranje sa pitanjima van baze znanja i analiza odgovora sistema | High | |
| 7   | Performanse | Sistem mora odgovoriti na korisnički upit u roku od maksimalno 3 sekunde u 95% slučajeva | Load testiranje sa simulacijom više korisnika i mjerenje vremena odziva | High |  |
| 8   | Skalabilnost | Sistem mora da podržava istovremeno najmanje 100 aktivnih korisnika bez značajnog pada performansi | Stres testiranje i simulacija opterećenja | High |  |
|  9   | Dostupnost | Sistem mora biti dostupan najmanje 99% vremena | Monitoring uptime-a i logova| High | Sistem treba raditi 24/7 |
| 10   | Upotrebljivost | Korisnički interfejs chatbot-a mora biti jednostavan za korištenje i omogućiti korisniku da postavi pitanje bez dodatne obuke | User testing sa stvarnim korisnicima | Medium |  | 
| 11   | Auditabilnost | Sistem mora čuvati logove svih interakcija (upita i odgovora) radi analize i poboljšanja sistema | Vršit će se provjera log baze i zapisa interakcija | High |  |
| 12        | Održavanje | Sistem mora omogućiti jednostavno dodavanje novih transkripata i ponovno treniranje modela bez prekida rada sistema | Testiranje procesa dodavanja novih podataka i update-a modela | Medium |  |
| 13        | Tačnost | Chatbot mora davati relevantne odgovore u najmanje 85% testiranih slučajeva na definisanom skupu pitanja | Testiranje na unaprijed definisanom setu pitanja i  poređenja sa očekivanim odgovorima | High |  |
| 14        | Transparentnost | Sistem mora na početku konverzacije korisniku jasno naznačiti da komunicira sa AI asistentom | Pregled pozdravne poruke chatbot-a | High | Etička i pravna obaveza |
