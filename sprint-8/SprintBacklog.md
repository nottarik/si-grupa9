# Sprint Backlog – Sprint 8

## Opis sprinta

Sprint 8 fokusira se na implementaciju real-time komunikacije između korisnika i agenata, izgradnju kompletnog AI toka odgovaranja i uvođenje zasebnih panela za agente. Nakon što je Sprint 7 postavio pipeline za obradu transkripata i izgradnju baze znanja, ovaj sprint tu bazu stavlja u upotrebu — chatbot sada klasificira upite, odgovara iz baze znanja, a kada nema odgovor ne izmišlja, već korisnika upućuje na agenta. Uvode se escalation queue, WebSocket komunikacija između korisnika i agenta, zasebni agent panel s vlastitim Live Queue-om i pristupom bazi znanja, te niz funkcionalnosti koje poboljšavaju korisničko iskustvo: historija razgovora, glasovni unos i upload audio fajlova s automatskom transkripcijom.

Tokom ovog sprinta implementiraju se funkcionalnosti vezane za:

- upload audio fajlova s automatskom transkripcijom putem Whisper API-ja
- glasovni unos u chatu — korisnik diktira pitanja umjesto tipkanja
- escalation queue i real-time WebSocket komunikaciju između korisnika i agenta
- zasebni agent panel s Live Queue-om i pristupom bazi znanja
- RAG retrieval i LLM klasifikaciju upita s usmjeravanjem na agenta
- historiju razgovora korisnika i automatsko zatvaranje sesija
- resolving chatova od strane agenta

---

## Pregled stavki sprinta

| ID | Naziv stavke | Kratak opis | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-------------|-----|-----------|-----------------|--------|
| PB-13 | Konvertovanje iz audio zapisa u transkript | Upload audio fajlova s automatskom transkripcijom (US-13.1) | Feature | High | 8 | Završeno |
| PB-22 | Chat UI — glasovni unos | Korisnik diktira pitanja putem mikrofona (US-22.2) | Feature | High | 5 | Završeno |
| PB-48 | Escalation queue u admin panelu | Prikaz eskaliranih upita i prihvatanje live chata s korisnikom (US-48.1, US-48.2) | Feature | High | 8 | Završeno |
| PB-49 | Historija razgovora korisnika | Korisnik pregledava sve prethodne razgovore (US-49.1) | Feature | Medium | 5 | Završeno |
| PB-50 | Automatsko obavještavanje agenta o završetku sesije | Agent se automatski diskonektuje kada korisnik izađe (US-50.1) | Feature | High | 5 | Završeno |
| PB-51 | Agent panel s Live Queue i bazom znanja | Zasebni panel za agenta s Live Queue i pretragom baze znanja (US-51.1, US-51.2) | Feature | High | 13 | Završeno |
| PB-52 | RAG retrieval i LLM klasifikacija upita | Klasifikacija RAG/LLM i retrieval iz vektorske baze (US-52.1, US-52.2) | Technical Task | High | 13 | Završeno |
| PB-53 | Obrada osnovne komunikacije sa LLM | AI odgovara na pozdrave, za nepoznate upite upućuje na agenta (US-53.1, US-53.2) | Feature | High | 8 | Završeno |
| PB-54 | WebSocket komunikacija između korisnika i agenta | Real-time dvosmjerna komunikacija (US-54.1) | Technical Task | High | 13 | Završeno |
| PB-55 | Resolving chatova | Agent označava razgovor kao riješen (US-55.1) | Feature | Medium | 5 | Završeno |

---

## Sprint Backlog stavke

---

### PB-13: Konvertovanje iz audio zapisa u transkript

**Prioritet:** High

**Poslovna vrijednost:** Automatizuje proces pretvaranja snimljenih poziva u tekstualne transkripte, eliminišući potrebu za ručnim prepisivanjem i ubrzavajući punjenje baze znanja.

**Pretpostavke:** Podržani formati su MP3 i WAV. Sistem koristi Whisper (Groq API) za transkripciju.

**Veze i zavisnosti:** Zavisi od PB-18 Upload i unos transkripata. Zavisi od PB-36 Sign In. Preduvjet za PB-23 Priprema za obradu transkripata.

---

#### US-13.1 — Konverzija audio zapisa u transkript

**Uloga:** Kao administrator, želim uploadati audio zapis poziva kako bi sistem automatski generisao transkript razgovora i pohranio ga u sistem.

**Acceptance Criteria:**

- Kada administrator pristupi modulu za upload, tada sistem mora prikazati opciju za odabir audio fajla
- Kada administrator učita validan audio fajl, tada sistem mora pokrenuti proces transkripcije i prikazati indikator napretka
- Kada transkripcija bude završena, tada sistem mora prikazati generisani transkript i omogućiti administratoru pregled prije pohrane
- Kada administrator potvrdi transkript, tada sistem mora pohraniti transkript na isti način kao i ručno uneseni transkript
- Kada audio fajl nije validnog formata ili je oštećen, tada sistem mora prikazati odgovarajuću poruku greške
- Sistem ne smije pohraniti transkript bez eksplicitne potvrde administratora

---

### PB-22: Chat UI — glasovni unos (Dictate)

**Prioritet:** High

**Poslovna vrijednost:** Poboljšava dostupnost i brzinu unosa, posebno za korisnike koji preferiraju glasovnu interakciju umjesto tipkanja.

**Pretpostavke:** Uređaj korisnika ima funkcionalan mikrofon i dozvole su dodijeljene. Koristi se Web Speech API — podržan u Chrome i Edge browserima.

**Veze i zavisnosti:** Zavisi od US-22.1 Postavljanje pitanja chatbotu tekstom.

---

#### US-22.2 — Postavljanje pitanja chatbotu glasovnim unosom

**Uloga:** Kao korisnik call centra, želim izgovoriti pitanje putem mikrofona kako bih komunikaciju s chatbotom učinio bržom i jednostavnijom.

**Acceptance Criteria:**

- Kada korisnik klikne na dugme za glasovni unos, tada sistem mora aktivirati prepoznavanje govora
- Kada korisnik završi govor, tada sistem mora pretvoriti govor u tekst i prikazati ga u polju za unos
- Kada korisnik potvrdi pitanje, tada sistem mora poslati pitanje chatbotu
- Sistem mora prikazati odgovarajuću poruku ako mikrofon nije dostupan
- Sistem ne smije prikazati grešku ako korisnik nije izgovorio ništa — umjesto toga mora ostati na čekanju

---


### PB-48: Escalation Queue u admin panelu

**Prioritet:** High

**Poslovna vrijednost:** Omogućava agentima pregled i prihvatanje eskaliranih korisničkih upita koji nisu riješeni chatbotom i zahtijevaju ljudsku intervenciju.

**Pretpostavke:** Chatbot je pokušao odgovoriti i uputio korisnika na agenta. WebSocket konekcija je dostupna.

**Veze i zavisnosti:** Zavisi od PB-52 RAG retrieval i LLM klasifikacija. Zavisi od PB-54 WebSocket komunikacija. Preduvjet za PB-50 Automatsko obavještavanje agenta.

---

#### US-48.1 — Prikaz eskaliranih upita u admin panelu

**Uloga:** Kao agent, želim vidjeti listu eskaliranih korisničkih upita u admin panelu kako bih mogao prihvatiti razgovor i pomoći korisniku.

**Acceptance Criteria:**

- Kada korisnik pristane na povezivanje s agentom, tada sistem mora dodati upit u escalation queue u admin panelu
- Queue mora prikazivati korisnički upit, vrijeme čekanja i status
- Sistem ne smije prikazati grešku pri učitavanju escalation queue-a
- Kada nema eskaliranih upita, sistem mora prikazati odgovarajuću poruku

---

#### US-48.2 — Prihvatanje eskaliranog upita i otvaranje live chata

**Uloga:** Kao agent, želim prihvatiti eskalirani upit i ući u live chat s korisnikom kako bih mu direktno pomogao.

**Acceptance Criteria:**

- Kada agent klikne "Prihvati", tada sistem mora otvoriti live chat s historijom razgovora korisnika s chatbotom
- Agent i korisnik moraju moći razmjenjivati poruke u realnom vremenu
- Korisnik mora dobiti obavijest da je agent preuzeo razgovor
- Sistem ne smije dozvoliti da dva agenta prihvate isti upit istovremeno

---

### PB-49: Historija razgovora korisnika

**Prioritet:** Medium

**Poslovna vrijednost:** Omogućava korisniku pregled prethodnih interakcija s chatbotom i agentima radi lakšeg praćenja vlastitih upita i dobivenih odgovora.

**Pretpostavke:** Razgovori su pohranjeni u bazi podataka i vezani za korisnički nalog.

**Veze i zavisnosti:** Zavisi od PB-36 Sign In. Zavisi od PB-22 Chat UI.

---

#### US-49.1 — Pregled vlastite historije razgovora

**Uloga:** Kao korisnik, želim pregledati historiju svojih razgovora s chatbotom i agentima kako bih mogao pratiti prethodne upite i odgovore.

**Acceptance Criteria:**

- Kada korisnik otvori "My History", tada sistem mora prikazati listu svih prethodnih razgovora s datumom i prvom porukom
- Kada korisnik klikne na razgovor, tada sistem mora prikazati kompletan sadržaj tog razgovora
- Kada nema historije, sistem mora prikazati odgovarajuću poruku
- Sistem ne smije prikazati razgovore koji ne pripadaju prijavljenom korisniku
- Sistem ne smije prikazati grešku pri učitavanju historije

---

### PB-50: Automatsko obavještavanje agenta o završetku korisničke sesije

**Prioritet:** High

**Poslovna vrijednost:** Sprečava da agent ostane u aktivnoj sesiji bez korisnika i osigurava čisto zatvaranje razgovora s obje strane.

**Pretpostavke:** Sistem prati status konekcije korisnika putem WebSocketa.

**Veze i zavisnosti:** Zavisi od PB-54 WebSocket komunikacija. Zavisi od PB-48 Escalation queue.

---

#### US-50.1 — Automatska diskoneksija agenta kada korisnik završi razgovor

**Uloga:** Kao agent, želim biti automatski obaviješten i diskonektovan kada korisnik izađe iz razgovora kako bih znao da je sesija završena.

**Acceptance Criteria:**

- Kada korisnik izađe iz chata ili se odjavi, tada sistem mora automatski diskonektovati agenta iz te sesije
- Agentu mora biti prikazana poruka "Korisnik je završio konverzaciju"
- Razgovor mora biti automatski označen kao završen
- Sistem ne smije ostaviti agenta u aktivnoj sesiji nakon što je korisnik izašao

---

### PB-51: Agent panel s Live Queue i pristupom bazi znanja

**Prioritet:** High

**Poslovna vrijednost:** Agentima pruža personalizovan panel s vlastitim aktivnim sesijama i direktnim pristupom bazi znanja, potpuno odvojen od globalnog admin pogleda.

**Pretpostavke:** Agent je prijavljen s ulogom CallCentarAgent. Admin i dalje vidi sve agente.

**Veze i zavisnosti:** Zavisi od PB-36 Sign In. Zavisi od PB-48 Escalation queue. Zavisi od PB-27 Izgradnja baze znanja.

---

#### US-51.1 — Agent Live Queue — prikaz upita specifičnih za agenta

**Uloga:** Kao agent, želim vidjeti samo moje aktivne upite i sesije u Live Queue-u kako bih se fokusirao na vlastiti rad bez suvišnih informacija.

**Acceptance Criteria:**

- Kada agent otvori panel, tada sistem mora prikazati samo upite i sesije dodijeljene tom agentu
- Live Queue se mora ažurirati u realnom vremenu bez reload-a stranice
- Agent ne smije vidjeti upite dodijeljene drugim agentima
- Sistem ne smije prikazati grešku pri učitavanju Live Queue-a

---

#### US-51.2 — Pretraga baze znanja iz agentovog panela

**Uloga:** Kao agent, želim pretraživati bazu znanja direktno iz svog panela kako bih brzo pronašao odgovore tokom live razgovora s korisnikom.

**Acceptance Criteria:**

- Kada agent unese ključnu riječ, tada sistem mora prikazati relevantne Q&A parove iz baze znanja
- Rezultati moraju biti sortirani po relevantnosti
- Kada nema rezultata, sistem mora prikazati odgovarajuću poruku
- Sistem ne smije prikazati grešku pri pretrazi

---

### PB-52: RAG retrieval i LLM klasifikacija upita

**Prioritet:** High

**Poslovna vrijednost:** Osigurava da korisnik dobije najtačniji odgovor — iz baze znanja kada postoji relevantan sadržaj, ili od LLM-a za opća pitanja, bez izmišljanja informacija.

**Pretpostavke:** Embeddinzi su pohranjeni u Qdrantu i LLM API (Groq) je dostupan.

**Veze i zavisnosti:** Zavisi od PB-27 Izgradnja baze znanja. Zavisi od PB-22 Chat UI. Preduvjet za PB-53.

---

#### US-52.1 — Klasifikacija upita — RAG ili LLM

**Uloga:** Kao korisnik, želim da sistem automatski odabere najprikladniji način odgovaranja na moje pitanje kako bih dobio tačan i relevantan odgovor.

**Acceptance Criteria:**

- Kada korisnik postavi pitanje, tada sistem mora klasificirati upit kao RAG ili LLM upit
- Kada upit odgovara sadržaju u bazi znanja, tada sistem mora koristiti RAG retrieval za generisanje odgovora
- Kada upit nije pokriven bazom znanja, tada LLM mora generisati odgovor ili uputiti na agenta
- Sistem ne smije pomiješati izvore odgovora za isti upit

---

#### US-52.2 — RAG retrieval — pronalaženje relevantnih odgovora

**Uloga:** Kao korisnik, želim da chatbot odgovori koristeći informacije iz baze znanja call centra kako bih dobio tačan odgovor.

**Acceptance Criteria:**

- Kada sistem klasificira upit kao RAG, tada mora pretražiti vektorsku bazu i pronaći najrelevantnije segmente
- Sistem mora koristiti pronađene segmente kao kontekst za generisanje odgovora
- Kada sistem ne pronađe relevantan sadržaj s dovoljnom sigurnošću, tada mora uputiti korisnika na agenta
- Sistem ne smije izmišljati informacije koje ne postoje u bazi znanja

---

### PB-53: Obrada osnovne komunikacije sa LLM

**Prioritet:** High

**Poslovna vrijednost:** Poboljšava korisničko iskustvo prirodnom konverzacijom za nebitne upite i minimizira nepotrebne eskalacije na agenta.

**Pretpostavke:** LLM može razlikovati nebitne upite od onih koji zahtijevaju intervenciju agenta.

**Veze i zavisnosti:** Zavisi od US-52.1 Klasifikacija upita. Zavisi od PB-48 Escalation queue.

---

#### US-53.1 — Odgovaranje na pozdrave i općenita pitanja

**Uloga:** Kao korisnik, želim da chatbot prirodno odgovori na pozdrave i jednostavna pitanja bez usmjeravanja na agenta.

**Acceptance Criteria:**

- Kada korisnik pošalje pozdrav (npr. "Hej", "Hello"), tada sistem mora prirodno odgovoriti bez eskalacije na agenta
- Sistem ne smije eskalirati na agenta za pozdrave i nebitna pitanja
- Sistem mora minimizovati broj nepotrebnih eskalacija na agenta

---

#### US-53.2 — Usmjeravanje na agenta kada chatbot nema odgovor

**Uloga:** Kao korisnik, želim biti upućen na agenta kada chatbot ne može odgovoriti na moje pitanje.

**Acceptance Criteria:**

- Kada chatbot ne može odgovoriti s dovoljnom sigurnošću, tada mora korisniku ponuditi opciju povezivanja s agentom
- Kada korisnik pristane, tada sistem mora dodati upit u escalation queue
- Kada korisnik odbije, tada sistem mora nastaviti konverzaciju bez eskalacije
- Sistem mora jasno objasniti korisniku zašto ga upućuje na agenta

---

### PB-54: WebSocket komunikacija između korisnika i agenta

**Prioritet:** High

**Poslovna vrijednost:** Omogućava neposrednu dvosmjernu komunikaciju bez kašnjenja, što je ključno za kvalitetnu korisničku podršku u realnom vremenu.

**Pretpostavke:** Backend podržava WebSocket konekcije.

**Veze i zavisnosti:** Zavisi od PB-48 Escalation queue. Preduvjet za PB-50 i PB-55.

---

#### US-54.1 — Real-time razmjena poruka između korisnika i agenta

**Uloga:** Kao korisnik, želim razmjenjivati poruke s agentom u realnom vremenu kako bih dobio brzu i direktnu pomoć.

**Acceptance Criteria:**

- Kada agent prihvati upit, tada sistem mora uspostaviti WebSocket konekciju između korisnika i agenta
- Poruke moraju biti isporučene u realnom vremenu bez potrebe za refreshom stranice
- Kada konekcija padne, sistem mora pokušati automatski se reconnectati
- Sistem mora prikazati indikator kada druga strana tipka poruku
- Sistem ne smije izgubiti poruke pri privremenom prekidu konekcije

---

### PB-55: Resolving chatova

**Prioritet:** Medium

**Poslovna vrijednost:** Omogućava čisto zatvaranje sesija i praćenje riješenih slučajeva, što poboljšava organizaciju rada agenata.

**Pretpostavke:** Razgovor mora biti aktivan da bi se mogao označiti kao riješen.

**Veze i zavisnosti:** Zavisi od PB-48 Escalation queue. Zavisi od PB-54 WebSocket komunikacija.

---

#### US-55.1 — Označavanje razgovora kao riješenog

**Uloga:** Kao agent, želim označiti razgovor kao riješen kako bih zatvorio aktivnu sesiju i oslobodio kapacitet za nove upite.

**Acceptance Criteria:**

- Kada agent klikne "Resolve", tada sistem mora označiti razgovor kao riješen i zatvoriti aktivnu sesiju
- Korisnik mora biti obaviješten da je razgovor zatvoren
- Riješeni razgovor mora biti vidljiv u historiji s odgovarajućim statusom
- Sistem ne smije dozvoliti slanje novih poruka u riješenom razgovoru
- Sistem ne smije prikazati grešku pri označavanju razgovora kao riješenog
