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
## **ID:** DL-15

**Datum:** 17/05/2026

**Naziv:** Korištenje gotovih govornih API-ja za glasovni unos i audio transkripciju

**Opis:**
Sprint 8 uvodi dvije funkcionalnosti povezane s govorom: korisnik može diktirati pitanje u chat, a administrator ili agent može uploadovati audio zapis i dobiti transkript prije spremanja. Bilo je potrebno odlučiti da li razvijati vlastitu speech-to-text logiku ili koristiti postojeće API-je.

**Razmatrane opcije:**
- Ručni unos transkripata bez audio funkcionalnosti
- Vlastiti speech-to-text model u backend-u
- Groq Whisper API za audio transkripciju i browser Web Speech API za glasovni unos
- Slanje svakog glasovnog unosa na backend radi server-side transkripcije

**Odabrana opcija:**
Korištenje Groq Whisper API-ja za transkripciju uploadovanih audio fajlova i browser Web Speech API-ja za glasovni unos u chatu.

**Razlog izbora:**
Vlastiti speech-to-text model bi značajno povećao zahtjeve za memorijom i procesorskim resursima, što nije pogodno za free-tier okruženje. Groq Whisper API omogućava praktičnu transkripciju audio fajlova, dok Web Speech API omogućava brzu implementaciju diktiranja direktno u browseru bez dodatnog backend opterećenja.

**Posljedice odluke:**

**Pozitivne:**
- audio transkripcija i diktiranje su isporučeni bez uvođenja vlastitog ML modela
- backend ostaje jednostavniji i manje opterećen
- korisnik može brže postavljati pitanja glasom
- administratori i agenti mogu puniti bazu znanja snimljenim pozivima bez ručnog prepisivanja

**Negativne:**
- funkcionalnost zavisi od dostupnosti eksternog transkripcijskog API-ja
- browser podrška za Web Speech API nije jednaka u svim browserima
- kvalitet transkripcije zavisi od kvaliteta audio zapisa
- potrebno je ručno pregledati automatski generisan transkript prije spremanja

**Status odluke:**
Aktivna

---

## **ID:** DL-16

**Datum:** 17/05/2026

**Naziv:** Preview-before-save tok za audio transkripte

**Opis:**
Audio transkripcija može sadržavati greške zbog šuma, akcenta, lošeg snimka ili neprepoznatog govora. Zbog toga je bilo potrebno odlučiti da li sistem smije automatski spremiti generisani transkript ili korisnik mora potvrditi tekst prije pohrane.

**Razmatrane opcije:**
- Automatsko spremanje transkripta odmah nakon transkripcije
- Preview transkripta i ručna potvrda prije spremanja
- Spremanje audio fajla bez transkripcije
- Ručno prepisivanje audio fajlova bez automatske pomoći

**Odabrana opcija:**
Preview transkripta i ručna potvrda prije konačnog spremanja u sistem.

**Razlog izbora:**
Transkript direktno utiče na bazu znanja i kasnije RAG odgovore chatbota. Ako se netačan transkript automatski spremi, greška se može prenijeti u Q&A parove i dovesti do loših odgovora. Pregled prije spremanja zadržava automatizaciju, ali dodaje kontrolu kvaliteta prije nego što sadržaj uđe u sistem.

**Posljedice odluke:**

**Pozitivne:**
- smanjuje se rizik pohrane netačnog ili nepotpunog transkripta
- korisnik ima kontrolu prije pokretanja daljnje obrade
- isti pipeline se može koristiti tek nakon potvrđenog teksta
- bolji kvalitet ulaznih podataka za bazu znanja

**Negativne:**
- proces unosa audio transkripta ima dodatni korak
- korisnik mora ručno pregledati i potvrditi generisani tekst
- nije potpuno automatizovan tok od audio fajla do baze znanja

**Status odluke:**
Aktivna

---

## **ID:** DL-17

**Datum:** 17/05/2026

**Naziv:** RAG/LLM routing sa confidence pragom i fallback-om prema agentu

**Opis:**
Chatbot u Sprintu 8 mora odgovoriti iz baze znanja kada postoji relevantan sadržaj, ali ne smije izmišljati odgovor kada relevantan sadržaj ne postoji. Bilo je potrebno definisati način odlučivanja između RAG odgovora, osnovnog LLM odgovora i eskalacije prema agentu.

**Razmatrane opcije:**
- Uvijek koristiti direktan LLM odgovor
- Uvijek koristiti RAG retrieval bez fallback-a
- Kombinovati klasifikaciju upita, RAG retrieval i confidence prag
- Svaki nepoznat upit odmah preusmjeriti agentu

**Odabrana opcija:**
Kombinovani RAG/LLM routing sa confidence pragom i fallback-om prema agentu.

**Razlog izbora:**
Ovaj pristup omogućava prirodan odgovor na pozdrave i općenite upite, ali za domenske upite koristi bazu znanja. Kada retrieval ne pronađe dovoljno pouzdan sadržaj, chatbot ne izmišlja odgovor nego korisniku nudi povezivanje s agentom. Time se balansira korisničko iskustvo, tačnost i sigurnost odgovora.

**Posljedice odluke:**

**Pozitivne:**
- smanjuje se rizik haluciniranih odgovora
- korisnik dobija odgovor iz baze znanja kada je sadržaj dostupan
- pozdravi i jednostavna pitanja ne opterećuju agente
- nepoznati upiti se jasno usmjeravaju prema ljudskom agentu

**Negativne:**
- prag pouzdanosti treba dodatno kalibrisati kroz testiranje
- LLM klasifikacija može pogriješiti kod kratkih ili dvosmislenih upita
- implementacija je složenija od običnog generativnog chata

**Status odluke:**
Aktivna

---

## **ID:** DL-18

**Datum:** 17/05/2026

**Naziv:** Eksplicitni model stanja za eskalacije i idempotentno kreiranje zahtjeva

**Opis:**
Eskalirani korisnički upit prolazi kroz više faza: čekanje, prihvatanje od agenta, eventualno vraćanje u queue, rješavanje ili napuštanje. Bilo je potrebno odlučiti kako modelovati ta stanja i spriječiti kreiranje duplih aktivnih zahtjeva za istog korisnika.

**Razmatrane opcije:**
- Jednostavan boolean flag `rijeseno`
- Eksplicitni statusi eskalacije i ručno definisani prijelazi u servisnom sloju
- Vanjska state machine biblioteka
- Oslanjanje na frontend da spriječi duple zahtjeve

**Odabrana opcija:**
Eksplicitni statusi `Cekanje`, `UToku`, `Rijesena` i `Napustena`, uz idempotentno kreiranje aktivne eskalacije.

**Razlog izbora:**
Broj statusa je ograničen i dovoljno jasan da se može održavati bez dodatne biblioteke. Idempotentnost sprečava da korisnik višestrukim klikom kreira više aktivnih queue stavki. Statusni model olakšava filtriranje queue-a, prikaz agentu i pisanje testova za prijelaze stanja.

**Posljedice odluke:**

**Pozitivne:**
- jasniji lifecycle eskaliranog razgovora
- manje duplikata u queue-u
- lakše testiranje statusnih prijelaza
- bolja osnova za agent status i resolving funkcionalnost

**Negativne:**
- potrebno je održavati usklađenost statusa kroz backend, bazu i frontend
- bez baze-level lockinga ostaju mogući race condition scenariji
- servisni sloj postaje odgovorniji i složeniji

**Status odluke:**
Aktivna

---

## **ID:** DL-19

**Datum:** 18/05/2026

**Naziv:** Odabir WebSocket protokola za real-time komunikaciju korisnika i agenta

**Opis:**
Za live chat između korisnika i agenta potreban je mehanizam koji omogućava dvosmjernu komunikaciju u realnom vremenu bez refreshovanja stranice. Sistem mora slati poruke, sistemske evente, queue sync i obavještenja o zatvaranju sesije.

**Razmatrane opcije:**
- Long polling preko HTTP zahtjeva
- Server-Sent Events za jednosmjerni server push
- WebSocket protokol
- Periodično osvježavanje queue-a i poruka

**Odabrana opcija:**
WebSocket protokol implementiran kroz FastAPI WebSocket endpoint-e.

**Razlog izbora:**
WebSocket podržava dvosmjernu komunikaciju u realnom vremenu i najviše odgovara chat use case-u. Long polling bi povećao broj HTTP zahtjeva i latenciju, a SSE nije dovoljan jer ne pokriva slanje poruka od klijenta prema serveru kroz isti kanal. FastAPI već podržava WebSocket endpoint-e, pa nije bilo potrebno uvoditi dodatnu biblioteku.

**Posljedice odluke:**

**Pozitivne:**
- poruke između korisnika i agenta stižu bez potrebe za reload-om
- isti kanal može nositi poruke, sistemske evente i indikatore
- queue se može ažurirati agentu u realnom vremenu
- arhitektura odgovara live chat funkcionalnosti

**Negativne:**
- potrebno je upravljati životnim ciklusom konekcija
- testiranje je složenije od standardnih HTTP ruta
- free-tier hosting može ograničiti broj i trajanje otvorenih veza
- horizontalno skaliranje zahtijevalo bi dodatno distribuirano rješenje

**Status odluke:**
Aktivna

---

## **ID:** DL-20

**Datum:** 18/05/2026

**Naziv:** Singleton `ConnectionManager` kao centralno mjesto upravljanja WebSocket vezama

**Opis:**
Nakon odabira WebSocket-a bilo je potrebno odrediti gdje se čuvaju aktivne veze korisnika i agenata. Pošto se poruke rutiraju između različitih endpoint-a i uloga, sistem mora imati centralno mjesto za slanje, broadcast i čišćenje neaktivnih konekcija.

**Razmatrane opcije:**
- Singleton `ConnectionManager` u memoriji aplikacije
- Redis pub/sub za distribuirane instance
- Čuvanje konekcija lokalno u svakom endpoint handler-u
- Prosljeđivanje konekcija kroz dependency injection

**Odabrana opcija:**
Singleton `ConnectionManager` u memoriji aplikacije.

**Razlog izbora:**
Projekat se u ovoj fazi pokreće kao jedna aplikacijska instanca, pa Redis pub/sub ne bi donio stvarnu korist u odnosu na kompleksnost. Singleton omogućava jednostavnu implementaciju i testiranje, a dovoljan je za MVP i demonstraciju real-time komunikacije.

**Posljedice odluke:**

**Pozitivne:**
- jednostavno centralizovano upravljanje vezama
- lakše slanje poruka korisniku ili agentu iz različitih dijelova aplikacije
- moguće je automatski čistiti mrtve veze pri neuspješnom slanju
- lako se testira uz mockovane WebSocket objekte

**Negativne:**
- restart aplikacije briše sve aktivne veze
- pristup nije pogodan za horizontalno skaliranje na više instanci
- stanje nije perzistentno i ne smije se koristiti kao izvor istine za historiju poruka

**Status odluke:**
Aktivna

---

## **ID:** DL-21

**Datum:** 18/05/2026

**Naziv:** Odvajanje agent panela od admin panela uz role-based vidljivost podataka

**Opis:**
Sprint 8 uvodi radni panel za call-centar agente. Bilo je potrebno odlučiti da li agenti koriste isti admin panel ili dobijaju vlastiti panel s ograničenim prikazom dodijeljenih razgovora, Live Queue-a i pretrage baze znanja.

**Razmatrane opcije:**
- Korištenje postojećeg admin panela za sve uloge
- Zaseban agent panel sa agent-specifičnim Live Queue-om
- Jedan zajednički queue vidljiv svim agentima bez ograničenja
- Samo backend API bez posebnog agent UI-a

**Odabrana opcija:**
Zaseban agent panel sa role-based prikazom sesija i agent-specifičnim Live Queue-om.

**Razlog izbora:**
Agentima treba radni prostor koji prikazuje samo relevantne aktivne upite i sesije, dok admin zadržava širi pregled sistema. Odvajanje panela smanjuje vizuelnu složenost za agente i sprečava da agent slučajno radi s podacima koji mu nisu dodijeljeni.

**Posljedice odluke:**

**Pozitivne:**
- agent vidi samo relevantne razgovore i zadatke
- admin i agent imaju jasnije odvojene odgovornosti
- lakše je kontrolisati pristup podacima kroz uloge
- Live Queue i chat panel su prilagođeni svakodnevnom radu agenta

**Negativne:**
- frontend ima više komponenti i odvojene navigacijske tokove
- potrebno je održavati role-based logiku na backend-u i frontend-u
- postoji rizik neusklađenog prikaza ako API i UI različito tumače status sesije

**Status odluke:**
Aktivna

---

## **ID:** DL-22

**Datum:** 18/05/2026

**Naziv:** Agent locking i zaobilaženje RAG toka tokom aktivne live sesije

**Opis:**
Kada agent preuzme razgovor, korisnikove naredne poruke ne smiju ponovo prolaziti kroz chatbot/RAG tok, jer bi chatbot mogao paralelno odgovarati dok agent već vodi razgovor. Bilo je potrebno odlučiti kako rutirati poruke u aktivnoj agentskoj sesiji.

**Razmatrane opcije:**
- Nastaviti slati svaku poruku i chatbotu i agentu
- Potpuno isključiti chat dok agent ne odgovori
- Zaključati aktivnu sesiju na dodijeljenog agenta i zaobići RAG tok
- Dozvoliti više agenata da istovremeno preuzmu isti razgovor

**Odabrana opcija:**
Agent locking: dok je eskalacija u statusu `UToku`, poruke korisnika se šalju dodijeljenom agentu i zaobilaze RAG odgovor.

**Razlog izbora:**
U live podršci mora biti jasno ko odgovara korisniku. Ako chatbot nastavi odgovarati paralelno s agentom, korisnik može dobiti kontradiktorne ili duplirane poruke. Zaključavanje sesije na agenta daje jasnu odgovornost i omogućava čisto zatvaranje razgovora kroz resolving tok.

**Posljedice odluke:**

**Pozitivne:**
- nema paralelnog odgovaranja chatbota tokom live agentske sesije
- korisnik zna da razgovara s agentom
- agent ima kontrolu nad aktivnim razgovorom
- resolving i historija razgovora postaju konzistentniji

**Negativne:**
- ako agent ne odgovori, korisnik ne dobija automatski RAG fallback dok je sesija aktivna
- potrebno je pravilno osloboditi ili zatvoriti sesiju ako agent napusti razgovor
- bez dodatnog baze-level zaključavanja ostaju mogući rijetki race condition scenariji

**Status odluke:**
Aktivna

---
## **ID:** DL-23

**Datum:** 20/05/2026

**Naziv:** Regresijski pristup poboljšanju PII maskiranja i Q&A ekstrakcije

**Opis:**
Sprint 9 je identifikovao da određeni edge case formati JMBG-a, telefonskih brojeva i loše ekstrahovanih Q&A parova mogu narušiti sigurnost podataka i kvalitet baze znanja. Bilo je potrebno odlučiti da li te slučajeve popravljati ručno ili kroz sistemska pravila i regresijske testove.

**Razmatrane opcije:**
- Ručno čišćenje problematičnih transkripata nakon obrade
- Proširenje pravila maskiranja i ekstrakcije uz regresijske testove
- Uvođenje dodatnog NLP modela za procjenu kvaliteta Q&A parova
- Oslanjanje na administratora da naknadno ukloni loše unose

**Odabrana opcija:**
Proširenje pravila PII maskiranja i ekstrakcije Q&A parova, uz automatizovane regresijske testove za poznate edge caseove.

**Razlog izbora:**
Problem se ponavlja na nivou pipeline-a i zato ga treba rješavati prije nego što podaci uđu u bazu znanja. Ručno čišćenje ne skalira i ne sprečava ponovno pojavljivanje istih grešaka. Regresijski testovi osiguravaju da se već riješeni formati ne pokvare u kasnijim izmjenama.

**Posljedice odluke:**

**Pozitivne:**
- smanjuje se rizik curenja PII podataka
- baza znanja dobija manje nekvalitetnih Q&A parova
- poznati bugovi su pokriveni regresijskim testovima
- pipeline ostaje determinističan i lakši za održavanje

**Negativne:**
- regex i heuristička pravila treba stalno održavati
- prestroga pravila mogu odbaciti neke legitimne kratke odgovore
- novi edge caseovi i dalje mogu zahtijevati dodatne testove

**Status odluke:**
Aktivna

---

## **ID:** DL-24

**Datum:** 20/05/2026

**Naziv:** Ocjenjivanje cijele chat sesije umjesto pojedinačnih poruka

**Opis:**
Raniji feedback mehanizam zasnivao se na impulsivnom ocjenjivanju pojedinačnih poruka. Sprint 9 zahtijeva relevantniju povratnu informaciju o kompletnom iskustvu razgovora, uključujući chatbot i potencijalnu eskalaciju prema agentu.

**Razmatrane opcije:**
- Zadržati thumbs-up/thumbs-down po poruci
- Dodati ocjenu 1–5 na kraju sesije
- Učiniti ocjenu obaveznom prije zatvaranja chata
- Prikupljati feedback samo od agenata

**Odabrana opcija:**
Forma za ocjenu kompletne sesije na kraju razgovora, s numeričkom ocjenom 1–5 i opcionalnim komentarom.

**Razlog izbora:**
Ocjena cijele sesije bolje odražava korisničko iskustvo od ocjene pojedinačne poruke. Opcionalni komentar daje dodatni kontekst administratoru i agentima, dok neobavezno slanje sprječava frustraciju korisnika.

**Posljedice odluke:**

**Pozitivne:**
- feedback je vezan za cijeli razgovor, a ne samo jednu poruku
- komentar korisnika pomaže adminu da razumije razlog ocjene
- uklanja se vizuelni šum thumbs-up/down kontrola iz Chat UI-a
- ocjene se mogu koristiti za kasniju analitiku kvaliteta

**Negativne:**
- manje korisnika može poslati feedback jer ocjena nije obavezna
- potrebno je spriječiti duplo ocjenjivanje iste sesije
- model feedback-a mora jasno razlikovati sesijske i poruka-level zapise

**Status odluke:**
Aktivna

---

## **ID:** DL-25

**Datum:** 20/05/2026

**Naziv:** Administratorski kontrolisan sistemski baner u Chat UI-u

**Opis:**
Korisnici moraju biti proaktivno obaviješteni o poznatim problemima ili planiranom održavanju bez prekidanja rada chata. Bilo je potrebno odlučiti kako prikazati takve obavijesti i ko ih kontroliše.

**Razmatrane opcije:**
- Hardkodirana poruka u Chat UI-u
- Modalna obavijest koja blokira chat
- Administratorski kontrolisan baner koji se može aktivirati i deaktivirati
- Slanje obavijesti kao obične chatbot poruke

**Odabrana opcija:**
Administratorski kontrolisan baner koji se prikazuje na vrhu Chat UI-a kada je aktivna sistemska obavijest.

**Razlog izbora:**
Baner je vidljiv i jasan, ali ne blokira korisnika. Administrator može mijenjati i deaktivirati poruku bez deploya, što je važno za dinamične situacije poput održavanja ili poznatih problema.

**Posljedice odluke:**

**Pozitivne:**
- korisnik je informisan prije slanja nepotrebnih upita
- obavijest ne prekida korištenje chata
- admin može upravljati sadržajem bez izmjene koda
- smanjuje se broj nepotrebnih eskalacija prema agentima

**Negativne:**
- zastarjela obavijest može zbuniti korisnike ako se ne deaktivira
- potrebno je dodatno stanje za pamćenje zatvaranja banera u toku sesije
- preduge poruke mogu narušiti izgled Chat UI-a

**Status odluke:**
Aktivna

---

## **ID:** DL-26

**Datum:** 21/05/2026

**Naziv:** Ručni Q&A unos uz trenutno embedovanje i indeksiranje u Qdrant

**Opis:**
Administratorima je bila potrebna mogućnost da dodaju provjerene Q&A parove direktno u bazu znanja bez kreiranja cijelog transkripta. Bilo je potrebno odlučiti da li ručni unos ide odmah u aktivnu bazu znanja ili prolazi kroz poseban proces čekanja.

**Razmatrane opcije:**
- Ručni unos kao prijedlog koji čeka dodatno odobrenje
- Ručni unos koji se odmah sprema, embeduje i indeksira u Qdrant
- Dodavanje ručnih unosa samo u PostgreSQL bez Qdrant indeksiranja
- Zadržavanje isključivo transkript-based unosa

**Odabrana opcija:**
Ručni Q&A unos koji se odmah validira, sprema, embeduje i indeksira u Qdrant, uz jasnu oznaku da je izvor ručni unos.

**Razlog izbora:**
Administrator unosi već provjerenu informaciju, pa dodatni approval korak nije potreban za MVP. Da bi chatbot odmah koristio novu informaciju, unos mora biti i u PostgreSQL bazi i u Qdrant vektorskoj bazi. Oznaka izvora omogućava kasnije razlikovanje ručnih i transkript-based unosa.

**Posljedice odluke:**

**Pozitivne:**
- nova provjerena informacija odmah postaje dostupna chatbotu
- nema potrebe za kreiranjem vještačkih transkripata
- izvor unosa ostaje transparentan kroz badge/source_type
- admin može brzo popravljati i dopunjavati bazu znanja

**Negativne:**
- pogrešan ručni unos odmah može uticati na odgovore chatbota
- update zahtijeva ponovno embedovanje i reindeksiranje
- greška u Qdrant indeksiranju može dovesti do nekonzistentnog stanja

**Status odluke:**
Aktivna

---

## **ID:** DL-27

**Datum:** 21/05/2026

**Naziv:** Singleton AI servisi i keširanje embeddinga za smanjenje latencije

**Opis:**
Chatbot odgovori su bili usporeni zbog ponovnog inicijaliziranja AI servisa i ponovnog generisanja embeddinga za iste upite. Bilo je potrebno optimizovati performanse bez promjene logike retrieval-a i bez uvođenja nove infrastrukture.

**Razmatrane opcije:**
- Nastaviti kreirati nove instance servisa po zahtjevu
- Singleton instance kroz module-level getter funkcije
- Redis keš za embeddinge i rezultate retrieval-a
- Eksternalizacija AI servisa na poseban mikroservis

**Odabrana opcija:**
Singleton instance AI servisa, `@lru_cache` za embeddinge i precizno mjerenje ukupne latencije kroz pipeline.

**Razlog izbora:**
Singleton i LRU keš su dovoljno jednostavni za trenutni obim projekta i ne zahtijevaju dodatnu infrastrukturu. Ovaj pristup smanjuje ponovnu inicijalizaciju modela i ponovne embedding operacije, a ne mijenja semantiku retrieval-a jer identičan tekst daje identičan vektor.

**Posljedice odluke:**

**Pozitivne:**
- model i klijenti se ne inicijaliziraju pri svakom zahtjevu
- ponovljeni identični upiti se brže obrađuju
- `latencija_ms` sada mjeri kompletan tok odgovora
- optimizacija ne mijenja retrieval i LLM logiku

**Negativne:**
- singleton stanje dijele svi zahtjevi i zahtijeva oprez pri budućim izmjenama
- LRU cache je u memoriji procesa i briše se restartom aplikacije
- semantički isti, ali tekstualno različiti upiti neće pogoditi keš

**Status odluke:**
Aktivna

---

## **ID:** DL-28

**Datum:** 21/05/2026

**Naziv:** User Settings meni za promjenu imena i destruktivne korisničke akcije

**Opis:**
Korisniku je trebalo omogućiti upravljanje osnovnim podacima i privatnošću bez kontaktiranja administratora: promjena imena, brisanje historije i brisanje naloga. Bilo je potrebno odlučiti gdje smjestiti te akcije i kako zaštititi destruktivne operacije.

**Razmatrane opcije:**
- Posebna Settings stranica
- Dropdown meni iz avatar ikone
- Administratorsko upravljanje svim promjenama
- Izložiti akcije direktno u glavnoj navigaciji

**Odabrana opcija:**
User Settings dropdown iz avatar ikone, s inline formom za promjenu imena i potvrdnim ekranima za brisanje historije ili naloga.

**Razlog izbora:**
Avatar meni je prirodno mjesto za korisničke postavke i ne opterećuje glavnu navigaciju. Destruktivne akcije zahtijevaju potvrdu jer su nepovratne i uključuju kaskadno brisanje povezanih podataka.

**Posljedice odluke:**

**Pozitivne:**
- korisnik samostalno upravlja imenom i privatnošću
- glavna navigacija ostaje jednostavna
- destruktivne akcije imaju eksplicitnu potvrdu
- promjena imena se odmah reflektuje u UI-u

**Negativne:**
- dropdown ima više stanja i mora biti pažljivo testiran
- kaskadno brisanje mora poštovati sve FK veze
- brisanje naloga može otežati kasniju analizu historijskih podataka

**Status odluke:**
Aktivna

---

## **ID:** DL-29

**Datum:** 21/05/2026

**Naziv:** Kontekstni meni za brisanje pojedinačnih chat sesija

**Opis:**
Korisnici su trebali mogućnost brisanja pojedinih razgovora iz historije chata bez brisanja cijele historije. Bilo je potrebno odlučiti kako izložiti ovu akciju u interfejsu bez narušavanja preglednosti liste historije.

**Razmatrane opcije:**
- Dugme za brisanje vidljivo uz svaku stavku historije
- Kontekstni meni koji se pojavljuje desnim klikom
- Dugme za brisanje unutar otvorene chat sesije
- Grupno brisanje sesija kroz checkbox selekciju

**Odabrana opcija:**
Kontekstni meni pri desnom kliku na stavku historije.

**Razlog izbora:**
Kontekstni meni ne zauzima prostor u listi i ne ometa osnovni tok pregledavanja historije. Korisnik koji želi ukloniti specifičan chat može to uraditi selektivno, dok je brisanje cijele historije već dostupno kroz User Settings.

**Posljedice odluke:**

**Pozitivne:**
- historija ostaje vizuelno čista
- korisnik može selektivno ukloniti samo jedan razgovor
- meni se može proširiti dodatnim opcijama u budućnosti
- UI se ažurira bez reload-a liste

**Negativne:**
- desni klik nije idealan za touch uređaje
- akcija može biti manje otkriva za korisnike koji ne očekuju kontekstni meni
- potrebno je pažljivo pozicionirati meni da ne izlazi iz vidljivog područja

**Status odluke:**
Aktivna

---

## **ID:** DL-30

**Datum:** 22/05/2026

**Naziv:** React Portal za prikaz UserMenu dropdowna iznad stacking context-a

**Opis:**
UserMenu dropdown se prikazivao ispod dijelova chat interfejsa iako je imao visoku `z-index` vrijednost. Uzrok je bio `backdrop-filter` na headeru koji kreira novi CSS stacking context.

**Razmatrane opcije:**
- Povećati `z-index` vrijednost
- Ukloniti `backdrop-filter` iz headera
- Ručno premjestiti dropdown u DOM
- Koristiti `ReactDOM.createPortal` i renderovati dropdown u `document.body`

**Odabrana opcija:**
Korištenje `ReactDOM.createPortal` za renderovanje dropdowna direktno u `document.body`.

**Razlog izbora:**
Portal je standardan React obrazac za renderovanje elemenata koji moraju izaći iz DOM hijerarhije roditelja. Uklanjanje `backdrop-filter` efekta narušilo bi postojeći dizajn, a povećanje `z-index`-a ne rješava stacking context problem.

**Posljedice odluke:**

**Pozitivne:**
- dropdown se prikazuje iznad svih elemenata aplikacije
- zadržava se postojeći vizuelni stil headera
- rješenje radi na svim mjestima gdje se UserMenu koristi

**Negativne:**
- portal elementi nisu u istom DOM stablu kao komponenta koja ih inicira
- event handling za klik van menija mora uzeti u obzir portal
- developeri moraju znati da je dropdown renderovan izvan headera

**Status odluke:**
Aktivna

---

## **ID:** DL-31

**Datum:** 24/05/2026

**Naziv:** Modalni prikaz konkretne sesije iz Ratings sekcije i stroži `/agent` RBAC

**Opis:**
Admin je iz Ratings sekcije trebao pregledati tačno onu chat sesiju za koju je ostavljen komentar. Prethodni pristup navigacije na Chat Logs sa tekstualnim filterom mogao je prikazati više sličnih sesija. Istovremeno je uočeno da admin može direktno pristupiti `/agent` ruti.

**Razmatrane opcije:**
- Navigacija na Chat Logs s predfiltriranim parametrima
- Modalni prikaz konkretne sesije po `sesija_id`
- Nova stranica za detalje sesije
- Zadržavanje `/agent` rute dostupne adminu i agentu

**Odabrana opcija:**
Modalni prikaz konkretne sesije u `Ratings` komponenti i ograničavanje `/agent` rute isključivo na agent rolu.

**Razlog izbora:**
Modal čuva kontekst Ratings sekcije i prikazuje tačno povezani razgovor, bez rizika da tekstualni filter vrati pogrešnu sesiju. Agent panel treba biti radno okruženje samo za agente, dok admin ima vlastite administrativne poglede.

**Posljedice odluke:**

**Pozitivne:**
- admin vidi tačno razgovor koji je korisnik ocijenio
- nema nepotrebne navigacije iz Ratings sekcije
- agent panel je zaštićen role-based pravilom
- admin navigacija je čišća jer ne prikazuje Agent link

**Negativne:**
- modal prikaz ne sadrži sve metapodatke iz Chat Logs prikaza
- dodaje se admin endpoint koji mora strogo provjeravati admin rolu
- promjene u route guard logici mogu zahtijevati dodatne regresijske testove

**Status odluke:**
Aktivna

---

## **ID:** DL-32

**Datum:** 24/05/2026

**Naziv:** WebSocket keepalive i replay `agent_connected` eventa pri spajanju korisnika

**Opis:**
U real-time komunikaciji uočeni su problemi gdje je korisnik mogao propustiti događaj da je agent već prihvatio eskalaciju, a idle WebSocket konekcije su se mogle zatvoriti iza proxy-ja. Bilo je potrebno odlučiti kako stabilizovati konekcije bez uvođenja nove infrastrukture.

**Razmatrane opcije:**
- Podesiti samo proxy timeout konfiguraciju
- Slati periodični keepalive ping iz aplikacije
- Ponovno emitovati stanje aktivne eskalacije pri spajanju korisnika
- Uvesti Redis pub/sub i perzistentni message buffer

**Odabrana opcija:**
Aplikacijski keepalive ping za korisnički i agentski WebSocket, te provjera aktivne `UToku` eskalacije pri korisničkom connect-u uz replay `agent_connected` eventa.

**Razlog izbora:**
Keepalive je jednostavno rješenje za idle timeout i ne zavisi samo od hosting/proxy konfiguracije. Replay stanja pri spajanju osigurava da korisnik dobije trenutno stanje sesije čak i ako je agent prihvatio razgovor prije završetka WebSocket handshake-a.

**Posljedice odluke:**

**Pozitivne:**
- smanjuje se rizik gašenja idle WebSocket veza
- korisnik dobija ispravno stanje ako je agent već prihvatio razgovor
- rješenje ne zahtijeva dodatnu infrastrukturu
- cleanup se izvršava kroz `finally` blokove

**Negativne:**
- keepalive ne rješava sve realne mrežne prekide
- više paralelnih `useEscalation` instanci može i dalje uzrokovati reconnect probleme
- WebSocket stanje ostaje u memoriji procesa i nije distribuirano

**Status odluke:**
Aktivna

---
## **ID:** DL-33

**Datum:** 25/05/2026

**Naziv:** Google Drive on-demand batch import kroz postojeći transcript pipeline

**Opis:**
Za dodatne user storyje bilo je potrebno omogućiti batch procesiranje fajlova sa web lokacije, prvenstveno Google Drive foldera, bez ručnog uploada svakog pojedinačnog fajla. Istovremeno je bilo važno da se obrada ne duplira i da svi fajlovi prođu kroz isti proces transkripcije, čišćenja, ekstrakcije i kreiranja/poboljšanja baze znanja.

**Razmatrane opcije:**
- Ručni upload svakog fajla pojedinačno
- Novi poseban pipeline samo za Google Drive
- Google Drive import koji koristi postojeći upload i transcript pipeline
- Celery/worker sistem za batch import
- Generalizovani remote-source sistem za Drive, S3 i slične izvore odmah u ovoj fazi

**Odabrana opcija:**
Google Drive on-demand import koji koristi postojeći transcript pipeline i pokreće se iz admin panela kao BackgroundTask.

**Razlog izbora:**
Ovaj pristup isporučuje traženi batch import bez uvođenja novog servisa, worker infrastrukture ili paralelne logike. Pošto se fajlovi obrađuju kroz isti `process_transcript` tok kao i ručni upload, kvalitet i ponašanje pipeline-a ostaju konzistentni. Google Drive je odabran kao prvi konkretan remote izvor, dok je S3/generalizovani remote-source pristup ostavljen kao moguće proširenje.

**Posljedice odluke:**

**Pozitivne:**
- administrator može pokrenuti import cijelog foldera umjesto pojedinačnih uploadova
- svi fajlovi prolaze kroz postojeći pipeline i završavaju u istim ekranima za transkripte i bazu znanja
- nema nove baze, migracije, Celery-ja ili dodatnog servisa
- loš fajl ne prekida cijeli batch jer se greške hvataju po fajlu
- implementacija je pogodna za demonstraciju i kasnije proširenje na druge izvore

**Negativne:**
- implementacija je trenutno on-demand, a ne automatski scheduled import
- podržan je Google Drive, dok S3 i slični izvori nisu implementirani u ovom koraku
- BackgroundTask radi unutar backend procesa i nije jednako robusan kao pravi job queue
- audio reimport može ponovo trošiti transkripcijske API resurse

**Status odluke:**
Aktivna

---

## **ID:** DL-34

**Datum:** 25/05/2026

**Naziv:** Version-aware deduplikacija Drive fajlova preko `modifiedTime`

**Opis:**
Nakon uvođenja Drive importa bilo je potrebno odlučiti kako razlikovati fajlove koji su već importovani od fajlova koji imaju isto ime, ali su naknadno izmijenjeni ili obrisani i ponovo uploadovani. Jednostavna deduplikacija po nazivu fajla ne bi prepoznala ažuriranje sadržaja.

**Razmatrane opcije:**
- Deduplikacija samo po nazivu fajla
- Uvijek reimportovati sve fajlove iz foldera
- Čuvanje hash vrijednosti preuzetog sadržaja
- Deduplikacija po folderu, nazivu fajla i Drive `modifiedTime`
- Čuvanje više verzija istog fajla kao aktivnih unosa

**Odabrana opcija:**
Deduplikacija po folderu, nazivu fajla i Drive `modifiedTime`, uz zamjenu stare verzije tek nakon što je nova verzija uspješno preuzeta i validirana.

**Razlog izbora:**
`modifiedTime` omogućava da sistem prepozna kada je fajl stvarno izmijenjen bez potrebe za dodatnim hashiranjem sadržaja. Stara verzija se briše tek nakon validacije nove kako se ne bi izgubio prethodni dobar transkript ako novi upload padne ili je nevalidan.

**Posljedice odluke:**

**Pozitivne:**
- izmijenjeni Drive fajlovi se mogu ponovo obraditi i zamijeniti staru verziju
- isti neizmijenjeni fajl se ne importuje više puta
- baza znanja ne dobija duplikate za isti fajl
- stara dobra verzija ostaje sigurna ako nova verzija ne prođe validaciju
- UI i dalje prikazuje čist naziv fajla bez tehničkog version sufiksa

**Negativne:**
- prvi import nakon ove promjene može jednom reimportovati stare Drive fajlove bez `modifiedTime` zapisa
- audio fajlovi mogu ponovno aktivirati Whisper/transkripcijski API
- logika brisanja stare verzije mora ukloniti transkript, segmente, bazu znanja i Qdrant vektore konzistentno
- sistem zavisi od tačnosti Google Drive `modifiedTime` vrijednosti

**Status odluke:**
Aktivna

---

## **ID:** DL-35

**Datum:** 25/05/2026

**Naziv:** Optimizacija Docker builda kroz CPU-only Torch, BuildKit cache i `.dockerignore`

**Opis:**
Backend build je trajao predugo jer je `sentence-transformers` preko `torch` dependency-ja povlačio veliki CUDA build, iako aplikacija embeddinge izvršava na CPU-u. Pored toga, izmjene u `requirements.txt` poništavale su cijeli pip install sloj i uzrokovale ponovno skidanje svih dependency-ja.

**Razmatrane opcije:**
- Zadržati postojeći Dockerfile i prihvatiti spor build
- Izbaciti `sentence-transformers` iz projekta
- Preći na potpuno eksterni embedding API
- Instalirati CPU-only Torch u poseban sloj i koristiti BuildKit pip cache
- Ručno instalirati dependency-je van Docker build procesa

**Odabrana opcija:**
CPU-only Torch u posebnom Docker sloju, BuildKit cache mount za pip, Dockerfile syntax directive i novi `backend/.dockerignore`.

**Razlog izbora:**
Aplikacija nema GPU i koristi CPU embedding, pa CUDA build ne donosi korist. Instalacija CPU-only Torch-a prije ostatka `requirements.txt` sprečava povlačenje CUDA paketa i čini sloj stabilnim između izmjena. BuildKit pip cache čuva wheel-ove pa naredni buildovi ne moraju ponovo skidati sve biblioteke.

**Posljedice odluke:**

**Pozitivne:**
- izbjegava se multi-GB CUDA download koji nije potreban za runtime
- prvi build je kraći nego ranije, a naredni buildovi nakon cache-a su višestruko brži
- tim je značajno ubrzao rad na projektu jer se dependency-ji ne skidaju ponovo pri svakom buildu
- runtime ponašanje ostaje isto jer embedding i ranije radi na CPU-u
- manji build context ubrzava slanje fajlova Docker daemonu

**Negativne:**
- BuildKit mora biti aktivan da bi `--mount=type=cache` radio
- prvi build i dalje mora jednom popuniti cache i može potrajati duže
- cache je vezan za lokalno/CI okruženje i može se resetovati
- developeri moraju razumjeti zašto se Torch instalira odvojeno od ostatka dependency-ja

**Status odluke:**
Aktivna

---

## **ID:** DL-36

**Datum:** 25/05/2026

**Naziv:** Single-click deployment na Azure preko `azd up`

**Opis:**
Projekat je trebao stabilniji deployment tok od privremenih tunela i ručnog povezivanja backend/frontend URL-ova. Bilo je potrebno odlučiti kako omogućiti jednostavno podizanje kompletne aplikacije uz minimalan broj komandi, ali bez migracije postojećih managed servisa za bazu, vektorsku bazu i LLM.

**Razmatrane opcije:**
- Nastaviti koristiti cloudflared tunel i ručno prevezivanje URL-ova
- Deploy samo backend-a na postojeći Render tok
- Full Azure migracija svih servisa, uključujući bazu i vektorsku bazu
- Azure deployment preko `azd up`: Container Apps za backend i Static Web Apps za frontend
- AWS deployment kao alternativni single-click tok

**Odabrana opcija:**
Azure Developer CLI deployment preko `azd up`, s backendom na Azure Container Apps i frontendom na Azure Static Web Apps, dok Supabase, Qdrant Cloud i Groq ostaju postojeći managed servisi.

**Razlog izbora:**
`azd up` omogućava da se infrastruktura, build i deploy pokrenu jednim tokom. Backend i frontend dobijaju trajne HTTPS URL-ove koji preživljavaju redeploy, pa nema potrebe za ručnim prevezivanjem tunela. Zadržavanje Supabase, Qdrant i Groq servisa smanjuje scope promjene i rizik migracije podataka.

**Posljedice odluke:**

**Pozitivne:**
- kompletan deployment se može pokrenuti jednom komandom
- backend i frontend dobijaju stabilne HTTPS URL-ove
- manje ručnog rada nakon svakog redeploya
- tajne se ubrizgavaju kroz `azd env` i ne commitaju se u repozitorij
- postojeća baza, Qdrant i Groq integracije ostaju nepromijenjene

**Negativne:**
- Docker Desktop mora biti instaliran i pokrenut zbog lokalnog image builda na Free Trial pretplati
- pogrešno postavljen `VITE_API_URL` može dovesti do toga da frontend zove stari backend
- Azure resursi mogu trošiti credit ako se ne ugase nakon testiranja
- potrebno je pažljivo reuse-ati `TOKEN_MAP_KEY` da se ne izgubi mogućnost dekripcije ranije maskiranih podataka

**Status odluke:**
Aktivna

---

## **ID:** DL-37

**Datum:** 25/05/2026

**Naziv:** Admin pregled kompletne sesije kroz spajanje bot i agent izvora poruka

**Opis:**
Admin pregledi u Ratings i Chat Logs sekcijama nisu uvijek prikazivali cijeli tok razgovora, posebno dio nakon eskalacije na ljudskog agenta. Bot poruke su bile u standardnim chat tabelama, dok su agent poruke čuvane u `Eskalacija.razgovor` JSON koloni. Bilo je potrebno odlučiti kako prikazati jedinstvenu sesiju bez dupliranja poruka.

**Razmatrane opcije:**
- Prikazivati samo bot poruke iz `Poruka` tabele
- Migrirati sve stare agent poruke iz JSON kolone u `Poruka` tabelu
- Spajati `Poruka` redove i `Eskalacija.razgovor` poruke u admin endpointu
- Spajanje raditi samo na frontend strani
- Prikazivati samo pojedinačni exchange iz Chat Logs reda

**Odabrana opcija:**
Backend endpoint spaja poruke iz `Poruka` tabele i `Eskalacija.razgovor` JSON kolone, deduplicira ih i vraća admin prikazu kao punu sesiju.

**Razlog izbora:**
Backend je bolje mjesto za spajanje jer poznaje oba izvora podataka i može centralizovano deduplicirati poruke. Time Ratings modal i Chat Logs Details dobijaju konzistentan prikaz bez ručne frontend rekonstrukcije razgovora.

**Posljedice odluke:**

**Pozitivne:**
- admin vidi kompletan razgovor, uključujući ljudskog agenta
- Ratings → View Chat prikazuje tačnu sesiju povezanu s komentarom
- Chat Logs Details više ne prikazuje samo jedan exchange
- deduplikacija sprečava ponavljanje bot poruka
- role labela za `agent` jasnije prikazuje ko je poslao poruku

**Negativne:**
- endpoint mora održavati logiku spajanja dva različita izvora poruka
- deduplikacija po `(role, content)` može biti gruba ako se ista poruka legitimno ponovi
- različiti formati historije poruka mogu otežati buduće promjene modela
- potrebno je paziti da admin-only endpoint ne bude dostupan običnim korisnicima

**Status odluke:**
Aktivna

---

## **ID:** DL-38

**Datum:** 25/05/2026

**Naziv:** Session-level rating kao primarni prikaz ocjena u Chat Logs

**Opis:**
Korisničke ocjene ostavljene nakon završetka sesije nisu se pojavljivale u Chat Logs prikazu jer je endpoint ranije čitao samo feedback vezan za pojedinačni odgovor. Nakon prelaska na ocjenu cijele sesije bilo je potrebno uskladiti admin preglede i filtere s novim modelom feedback-a.

**Razmatrane opcije:**
- Nastaviti prikazivati samo response-level feedback
- Migrirati session-level feedback u response-level zapise
- U `/chat/logs` prikazu koristiti kombinovani prikaz: prosjek response feedback-a ili session rating
- Prikazati ocjene samo u Ratings sekciji, a ne u Chat Logs

**Odabrana opcija:**
`/chat/logs` koristi `COALESCE` logiku: ako postoji per-response prosjek koristi se on, a inače se prikazuje session-level rating. `min_rating` filter koristi istu kombinovanu vrijednost.

**Razlog izbora:**
Ovaj pristup podržava i stariji response-level feedback i novi session-level feedback bez migracije podataka. Admin dobija konzistentan prikaz ocjena u Chat Logs i Ratings sekcijama, a filter po minimalnoj ocjeni ostaje tačan.

**Posljedice odluke:**

**Pozitivne:**
- session rating se vidi u Chat Logs bez dodatne migracije
- postojeći response-level feedback ostaje podržan
- `min_rating` filter radi nad istom vrijednošću koja se prikazuje korisniku
- admin lakše povezuje ocjenu s cijelim razgovorom

**Negativne:**
- query postaje složeniji zbog dodatnog subquery-ja i `COALESCE` logike
- potrebno je jasno razlikovati ocjenu poruke i ocjenu sesije u budućoj analitici
- ako postoje oba tipa feedback-a, prioritet prikaza mora ostati dosljedan

**Status odluke:**
Aktivna

---

## **ID:** DL-39

**Datum:** 25/05/2026

**Naziv:** Dokumentovanje scheduled/S3 proširenja bez implementacije u ovom koraku

**Opis:**
Dodatni story zahtjevi spominjali su batch procesiranje sa web lokacija poput Google Drive-a i S3, on-demand i scheduled pokretanje, te kompletan pipeline run. Implementiran je Google Drive on-demand tok, dok bi scheduled izvršavanje i dodatni izvori zahtijevali dodatnu infrastrukturu i širi dizajn.

**Razmatrane opcije:**
- Implementirati Google Drive, S3 i scheduled import odjednom
- Implementirati samo Google Drive on-demand i dokumentovati scheduled/S3 kao proširenje
- Ne raditi remote import u ovom sprintu
- Uvesti generički RemoteSource interfejs i sve izvore odmah podržati

**Odabrana opcija:**
Isporučen je Google Drive on-demand import kroz postojeći pipeline, a scheduled runs i dodatni izvori poput S3 dokumentovani su kao buduće proširenje.

**Razlog izbora:**
Google Drive on-demand pokriva najkonkretniji dio potrebe i može se demonstrirati bez značajnog širenja infrastrukture. Scheduled import bi zahtijevao pouzdano periodično pokretanje, interne API rute i dodatno planiranje sigurnosti, dok bi S3 zahtijevao novi storage adapter. Dokumentovanje proširenja ostavlja jasan put naprijed bez predstavljanja neimplementiranog rada kao gotovog.

**Posljedice odluke:**

**Pozitivne:**
- tim može demonstrirati stvarni remote batch import
- scope ostaje kontrolisan i stabilan
- postojeći pipeline ostaje centralno mjesto obrade
- dokumentovan je realan put za scheduled import i S3 podršku
- izbjegava se rizik polovične implementacije više različitih izvora

**Negativne:**
- scheduled import nije automatski dostupan korisniku u ovoj verziji
- S3 nije stvarno implementiran, nego samo arhitekturno predviđen
- korisnik i dalje mora ručno pokrenuti Drive import iz admin panela
- buduća implementacija mora paziti na autentifikaciju internih scheduled poziva

**Status odluke:**
Aktivna

---
