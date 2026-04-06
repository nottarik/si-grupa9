## Non-Functional Requirements (NFR)

| ID | Kategorija | Opis zahtjeva | Kako će se provjeriti | Prioritet | Napomena |
|----|------------|--------------|-----------------------|----------|----------|
| NFR-1   |            |              |                       |          |          |
| NFR-2   |            |              |                       |          |          |
| NFR-3   |            |              |                       |          |          |
| NFR-4   |            |              |                       |          |          |
| NFR-5   |            |              |                       |          |          |
| NFR-6   |            |              |                       |          |          |
| NFR-7   | Performanse | Sistem mora odgovoriti na korisnički upit u roku od maksimalno 3 sekunde u 95% slučajeva | Load testiranje sa simulacijom više korisnika i mjerenje vremena odziva | Visok | Ovo je vrlo važno za korisničko iskustvo |
| NFR-8   | Skalabilnost | Sistem mora da podržava istovremeno najmanje 100 aktivnih korisnika bez značajnog pada performansi | Stres testiranje i simulacija opterećenja | Visok | Ovo je važno podržati iz razloga što call centri imaju veliki broj korisnika |
| NFR-9   | Dostupnost | Sistem mora biti dostupan najmanje 99% vremena | Monitoring uptime-a i logova| Visok | Sistem treba raditi 24/7 |
| NFR-10   | Upotrebljivost | Korisnički interfejs chatbot-a mora biti jednostavan za korištenje i omogućiti korisniku da postavi pitanje bez dodatne obuke | User testing sa stvarnim korisnicima | Srednji | Bitno je za krajnje korisnike | 
| NFR-11   | Auditabilnost | Sistem mora čuvati logove svih unterakcija (upita i odgovora) radi analize i poboljšanja sistema | Vršit će se provjera log baze i zapisa interakcija | Visok | Važno kako bi se chatbot unapredio |
| NFR-12        | Održavanje | Sistem mora omogućiti jednostavno dodavanje novih transkripata i ponovno treniranje modela bez prekida rada sistema | Testiranje procesa dodavanja novih podataka i update-a modela | Srednji | Bitno za dugoročni razvoj |
| NFR-13        | Tačnost | Chatbot mora davati relevantne odgovore u najmanje 85% testiranih slučajeva na definisanom skupu pitanja | Testiranje na unaprijed definisanom setu pitanja i  poređenja sa očekivanim odgovorima | Visok | Ključno za kvalitet sistema i zadovoljstvo korisnika a takođe i za smanjenje opterećenja agenata |
| NFR-14        | Transparentnost | Sistem mora na početku konverzacije korisniku jasno naznačiti da komunicira sa AI asistentom | Pregled pozdravne poruke chatbot-a | Visok | Etička i pravna obaveza |
