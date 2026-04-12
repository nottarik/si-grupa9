# Architecture Overview

## 1. Arhitektonski pristup

Sistem je dizajniran kao **modularni monolit**, gdje su sve funkcionalnosti implementirane unutar jedne aplikacije, ali jasno razdvojene po modulima sa definisanim odgovornostima.  

Ovakav pristup je odabran jer omogućava:
- brži razvoj MVP-a  
- jednostavnije testiranje  
- manju operativnu kompleksnost u ranim fazama projekta  

Arhitektura prati **slojeviti (layered) pristup**:

- **Presentation sloj (UI)** – korisnički interfejs (Chat UI i Admin Dashboard)  
- **Application sloj** – poslovna logika i obrada podataka  
- **Data sloj** – baza podataka i integracija sa eksternim servisima  

Sistem dodatno integriše **LLM i RAG pristup** kroz poseban servisni sloj, čime se omogućava generisanje kontekstualno relevantnih odgovora bez treniranja modela od nule.

---

## 2. Glavne komponente sistema

| Komponenta | Tip | Opis |
|---|---|---|
| Authentication modul | Backend | Autentifikacija i autorizacija korisnika |
| Transcript Management modul | Backend | Upravljanje transkriptima i audio zapisima |
| Processing Pipeline modul | Backend | Obrada i transformacija podataka |
| Knowledge Base modul | Backend / Data | Embeddingi i pretraga |
| Chatbot modul | Backend | RAG obrada upita |
| Feedback & Evaluation modul | Backend | Prikupljanje feedbacka |
| Admin Dashboard modul | Frontend + Backend | Administracija i pregled podataka |
| Database i storage sloj | Data sloj | Pohrana svih podataka |
| Eksterni AI servisi | Eksterni | LLM, Speech-to-Text i embedding modeli |

---

## 3. Odgovornosti komponenti

### 3.1 Authentication modul
Upravlja prijavom, autentifikacijom i autorizacijom korisnika (admin, agent, korisnik).

---

### 3.2 Transcript Management modul
Omogućava upload, unos i pregled transkripata i audio zapisa.

---

### 3.3 Processing Pipeline modul
Zadužen za obradu transkripata kroz više faza:
- normalizacija teksta  
- razdvajanje po ulogama  
- maskiranje osjetljivih podataka  

---

### 3.4 Knowledge Base modul
- generisanje embeddinga  
- pohrana u vektorsku bazu  
- omogućavanje semantičke pretrage  

---

### 3.5 Chatbot modul
Obrada korisničkih upita koristeći RAG pristup:
- pretraga relevantnih informacija  
- slanje konteksta LLM-u  
- generisanje odgovora  

---

### 3.6 Feedback & Evaluation modul
Prikuplja:
- ocjene korisnika  
- komentare  
- prijave netačnih odgovora  

---

### 3.7 Admin Dashboard modul
Omogućava administratoru:
- pregled transkripata  
- pregled pitanja i odgovora  
- analizu prijavljenih problema  

---

### 3.8 Database i storage sloj
Pohranjuje:
- korisnike  
- transkripte  
- interakcije  
- ocjene i prijave  

---

### 3.9 Eksterni AI servisi
- Speech-to-Text API → transkripcija audio zapisa  
- LLM API → generisanje odgovora  
- embedding modeli → pretvaranje teksta u vektore  

---

## 4. Tok podataka i interakcija

### 4.1 Obrada podataka

1. Administrator uploaduje transkript ili audio zapis  
2. Podaci se šalju u Processing Pipeline  
3. Pipeline vrši obradu kroz više faza  
4. Podaci se pretvaraju u embeddinge  
5. Embeddingi se pohranjuju u bazu znanja  

---

### 4.2 Chatbot tok

1. Korisnik postavlja pitanje kroz Chat UI  
2. Sistem pretražuje relevantne informacije iz baze znanja  
3. Kontekst se šalje LLM-u  
4. Generisani odgovor se vraća korisniku  

---

### 4.3 Feedback tok

1. Korisnik ocjenjuje odgovor ili prijavljuje problem  
2. Podaci se spremaju u bazu  
3. Administrator analizira rezultate i unapređuje sistem  

---

## 5. Ključne tehničke odluke

| Odluka | Razlog |
|---|---|
| Modularni monolit | Brži razvoj MVP-a, lakši deployment i manja kompleksnost |
| RAG pristup | Povećava tačnost bez treniranja modela |
| Eksterni AI servisi | Smanjuju kompleksnost razvoja i ubrzavaju implementaciju |
| Vektorska baza | Omogućava semantičku pretragu |
| Asinhrona obrada | Efikasna obrada dugotrajnih operacija |

### Alternativa (nije odabrana)

- Mikroservisi  → prevelika kompleksnost za ranu fazu  
- Treniranje modela  → visoki troškovi i složenost  

---

## 6. Ograničenja i rizici arhitekture

| Rizik | Utjecaj | Mitigacija |
|---|---|---|
| Skalabilnost monolita | Visok | Planirana migracija na mikroservise |
| Zavisnost od API-ja | Visok | Retry i fallback mehanizmi |
| Loš kvalitet transkripata | Srednji | Validacija i filtriranje podataka |
| LLM hallucination | Visok | Korištenje RAG pristupa |
| Performanse pretrage | Srednji | Optimizacija i caching |
| Privacy i sigurnost | Visok | Maskiranje podataka i kontrola pristupa |

---

## 7. Otvorena pitanja

| # | Pitanje | Prioritet |
|---|---|---|
| 1 | Koji LLM koristiti u produkciji? | Visok |
| 2 | Koju vektorsku bazu koristiti? | Visok |
| 3 | Kako optimizirati performanse pretrage? | Srednji |
| 4 | Kako riješiti monitoring i logging sistema? | Srednji |
| 5 | Kako osigurati zaštitu podataka (GDPR)? | Visok |

---