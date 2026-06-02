# Sprint Backlog — Sprint 10

## Opis sprinta

Sprint 10 usmjeren je na automatizaciju, skalabilnost i produkcijsku infrastrukturu sistema. Nakon što je Sprint 9 isporučio stabilan, optimizovan i testiran sistem, ovaj sprint podiže operativnu zrelost na nivo koji omogućava trajno, autonomno i skalabilno funkcionisanje u produkcijskom okruženju.

Tokom ovog sprinta implementiraju se funkcionalnosti vezane za:

- batch procesiranje fajlova iz eksternih izvora — automatski import transkripata iz Google Drive-a
- scheduled pipeline obradu — autonomno pokretanje kompletnog toka obrade prema administratorski konfiguriranom rasporedu
- live prikaz napretka pipeline obrade u admin panelu — pregled statusa svih faza u realnom vremenu
- single-click cloud deployment — automatsko deployanje kompletnog sistema na Azure/AWS infrastrukturu jednim komandnim pozivom
- optimizaciju build procesa i CI/CD performansi — dramatično skraćivanje Docker rebuild vremena kroz cache mehanizme i CPU-only ML dependency layere
- prevenciju duplih unosa u bazu znanja — provjera duplikata na svim putanjama unosa s automatskim preskakanjem ili porukom administratoru
- bulk brisanje razgovora iz Chat Logs — checkbox selekcija i grupno brisanje s kaskadnim uklanjanjem svih pridruženih podataka
- razumljive i korisnički prilagođene poruke o greškama — eliminacija sirovih tehničkih poruka kroz cijelu aplikaciju

---

## Pregled stavki sprinta

| ID | Naziv stavke | Kratak opis | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-------------|-----|-----------|-----------------|--------|
| PB-66 | Batch procesiranje fajlova iz eksternih izvora | Automatski batch import transkripata iz Google Drive-a (US-66.1) | Feature | High | 13 | Završeno |
| PB-67 | Scheduled pipeline obrada i automatsko ažuriranje baze znanja | Autonomno pokretanje kompletnog pipeline-a prema konfiguriranom rasporedu uz live prikaz statusa (US-67.1, US-67.2) | Feature | High | 13 | Završeno |
| PB-68 | Single-click cloud deployment | Automatski deploy kompletnog sistema na cloud infrastrukturu jednim komandnim pozivom (US-68.1) | DevOps | High | 8 | Završeno |
| PB-69 | Optimizacija build procesa i CI/CD performansi | Optimizacija Docker build procesa kroz cache mehanizme i CPU-only ML dependency layer (US-69.1) | Technical Task | High | 8 | Završeno |
| PB-70 | Prevencija duplih unosa u bazu znanja | Provjera duplikata na svim mjestima unosa u bazu znanja — ručni unos, obrada transkripata, batch import i spašavanje Q&A pri eskalaciji (US-70.1) | Technical Task | High | 5 | Završeno |
| PB-71 | Bulk brisanje razgovora iz Chat Logs, Transcripts i Issues | Checkbox selekcija i dugme za grupno brisanje označenih razgovora u Chat Logs pregledu, dostupno samo adminu (US-71.1) | Feature | Medium | 5 | Završeno |
| PB-72 | Razumljive i korisnički prilagođene poruke o greškama | Nijedna poruka o grešci ne smije prikazivati sirove tehničke poruke; jasne korisnički razumljive poruke za sve akcije (US-72.1) | Feature | High | 5 | Završeno |

---

## Sprint Backlog stavke

---

### PB-66 — Batch procesiranje fajlova iz eksternih izvora

**Prioritet:** High

**Poslovna vrijednost:** Eliminiše ručni unos transkripata fajl po fajl — administrator može jednim korakom importovati cijeli folder iz eksternog izvora, čime se drastično smanjuje operativno opterećenje i ubrzava unos novih podataka u sistem.

**Pretpostavke:** Sistem ima konfiguriran pristup eksternim izvorima (Google Drive API credentials). Postojeći transcript pipeline ostaje nepromijenjen — batch import samo automatizuje korak preuzimanja fajlova.

**Veze i zavisnosti:** Nadograđuje PB-18 Upload i unos transkripata. Preduvjet za PB-67 Scheduled pipeline obradu.

---

#### US-66.1 — Batch import transkripata iz eksternih izvora

| Polje | Vrijednost |
|---|---|
| **ID** | 66.1 |
| **Naziv** | Batch import transkripata iz eksternih izvora |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Automatizuje unos transkripata u sistem iz eksternih storage servisa bez potrebe za ručnim preuzimanjem i uploadom svakog fajla posebno |

**Uloga:**
Kao administrator, želim importovati više fajlova iz Google Drive-a, S3 storage-a i sličnih eksternih izvora kako bih automatizovao unos transkripata u sistem.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su kredencijali za pristup eksternim izvorima konfigurirani u sistemskim postavkama. Otvoreno pitanje: Da li administrator treba moći selektovati pojedinačne fajlove unutar foldera ili se uvijek importuje cijeli folder?

**Veze sa drugim storyjima ili zavisnostima:**
Nadograđuje US-18.1 Upload transkripata putem fajla. Preduvjet za US-67.1 Scheduled pokretanje kompletnog pipeline-a.

**Acceptance Criteria:**
- Administrator mora moći pokrenuti batch import unosom folder URL-a ili ID-a eksternog izvora
- Sistem mora automatski preuzeti sve podržane fajlove iz navedenog foldera i provući ih kroz postojeći transcript pipeline
- Sistem mora preskočiti fajlove koji su već obrađeni (deduplikacija po imenu i checksumu fajla)
- Kada se fajl izmijeni na eksternom izvoru, sistem mora automatski re-importovati novu verziju pri sljedećem importu
- Greška pri obradi jednog fajla ne smije prekinuti obradu preostalih fajlova u batch skupu
- Administrator mora vidjeti sumarni izvještaj po završetku batch importa: broj uspješno obrađenih, preskočenih i neuspješnih fajlova
- Sistem mora logirati svaki batch import s identifikatorom izvora, vremenom pokretanja i rezultatom obrade

---

### PB-67 — Scheduled pipeline obrada i automatsko ažuriranje baze znanja

**Prioritet:** High

**Poslovna vrijednost:** Sistem postaje autonoman — nova znanja iz transkripata automatski dospijevaju u bazu znanja prema definiranom rasporedu bez ikakve administratorske intervencije, čime chatbot ostaje trajno ažuran s najnovijim informacijama.

**Pretpostavke:** Batch import iz eksternih izvora (PB-66) je implementiran i funkcionalan. CI/CD infrastruktura i serversko okruženje podržavaju scheduled task izvršavanje.

**Veze i zavisnosti:** Zavisi od PB-66 Batch procesiranje fajlova iz eksternih izvora. Nadograđuje PB-27 Izgradnja baze znanja i PB-52 RAG retrieval i LLM klasifikacija upita.

---

#### US-67.1 — Scheduled pokretanje kompletnog pipeline-a

| Polje | Vrijednost |
|---|---|
| **ID** | 67.1 |
| **Naziv** | Scheduled pokretanje kompletnog pipeline-a |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Oslobađa administratora od ručnog pokretanja obrade — sistem autonomno importuje, obrađuje i ažurira bazu znanja prema konfiguriranom rasporedu |

**Uloga:**
Kao administrator, želim definisati raspored automatskog pokretanja pipeline-a kako bi sistem samostalno obrađivao nove transkripte i ažurirao bazu znanja.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da je batch import konfiguriran i funkcionalan. Otvoreno pitanje: Da li administrator treba moći definisati različite rasporede za različite izvore podataka, ili postoji jedan globalni raspored za sve?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-66.1 Batch import transkripata iz eksternih izvora. Preduvjet za US-67.2 Live prikaz napretka pipeline obrade.

**Acceptance Criteria:**
- Administrator mora moći uključiti ili isključiti scheduled obradu iz admin panela
- Administrator mora moći definisati frekvenciju izvršavanja: hourly, daily ili weekly
- Kada scheduled obrada dostigne konfigurirano vrijeme, sistem mora automatski pokrenuti kompletan pipeline: import transkripata, transkripciju, ekstrakciju Q&A parova, generisanje embeddinga i ažuriranje baze znanja
- Status svakog izvršavanja (pokrenuto, u toku, završeno, neuspješno) mora biti vidljiv u admin panelu
- Sistem mora prikazati posljednje vrijeme izvršavanja i sažetak rezultata (broj obrađenih fajlova, novododanih Q&A parova)
- Scheduled obrada ne smije biti pokrenuta paralelno — ako je prethodni run još u toku, novi run se odgađa do završetka tekućeg
- Administrator mora moći ručno pokrenuti pipeline neovisno od konfiguriranog rasporeda

---

#### US-67.2 — Live prikaz napretka pipeline obrade

| Polje | Vrijednost |
|---|---|
| **ID** | 67.2 |
| **Naziv** | Live prikaz napretka pipeline obrade |
| **Sprint** | 10 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Administrator ima pun uvid u tok automatske obrade u realnom vremenu bez potrebe za ručnom provjerom logova, što ubrzava identifikaciju problema i povećava povjerenje u sistem |

**Uloga:**
Kao administrator, želim pratiti napredak pipeline obrade u realnom vremenu kako bih imao pregled trenutnog statusa sistema i mogao brzo reagovati na eventualne greške.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da backend šalje status updates putem WebSocket veze ili polling mehanizma. Otvoreno pitanje: Koliko dugo se čuvaju historijski logovi prethodnih pipeline run-ova u UI-u?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-67.1 Scheduled pokretanje kompletnog pipeline-a.

**Acceptance Criteria:**
- Sistem mora prikazivati naziv i status trenutno obrađivanog fajla za vrijeme trajanja pipeline obrade
- Sistem mora prikazivati status svake faze pipeline-a u realnom vremenu (Import → Transkripcija → Ekstrakcija Q&A → Generisanje embeddinga → Ažuriranje baze znanja)
- UI mora automatski osvježavati status bez potrebe za ručnim reload-om stranice
- Administrator mora vidjeti datum i vrijeme posljednjeg uspješnog scheduled runa
- Kada pipeline naiđe na grešku, sistem mora istaknuti fazu u kojoj je greška nastala s kratkim opisom problema
- Prikaz napretka mora biti dostupan i za ručno pokrenute pipeline run-ove, ne samo scheduled

---

### PB-68 — Single-click cloud deployment

**Prioritet:** High

**Poslovna vrijednost:** Eliminiše ručne korake i mogućnosti greške pri postavljanju produkcijskog okruženja — razvojni tim može isporučiti kompletan sistem brzo, konzistentno i ponovljivo na cloud infrastrukturu bez specifičnog DevOps znanja za svaki korak.

**Pretpostavke:** Azure/AWS account je konfiguriran s potrebnim dozvolama. Svi servisi sistema (backend, frontend, vektorska baza) su kontejnerizovani i spremni za cloud deployment.

**Veze i zavisnosti:** Zavisi od PB-69 Optimizacija build procesa i CI/CD performansi. Nadograđuje PB-63 End-to-end i regresijsko testiranje sistema — testovi se izvršavaju kao dio deployment procesa.

---

#### US-68.1 — Single-click deploy sistema

| Polje | Vrijednost |
|---|---|
| **ID** | 68.1 |
| **Naziv** | Single-click deploy sistema |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Razvojni tim može deployati kompletan sistem u produkciju jednim komandnim pozivom, bez ručnog konfiguriranja infrastrukture i bez rizika od greške u procesu postavljanja |

**Uloga:**
Kao razvojni tim, želimo deployati kompletan sistem jednim komandnim pozivom kako bismo pojednostavili postavljanje produkcijskog okruženja i osigurali ponovljiv, konzistentan deployment proces.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da su cloud provider credentials konfigurirani lokalno ili u CI/CD okruženju. Otvoreno pitanje: Da li deployment skripta treba podržavati i rollback na prethodnu verziju u slučaju neuspješnog deploya?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od US-69.1 Optimizacija build vremena backend sistema. Preduvjet za produkcijsku isporuku sistema.

**Acceptance Criteria:**
- Sistem mora podržavati deploy kompletne aplikacije jednim komandnim pozivom (npr. jedan shell skript ili CLI komanda)
- Backend i frontend moraju biti automatski deployani kao dio istog deployment procesa
- Cloud infrastruktura (compute, networking, storage) mora biti automatski provisionirana bez ručnih koraka
- Deploy mora generisati trajne HTTPS endpointe koji su odmah dostupni po završetku procesa
- Deployment skripta mora prikazivati status napretka deployanja u terminalu
- Neuspješan deployment mora prikazati jasnu poruku greške s naznačenim korakom koji je zakazao
- Ponovljeno pokretanje deployment skripte na već deployaniom sistemu ne smije narušiti postojeće podatke ni konfiguraciju

---

### PB-69 — Optimizacija build procesa i CI/CD performansi

**Prioritet:** High

**Poslovna vrijednost:** Ubrzava razvojni ciklus i smanjuje troškove CI/CD izvršavanja — rebuild koji je trajao više od 25 minuta sada se izvršava za 10–15 sekundi, što direktno povećava produktivnost tima i skraćuje feedback loop pri razvoju i testiranju.

**Pretpostavke:** Projekt koristi Docker za kontejnerizaciju. CI/CD pipeline je postavljen na GitHub Actions ili sličnom servisu. ML zavisnosti (PyTorch i slično) su najveći doprinos sporom build vremenu.

**Veze i zavisnosti:** Preduvjet za PB-68 Single-click cloud deployment. Nadograđuje PB-63 End-to-end i regresijsko testiranje sistema kroz ubrzanje CI pipeline-a.

---

#### US-69.1 — Optimizacija build vremena backend sistema

| Polje | Vrijednost |
|---|---|
| **ID** | 69.1 |
| **Naziv** | Optimizacija build vremena backend sistema |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Dramatično skraćuje trajanje Docker rebuildova kroz cache mehanizme i razdvajanje ML dependency layera, čime se ubrzava razvojni ciklus i CI/CD pipeline bez promjena u funkcionalnosti aplikacije |

**Uloga:**
Kao razvojni tim, želimo optimizovati Docker build proces kako bi rebuild sistema trajao značajno kraće i kako bismo ubrzali iteracije razvoja i CI/CD pipeline izvršavanja.

**Pretpostavke i otvorena pitanja:**
ML dependency paketi (npr. PyTorch, transformers) su primarni uzrok dugog build vremena. Pretpostavlja se da produkcijsko okruženje koristi CPU inference bez GPU zahtjeva. Otvoreno pitanje: Da li cache slojevi trebaju biti pohranjeni u GitHub Actions cache-u ili u container registry-ju?

**Veze sa drugim storyjima ili zavisnostima:**
Preduvjet za US-68.1 Single-click deploy sistema. Utiče na sve CI/CD workflowe definisane u US-63.1 i US-63.2.

**Acceptance Criteria:**
- Build proces mora koristiti Docker layer cache mehanizme — dependency slojevi ne smiju biti rebuild-ovani ako se zavisnosti nisu promijenile
- Sistem mora koristiti CPU-only varijantu ML dependency paketa umjesto GPU varijante kako bi se smanjila veličina i trajanje build-a
- Vrijeme cached rebuildova (bez promjena u zavisnostima) mora biti značajno smanjeno u odnosu na prethodnu implementaciju
- Optimizacija ne smije promijeniti runtime ponašanje aplikacije niti uticati na produkcijsku funkcionalnost
- CI/CD pipeline mora koristiti optimizovanu build konfiguraciju i time smanjiti ukupno trajanje pipeline izvršavanja
- Dockerfile mora biti organizovan tako da se slojevi koji se rijetko mijenjaju (zavisnosti) nalaze ispred slojeva koji se često mijenjaju (aplikacijski kod)

---

### PB-70 — Prevencija duplih unosa u bazu znanja

**Prioritet:** High

**Poslovna vrijednost:** Osigurava konzistentnost baze znanja eliminacijom dupliranih unosa koji bi degradirali kvalitet retrieval-a i zbunjivali chatbot pri odgovaranju — provjera se primjenjuje na svim putanjama unosa bez izuzetka.

**Pretpostavke:** Provjera duplikata primjenjuje se na sve putanje unosa u KB. Poređenje se vrši na nivou teksta pitanja.

**Veze i zavisnosti:** Zavisi od PB-59 Ručni unos Q&A parova, PB-60 Kuriranje KB, PB-66 Batch import. Vezano za PB-48 Escalation queue i PB-56 Ekstrakcija Q&A parova.

---

#### US-70.1 — Sprječavanje duplikata pitanja u bazi znanja

| Polje | Vrijednost |
|---|---|
| **ID** | 70.1 |
| **Naziv** | Sprječavanje duplikata pitanja u bazi znanja |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Osigurava konzistentnost baze znanja eliminacijom dupliranih unosa koji bi degradirali kvalitet retrieval-a i zbunjivali chatbot pri odgovaranju |

**Uloga:**
Kao administrator, želim spriječiti dodavanje identičnih pitanja u bazu znanja kako bi podaci ostali konzistentni i bez dupliranih unosa.

**Pretpostavke i otvorena pitanja:**
Provjera duplikata primjenjuje se na sve putanje unosa u KB. Otvoreno pitanje: Da li se duplikat detektuje egzaktnim podudaranjem teksta ili semantičkom sličnošću?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od PB-59 Ručni unos Q&A parova. Zavisi od PB-60 Kuriranje KB. Zavisi od PB-66 Batch import.

**Acceptance Criteria:**
- Sistem ne smije dozvoliti dodavanje identičnog pitanja više puta u bazu znanja
- Provjera duplikata mora raditi kod ručnog unosa Q&A parova
- Provjera duplikata mora raditi tokom obrade transkripata
- Provjera duplikata mora raditi tokom batch importa fajlova
- Provjera duplikata mora raditi prilikom spašavanja Q&A parova iz eskalacija
- Kod batch importa duplikati se moraju automatski preskočiti bez prekida obrade ostalih fajlova
- Administrator mora dobiti poruku da pitanje već postoji prilikom ručnog unosa duplikata

---

### PB-71 — Bulk brisanje razgovora iz Chat Logs, Transcripts i Issues

**Prioritet:** Medium

**Poslovna vrijednost:** Administratoru omogućava efikasno čišćenje historije razgovora bez potrebe za pojedinačnim brisanjem, što štedi vrijeme pri upravljanju velikim brojem zapisa.

**Pretpostavke:** Brisanje je trajno i kaskadira na sve povezane podatke. Funkcionalnost dostupna isključivo administratoru.

**Veze i zavisnosti:** Nadograđuje PB-49 Historija razgovora korisnika i PB-55 Resolving chatova. Zavisi od PB-36 Sign In (provjera admin uloge).

---

#### US-71.1 — Brisanje više razgovora odjednom

| Polje | Vrijednost |
|---|---|
| **ID** | 71.1 |
| **Naziv** | Brisanje više razgovora odjednom |
| **Sprint** | 10 |
| **Prioritet** | Medium |
| **Poslovna vrijednost** | Administratoru omogućava efikasno čišćenje historije razgovora bez potrebe za pojedinačnim brisanjem, što štedi vrijeme pri upravljanju velikim brojem zapisa |

**Uloga:**
Kao administrator, želim označiti i obrisati više razgovora odjednom kako bih efikasnije upravljao historijom razgovora.

**Pretpostavke i otvorena pitanja:**
Brisanje je trajno i kaskadira na sve povezane podatke. Otvoreno pitanje: Da li dodati soft delete s mogućnošću oporavka ili isključivo trajno brisanje?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od Sign In (PB-36). Zavisi od PB-34 Pregled postavljenih pitanja i odgovora.

**Acceptance Criteria:**
- Sistem mora prikazivati checkbox za svaki razgovor u Chat Logs, Transcripts i Issues tabelama
- Sistem mora podržavati "Select All" opciju koja označava sve vidljive zapise
- Dugme "Delete selected (N)" mora prikazivati trenutni broj označenih razgovora
- Kada administrator potvrdi brisanje, sistem mora obrisati razgovore, transkripte ili prijave zajedno sa svim povezanim podacima
- Samo administrator mora imati mogućnost bulk brisanja razgovora
- Sistem ne smije obrisati razgovore bez eksplicitne potvrde administratora

---

### PB-72 — Razumljive i korisnički prilagođene poruke o greškama

**Prioritet:** High

**Poslovna vrijednost:** Poboljšava korisničko iskustvo i smanjuje konfuziju prikazivanjem jasnih, kontekstualnih poruka umjesto tehničkih grešaka sistema — korisnik uvijek zna šta je pošlo po zlu i kako može nastaviti rad.

**Pretpostavke:** Backend vraća standardizovan format grešaka. Primjenjuje se na sve korisničke uloge — administrator, agent i krajnji korisnik.

**Veze i zavisnosti:** Zavisi od svih funkcionalnosti koje uključuju API pozive i obradu podataka — posebno PB-18 Upload transkripata, PB-27 Izgradnja baze znanja, PB-46 Status pipeline obrade i PB-59 Ručni unos Q&A parova.

---

#### US-72.1 — Prikaz razumljivih poruka o greškama

| Polje | Vrijednost |
|---|---|
| **ID** | 72.1 |
| **Naziv** | Prikaz razumljivih poruka o greškama |
| **Sprint** | 10 |
| **Prioritet** | High |
| **Poslovna vrijednost** | Poboljšava korisničko iskustvo i smanjuje konfuziju prikazivanjem jasnih poruka umjesto tehničkih grešaka sistema |

**Uloga:**
Kao korisnik sistema (administrator, agent ili krajnji korisnik), želim vidjeti jasne i razumljive poruke o greškama kako bih znao šta je pošlo po zlu i kako mogu nastaviti korištenje sistema.

**Pretpostavke i otvorena pitanja:**
Pretpostavlja se da backend vraća standardizovan format grešaka. Otvoreno pitanje: Da li sistem treba podržati internacionalizaciju poruka o greškama u budućnosti?

**Veze sa drugim storyjima ili zavisnostima:**
Zavisi od svih funkcionalnosti koje uključuju API pozive i obradu podataka. Posebno vezano za PB-18 Upload transkripata, PB-27 Izgradnja baze znanja, PB-46 Status pipeline obrade i PB-59 Ručni unos Q&A parova.

**Acceptance Criteria:**
- Nijedna poruka o grešci ne smije prikazivati sirove tehničke poruke poput "Request failed with status code 500" ili HTTP status kodove
- Kada backend vrati korisnički razumljivo objašnjenje greške, tada sistem mora prikazati upravo tu poruku
- Kada backend ne vrati objašnjenje greške, tada sistem mora prikazati fallback poruku prilagođenu konkretnoj akciji
- Upload transkripata mora prikazati jasnu poruku kada upload ne uspije
- Pipeline obrada mora prikazati razumljive greške umjesto stack trace informacija
- Ručni unos i uređivanje baze znanja moraju prikazivati validacione poruke za neispravne podatke
- Brisanje i izmjena unosa moraju prikazati poruku kada akcija nije uspješna
- Sistem ne smije prikazati stack trace, SQL greške niti interne detalje servera krajnjem korisniku
- Sve poruke o greškama moraju biti konzistentnog vizualnog prikaza kroz cijelu aplikaciju
