# Sprint Review Summary  

---

## Pregled sprinta

Cilj Sprinta 8 bio je omogućiti potpunu funkcionalnost chatbot sistema kroz povezivanje baze znanja, LLM obrade upita i komunikacije između korisnika i agenata u realnom vremenu. Fokus sprinta bio je na implementaciji RAG retrieval sistema, agent panela, escalation queue-a, WebSocket komunikacije i dodatnih funkcionalnosti koje poboljšavaju korisničko iskustvo poput glasovnog unosa i historije razgovora.

---

## Isporučene stavke

| ID   | Naziv stavke                                                        | Tip              | Prioritet | Status    |
|------|---------------------------------------------------------------------|------------------|-----------|----------|
| PB-13 | Upload audio fajlova i automatska transkripcija                   | Feature          | High      | Završeno |
| PB-22 | Glasovni unos u chat (mikrofon)                                   | Feature          | High      | Završeno |
| PB-48 | Escalation queue u admin panelu                                    | Feature          | High      | Završeno |
| PB-49 | Historija razgovora korisnika                                      | Feature          | Medium    | Završeno |
| PB-50 | Automatska odjava agenta pri završetku korisničke sesije          | Technical Task   | High      | Završeno |
| PB-51 | Agent panel s Live Queue i pristupom bazi znanja                  | Feature          | High      | Završeno |
| PB-52 | RAG retrieval i LLM klasifikacija upita                            | Feature          | High      | Završeno |
| PB-53 | LLM za općenita pitanja i usmjeravanje na agenta                  | Feature          | High      | Završeno |
| PB-54 | WebSocket komunikacija između korisnika i agenta                 | Feature          | High      | Završeno |
| PB-55 | Resolving chatova                                                  | Feature          | Medium    | Završeno |

---

## Šta je završeno

Tokom sprinta uspješno su implementirane funkcionalnosti koje omogućavaju rad chatbot sistema u stvarnim scenarijima komunikacije između korisnika i agenata.

Implementiran je **escalation queue** kroz koji administratori i agenti mogu pratiti eskalirane korisničke zahtjeve. Dodan je zaseban **agent panel** sa Live Queue prikazom aktivnih razgovora i pristupom bazi znanja tokom komunikacije s korisnicima.

Sistem sada podržava **RAG retrieval** i **LLM klasifikaciju korisničkih upita**. Kada chatbot pronađe relevantan sadržaj u bazi znanja, koristi ga za odgovor korisniku, dok u slučajevima kada odgovor nije dostupan korisnika usmjerava prema agentu.

Realizovana je **WebSocket komunikacija** između korisnika i agenata, čime je omogućena razmjena poruka u realnom vremenu bez potrebe za osvježavanjem stranice. Dodana je i funkcionalnost **resolving chatova** radi pravilnog zatvaranja razgovora i upravljanja sesijama.

Korisničko iskustvo unaprijeđeno je kroz **glasovni unos putem mikrofona**, pregled **historije razgovora** i mogućnost **upload-a audio fajlova sa automatskom transkripcijom**.

---

## Šta nije završeno


Sve planirane stavke Sprinta 8 su uspješno završene i demonstrirane 

---

## Demonstrirane funkcionalnosti ili artefakti

Tokom sprint review sastanka demonstrirane su sljedeće funkcionalnosti:

- Escalation queue u admin panelu  
- Agent panel sa Live Queue prikazom  
- WebSocket komunikacija između korisnika i agenata  
- Glasovni unos putem mikrofona  
- Historija korisničkih razgovora  
- Upload audio fajlova i automatska transkripcija  
- RAG retrieval i LLM klasifikacija upita  
- Preusmjeravanje korisnika prema agentu  
- Resolving i zatvaranje chat sesija  
- Automatska odjava agenta po završetku sesije  

---

## Glavni problemi i blokeri

Najveći izazov tokom sprinta bio je povezivanje više različitih komponenti sistema u jedinstven workflow koji uključuje chatbot, bazu znanja, agente i real-time komunikaciju.

Posebna pažnja bila je potrebna prilikom implementacije WebSocket komunikacije kako bi se osigurala stabilna razmjena poruka i pravilno zatvaranje sesija bez ostavljanja aktivnih konekcija.

Dodatni izazov predstavljalo je usklađivanje RAG retrieval sistema i LLM klasifikacije kako bi chatbot mogao pravilno razlikovati upite na koje može odgovoriti od onih koje treba eskalirati agentu.

---

## Ključne odluke donesene u sprintu

- Za komunikaciju između korisnika i agenata korišten je WebSocket pristup radi omogućavanja real-time razmjene poruka.  
- Agent panel implementiran je kao zaseban dio sistema odvojen od administratorskog panela.  
- Chatbot ne generiše odgovore kada ne postoji relevantan sadržaj u bazi znanja, već korisnika usmjerava prema agentu.  
- Upload audio fajlova povezan je sa automatskom transkripcijom prije pohrane podataka.  
- Završeni razgovori označavaju se kao resolved radi lakšeg upravljanja historijom sesija.  

---

## Povratna informacija Product Ownera

Product Owner je pozitivno ocijenio implementaciju real-time komunikacije, agent panela i integraciju baze znanja sa chatbot sistemom.

Tokom review sastanka naglašeno je da tim treba nastaviti pojačavati tempo razvoja projekta i paralelno raditi na većem broju user storija i Product Backlog stavki u narednim sprintovima.

---

## Zaključak za naredni sprint

Sprint 8 uspješno je povezao chatbot sistem, bazu znanja i komunikaciju između korisnika i agenata u jednu funkcionalnu cjelinu. Sistem sada podržava klasifikaciju upita, eskalaciju prema agentima i komunikaciju u realnom vremenu.

Za Sprint 9 planirano je dodatno poboljšati performanse sistema i dodati nove funkcionalnosti koje će olakšati korištenje aplikacije i unaprijediti ukupno korisničko iskustvo.