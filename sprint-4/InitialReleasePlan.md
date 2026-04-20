# Pregled release plana

Ovaj dokument definira inicijalni plan isporuke sistema za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra.  
Plan je organiziran u inkremente koji pokrivaju sprintove od 5 do 12.

---

## Pregled inkremenata

| Inkrement | Naziv | Sprintovi | Ključni cilj |
|-----------|------|-----------|-------------|
| **I1** | Osnovni chatbot i transkripti | Sprint 5–6 | Osnovna interakcija korisnika i unos podataka |
| **I2** | Obrada podataka i baza znanja | Sprint 7 | Priprema podataka za AI |
| **I3** | AI chatbot (RAG) | Sprint 8 | Inteligentno odgovaranje |
| **I4** | Audio obrada i glasovni unos | Sprint 9 | Rad sa audio podacima |
| **I5** | Feedback i evaluacija | Sprint 10 | Praćenje kvaliteta |
| **I6** | Administracija i agent workflow | Sprint 11 | Upravljanje i unapređenje |
| **I7** | Finalizacija sistema | Sprint 12 | Privatnost i stabilizacija |

---

# Detalji po inkrementima

---

## Inkrement 1: Osnovni chatbot i transkripti (MVP)

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 1 – Osnovni chatbot i transkripti |
| **Cilj inkrementa** | Omogućiti osnovnu funkcionalnost sistema kroz unos transkripata i komunikaciju korisnika sa chatbotom |
| **Okvirni sprintovi** | Sprint 5–6 |
### Glavne funkcionalnosti

- Implementacija modula za upload transkripata putem fajla i ručni unos (PB 18, US 18.1–18.3)  
- Razvoj osnovnog chat interfejsa za komunikaciju korisnika sa sistemom (PB 22, US 22.1)  
- Implementacija jednostavne logike odgovaranja bez korištenja AI modela (rule-based ili fallback pristup)  
- Mehanizam za prepoznavanje nesigurnosti i prikaz odgovarajuće fallback poruke (PB 31)  
- Prikaz i pregled unesenih transkripata kroz listu (PB 33)  

### Zavisnosti

- Zavisi od autentifikacije i RBAC sistema  
- Potrebna inicijalna struktura baze podataka za pohranu transkripata  
- Osnovna validacija podataka mora biti definisana  

### Glavni rizici

- Loš kvalitet ulaznih transkripata može direktno uticati na kvalitet odgovora (RIZ-001)  
- Fallback mehanizam može biti nedovoljno jasan korisniku i narušiti UX (RIZ-019)  
- Korisnici možda neće koristiti sistem ukoliko odgovori nisu korisni (RIZ-017)  

---

## Inkrement 2: Obrada podataka i baza znanja

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 2 – Obrada podataka i baza znanja |
| **Cilj inkrementa** | Transformisati transkripte u strukturiranu i sigurnu bazu znanja pogodnu za AI obradu |
| **Okvirni sprintovi** | Sprint 7 |

### Glavne funkcionalnosti

- Implementacija parsiranja i normalizacije teksta kako bi podaci bili konzistentni (US 23.1)  
- Razdvajanje transkripata prema ulogama (agent / korisnik) radi boljeg razumijevanja konteksta (US 23.2)  
- Maskiranje osjetljivih podataka prije pohrane i obrade (US 26.1)  
- Generisanje embeddinga iz tekstualnih podataka  
- Kreiranje i upravljanje vektorskom bazom za čuvanje semantičkih reprezentacija (PB 27)  

### Zavisnosti

- Zavisi od kvalitetno unesenih transkripata iz prethodnog inkrementa  
- Potrebna integracija sa servisima za generisanje embeddinga  
- Mora biti ispunjen NFR za privatnost i sigurnost podataka  

### Glavni rizici

- Neadekvatno maskiranje može dovesti do izlaganja ličnih podataka (RIZ-003)  
- Nekvalitetni ili pristrani podaci mogu negativno uticati na AI model (RIZ-026)  
- Kvar u processing pipeline-u može zaustaviti dalji razvoj sistema (RIZ-034)  

---

## Inkrement 3: AI chatbot (RAG)

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 3 – AI chatbot (RAG) |
| **Cilj inkrementa** | Omogućiti inteligentno generisanje odgovora korištenjem baze znanja i LLM modela |
| **Okvirni sprintovi** | Sprint 8 |

### Glavne funkcionalnosti

- Implementacija semantičke pretrage nad vektorskom bazom  
- Prikupljanje relevantnog konteksta za korisnički upit  
- Slanje konteksta i upita LLM modelu  
- Generisanje odgovora na osnovu dostupnih podataka (RAG pristup)  

### Zavisnosti

- Zavisi od embeddinga i vektorske baze iz prethodnog inkrementa  
- Potrebna integracija sa LLM API servisom  

### Glavni rizici

- Chatbot može generisati netačne ili izmišljene odgovore (halucinacije) (RIZ-006)  
- Postoji rizik od curenja podataka kroz model (RAG leakage) (RIZ-028)  
- Performanse sistema mogu biti narušene zbog kompleksnosti pretrage (RIZ-007)  

---

## Inkrement 4: Audio obrada i glasovni unos

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 4 – Audio obrada |
| **Cilj inkrementa** | Omogućiti obradu audio zapisa i interakciju putem glasa |
| **Okvirni sprintovi** | Sprint 9 |

### Glavne funkcionalnosti

- Implementacija konverzije audio zapisa u tekst (US 13.1)  
- Integracija sa eksternim speech-to-text servisima  
- Omogućavanje glasovnog unosa u chatbot interfejsu (US 22.2)  

### Zavisnosti

- Zavisi od eksternih AI servisa za obradu govora  
- Zavisi od postojeće logike obrade teksta  

### Glavni rizici

- Loš kvalitet audio zapisa može dovesti do pogrešne transkripcije (RIZ-010)  
- Zavisnost od eksternih servisa može uticati na dostupnost sistema (RIZ-008)  
- Varijacije u govoru mogu smanjiti tačnost sistema (RIZ-001)  

---

## Inkrement 5: Feedback i evaluacija

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 5 – Feedback i evaluacija |
| **Cilj inkrementa** | Omogućiti mjerenje i unapređenje kvaliteta chatbot odgovora |
| **Okvirni sprintovi** | Sprint 10 |

### Glavne funkcionalnosti

- Omogućavanje korisnicima da ocijene odgovore chatbot-a (US 15.1, 15.2)  
- Implementacija sistema za prijavu netačnih odgovora (US 28.1, 28.2)  
- Logovanje svih interakcija radi analize i poboljšanja sistema  

### Zavisnosti

- Zavisi od funkcionalnog chatbot sistema  
- Potrebna baza za čuvanje interakcija i evaluacija  

### Glavni rizici

- Nedovoljno testiranje može dovesti do lošeg kvaliteta sistema (RIZ-025)  
- Nedostatak auditabilnosti otežava analizu problema (RIZ-022)  
- Korisnici možda neće koristiti opciju feedback-a (RIZ-017)  

---
## Inkrement 6: Administracija i agent workflow

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 6 – Administracija i agent workflow |
| **Cilj inkrementa** | Omogućiti upravljanje sistemom i kontinuirano poboljšanje chatbot-a |
| **Okvirni sprintovi** | Sprint 11 |

### Glavne funkcionalnosti

- Pregled svih pitanja i odgovora kroz administratorski panel (PB 34)  
- Upravljanje prijavljenim problemima i njihov status (PB 35)  
- Filtriranje i pretraga podataka radi lakšeg upravljanja (US 33.3, 35.4)  
- Pregled neodgovorenih pitanja (US 31.1)  
- Omogućavanje agentima da odgovore na pitanja (US 31.2)  
- Dodavanje odgovora u bazu znanja za buduće korištenje (US 31.3)  

### Zavisnosti

- Zavisi od feedback sistema  
- Zavisi od baze podataka i logova  

### Glavni rizici

- Baza znanja može postati zastarjela bez redovnog održavanja (RIZ-004)  
- Nedostatak podataka može smanjiti kvalitet sistema (RIZ-002)  
- Loš fallback može povećati opterećenje agenata (RIZ-019)  

---

## Inkrement 7: Finalizacija sistema

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 7 – Finalizacija sistema |
| **Cilj inkrementa** | Osigurati privatnost korisnika i stabilnost sistema za produkciju |
| **Okvirni sprintovi** | Sprint 12 |

### Glavne funkcionalnosti

- Pregled historije razgovora (US 22.3)  
- Brisanje podataka korisnika (US 22.4)  
- Upravljanje privatnošću (opt-out iz treninga)  
- Finalna optimizacija i stabilizacija sistema  

### Zavisnosti

- Zavisi od logova i baze podataka  
- Mora zadovoljiti sve NFR zahtjeve  

### Glavni rizici

- Neusklađenost sa GDPR regulativama (RIZ-020)  
- Rizik izlaganja ličnih podataka (RIZ-003)  
- Problemi sa dostupnošću sistema (RIZ-023)  

---
