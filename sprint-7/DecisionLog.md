# Decision log

## **ID:** DL-01  

**Datum:** 25/04/2026  

**Naziv:** Prilagođavanje deployment infrastrukture zbog nedostupnosti Oracle Always Free instanci  

**Opis:**  
Za projekat je bilo potrebno odabrati infrastrukturu koja omogućava pokretanje backend-a, frontend-a i AI komponenti bez dodatnih troškova, jer se projekat razvija u studentskom/timskom okruženju i oslanja se na free-tier servise. Prvobitno je planirano korištenje Oracle Always Free tier-a, ali su potrebne compute instance u trenutku rada bile zauzete ili nedostupne, pa je tim morao primijeniti drugačiji pristup za dio sistema.  

**Razmatrane opcije:**  
- Oracle Always Free tier  
- Render free plan  
- Supabase free tier  
- Qdrant Cloud free tier  
- Lokalno pokretanje preko Docker Compose-a  

**Odabrana opcija:**  
Kombinovani free-tier pristup: dio infrastrukture ostaje na Oracleu gdje je to moguće, dok se ostale komponente pokreću kroz dostupne free-tier servise i lokalno razvojno okruženje.  

**Razlog izbora:**  
Oracle Always Free tier je prvobitno bio preferirana opcija jer omogućava stabilno i besplatno hostanje dijela infrastrukture. Međutim, zbog nedostupnosti potrebnih instanci nije bilo moguće kompletan sistem postaviti na Oracle. Zbog toga je odlučeno da dio koji je moguće zadržati ostane na Oracleu, dok se za preostale komponente koristi drugačiji pristup kroz dostupne besplatne servise kao što su Render, Supabase i Qdrant Cloud.  

**Posljedice odluke:**  

**Pozitivne:**  
- projekat se može nastaviti razvijati bez čekanja dostupnosti Oracle instanci  
- zadržava se free-tier pristup bez dodatnih troškova  
- moguće je testirati sistem u realnijem okruženju  
- dio infrastrukture ostaje na Oracleu, čime se ne odbacuje prvobitni plan u potpunosti  

**Negativne:**  
- infrastruktura je podijeljena na više servisa  
- potrebno je dodatno voditi računa o environment varijablama i konekcijama između servisa  
- free-tier servisi imaju ograničenja u performansama i dostupnosti  
- kasnije može biti potrebna migracija na stabilnije hosting rješenje  

**Status odluke:**  
Aktivna  

---

## **ID:** DL-02  

**Datum:** 25/04/2026  

**Naziv:** Odabir Supabase PostgreSQL baze za relacione podatke  

**Opis:**  
Sistem za AI chatbot asistenta zahtijeva bazu podataka za čuvanje korisnika, transkripata, segmenata, baze znanja, chat sesija, poruka, odgovora, feedback-a i anomalija. Baza mora podržati relacione veze između entiteta i omogućiti jednostavan rad tokom razvoja i testiranja.  

**Razmatrane opcije:**  
- Lokalni PostgreSQL  
- Supabase PostgreSQL  
- Neon PostgreSQL  
- Railway PostgreSQL  

**Odabrana opcija:**  
Supabase PostgreSQL  

**Razlog izbora:**  
Supabase je odabran jer omogućava besplatan PostgreSQL hosting, jednostavno upravljanje tabelama i konekcijama, te je dovoljno pogodan za razvojnu fazu projekta. Pošto sistem ima više povezanih entiteta, PostgreSQL odgovara potrebama projekta bolje od nerelacionih baza. Supabase također olakšava timski rad jer članovi tima mogu pristupiti istoj bazi bez potrebe za lokalnim podešavanjem identičnog okruženja.  

**Posljedice odluke:**  

**Pozitivne:**  
- jednostavno pokretanje relacione baze bez dodatnih troškova  
- lakše dijeljenje baze između članova tima  
- PostgreSQL podržava sve potrebne relacije u sistemu  
- pogodno za čuvanje korisnika, transkripata, poruka i odgovora chatbota  

**Negativne:**  
- free plan ima ograničenja u resursima  
- potrebno je paziti na sigurnost konekcijskih podataka  
- veća zavisnost od eksternog servisa  
- kasnije može biti potrebna migracija ako projekat preraste free-tier ograničenja  

**Status odluke:**  
Aktivna  

---

## **ID:** DL-03  

**Datum:** 26/04/2026  

**Naziv:** Odabir Qdrant vektorske baze za RAG pretragu  

**Opis:**  
AI chatbot mora moći pronaći relevantne dijelove baze znanja na osnovu korisničkog pitanja. Za to je potrebna vektorska baza koja čuva embeddinge segmenata i omogućava semantičku pretragu nad transkriptima i unosima baze znanja.  

**Razmatrane opcije:**  
- Qdrant  
- Pinecone  
- pgvector unutar PostgreSQL baze  
- lokalno čuvanje embeddinga bez posebne vektorske baze  

**Odabrana opcija:**  
Qdrant  

**Razlog izbora:**  
Qdrant je odabran jer je pogodan za RAG sistem, podržava vektorsku pretragu, može se koristiti kroz free-tier opciju i dobro se uklapa u arhitekturu projekta. Odvojena vektorska baza omogućava da se relacione informacije čuvaju u PostgreSQL bazi, dok se semantička pretraga izvršava nad embeddingima u Qdrantu. Time se jasno razdvaja poslovna baza podataka od AI retrieval dijela sistema.  

**Posljedice odluke:**  

**Pozitivne:**  
- omogućena semantička pretraga nad bazom znanja  
- jasna podjela između relacione baze i vektorske pretrage  
- pogodno za RAG pristup u chatbotu  
- moguće je povezati pronađeni vektorski rezultat sa konkretnim unosom baze znanja  

**Negativne:**  
- uvodi se dodatni servis koji treba konfigurisati i održavati  
- potrebno je sinhronizovati podatke između PostgreSQL baze i Qdranta  
- greške u embedding procesu mogu uticati na kvalitet odgovora chatbota  
- free-tier ograničenja mogu uticati na obim testiranja  

**Status odluke:**  
Aktivna  

---

## **ID:** DL-04  

**Datum:** 27/04/2026  

**Naziv:** Asinhrona obrada transkripata u Python backend-u umjesto zasebnog free background worker-a  

**Opis:**  
Obrada transkripata, generisanje embeddinga i priprema baze znanja mogu trajati duže od običnog API zahtjeva. Zbog toga je bilo potrebno odlučiti kako će se izvršavati dugotrajniji procesi, posebno obrada transkripata i priprema podataka za RAG sistem.  

**Razmatrane opcije:**  
- Celery worker sa Redis brokerom  
- Background worker na posebnom hosting servisu  
- Python asinhrona obrada unutar backend aplikacije  
- Ručna obrada transkripata bez asinhronog procesa  

**Odabrana opcija:**  
Python asinhrona obrada unutar backend aplikacije za trenutnu fazu projekta.  

**Razlog izbora:**  
Celery je bio razmatran kao standardno rješenje za dugotrajne taskove, ali tim nije mogao pronaći pouzdanu besplatnu opciju za odvojene background workere u okviru dostupnih free-tier servisa. Zbog toga je odlučeno da se u trenutnoj fazi obrada radi asinhrono kroz Python backend, bez dodatnog zasebnog worker servisa. Ovim se pojednostavljuje deployment i smanjuje broj servisa koje treba održavati.  

**Posljedice odluke:**  

**Pozitivne:**  
- jednostavniji deployment jer nema dodatnog worker servisa  
- smanjen broj eksternih zavisnosti  
- obrada transkripata može se implementirati direktno u Python backend-u  
- rješenje je dovoljno za trenutni obim projekta i demonstraciju funkcionalnosti  

**Negativne:**  
- backend može biti opterećeniji tokom obrade većih transkripata  
- manje skalabilno od odvojenog Celery worker pristupa  
- potrebno je pažljivo rukovati timeoutima i greškama u obradi  
- u kasnijoj fazi može biti potrebna migracija na pravi background worker sistem  

**Status odluke:**  
Aktivna  

---

## **ID:** DL-05  

**Datum:** 28/04/2026  

**Naziv:** Odabir RAG pristupa za generisanje odgovora chatbota  

**Opis:**  
Chatbot treba pomagati agentima call centra tako što odgovara na pitanja koristeći prethodno obrađene transkripte i bazu znanja. Potrebno je odlučiti da li će chatbot odgovarati samo generativno ili će odgovore zasnivati na pronađenim relevantnim informacijama iz baze znanja.  

**Razmatrane opcije:**  
- Direktno slanje pitanja LLM modelu bez konteksta  
- Klasična keyword pretraga nad bazom znanja  
- Retrieval-Augmented Generation pristup  
- Ručno pretraživanje baze znanja bez AI generisanja odgovora  

**Odabrana opcija:**  
Retrieval-Augmented Generation pristup  

**Razlog izbora:**  
RAG pristup je odabran jer omogućava da chatbot prije generisanja odgovora pronađe relevantne dijelove baze znanja. Na taj način se smanjuje rizik da chatbot odgovara bez oslonca na podatke iz projekta. Pitanje korisnika se pretvara u embedding, zatim se kroz vektorsku bazu pronalaze relevantni segmenti, a pronađeni kontekst se koristi za generisanje odgovora.  

**Posljedice odluke:**  

**Pozitivne:**  
- odgovori chatbota se zasnivaju na sadržaju baze znanja  
- moguće je pratiti izvor odgovora kroz segment/transkript  
- sistem je pogodniji za call-centar scenarije gdje je bitna tačnost informacija  
- omogućava fallback odgovor ako nema dovoljno pouzdanog konteksta  

**Negativne:**  
- kvalitet odgovora zavisi od kvaliteta transkripata i embeddinga  
- pogrešan retrieval može dovesti do nepreciznog odgovora  
- implementacija je složenija od običnog poziva LLM modela  
- potrebno je testirati prag pouzdanosti i ponašanje sistema kod nepoznatih pitanja  

**Status odluke:**  
Aktivna  

---

## **ID:** DL-06  

**Datum:** 28/04/2026  

**Naziv:** Korištenje lokalnih embeddinga i Groq LLM API-ja  

**Opis:**  
Za AI dio sistema potrebno je odabrati način generisanja embeddinga i model koji će generisati konačne odgovore chatbota. Rješenje treba biti dovoljno brzo, dostupno kroz free-tier ili niskobudžetni pristup i pogodno za integraciju sa Python backend-om.  

**Razmatrane opcije:**  
- OpenAI API za embeddinge i generisanje odgovora  
- Lokalni embedding model i Groq API za LLM odgovore  
- Potpuno lokalni LLM model  
- Samo keyword-based pretraga bez LLM-a  

**Odabrana opcija:**  
Lokalni embedding model uz Groq API za generisanje odgovora.  

**Razlog izbora:**  
Lokalni embedding model smanjuje zavisnost od plaćenih API poziva za svaku obradu segmenta, dok Groq API omogućava brzo generisanje odgovora na osnovu pronađenog konteksta. Ovaj pristup je pogodan za studentski projekat jer balansira troškove, brzinu i kvalitet odgovora.  

**Posljedice odluke:**  

**Pozitivne:**  
- manji troškovi jer se embeddingi mogu generisati lokalno  
- brži odgovori kroz eksterni LLM API  
- bolja kontrola nad RAG pipeline-om  
- mogućnost ponovne upotrebe embeddinga bez stalnog slanja podataka eksternom servisu  

**Negativne:**  
- lokalni embedding model može zahtijevati dodatne resurse  
- Groq API zahtijeva validan API ključ i stabilnu konekciju  
- kvalitet odgovora zavisi od kvaliteta prompta i pronađenog konteksta  
- potrebno je paziti na sigurnost API ključeva  

**Status odluke:**  
Aktivna  

---

## **ID:** DL-07  

**Datum:** 29/04/2026  

**Naziv:** Izolacija testnog okruženja od glavne baze podataka  

**Opis:**  
Pošto sistem radi sa korisnicima, transkriptima, segmentima, bazom znanja i chat historijom, potrebno je odlučiti kako testirati funkcionalnosti bez narušavanja podataka u glavnoj bazi. Testiranje direktno nad glavnom bazom može dovesti do nekonzistentnih podataka i otežati validaciju rezultata.  

**Razmatrane opcije:**  
- Testiranje direktno nad glavnom bazom  
- Korištenje posebne testne baze  
- Mockovanje svih baza i servisa  
- Ručno testiranje bez automatskih testova  

**Odabrana opcija:**  
Korištenje odvojenog testnog okruženja i posebne testne baze gdje je moguće.  

**Razlog izbora:**  
Odvojeno testno okruženje omogućava sigurnije testiranje API ruta, autentifikacije, obrade transkripata i RAG logike bez rizika da se oštete stvarni razvojni podaci. Ovaj pristup je pogodniji za integracijske testove jer se može provjeriti stvarno ponašanje sistema, ali bez rada nad glavnom bazom.  

**Posljedice odluke:**  

**Pozitivne:**  
- sigurnije testiranje backend i frontend funkcionalnosti  
- smanjen rizik od oštećenja glavnih podataka  
- lakša provjera migracija i API ruta  
- bolja kontrola nad testnim scenarijima  

**Negativne:**  
- potrebno je održavati dodatnu konfiguraciju za testno okruženje  
- migracije se moraju usklađivati između glavne i testne baze  
- potrebno je dodatno vrijeme za pripremu testnih podataka  
- testno okruženje možda neće uvijek potpuno odgovarati produkcionom okruženju  

**Status odluke:**  
Aktivna  

---

## **ID:** DL-08  

**Datum:** 30/04/2026  

**Naziv:** Resetovanje state-a komponente putem remount mehanizma u frontend-u  

**Opis:**  
Klik na već aktivnu sekciju u sidebaru nije resetovao prikaz liste transkripata. Bilo je potrebno omogućiti da svaki klik na sekciju vrati korisnika na početni prikaz liste.  

**Razmatrane opcije:**  
- Ručno resetovanje state-a unutar komponente  
- Korištenje global state management rješenja  
- Forsiranje remount-a komponente putem key promjene  

**Odabrana opcija:**  
Forsiranje remount-a komponente korištenjem promjene key vrijednosti.  

**Razlog izbora:**  
Ovaj pristup je jednostavan za implementaciju, ne zahtijeva dodatne biblioteke i omogućava brzo resetovanje interne state logike komponente bez većih izmjena u kodu.  

**Posljedice odluke:**  

**Pozitivne:**  
- jednostavna implementacija  
- rješava problem navigacije bez velikih promjena  
- omogućava konzistentno ponašanje korisničkog interfejsa  

**Negativne:**  
- može imati uticaj na performanse ako se koristi prečesto  
- dolazi do gubitka lokalnog state-a komponente  

**Status odluke:**  

Aktivna  

---

## **ID:** DL-09  

**Datum:** 30/04/2026  

**Naziv:** Korištenje stvarnih podataka umjesto hardkodiranih vrijednosti na dashboardu  

**Opis:**  
Dashboard je inicijalno koristio hardkodirane vrijednosti koje nisu odražavale stvarno stanje sistema, pa je bilo potrebno omogućiti prikaz stvarnih podataka iz backend-a.  

**Razmatrane opcije:**  
- Hardkodirani podaci  
- Mock podaci  
- Povlačenje stvarnih podataka putem API-ja  

**Odabrana opcija:**  
Korištenje stvarnih podataka gdje je moguće, uz placeholder vrijednosti za metrike koje još nisu implementirane.  

**Razlog izbora:**  
Prikaz stvarnih podataka omogućava realniji uvid u stanje sistema i bolju pripremu za demonstraciju projekta.  

**Posljedice odluke:**  

**Pozitivne:**  
- dashboard prikazuje realne podatke  
- bolji uvid u stanje sistema  
- aplikacija je spremnija za demonstraciju  

**Negativne:**  
- zavisnost od backend endpointa  
- neke metrike ostaju nepotpune  
- potrebno koristiti placeholdere  

**Status odluke:**  

Aktivna

---

## **ID:** DL-10

**Datum:** 07/05/2026

**Naziv:** Razdvajanje monolitnog preprocessing servisa u zasebne module

**Opis:**
Originalni preprocessing pipeline bio je implementiran kao jedan veliki servisni fajl koji je kombinovao
normalizaciju, PII maskiranje, ekstrakciju segmenata i kreiranje Q&A parova. Rastom funkcionalnosti i potrebom za
granularnim testovima postalo je potrebno jasno razdvojiti odgovornosti.

**Razmatrane opcije:**
- Zadržati monolitni servis i dodati unit testove za interne funkcije
- Razdvojiti logiku u zasebne module unutar `preprocessing/` paketa
- Uvesti plugin arhitekturu sa dinamičkim registrovanjem procesora

**Odabrana opcija:**
Razdvajanje u zasebne module: `normalize`, `speakers`, `chunking`, `pii/recognizers`, `pii/masker`, `pii/token_store`,
`audit`, `speakers_llm`.

**Razlog izbora:**
Svaki modul ima jasan ulaz i izlaz što omogućava testiranje u izolaciji bez pokretanja cijelog pipeline-a. Plugin
arhitektura bi uvela nepotrebnu kompleksnost za trenutni obim projekta.

**Posljedice odluke:**

**Pozitivne:**
- svaki modul može se testirati neovisno
- lakše praćenje odgovornosti i uvođenje izmjena
- jasnija granica između normalizacije, PII obrade i chunking-a

**Negativne:**
- više fajlova za navigaciju kroz projekat
- import putanje su duže i podložne grešci pri refaktoringu

**Status odluke:**
Aktivna

---

## **ID:** DL-11

**Datum:** 08/05/2026

**Naziv:** Odlaganje generisanja embeddinga do koraka odobravanja unosa

**Opis:**
U prethodnoj verziji pipeline-a, embedding se generisao odmah pri uploadu transkripta. Na free-tier hosting okruženju
(Render) ovo je uzrokovalo OOM greške jer se sentence-transformers model učitava u memoriju za svaki zahtjev.
Embedding je premješten u kasniji korak — tek kada administrator odobri unos baze znanja.

**Razmatrane opcije:**
- Generisanje embeddinga pri uploadu (prethodni pristup)
- Odlaganje embeddinga do odobravanja unosa
- Eksternalizacija embeddinga na zasebni worker servis

**Odabrana opcija:**
Odlaganje embeddinga do koraka odobravanja unosa u bazi znanja.

**Razlog izbora:**
Upload je sinhronizovan korisnički zahtjev koji mora biti brz. Embedding je skup korak koji administrator ionako ne
može koristiti sve dok unos nije odobren. Odlaganjem se eliminišu OOM greške na free-tier bez uvođenja zasebnog worker
servisa.

**Posljedice odluke:**

**Pozitivne:**
- nema OOM grešaka pri uploadu na free-tier okruženju
- upload odgovor je brži za korisnika
- embedding se radi samo za odobrene, kvalitetne unose

**Negativne:**
- Qdrant kolekcija se ne popunjava odmah po uploadu
- potreban je zaseban korak odobravanja koji mora triggerovati embedding
- administrator mora biti svjestan da unosi nisu pretraživi dok ne budu odobreni

**Status odluke:**
Aktivna

---

## **ID:** DL-12

**Datum:** 08/05/2026

**Naziv:** Enkriptovanje PII token mape Fernet algoritmom i čuvanje u bazi kao TokenMapRecord

**Opis:**
Maskiranje PII zamjenjuje originalne vrijednosti placeholderima, ali za potrebe revizije ili korekcije potrebno je
negdje čuvati mapiranje placeholder → originalna vrijednost. Čuvanje u čistom tekstu u bazi nije prihvatljivo zbog
regulatornih i sigurnosnih razloga.

**Razmatrane opcije:**
- Čuvanje token mape u čistom tekstu u bazi
- Enkriptovanje Fernet simetričnim ključem i čuvanje kao blob
- Eksternalna usluga za upravljanje tajnama (npr. HashiCorp Vault)
- Nepovratno maskiranje bez mogućnosti rekonstrukcije

**Odabrana opcija:**
Fernet enkriptovanje i čuvanje kao `TokenMapRecord` u relacionoj bazi.

**Razlog izbora:**
Fernet je dostupan kroz standardnu Python `cryptography` biblioteku koja je već u projektu. Za razliku od eksternih
usluga, ne uvodi novu infrastrukturnu zavisnost. Simetričan ključ se konfigurira kroz `TOKEN_MAP_KEY` env varijablu.
Nepovratno maskiranje je odbačeno jer revizija zahtijeva mogućnost rekonstrukcije.

**Posljedice odluke:**

**Pozitivne:**
- PII vrijednosti nikad nisu u čistom tekstu u bazi
- revizija je moguća za ovlaštene korisnike s ključem
- implementacija je lagana i nema novih infrastrukturnih zavisnosti

**Negativne:**
- gubitak `TOKEN_MAP_KEY` čini sve pohranjene token mape nepovratno nedekriptabilnim
- efemerni ključ pri nepostavljenoj varijabli znači gubitak mapa nakon restarta
- simetričan ključ mora biti siguran i rotiran po sigurnosnoj politici

**Status odluke:**
Aktivna

---

## **ID:** DL-13

**Datum:** 09/05/2026

**Naziv:** LLM speaker labeling kao fallback za audio transkripte s privacy boundary-em

**Opis:**
Pattern-based detekcija govornika (`split_turns`) ne funkcioniše za audio transkripte koji nemaju prefiks oznake
(Agent:/Korisnik:). Za takve slučajeve potreban je inteligentni fallback koji može prepoznati govornika iz konteksta
razgovora. Istovremeno, pravilo privatnosti zabranjuje slanje originalnog teksta s PII prema eksternom API-ju.

**Razmatrane opcije:**
- Označiti sve neprepoznate turnove kao `unknown` i preskočiti ih
- Poslati originalni tekst Groq LLM-u za labelovanje
- Poslati maskirani tekst Groq LLM-u za labelovanje
- Implementirati lokalni NER model za identifikaciju govornika

**Odabrana opcija:**
Slanje isključivo maskiranog teksta Groq LLM-u kao fallback, pri čemu LLM dobija instrukciju da čuva placeholdere
netaknutima.

**Razlog izbora:**
Maskiranje mora prethoditi svakom eksternom API pozivu — to je nepregovorivo pravilo privatnosti. Lokalni NER model bi
bio složeniji za postavljanje na free-tier bez GPU-a. Fallback na `[]` pri nedostupnosti Groqa osigurava da pipeline
ne pada.

**Posljedice odluke:**

**Pozitivne:**
- audio transkripti bez oznaka govornika mogu biti ispravno labelovani
- privacy boundary je garantovan na nivou koda i verificiran testom
- fallback na `[]` znači da pipeline degradira gracefully bez crash-a

**Negativne:**
- LLM call produžava trajanje pipeline-a za audio transkripte
- kvalitet labelovanja ovisi o Groq API-ju i može varirati
- placeholderi u tekstu mogu zbuniti LLM i dovesti do netačnog labelovanja

**Status odluke:**
Aktivna

---

## **ID:** DL-14

**Datum:** 10/05/2026

**Naziv:** Filtriranje Q&A parova kroz `_is_procedural_qa` provjeru kvaliteta

**Opis:**
Pipeline može kreirati Q&A parove iz svakog user→agent turn para, ali mnogi od njih su previše kratki ili se uglavnom
sastoje od PII placeholdera i ne nose proceduralni sadržaj koji bi bio koristan za RAG pretragu.

**Razmatrane opcije:**
- Kreirati Q&A par za svaki user→agent turn par bez filtriranja
- Filtrirati prema minimalnoj dužini pitanja i odgovora
- Filtrirati prema minimalnoj dužini i maksimalnom udjelu placeholdera u odgovoru
- Ručno označavanje Q&A parova od strane administratora bez automatskog filtriranja

**Odabrana opcija:**
Automatsko filtriranje kroz `_is_procedural_qa`: minimalno 5 riječi u pitanju, minimalno 10 u odgovoru, maksimalno 15%
placeholdera u odgovoru.

**Razlog izbora:**
Kratki odgovori ili odgovori koji se uglavnom sastoje od placeholdera ne prenose proceduralni kontekst i smanjuju
kvalitet RAG retrieval-a. Fiksni pragovi su konzervativni i mogu se prilagoditi ako budu prestrogi, ali sprečavaju
generisanje besmislenih Q&A unosa koji bi zatrpali bazu znanja.

**Posljedice odluke:**

**Pozitivne:**
- baza znanja sadrži samo proceduralne Q&A parove
- manji broj niskokvalitetnih unosa znači bolji RAG retrieval
- manje unosa koje administrator mora ručno pregledati

**Negativne:**
- neki legitimni kratki odgovori mogu biti odbačeni
- pragovi su arbitrarni i mogu zahtijevati kalibraciju
- nije moguće lako rekonstruisati koji su parovi odbačeni bez pregleda loga

**Status odluke:**
Aktivna
