# Product Backlog


> **Promjene**
>- **Sprint 10 — Dodano:** Batch procesiranje fajlova iz eksternih izvora (PB-66); Scheduled pipeline obrada i automatsko ažuriranje baze znanja (PB-67); Single-click cloud deployment (PB-68); Optimizacija build procesa i CI/CD performansi (PB-69); Prevencija duplih unosa u bazu znanja (PB-70); Bulk brisanje razgovora iz Chat Logs (PB-71);  Razumljive i korisnički prilagođene poruke o greškama (PB-72)

---

| ID | Naziv stavke | Kratak opis | Tip | Prioritet | Procjena | Status | Napomena |
|----|--------------|-------------|-----|-----------|----------|--------|----------|
| 1 | Istraživanje domene | Analiza call centra i njegovih potreba te pregled sličnih rješenja na tržištu | research | High | 5 | Done | / |
| 2 | Mapiranje stakeholdera | Identifikacija aktera, njihovih potreba i potencijalnih konflikata | research | High | 3 | Done | deliverable |
| 3 | Product Vision | Definisanje za koga se gradi, koji problem rješava i mjerila uspjeha | documentation | High | 2 | Done | deliverable |
| 4 | Team Charter | Raspodjela uloga, komunikacija i način održavanja sastanaka | documentation | High | 2 | Done | deliverable |
| 5 | Istraživanje ulaznih formata | Analiza formata transkripata | research | High | 5 | In Progress | ključna arhitekturalna odluka |
| 6 | Istraživanje RAG i LLM servisa | Pregled embedding modela, vektorskih baza i LLM API-ja | research | High | 8 | In Progress | / |
| 7 | Definisanje MVP opsega | Precizno odvajanje MVP-a od post-MVP funkcionalnosti | documentation | High | 3 | Done | sastavni dio Product Vision deliverable-a |
| 8 | Početni Product Backlog | Kreiranje početnog backloga sa tehničkim zadacima | documentation | High | 3 | Done | deliverable, ažurirati svaki sprint |
| 9 | User Stories | Pisanje user stories za krajnje korisnike (klijent, agent i admin) | documentation | High | 8 | In Progress | deliverable, jasni, granularni, provjerljivi |
| 10 | Acceptance Criteria | Za svaki story navesti mjerljive i provjerljive acceptance kriterije | documentation | High | 5 | In Progress | jasni, testabilni, povezani sa očekivanim ponašanjem |
| 11 | Nefunkcionalni zahtjevi | Definisanje nefunkcionalnih zahtjeva sa opisom, tipom i prioritetom | documentation | High | 3 | In Progress | deliverable |
| 12 | Ažuriranje backloga | Analiza svih stavki po poslovnoj vrijednosti i tehničkim zavisnostima | documentation | Medium | 3 | In Progress | / |
| 13 | Konvertovanje iz audio zapisa u transkript | Istražiti API-eve potrebne za konvertovanje | research | Medium | 3 | In Progress | / |
| 14 | Plan baze podataka | Dizajn baze podataka za pohranu audio zapisa, transkripata, korisničkih računa, pitanja, odgovora i pripadajućih metapodataka | technical | High | 5 | Not Started | / |
| 15 | Ocjena odgovora chatbota | Istražiti najbolji način za rješavanje netačnih odgovora i korištenje povratnih informacija korisnika | research | High | 5 | In Progress | / |
| 16 | Risk Register | Identifikacija rizika s vjerovatnoćom, uticajem i strategijom mitigacije | documentation | High | 5 | Not Started | deliverable |
| 17 | Use Case Model | UML dijagram aktera i interakcija | documentation | High | 5 | Not Started | deliverable, važno je imati ili domain model ili use case model |
| 18 | Upload i unos transkripata | Prijem i pohrana transkripata ili poziva s osnovnom validacijom | feature | High | 8 | Not Started | MVP inkrement |
| 19 | Osmisliti testne strategije | Vrste testova, cilj testiranja i načini evidentiranja | research | High | 5 | Not Started | deliverable |
| 20 | Definition of Done | Prihvatiti zajedničku definiciju završene stavke | documentation | High | 2 | Not Started | deliverable |
| 21 | Osnovni skeleton projekta | Tehnički skeleton sistema, GitHub repo, struktura foldera i postavljanje alata za rad | technical task | High | 8 | Not Started | deliverable |
| 22 | Chat UI | Jednostavan chat interfejs s poljem za unos i prikazom odgovora | feature | High | 5 | Not Started | MVP inkrement |
| 23 | Priprema za obradu transkripata | Normalizacija teksta, razdvajanje po ulogama i maskiranje osjetljivih podataka | technical task | High | 13 | Done | MVP inkrement |
| 24 | Parser za razdvajanje uloga | Detekcija redova Agent/Korisnik i segmentacija dijaloga | technical | High | 5 | Not Started | MVP inkrement |
| 25 | Normalizacija teksta | Uklanjanje šuma, standardizacija interpunkcije i formata | technical | High | 3 | Not Started | MVP inkrement |
| 26 | Maskiranje osjetljivih podataka | Detekcija i zamjena (ime, telefon, JMBG) prije obrade | technical | High | 5 | Done | MVP inkrement |
| 27 | Izgradnja baze znanja | Generisanje embeddinga, pohrana u vektorsku bazu i retrieval mehanizam | feature | High | 13 | Done | MVP inkrement |
| 28 | Prijava netačnog odgovora | Korisnik može prijaviti netačan odgovor | technical task | Medium | 8 | Not Started | / |
| 29 | Korisnička dokumentacija | Upute za korištenje chatbota, admin panela i unos transkripata | documentation | High | 3 | Not Started | deliverable |
| 30 | Izgradnja razvojnog okruženja | Konfiguracija baze podataka, Dockera i backend frameworka. | feature | Medium | 3 | Not Started | MVP inkrement |
| 31 | Odgovor kada nema sigurnog responsea | Poruka korisniku i opcionalno preusmjeravanje na agenta | feature | High | 3 | Not Started | MVP inkrement |
| 32 | Potvrda i obrada netačnog odgovora | Obrađuje se prijem netačnog odgovora | technical task | Medium | 8 | Not Started | / |
| 33 | Pregled unesenih transkripata | Tabela s listom fajlova, datumom, statusom obrade | feature | High | 3 | Done | MVP inkrement |
| 34 | Pregled postavljenih pitanja i odgovora |Omogućava administratoru prikaz postavljenih pitanja i odgovora| feature | High | 3 | Done | MVP inkrement |
| 35 | Pregled prijavljenih problema | Omogućava administratoru prikaz prijavljenih odgovora  | feature | Medium | 3 | Not Started | MVP inkrement |
| 36 | Sign In | Sistem za autentifikaciju korisnika  | technical task | Medium | 5 | Done | MVP inkrement |
| 37 | Sign Out | Odjava iz sistema  | technical task | Medium | 5 | Done | MVP inkrement |
| 38 | Uređivanje postojećih transkripata | Administrator može izmijeniti sadržaj ili metapodatke prethodno unesenog transkripata | feature | High | 5 | Done | MVP inkrement |
| 39 | Brisanje transkripata s potvrdom akcije | Administrator može trajno obrisati transkript uz obaveznu potvrdu | feature | High | 3 | Done | MVP inkrement |
| 40 | Filtriranje i pretraga transkripata | Pretraga transkripata po ključnoj riječi, datumu i agentu | feature | High | 5 | Done | MVP inkrement |
| 41 | Dodjela i upravljanje ulogama korisnika | Administrator može dodijeliti ili promijeniti ulogu registrovanog korisnika | feature | High | 5 | Done | MVP inkrement |
| 42 | Pregled i brisanje korisnika | Administrator može pregledati listu korisnika i ukloniti nalog | feature | High | 5 | Done | MVP inkrement |
| 43 | Dashboard s aktuelnim podacima | Prikaz stvarnih agregiranih podataka na admin dashboardu (broj transkripata, korisnika, itd.) | feature | Medium | 3 | Done | MVP inkrement |
| 44 | Validacija formata transkripata | Provjera da transkript slijedi format Agent:/Korisnik: prije pohrane, s prikazom greške | technical task | High | 3 | Done | MVP inkrement |
| 45 | Account Settings | Upravljanje korisničkim nalogom — promjena korisničkog imena, lozinke i profilnih podataka | feature | Medium | 5 | Implementirano kao PB-64 User Settings u Sprintu 9 | MVP inkrement |
| 46 | Prikaz statusa obrade transkripata | Administratorski UI prikazuje status obrade svakog transkripata (Pending, Processing, Completed, Failed) s prikazom grešaka | feature | Medium | 5 | Done | MVP inkrement |
| 47 | Agent queue — pregled i potvrđivanje Q&A parova | Agent ima vlastiti prikaz s listom Q&A parova na čekanju koje pregleda i potvrđuje ili odbija, slično kao admin | feature | High | 8 | Done | MVP inkrement |
| 48 | Escalation queue u admin panelu | Admin panel prikazuje listu eskaliranih korisničkih upita koje agent može prihvatiti i ući u live chat s korisnikom | feature | High | 8 | Done | MVP inkrement |
| 49 | Historija razgovora korisnika | Korisnik može pregledati sve prethodne razgovore s chatbotom i agentima | feature | Medium | 5 | Done | MVP inkrement |
| 50 |  Automatsko obavještavanje agenta o završetku korisničke sesije | Kada korisnik izađe iz razgovora, agent se automatski diskonektuje s porukom da je korisnik završio konverzaciju | feature | High | 5 | Done | MVP inkrement |
| 51 | Agent panel s Live Queue i pristupom bazi znanja | Agent ima vlastiti panel odvojen od admina — Live Queue specifičan za njega, pretraga baze znanja i vlastita historija | feature | High | 13 | Done | MVP inkrement |
| 52 | RAG retrieval i LLM klasifikacija upita | Implementiran RAG retrieval i LLM koji klasificira da li upit pripada bazi znanja ili treba biti preusmjeren | technical task | High | 13 | Done | MVP inkrement |
| 53 |  Obrada osnovne komunikacije sa LLM | AI odgovara na pozdrave i općenita pitanja bez eskalacije; za nepoznate upite upućuje korisnika na agenta | feature | High | 8 | Done | MVP inkrement |
| 54 | WebSocket komunikacija između korisnika i agenta | Real-time dvosmjerna komunikacija između korisnika u chatu i agenta u panelu putem WebSocketa | technical task | High | 13 | Done | MVP inkrement |
| 55 | Resolving chatova | Agent ili admin može označiti razgovor kao riješen čime se zatvara aktivna sesija | feature | Medium | 5 | Done | MVP inkrement |
| 56 | Poboljšanje maskiranja PII podataka i ekstrakcije Q&A parova | Poboljšanje PII maskiranja (edge case formati JMBG i telefona) i ekstrakcije Q&A parova iz transkripata | bug fix | High | 8 | Done | Sprint 9 |
| 57 | Ocjena razgovora po završetku sesije | Forma za numeričku ocjenu (1–5) prikazuje se korisniku na kraju chat sesije; zamjenjuje thumbs-up/down po pojedinoj poruci | feature | High | 5 | Done | Sprint 9; zamjenjuje pristup iz PB-15 |
| 58 | Sistemske obavijesti u chatbotu | Administrator postavlja vidljivi baner s porukom o poznatim problemima ili planiranom održavanju koji se prikazuje pri otvaranju Chat UI-a | feature | Medium | 3 | Done | Sprint 9 |
| 59 | Mogućnost ručnog unosa Q&A para direktno u bazu znanja bez transkripata | Administrator direktno unosi validirane Q&A parove u bazu znanja; sistem generiše embedding i pohranjuje par u Qdrant bez potrebe za transkriptom | feature | High | 5 | Done | Sprint 9 |
| 60 | Pregled i kuriranje sadržaja baze znanja | Administrator pregleda sve unose, uklanja nevažeće i testne podatke te odobrava prijedloge iz agentskih odgovora i ručnih unosa | feature | High | 8 | Done | Sprint 9 |
| 61 | Optimizacija performansi chatbota | Smanjenje latencije odgovora — cilj ispod 3 s za RAG upite i ispod 5 s za LLM upite; keširanje embeddinga unutar sesije | technical task | High | 8 | Done | Sprint 9 |
| 62 | Prikaz komentara uz ocjene razgovora u admin i agent panelu | Admin vidi sve komentare uz ocjene, agent vidi samo komentare razgovora na koje je on odgovorio (US-62.1) | Feature | Medium | 5 | Done |
| 63 | End-to-end i regresijsko testiranje sistema | Pokrivenost unit testovima ≥ 80%, E2E testovi kritičnih putanja, regresijski testovi za ispravljene greške integrisani u CI/CD pipeline | technical task | High | 13 | Done | Sprint 9 |
| 64 | User Settings | Korisnik može promijeniti ime, obrisati cijelu historiju razgovora i obrisati vlastiti nalog | feature | Medium | 5 | Done | Sprint 9; MVP inkrement |
| 65 | Brisanje pojedinačnog chata iz historije | Korisnik može obrisati specifičan chat iz historije razgovora s potvrdom akcije | feature | Medium | 3 | Done | Sprint 9; MVP inkrement |
| 66 | Batch procesiranje fajlova iz eksternih izvora | Administrator može pokrenuti batch import fajlova iz Google Drive-a; sistem automatski preuzima i obrađuje više fajlova kroz postojeći transcript pipeline | feature | High | 13 | Done | Sprint 10; podržava on-demand i scheduled import; deduplikacija i verzionisanje fajlova implementirani |
| 67 | Scheduled pipeline obrada i automatsko ažuriranje baze znanja | Sistem automatski pokreće kompletan pipeline obrade: import transkripata, transkripcija, ekstrakcija Q&A parova, generisanje embeddinga i ažuriranje baze znanja | feature | High | 13 | Done | Sprint 10; admin kontroliše raspored izvršavanja; live progress i status izvršavanja vidljivi u admin panelu |
| 68 | Single-click cloud deployment | Omogućeno automatsko deployanje kompletnog sistema na Azure/AWS infrastrukturu jednim komandnim pozivom | devops | High | 8 | Done | Sprint 10; Azure Container Apps + Static Web Apps; automatski provision infrastrukture i HTTPS endpointa |
| 69 | Optimizacija build procesa i CI/CD performansi | Optimizovan Docker build proces korištenjem cache mehanizama i CPU-only ML dependency layera čime je značajno smanjeno vrijeme rebuildanja sistema | technical task | High | 8 | Done | Sprint 10; build vrijeme smanjeno sa preko 25 minuta na približno 10–15 sekundi za cached rebuildove |
| 70 | Prevencija duplih unosa u bazu znanja | Sistem sprječava dodavanje identičnih pitanja u bazu znanja kroz ručni unos, obradu transkripata, batch import i spašavanje Q&A parova iz eskalacija | technical task | High | 5 | Done | Sprint 10; duplikati se automatski preskaču tokom importa bez prekida obrade |
| 71 | Bulk brisanje razgovora iz Chat Logs, Transcripts i Issues | Administrator može označiti više razgovora i obrisati ih zajedno sa svim povezanim podacima | feature | Medium | 5 | Done | Sprint 10; podržani checkboxovi, select all i Delete selected akcija |
| 72 | Razumljive i korisnički prilagođene poruke o greškama | Nijedna poruka o grešci ne smije prikazivati sirove tehničke poruke; sistem prikazuje jasne, korisnički razumljive poruke za sve akcije (upload, pipeline, KB unos, brisanje) | feature | High | 5 | Done | Sprint 10 |



