# Test Strategy

## Cilj testiranja

Cilj testiranja sistema za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra je osigurati da sve funkcionalnosti sistema rade ispravno, pouzdano i sigurno u skladu sa definisanim zahtjevima i acceptance kriterijima.

**Ciljevi su:**

- Verificirati da funkcionalnosti unosa i uploada transkripata (fajl i ručni unos) rade ispravno, uključujući validaciju formata i pravilnu pohranu podataka u sistem.

- Potvrditi da obrada transkripata (parsiranje, normalizacija i razdvajanje po ulogama) funkcioniše ispravno i da su podaci pripremljeni za dalju upotrebu.

- Provjeriti da sistem adekvatno maskira osjetljive i lične podatke prije njihove obrade i pohrane, u skladu sa sigurnosnim i privatnosnim zahtjevima.

- Verificirati da chatbot generiše relevantne i tačne odgovore na osnovu baze znanja, u skladu sa definisanim kriterijima tačnosti.

- Osigurati da sistem pravilno prepoznaje situacije u kojima chatbot nije siguran u odgovor i da u tim slučajevima vrši preusmjeravanje komunikacije na ljudskog agenta bez gubitka konteksta.

- Validirati funkcionalnosti za prijavu netačnih odgovora i obradu korisničkog feedback-a, uključujući evidentiranje i kasniju obradu od strane administratora.

- Provjeriti da administratorski dio sistema omogućava pregled, validaciju i upravljanje transkriptima, pitanjima i prijavljenim problemima bez grešaka.

- Potvrditi da su implementirani sigurnosni mehanizmi (HTTPS, autentifikacija i kontrola pristupa) ispravni i da neovlašteni korisnici ne mogu pristupiti zaštićenim dijelovima sistema.

- Provjeriti performanse sistema, uključujući vrijeme odziva (manje od 3 sekunde u većini slučajeva) i stabilan rad pri većem broju istovremenih korisnika.

- Osigurati da sistem radi stabilno i pouzdano, bez generisanja netačnih ili neprovjerenih odgovora, te da se pravilno ponaša u slučaju grešaka.

- Provjeriti da korisnički interfejs omogućava jednostavno, intuitivno i jasno korištenje sistema za sve tipove korisnika (krajnji korisnici, agenti i administratori).

## Nivoi testiranja 
### Unit testiranje

Unit testiranje provjerava ispravnost individualnih komponenti sistema izolovano od ostatka aplikacije. Fokus je na poslovnoj logici unutar pojedinih modula.

| Atribut | Opis |
|--------|------|
| Cilj | Verificirati ispravnost pojedinačnih funkcija i klasa unutar modula |
| Ko testira | Developeri (tokom razvoja) |
| Kada | Kontinuirano tokom svakog sprinta, prije commita koda |
| Alati | Jest (JavaScript/TypeScript), PyTest (Python backend) |
| Pokrivenost | Cilj: minimalno 80% code coverage za poslovnu logiku |

---

### Integraciono testiranje

Integraciono testiranje verificira ispravnost komunikacije i razmjene podataka između više modula sistema koji zajedno ostvaruju određenu funkcionalnost.

| Atribut | Opis |
|--------|------|
| Cilj | Verificirati da moduli ispravno komuniciraju i razmjenjuju podatke |
| Ko testira | Developeri / QA tim |
| Kada | Nakon završetka razvoja modula, na kraju svakog sprinta |
| Alati | Supertest (API testiranje), Postman / Newman (automatizacija API testova) |

---

### Sistemsko testiranje

Sistemsko testiranje verificira kompletan sistem kao cjelinu u okruženju što bližem produkcijskom. Pokriva end-to-end tokove i nefunkcionalne zahtjeve.

| Atribut | Opis |
|--------|------|
| Cilj | Verificirati cjelokupni sistem u realističnom okruženju – funkcionalni i nefunkcionalni zahtjevi |
| Ko testira | QA tim / tester |
| Kada | U fazi stabilizacije sistema (Sprint 11) |
| Alati | Playwright / Cypress (E2E), k6 / JMeter (load testing) |

---

### Prihvatno testiranje (UAT)

Prihvatno testiranje provode krajnji korisnici ili njihovi predstavnici kako bi potvrdili da sistem zadovoljava njihove potrebe i poslovne zahtjeve prije puštanja u produkciju.

| Atribut | Opis |
|--------|------|
| Cilj | Potvrditi da sistem ispunjava poslovne zahtjeve i da je spreman za produkciju |
| Ko testira | Predstavnici krajnjih korisnika (korisnik call centra, agent, administrator) |
| Kada | Na kraju razvojnog ciklusa, neposredno prije završne demonstracije (Sprint 12-13) |
| Alati | Ručno testiranje uz predefinisane test scenarije zasnovane na user stories |

---

## Šta se testira i na kojem nivou

Tabela prikazuje pokrivenost testiranjem po funkcionalnim oblastima sistema. Za svaki nivo testiranja navedeno je šta se konkretno provjerava u okviru te funkcionalne oblasti, ili je naznačeno da taj nivo nije primjenjiv.  
 

| Funkcionalna oblast / User Story | Unit | Integraciono | Sistemsko | Prihvatno |
|--------------------------------|------|-------------|-----------|-----------|
| US-25/26: Prijava i odjava iz sistema | Logika provjere kredencijala, hashiranje lozinke, generisanje tokena, logika blokiranja naloga nakon 5 neuspjelih pokušaja | Provjera RBAC-a - svaka uloga dobija ispravan dashboard; provjera da sesija ističe nakon 30 min neaktivnosti (NFR-2) | E2E: prijava, zaštićene rute, automatska odjava po isteku sesije, blokada naloga nakon 5 pokušaja (NFR-2) | Korisnik se prijavljuje i pristupa funkcijama svoje uloge; provjera odjave i blokade |
| US-1: Upload transkripata (fajl) | Validacija formata (TXT, PDF prihvata; ostalo se odbija), provjera veličine | Fajl prolazi od upload modula do pohrane i processing pipeline-a | E2E: upload-> pohrana -> prikaz u listi transkripata | Administrator uploaduje realni transkript i provjerava rezultat |
| US-2: Ručni unos transkripata | Validacija obaveznih polja, provjera minimalnih dužina i formata datuma | Djelimično - provjerava da se uneseni podaci ispravno pohranjuju u bazu | E2E: unos forme -> pohrana -> prikaz u listi | Administrator ručno unosi transkript i potvrđuje prikaz |
| US-3: Validacija transkripata | Svako validaciono pravilo izolovano (prazna polja, format, minimalna dužina | Provjera da validacijske greške blokuju pohranu i vraćaju ispravan odgovor | Djelimično - provjera u okviru upload i unos scenarija | N/A - tehnička funkcionalnost, ne testira se direktno u UAT-u |
| US-4 (ID27): Konverzija audio u transkript | Djelimično - provjera da sistem prepoznaje format i pokreće konverziju | Audio API -> transkripcija -> pohrana generisanog teksta u sistem | E2E: upload audio -> prikaz transkripata -> administrator potvrđuje sadržaj | Administrator uploaduje audio poziv i pregledava generisani transkript |
| US-4/5: Pregled i detalji transkripta | N/A - pretežno UI prikaz bez poslovne logike | Djelimično - provjera da se ispravni podaci učitavaju iz baze za prikaz | Prikaz liste, otvaranje detalja, provjera svih prikazanih polja | Administrator pregledava listu i otvara pojedinačni transkript |
| US-6: Pretraga i filtriranje transkripta | Logika filtriranja i pretrage - ispravnost upita prema bazi | Djelimično - provjera da filteri vraćaju ispravne rezultate iz baze | E2E: primjena filtera, resret filtera, provjera praznih rezultata | Djelimično - administrator provjerava pretragu po ključnoj riječi |
| US-27: Normalizacija teksta | Svaka normalizacijska operacija izolovano (razmaci, interpunkcija, znakovi) | Provjera da normalizovani tekst ispravno ulazi u naredne faze pipline-a | Djelimično - provjera u sklopu end-to-end toka obrade transkripata | N/A - interna tehnička obrada, nije vidljiva krajnjim korisnicima |
| US-28: Razdvajanje po ulogama | Parser logika - ispravno razdvajanje redova s oznakama Agent/Korisnik | Provjera da razdvojeni segmenti ispravno ulaze u embedding pipeline | Djelimično - provjera u sklopu end-to-end toka obrade transkripata | N/A - interna tehnička obrada, nije vidljiva krajnjim korisnicima |
| US-8: Maskiranje osjetljivih podataka | Regex/NLP detekcija JMBG, telefona i imena - sve varijante formata | Provjera da maskirani tekst ulazi u chatbot i da se original ne pohranjuje u log; provjera da originalni transkripti nisu prisutni u bazi nakon 24h (NFR-3) | Sigurnosni test: originalni podaci ne smiju se naći ni ulogovima ni u bazi; automatska provjera brisanja nakon 24h (NFR-3) | Djelimično - korisnik unosi poruku s osobnim podacima i potvrđuje obavijest o zamjeni |
| US-7: Postavljanje pitanja chatbotu (tekst) | Logika slanja upita, provjera praznog polja, validacija inputa | Pitanja korisnika -> RAG pretraga -> LLM API -> prikaz odgovora; provjera da sistem signalizira nesigurnost kada je pouzdanost ispod 70% (NFR-6) | E2E: korisnik postavlja pitanje, sistem vraća odgovor u roku od 3 sekunde (NFR-7); provjera eskalacije pri pouzdanosti ispod 70% (NFR-6) | Korisnik postavlja stvarna pitanja i ocjenjuje relevantnost odgovora; provjera poruke o nesigurnom odgovoru |
| US-9: Glasovni unos (Dictate) | Djelimično - provjera da sistem ispravno šalje audio Speech-to-Text API-ju| Speech-to-Text API -> pretvorba u tekst -> prikaz u input polju | E2E: korisnik govori pitanje, tekst se prikazuje i šalje chatbotu | Korisnik koristi glasovni unos i potvrđuje tačnost pretvorbe |
| US-10: Pregled historije razgovora | N/A - pretežno UI prikaz | Djelimično - provjera da se historija ispravno učitava iz baze za prijavljenog korisnika | E2E: prikaz historije hronološkim redom, poruka kad nema historije | Korisnik otvara historiju i vidi prethodne razgovore |
| US-11: Brisanje historije razgovora | Logika brisanja jednog i više zapisa, provjera potvrde brisanja | Djelimično - provjera da se zapis trajno uklanja iz baze | E2E: brisanje jednog i bulk delete, ažuriranje prikaza, provjera da zapis nije dostupan | Korisnik briše razgovore i potvrđuje da nisu vidljivi u historiji |
| US-12: Admin pregled svih pitanja i odgovora | N/A - pretežno UI prikaz | Djelimično - provjera da administrator vidi interakcije svih korisnika uz ispravno filtriranje | E2E: prikaz interakcija, filtriranje po datumu i ocjeni, prazna lista | Administrator pregledava interakcije i filtrira po kriterijima |
| US-13: Ocjena odgovora chatbota | Logika prihvatanja ocjene, validacija opsega, vezivanje za odgovor | Ocjena se pohranjuje u bazu i ispravno veže za konkretan chatbot odgovor | E2E: korisnik ocjenjuje odgovor, porvrda se prikazuje, ocjena vidljiva u admin panelu | Korisnik ocjenjuje odgovor i potvrđuje da je ocjena prihvaćena |
| US-14: Komentar uz ocjenu | Validacija komentara - prazno polje odbija, ispravno vezivanje uz ocjenu | Djelimično - provjera da se komentar pohranjuje uz ocjenu u bazi | E2E: korisnik daje negativnu ocjenu, otvara se polje za komentar, komentar se šalje | Korisnik ostavlja komentar uz negativnu ocjenu i dobija potvrdu |
| US-15: Pregled prosječne ocjene (admin) | Logika agregacije ocjena, filtriranje po vremenskom periodu | Djelimično - provjera da upit prema bazi vraća ispravne agregirane podatke | E2E: adminitrator mijenja vremenski period i vidi ažuriranu statistiku | Djelimično - administrator pregledava ocjene i provjerava trendove |
| US-16: Prijava netačnog odgovora | Validacija forme - prazna prijava se odbija, obavezna polja se provjeravaju | Prijava se pohranjuje u bazu i ispravno veže za konkretan chatbot odgovor | E2E: korisnik prijavljuje problem, dobija potvrdu, prijava vidljiva u admin modulu | Korisnik prijavljuje netačan odgovor i potvrđuje prijem obavijesti |
| US-17: Kategorizacija prijavljenog problema | Validacija da kategorija mora biti odabrana, provjera dostupnih kategorija | Djelimično - provjera da se odabrana kateogorija ispravno veže uz prijavu u bazi | E2E: forma za prijavu prikazuje kategorije, odabrana kategorija se pohranjuje | Korisnik odabire kategoriju greške i potvrđuje slanje prijave |
| US-18/19: Lista i detalji prijavljenih problema | N/A - pretežno UI prikaz | Djelimično - provjera da administrator vidi sve prijave s ispravnim podacima | E2E: prikaz liste, otvaranje detalja, provjera svih polja (pitanje, odgovor, kategorija, datum) | Administrator otvara prijavu i provjerava sve prikazane informacije |
| US-20: Promjena statusa prijave | Logika provjere validnih statusa, odbijanje nevalidnih vrijednosti | Djelimično - provjera da se promjena statusa reflektuje u bazi i u prikazu | E2E: administrator mijenja status, promjena je odmah vidljiva u listi prijava | Administrator mijenja status prijave i potvrđuje ažuriranje |
| US-21: Filtriranje prijavljenih problema | Logika filtriranja po statusu, kategoriji i datumu | Djelimično - provjera da filtrirani upit vraća ispravne rezultate iz baze | E2E: primjena filtera, reset filtera, provjera praznih rezultata | Djelimično - administrator filtrira prijave i provjerava relevantnost rezultata |
| US-22: Pregled neodgovorenih pitanja (agent) | N/A - pretežno UI prikaz | Djelimično - provjera da agent vidi samo pitanja sa statusom 'Čeka odgovor' | E2E: prikaz liste, sadržaj svakog zapisa (pitanje, datum, status), prazna lista | Agent otvara modul i vidi pitanja koja čekaju njegovu intervenciju |
| US-23: Unos agentovog odgovora | Validacija praznog odgovora, provjera promjene statusa | Agentov odgovor se pohranjuje, status se mijenja u 'Odgovoreno', korisnik dobija obavijest | E2E: agent odgovara, korisnik dobija obavijest, status pitanja se ažurira | Agent unosi odgovor i korisnik potvrđuje prijem odgovora |
| US-24: Upotreba agentovog odgovora za bazu znanja | Logika označavanja odgovora kao validnog, provjera odobravanja/odbijanja | Odobreni par pitanje/odgovor se ispravno dodaje u trening dataset u bazi | E2E: administrator odobrava odgovor, par se pojavljuje u bazi znanja | Administrator odobrava agentov odgovor i potvrđuje dodavanje u bazu znanja |
| Izgradnja baze znanja (embedding, RAG) | Generisanje embeddinga za ulazni tekst, provjera dimenzija i formata vektora | Pipeline: tekst -> embedding -> pohrana u vektorsku bazu -> uspješan retrieval | E2E: upit chatbota pokreće pretragu, relevantni kontekst se šalje u LLM-u | N/A - interna tehnička komponenta, testira se indirektno kroz chatbot odgovore |
| Preusmjeravanje na ljudskog agenta | Logika detekcije kada chatbot nema pouzdan odgovor (prag pouzdanosti 70% - NFR-6) | Chatbot eskalira pitanje u roku od 10 sekundi (NFR-5), ono se pojavljuje u agentovom modulu s punim kontekstom razgovora| E2E: korisnik postavlja pitanje van baze znanja, razgovor se eskalira agentu unutar 10s; mjerenje vremena preusmjeravanja (NFR-5) | Korisnik dobija obavijest o eskalaciji, agent vidi pitanje s kontekstom razgovora |
| NFR: Sigurnost i HTTPS/TLS | N/A - ne testira se na unit nivou  | Provjera da svi endpointi rade isključivo putem HTTPS-a s TLS verzijom minimalno 1.2 (NFR-1); SSL Labs skeniranje | Penetracijsko: odbijanje HTTP zahtjeva, provjera TLS verzije na svim endpointima, security headeri (NFR-1); blokada naloga nakon 5 pokušaja, istek sesije nakon 30 min (NFR-2) | N/A - infrastrukturni zahtjev, ne testira se u UAT-u |
| NFR: Performanse (odziv <3s, 100 korisnika) | N/A - ne testira se na unit nivou | N/A - zahtijeva realno opterećenje, ne može se testirati na unit/integ nivou | Load test s k6/JMeter: 100 simultanih korisnika, mjerenje p95 vremena odziva (<3s u 95% slučajeva na uzorku od 1000 zahtjeva - NFR-7); odziv ne smije prelaziti 5s ni pri punom opterećenju (NFR-8) | N/A - automatizovani load test, ne provodi se ručno u UAT-u |
| NFR: Dostupnost 99%, rad 24/7 | N/A - ne testira se na unit nivou | N/A - zahtijeva dugotrajna mjerenja u produkcijskom okruženju | Monitoring uptime-a (max ~87% nedostupnosti godišnje - NFR-9); provjera oporavka nakon pada; verifikacija da se logovi čuvaju minimalno 12 mjeseci (NFR-9, NFR-11) | N/A - mjeri se kontinuiranim monitoringom, nije dio ručnog UAT-a |
| NFR: Tačnost chatbota (>= 85%) | N/A - ne može se mjeriti na nivou pojedinačn funkcije | N/A - zahtijeva kompletan sistem s popunjenom bazom znanja | Evaluacija na referentnom setu od minimalno 100 testnih pitanja s očekivanim odgovorima; izračun stope tačnosti (NFR-13); provjera eskalacije pri pouzdanosti ispod 70% (NFR-6) | Korisnici procjenjuju relevantnost odgovora tokom UAT sesija; provjera da chatbot jasno naznačuje nesiguran odgovor |

## Veza sa acceptance kriterijima

Svaki test slučaj direktno je vezan za jedan ili više acceptance kriterija definisanih u dokumentu User Stories. Ovaj pristup osigurava da se nijedan acceptance kriterij ne preskoči i da postoji potpuna sljedivost od zahtjeva do testa.

| TC ID | Acceptance Kriterij | User Story | Nivo testiranja |
|------|--------------------|-----------|----------------|
| TC-1-01 | Sistem prikazuje opciju za odabir fajla kada administrator pristupi modulu za upload | US-1: Upload transkripata | Sistemsko, Prihvatno |
| TC-1-02 | Sistem pohranjuje transkript i prikazuje poruku o uspješnom uploadu pri učitavanju validnog fajla | US-1: Upload transkripata | Integraciono, Sistemsko |
| TC-1-03 | Sistem prikazuje odgovarajuću poruku greške kada fajl nije validnog formata | US-1: Upload transkripata | Unit, Sistemsko |
| TC-8-01 | Sistem detektuje i maskira ime, telefon i JMBG u poruci korisnika prije slanja chatbotu | US-8: Maskiranje podataka | Unit, Integraciono |
| TC-8-02 | Sistem ne smije slati originalne nemaskirane podatke chatbotu niti ih pohranjivati u logovima | US-8: Maskiranje podataka | Unit, Sistemsko |
| TC-7-01 | Sistem prikazuje polje za unos pitanja kada korisnik otvori chatbot sučelje | US-7: Postavljanje pitanja | Sistemsko, Prihvatno |
| TC-7-02 | Sistem prikazuje odgovor chatbota kada korisnik unese pitanje i potvrdi slanje | US-7: Postavljanje pitanja | Integraciono, Sistemsko, Prihvatno |
| TC-25-01 | Sistem preusmjerava korisnika na odgovarajući dashboard prema ulozi pri ispravnoj prijavi | US-25: Sign In | Unit, Integraciono, Prihvatno |
| TC-25-02 | Sistem ne dozvoljava direktan pristup zaštićenim stranicama bez prijave | US-25: Sign In | Integraciono, Sistemsko |
| TC-16-01 | Sistem prikazuje formu za prijavu kada korisnik odabere opciju “Prijavi problem” | US-16: Prijava netačnog odgovora | Sistemsko, Prihvatno |
| TC-23-01 | Status pitanja mijenja se u “Odgovoreno” i korisnik biva obaviješten kada agent pošalje odgovor | US-23: Agentov odgovor | Integraciono, Sistemsko, Prihvatno |
| TC-NFR-07 | Sistem odgovara u roku od 3 sekunde u 95% slučajeva pod opterećenjem | NFR-7: Performanse | Sistemsko |
| TC-NFR-13 | Chatbot daje relevantne odgovore u najmanje 85% testiranih pitanja iz referentnog seta | NFR-13: Tačnost | Sistemsko, Prihvatno |

## Način evidentiranja rezultata testiranja

Rezultati testiranja evidentiraju se kroz strukturirane test case-ove koji su direktno povezani sa user story-ima i njihovim acceptance kriterijima.

Za svaki test case bilježe se sljedeće informacije:
| ID testa | Opis testa | Ulazni podaci | Očekivani rezultat | Stvarni rezultat | Status (PASS/FAIL) | ID bug-a | Opis greške | Prioritet greške | Datum izvršenja | Odgovorna osoba | Napomena |
|----------|------------|---------------|--------------------|------------------|--------------------|----------|--------------|------------------|-----------------|------------------|----------|
|          |            |               |                    |                  |                    |          |              |                  |                 |                  |          |



---

## Glavni rizici kvaliteta

| ID | Rizik | Vjerovatnoća | Utjecaj | Strategija ublažavanja |
|----|------|-------------|--------|-------------------------|
| R-01 | Netačni ili nepouzdani odgovori chatbot-a | Srednja | Visok | Testiranje na unaprijed definisanom skupu pitanja; validacija odgovora i poređenje sa očekivanim rezultatima |
| R-02 | Neispravno maskiranje osjetljivih podataka | Srednja | Visok | Testiranje na transkriptima sa ličnim podacima; provjera baze i logova da li su podaci maskirani |
| R-03 | Neispravan fallback mehanizam | Srednja | Visok | Testiranje scenarija nesigurnih odgovora; provjera preusmjeravanja na agenta bez gubitka konteksta |
| R-04 | Greške u obradi i pohrani transkripata | Srednja | Visok | Unit i integraciono testiranje parsiranja, validacije i spremanja transkripata |
| R-05 | Neautorizovan pristup administratorskom dijelu sistema | Niska | Kritičan | Testiranje autentifikacije i RBAC-a; pokušaji neovlaštenog pristupa (penetration testiranje) |
| R-06 | Pad performansi sistema pod opterećenjem | Srednja | Visok | Load i stress testiranje; simulacija više korisnika i mjerenje vremena odziva |
| R-07 | Nedovoljna upotrebljivost korisničkog interfejsa | Srednja | Srednji | UI i user testing sa stvarnim korisnicima; analiza povratnih informacija |
| R-08 | Regresije nakon izmjena sistema | Srednja | Visok | Automatizovani regresioni testovi; ponavljanje ključnih scenarija nakon svake izmjene |
| R-09 | Neispravno evidentiranje korisničkog feedback-a | Niska | Srednji | Testiranje prijave netačnih odgovora i njihove obrade u administratorskom dijelu |
| R-10 | Nedostupnost sistema ili pad stabilnosti | Niska | Srednji | Monitoring sistema, testiranje dostupnosti i fallback mehanizama |
