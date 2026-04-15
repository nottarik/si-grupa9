# Architecture Overview – Call Centar Chatbot Sistem

## 1. Kratak opis arhitektonskog pristupa

Sistem je projektovan kao višeslojna web aplikacija zasnovana na modularnom monolitu, sa jasno razdvojenim prezentacijskim, aplikativnim i podatkovnim slojem, te izdvojenim AI servisima. Predložena arhitektura prati princip razdvajanja odgovornosti (Separation of Concerns) kako bi se osigurala nesmetana i nezavisna izmjena, testiranje i skaliranje svakog dijela sistema.

**Ključni arhitektonski stil:**
Layered monolitni backend s RESTful API komunikacijom i izdvojenim AI servisima; ostavlja se mogućnost kasnijeg prelaska na mikroservise za AI komponentu.

### Osnovni principi

- **Modularnost** – svaka funkcionalnost se razvija i deployuje nezavisno unutar zajedničkog backenda
- **Sigurnost** – GDPR usklađenost i RBAC kontrola pristupa ugrađene su od početka razvoja
- **AI kao servis** – AI modul komunicira s ostatkom sistema kroz definirani API, što omogućava zamjenu ili upgrade modela bez utjecaja na ostale dijelove
- **Kontejnerizacija** – svi servisi su pokrenuti u Docker kontejnerima, čime se osigurava konzistentnost između razvojnog i produkcijskog okruženja

---

## 2. Glavne komponente sistema

### 2.1 Korisnici

U sistemu su definirane dvije primarne vrste korisnika:

- **Administrator** – upravljanje transkriptima, korisnicima i konfiguracijom sistema
- **Agent / Krajnji korisnik** – interakcija s chatbotom putem Chat UI-ja

Sve uloge prolaze kroz isti Auth & RBAC sloj na backendu koji na osnovu JWT tokena određuje dozvole i nivo pristupa.

**Razlike:**
- Administrator: puni pristup + upravljanje transkriptima, korisnicima i konfiguracijom
- Agent / Korisnik: pristup isključivo Chat UI-ju i vlastitim interakcijama

---

### 2.2 Prezentacijski sloj – Frontend

Korisnički interfejs kojeg koriste svi tipovi korisnika sistema.

- **Chat UI** – sučelje za postavljanje pitanja i pregled odgovora chatbota
- **Admin Dashboard** – pregled transkripata, analiza prijavljenih problema, upravljanje korisnicima
- Pregled historije interakcija i ocjena
- Upravljanje uploadom transkripata i audio zapisa

---

### 2.3 Aplikativni sloj – Backend

Odgovoran za:

- Poslovnu logiku i validaciju podataka
- Autentifikaciju i autorizaciju (JWT + RBAC)
- Komunikaciju između svih komponenti sistema
- Orkestraciju eksternih AI servisa

Nakon što se korisnik prijavi, izdaje mu se JWT token koji prati svaki naredni zahtjev prema API-ju. RBAC sloj provjerava permisije te odobrava ili odbija zahtjev. Nakon toga nastupa poslovna logika: validacija podataka, upravljanje transkriptima i interakcijama, orkestracija eksternih servisa te logovanje akcija. Svaka akcija propagira se prema bazi podataka, AI modulu, Audio-to-Transcript servisu ili Feedback modulu.

#### Funkcionalnosti:

- RESTful API
- Autentifikacija i autorizacija (JWT + RBAC)
- Upload i upravljanje transkriptima i audio zapisima
- Upravljanje feedbackom i prijavama netačnih odgovora
- Logovanje svih korisničkih interakcija

---

### 2.4 Specijalizovani servisi

#### 2.4.1 Audio-to-Transcript API

Zasebni servis koji prima audio zapise i vrši automatsku transkripciju putem eksternog Speech-to-Text API-ja (npr. OpenAI Whisper, Google Speech-to-Text).

Servis uključuje:

- Prijem audio fajla putem HTTP endpointa
- Slanje na vanjski Speech-to-Text API
- Normalizaciju i čišćenje generisanog teksta
- Vraćanje strukturiranog transkripta Backendu

Transkript se nakon obrade dalje prosljeđuje u Processing Pipeline.

---

#### 2.4.2 Processing Pipeline

Poseban podsistem za obradu i transformaciju transkripata prije pohrane u bazu znanja.

Pipeline prolazi kroz sljedeće faze:

1. **Normalizacija teksta** – uklanjanje suvišnih znakova, formatiranje
2. **Razdvajanje po ulogama** – identifikacija agent/korisnik tura u razgovoru
3. **Maskiranje osjetljivih podataka** – anonimizacija ličnih podataka (GDPR)
4. **Generisanje embeddinga** – pretvaranje teksta u vektore putem eksternog embedding modela
5. **Pohrana u vektorsku bazu** – indeksiranje za semantičku pretragu

---

#### 2.4.3 AI Chatbot modul (RAG)

Centralna AI komponenta odgovorna za generisanje odgovora na korisničke upite. Komunicira s backendom kroz interni API poziv.

Tok obrade upita:

1. Korisnik postavlja pitanje kroz Chat UI
2. Backend prima upit i prosljeđuje ga AI modulu
3. AI modul pretražuje relevantne informacije iz vektorske baze (semantička pretraga)
4. Pronađeni kontekst se šalje LLM-u zajedno s upitom
5. LLM generuje odgovor koji se vraća korisniku

Ovaj RAG pristup (Retrieval-Augmented Generation) osigurava kontekstualno tačne odgovore bez potrebe za treniranjem modela od nule.

---

### 2.5 Auth API

Izdvojeni autentifikacijski servis koji upravlja:

- Registracijom i prijavom korisnika
- Izdavanjem i verifikacijom JWT tokena
- RBAC tabelom permisija po ulogama
- Logiranjem pristupa i sesija

Svaki API poziv prolazi kroz ovaj servis prije nego dođe do poslovne logike backenda.

---

### 2.6 Sloj podataka

Centralno skladište svih podataka sistema.

- Korisnici, uloge i sesije
- Transkripti i audio zapisi
- Embeddingi u vektorskoj bazi
- Historija korisničkih interakcija
- Ocjene, komentari i prijave netačnih odgovora

---

### 2.7 Docker infrastruktura

Svi servisi sistema pokreću se unutar Docker kontejnera:

| Kontejner | Opis |
|---|---|
| backend | Glavni aplikativni sloj (RESTful API, RBAC, poslovna logika) |
| auth-service | Auth API (JWT, RBAC) |
| audio-transcript-service | Audio-to-Transcript API |
| ai-chatbot-service | RAG Chatbot modul |
| processing-pipeline | Processing Pipeline za obradu transkripata |
| database | Relacijska baza podataka |
| vector-db | Vektorska baza za embeddings |
| frontend | Chat UI i Admin Dashboard |

Docker Compose se koristi za lokalni razvoj; produkcija se deployuje na odabranoj cloud ili on-premise infrastrukturi.

---

## 3. Odgovornosti komponenti

| Komponenta | Odgovornost |
|---|---|
| Frontend | Prikazuje podatke korisniku, prikuplja input putem Chat UI-ja i Admin Dashboarda, vrši osnovnu klijentsku validaciju. Ne sadrži poslovnu logiku |
| Backend API | Provodi autentifikaciju, autorizaciju, poslovnu logiku i upravlja pozivima prema bazi i AI modulu |
| Auth API | Upravlja korisničkim identitetima, sesijama i pravima pristupa. Svaki API poziv prolazi kroz ovaj servis |
| Audio-to-Transcript API | Prima audio zapise, vrši transkripciju putem eksternog Speech-to-Text API-ja, vraća strukturirani tekst Backendu |
| Processing Pipeline | Normalizira, maskira i pretvara transkripte u embeddings za pohranu u vektorsku bazu |
| AI Chatbot modul | Prima korisničke upite, vrši semantičku pretragu, šalje kontekst LLM-u i vraća generirani odgovor |
| Relacijska baza | Trajno čuva sve poslovne podatke. Jedino Backend ima direktan pristup bazi |
| Vektorska baza | Čuva embeddings i omogućava semantičku pretragu. Pristupa joj isključivo AI Chatbot modul |
| Eksterni AI servisi | Speech-to-Text API, LLM API i embedding modeli koji se pozivaju putem eksternih HTTP poziva |

---

## 4. Tok podataka i interakcija

### 4.1 Upload i obrada transkripta (tekstualni)

Administrator uploaduje transkript putem Admin Dashboarda → Frontend šalje HTTP POST zahtjev prema Backend API-ju → Backend validira podatke i provjerava RBAC dozvole → Transkript se prosljeđuje Processing Pipelineu → Pipeline normalizira tekst, maskira osjetljive podatke i generiše embeddings → Embeddingi se pohranjuju u vektorsku bazu → Administrator prima potvrdu o uspješnoj obradi.

---

### 4.2 Upload i obrada audio zapisa

Administrator uploaduje audio fajl → Backend prima fajl i prosljeđuje ga Audio-to-Transcript API-ju → Servis šalje audio na vanjski Speech-to-Text API → Generirani transkript se vraća Backendu → Backend prosljeđuje transkript Processing Pipelineu → Pipeline vrši obradu i pohrana u vektorsku bazu.

---

### 4.3 Chatbot tok (RAG)

Korisnik postavlja pitanje kroz Chat UI → Frontend šalje HTTP POST zahtjev prema Backend API-ju → Backend prosljeđuje upit AI Chatbot modulu → Modul vrši semantičku pretragu u vektorskoj bazi → Pronađeni kontekst se šalje LLM API-ju → Generirani odgovor se vraća Backendu → Backend loguje interakciju u bazu → Odgovor se prikazuje korisniku.

---

### 4.4 Feedback tok

Korisnik ocjenjuje odgovor ili prijavljuje problem → Frontend šalje HTTP POST zahtjev prema Backendu → Backend sprema ocjenu, komentar ili prijavu u bazu → Administrator analizira prijavljene probleme putem Admin Dashboarda → Na osnovu analize vrši se optimizacija i unapređenje sistema.

---

**Napomena:**
Sva komunikacija između Frontenda i Backenda odvija se putem RESTful HTTP/HTTPS API-ja. AI Chatbot modul, Audio-to-Transcript API i Processing Pipeline komuniciraju s Backendom kroz interni API (unutar iste Docker mreže), ne izlažući se direktno na internet.

---

## 5. Ključne tehničke odluke

| Odluka | Obrazloženje |
|---|---|
| Modularni monolit | Brži razvoj MVP-a, lakši deployment i manja kompleksnost u ranoj fazi |
| RAG pristup | Povećava tačnost odgovora bez potrebe za treniranjem modela od nule |
| Audio-to-Transcript API kao zasebni servis | Omogućava nezavisno skaliranje i zamjenu Speech-to-Text provajdera bez utjecaja na ostatak sistema |
| Auth API kao zasebni servis | Centralizovana autentifikacija i autorizacija, lakša zamjena auth strategije |
| Eksterni AI servisi | Smanjuju kompleksnost razvoja i ubrzavaju implementaciju (LLM, Speech-to-Text, embedding modeli) |
| Vektorska baza | Omogućava efikasnu semantičku pretragu embeddinga |
| Asinhrona obrada | Efikasna obrada dugotrajnih operacija (transkripcija, generisanje embeddinga) bez blokiranja korisničkog zahtjeva |
| JWT autentifikacija | Stateless token-based autentifikacija omogućava horizontalno skaliranje backenda |
| RBAC model pristupa | Sprečava neautorizovani pristup podacima i funkcionalnostima |
| Docker kontejnerizacija | Osigurava konzistentnost između razvojnog i produkcijskog okruženja; svaki servis je izolovan |
| Maskiranje podataka u Pipelineu | GDPR usklađenost kroz anonimizaciju osjetljivih podataka prije pohrane |

### Alternative (nisu odabrane)

- Mikroservisi → prevelika kompleksnost za ranu fazu razvoja
- Treniranje modela od nule → visoki troškovi i složenost; RAG pristup je efikasnija alternativa

---

## 6. Ograničenja i rizici

### 6.1 Tehnička ograničenja

- Kvalitet transkripcije ovisi o kvalitetu audio zapisa. Loš zvuk može zahtijevati ručnu korekciju. *(Speech-to-Text tačnost)*
- AI analiza i generisanje odgovora mogu imati veću latenciju kod kompleksnijih upita. Asinhrona obrada ublažava ovo, ali korisnici ne dobijaju uvijek trenutne rezultate. *(LLM latencija)*
- Relacijska baza može postati usko grlo pri velikom broju simultanih interakcija. *(Skalabilnost baze)*
- Sistem je dizajniran kao online aplikacija; nema podrške za offline rad. *(Ograničena offline funkcionalnost)*

---

### 6.2 Sigurnosni rizici

| Rizik | Utjecaj | Mitigacija |
|---|---|---|
| SQL Injection / XSS | Visok | ORM, input validacija, Content Security Policy headeri |
| Neautorizovani pristup podacima | Visok | JWT + RBAC; svaki API poziv prolazi kroz Auth API |
| LLM hallucination | Visok | RAG pristup ograničava odgovore na dostupni kontekst |
| Privacy i GDPR | Visok | Maskiranje osjetljivih podataka u Processing Pipelineu |
| Zavisnost od eksternih API-ja | Visok | Retry i fallback mehanizmi; mogućnost zamjene provajdera |
| Loš kvalitet transkripata | Srednji | Validacija i filtriranje podataka u Pipelineu |
| Performanse semantičke pretrage | Srednji | Optimizacija indeksiranja i caching čestih upita |

---

### 6.3 Arhitektonski rizici

- Ako odabrani LLM ili Speech-to-Text provajder ne daje zadovoljavajuće rezultate, zamjena zahtijeva redizajn odgovarajućeg servisa. *(Ovisnost o eksternim AI provajderima)*
- Trenutna arhitektura je monolitni backend. Ako sistem značajno poraste po obimu, može biti potrebna migracija prema mikroservisima. *(Monolitni backend)*

---

## 7. Otvorena pitanja

| # | Pitanje | Prioritet |
|---|---|---|
| 1 | Koji LLM koristiti u produkciji? (GPT-4, Claude, Mistral...) | Visok |
| 2 | Koju vektorsku bazu koristiti? (Pinecone, Weaviate, pgvector...) | Visok |
| 3 | Koji Speech-to-Text provajder koristiti? (Whisper, Google, AWS Transcribe...) | Visok |
| 4 | Kako osigurati zaštitu podataka u skladu s GDPR-om? | Visok |
| 5 | Hosting i deployment – on-premise ili cloud? | Visok |
| 6 | Kako optimizirati performanse semantičke pretrage? | Srednji |
| 7 | Kako riješiti monitoring i logging sistema? | Srednji |
| 8 | Strategija backup-a baze podataka | Srednji |
