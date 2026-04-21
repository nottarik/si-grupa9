# Pregled release plana

Ovaj dokument definira inicijalni plan isporuke sistema za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra.  
Plan je organiziran u inkremente koji pokrivaju sprintove od 5 do 12.

---

## Pregled inkremenata

| Inkrement | Naziv | Sprintovi | Ključni cilj |
|-----------|------|-----------|-------------|
| **I1** | Unos transkripata, obrada podataka i izgradnja baze znanja | Sprint 5–7 | Osnovna interakcija korisnika; Administrator unosi podatke koji se obrađuju i grade bazu znanja |
| **I2** | AI chatbot i prošireni unos | Sprint 8-9 | Korisnici komuniciraju s funkcionalnim RAG chatbotom tekstom i glasom, audio obrada podataka |
| **I3** | Feedback, evaluacija i administracija | Sprint 10-11| Praćenje kvaliteta odgovora i upravljanje sistemom; agenti rješavaju eskalacije |
| **I4** | Finalizacija sistema i korisnički kontrolni mehanizmi | Sprint 12 | Privatnost, GDPR usklađenost i stabilizacija sistema za produkciju |

---

# Detalji po inkrementima

---

## Inkrement 1: Unos transkripata, obrada podataka i izgradnja baze znanja

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 1 – Unos transkripata, obrada podataka i izgradnja baze znanja |
| **Cilj inkrementa** | Omogućiti administratorima unos transkripata u svim podržanim formatima i pretvoriti ih u strukturiranu vektorsku bazu znanja pogodnu za AI obradu. Na kraju ovog inkrementa baza znanja je popunjena i chatbot ima odakle da odgovara — ovo je temelj za sve naredne inkremente |
| **Okvirni sprintovi** | Sprint 5–7 |
### Glavne funkcionalnosti

- Upload transkripata putem fajla (TXT, PDF) s validacijom formata i pohranom (PB-18, US-18.1–18.3)
- Ručni unos transkripata putem forme s obaveznim poljima (datum, agent, sadržaj)
- Konverzija audio zapisa u transkript — integracija s eksternim Speech-to-Text servisima (US-13.1)
- Prikaz i pregled liste unesenih transkripata (PB-33)
- Normalizacija teksta i razdvajanje transkripata po ulogama Agent/Korisnik (US-23.1, US-23.2)
- Maskiranje osjetljivih podataka (JMBG, telefon, ime) prije pohrane i obrade (US-26.1, NFR-3)
- Generisanje embeddinga iz tekstualnih podataka i pohrana u vektorsku bazu (PB-27)
- Retrieval mehanizam — semantička pretraga za RAG pretragu
-  Minimalni administratorski UI za upload, unos i pregled transkripata


### Zavisnosti

- Autentifikacija i RBAC sistem moraju biti funkcionalni
- Inicijalna struktura baze podataka mora biti definisana 
- LLM API i embedding servis moraju biti odabrani i pristup konfigurisan
- NFR zahtjevi za privatnost i sigurnost podataka moraju biti definirani (NFR-3, NFR-4)

### Glavni rizici

- Loš kvalitet ulaznih transkripata narušava bazu znanja i tačnost budućih odgovora (RIZ-001)
- Neadekvatno maskiranje može dovesti do izlaganja ličnih podataka (RIZ-003)
- Nekvalitetni ili pristrani podaci mogu negativno uticati na AI model (RIZ-026)
- Kvar u processing pipeline-u može zaustaviti dalji razvoj sistema (RIZ-034)
- Zavisnost od eksternih Speech-to-Text servisa može uticati na dostupnost sistema (RIZ-008)

---

## Inkrement 2: AI chatbot i prošireni unos

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 2 – AI chatbot i prošireni unos |
| **Cilj inkrementa** | Uvesti kompletnu korisničku interakciju s chatbotom — tekstualnu i glasovnu — s inteligentnim generisanjem odgovora korištenjem RAG pristupa i baze znanja iz prethodnog inkrementa. Na kraju ovog inkrementa sistem je funkcionalan za krajnje korisnike |
| **Okvirni sprintovi** | Sprint 8-9 |

### Glavne funkcionalnosti

- Implementacija semantičke pretrage nad vektorskom bazom i prikupljanje relevantnog konteksta
- Slanje konteksta i upita LLM modelu i generisanje odgovora (RAG pristup)
- Chat UI — web interfejs s poljem za unos pitanja i prikazom odgovora (PB-22, US-22.1)
- AI transparentnost — poruka da korisnik komunicira s AI sistemom (NFR-14)
- Mehanizam za prepoznavanje nesigurnosti odgovora i eskalacija (PB-31, NFR-6)
- Glasovni unos pitanja putem mikrofona (US-22.2)
- Eskalacija korisničkog upita ljudskom agentu 

### Zavisnosti

- Inkrement I1 mora biti završen
- LLM API servis mora biti konfigurisan
- Speech-to-Text servis mora biti konfigurisan  

### Glavni rizici

- Halucinacije modela i netačni odgovori (RIZ-006)
- Curenje podataka kroz model (RIZ-028)
- Spor odziv sistema (RIZ-007)
- Slaba adopcija korisnika ako odgovori nisu korisni (RIZ-017)
- Loš fallback UX (RIZ-019)  

---

## Inkrement 3: Feedback, evaluacija i administracija


| | |
|---|---|
| **Naziv inkrementa** | Inkrement 3 – Feedback, evaluacija i administracija |
| **Cilj inkrementa** | Uvesti mehanizme za praćenje kvaliteta chatbot odgovora i pružiti administratorima i agentima alate za upravljanje sistemom i kontinuirano poboljšanje baze znanja |
| **Okvirni sprintovi** | Sprint 10-11 |

### Glavne funkcionalnosti

- Ocjena odgovora chatbota s komentarom (US-15.1, US-15.2)
- Prijava netačnih odgovora (US-28.1, US-28.2)
- Logovanje svih interakcija (NFR-11)
- Pregled pitanja i odgovora kroz admin panel (PB-34)
- Upravljanje prijavljenim problemima (PB-35)
- Filtriranje i pretraga podataka
- Pregled neodgovorenih pitanja — agent panel (US-31.1)
- Agent odgovara na eskalirana pitanja bez gubitka konteksta (US-31.2)
- Dodavanje odobrenih odgovora u bazu znanja (US-31.3)
- Administratorski dashboard za praćenje kvaliteta sistema

### Zavisnosti

- Inkrement I2 mora biti završen
- Mora postojati funkcionalna baza za feedback i logove
- Fallback mehanizam mora raditi  

### Glavni rizici

- Korisnici ne koriste feedback opcije (RIZ-017)
- Nepotpuni logovi otežavaju analizu (RIZ-022)
- Zastarjela baza znanja (RIZ-004)
- Nekvalitetni agentovi odgovori bez validacije (RIZ-002) 

---

## Inkrement 4: Finalizacija i korisnički kontrolni mehanizmi

| | |
|---|---|
| **Naziv inkrementa** | Inkrement 4 – Finalizacija i korisnički kontrolni mehanizmi |
| **Cilj inkrementa** | Implementirati finalne korisničke kontrole nad podacima, ispuniti GDPR zahtjeve i stabilizovati sistem za produkcijsko puštanje |
| **Okvirni sprintovi** | Sprint 12 |

### Glavne funkcionalnosti

- Pregled historije razgovora (US-22.3)
- Brisanje podataka iz historije (US-22.4)
- Opt-out iz korištenja razgovora za treniranje
- Finalna optimizacija i bug fixing
- Korisnička i tehnička dokumentacija
- Finalna optimizacija korisničkog interfejsa

### Zavisnosti

- Svi prethodni inkrementi moraju biti završeni
- Logovi i baza podataka moraju biti stabilni
- Svi NFR zahtjevi moraju biti zadovoljeni  

### Glavni rizici

- Neusklađenost sa GDPR pravilima (RIZ-020)
- Rizik izlaganja ličnih podataka (RIZ-003)
- Problemi sa dostupnošću kasno otkriveni (RIZ-023)

---




