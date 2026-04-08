## User Stories

Projekat: _Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu snimljenih poziva iz call centra_

Ukupno stavki: 35  
Pokrivene uloge: Krajnji korisnik, Agent, Administrator, Developer, Tim

### US-1. Istraživanje domene

**Backlog referenca:** Backlog #1 – Istraživanje domene  
**Tip:** Research  
**Prioritet:** High  
**Status:** Done 

**Opis:**
Kao član razvojnog tima, želim da istražim domenu call centra i analiziram slična postojeća rješenja na tržištu, kako bih stekao razumijevanje problema koji sistem treba da riješi

**Poslovne vrijednosti:**
Duboko razumijevanje domene omogućava promišljeno donošenje odluka, smanjuje rizik od grešaka u ranijim fazama razvoja i osigurava usklađenost sistema sa stvarnim potrebama call centara.

**Pretpostavke i otvorena pitanja:**
- Postoji dostupna literatura i primjeri sličnih sistema.
- Tim ima pristup internetu i relevantnim izvorima informacija.
- Istraživanje se provodi u toku prve faze projekta.

**Veza sa drugim storijima ili zavisnostima:**
- Nema direktnih zavisnosti 
- Rezultati utiču na US-3 (Product Vision), US-5 (Istraživanje ulaznih formata), US-6(Istraživanje RAG i LLM servisa).

**Acceptance criteria:**
- Tim mora dokumentovati ključne karakteristike call centar domena (tipovi upita, radno okruženje, akteri).
- Tim mora identificovati najmanje 3 slična rješenja na tržištu i opisati njihove prednosti i nedostatke.
- Istraživanje mora imati sažeto napisan rezultat koji je dostupan svim članovima tima.
- Ishodi istraživanja moraju biti prezentovani na timskom sastanku i usvojeni od strane tima.
- Dokument mora sadržavati zaključke koji se koriste za definisanje MVP opsega.


### US-2. Mapiranje stakeholdera

**Backlog referenca:** Backlog #2 – Mapiranje stakeholdera  
**Tip:** Research  
**Prioritet:** High  
**Status:** Done  

**Opis:**
Kao product owner, želim da identifikujem sve aktere sistema i definišem njihove uloge, interese, očekivanja i uticaj, kako bih osigurao da su zahtjevi razvoja usklađeni s potrebama svih ključnih strana.

**Poslovne vrijednosti:**
Jasno mapiranje stakeholdera sprječava propuste u zahtjevima, pomaže u rješavanju potencijalnih konflikata interesa i pruža uvod za planiranje komunikacije tokom projekta.

**Pretpostavke i otvorena pitanja:**
- Tim je završio osnovno istraživanje domene (US-1).
- Stakeholderi su dostupni za konsultacije ili postoji dovoljno informacija o njihovim ulogama.
- Stakeholder mapa se ažurira tokom projekta ukoliko se pojave novi akteri.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-1 (Istraživanje domene).
- Rezultati utiču na US-3 (Product Vision) i US-9 (User Stories).

**Acceptance criteria:**
- Dokument mora sadržavati tabelu sa svim identifikovanim stakeholderima: krajnji korisnik, agent, administrator, menadžment, developeri.
- Za svakog stakeholdera mora biti definirano: uloga, interes, očekivanja, uticaj na sistem i prioritet komunikacije.
- Stakeholder mapa mora biti vizuelno prikazana (dijagram ili tabela).
- Dokument mora biti odobren od strane tima i dostupan svim članovima.
- Eventualni konflikti interesa između stakeholdera moraju biti identificirani i dokumentovani.


### US-3. Product Vision

**Backlog referenca:** Backlog #3 – Product Vision  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** Done  

**Opis:**
Kao product owner, želim da definiram jasnu viziju proizvoda koja opisuje za koga se sistem gradi, koji problem rješava i kako se mjeri uspjeh, kako bi cijeli tim imao zajednički cilj i smjer razvoja.

**Poslovne vrijednosti:**
Product Vision služi kao kompas za sve odluke tokom razvoja i osigurava da tim ne skrene s puta prema stvarnoj vrijednosti za korisnike.

**Pretpostavke i otvorena pitanja:**
- Istraživanje domene (US-1) i mapiranje stakeholdera (US-2) su završeni.
- Product owner ima ovlast za donošenje promišljenih odluka.
- Vizija se može prepravljati tokom projekta ukoliko se okolnosti promijene.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-1 (Istraživanje domene) i US-2 (Mapiranje stakeholdera).
- Utiče na US-7 (Definisanje MVP opsega) i US-9 (User Stories).

**Acceptance criteria:**
- Dokument mora sadržati: naziv projekta, opis problema, ciljne korisnike i vrijednost sistema.
- Mora biti jasno definisano šta ulazi i šta ne ulazi u MVP.
- Dokument mora sadržavati ključna ograničenja i pretpostavke (pravne, tehničke).
- Vizija mora biti prihvaćena od strane cijelog tima
- Dokument mora biti objavljen na zajedničkom repozitoriju i dostupan svim članovima.


### US-4. Team Charter

**Backlog referenca:** Backlog #4 – Team Charter  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** Done  

**Opis:**
Kao tim, želimo da definišemo raspodjelu uloga, načine komunikacije i format održavanja sastanaka, kako bismo uspostavili jasna pravila  i odgovornosti unutar tima.

**Poslovne vrijednosti:**
Team Charter sprječava nesporazume u timu, osigurava efikasnu komunikaciju i jasno definiše ko je odgovoran za koje aktivnosti tokom projekta.

**Pretpostavke i otvorena pitanja:**
- Svi članovi tima su identifikovani i dostupni za suradnju.
- Tim radi po Scrum metodologiji (posao se dijeli na male dijelove i radi se u sprintovima, uz stalnu komunikaciju tima)
- Charter se može prepravljati uz saglasnost tima.

**Veza sa drugim storijima ili zavisnostima:**
- Nema tehničkih zavisnosti – dokument se kreira na početku projekta.
- Usklađen sa US-3 (Product Vision) po pitanju uloga i komunikacije.

**Acceptance criteria:**
- Dokument mora sadržavati listu svih članova tima s dodijeljenim ulogama 
- Mora biti definisano: format sastanaka, koliko se često održava sastanak, kanali komunikacije i alati za suradnju.
- Moraju biti navedena pravila ponašanja i procedure rješavanja konflikata.
- Charter mora biti odobren od svih članova tima.
- Dokument mora biti postavljen na zajedničkom repozitoriju dostupnom svim članovima.


### US-5. Istraživanje ulaznih formata

**Backlog referenca:** Backlog #5 – Istraživanje ulaznih formata  
**Tip:** Research  
**Prioritet:** High  
**Status:** In Progress  

**Opis:**
Kao developer, želim da istražim i dokumentujem moguće formate ulaznih transkripta (tekstualni, CSV, JSON, audio), kako bih donio informisanu odluku o prihvatanju i obradi podataka u sistemu.

**Poslovne vrijednosti:**
Odabir ispravnog ulaznog formata je ključna arhitekturalna odluka koja direktno utiče na niz koraka obrade podataka i kvalitet baze znanja chatbota.

**Pretpostavke i otvorena pitanja:**
- Postoje stvarni primjeri transkripta iz call centara koji su dostupni za analizu.
- Tim ima tehničko znanje za analizu različitih formata podataka
- Odluka o formatu mora biti donesena prije implementacije parsera (program ili dio softvera koji čita neki tekst ili podatke i razbija ih na dijelove koje računar može razumjeti i obraditi.) (US-24).

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-1 (Istraživanje domene).
- Utiče na US-18 (Upload transkripta), US-23 (Priprema za obradu), US-24 (Parser).

**Acceptance criteria:**
- Tim mora istražiti i dokumentovati najmanje 3 različita formata ulaznih transkripata.
- Za svaki format moraju biti opisane prednosti, nedostaci i tehnička izvodivost programa.
- Mora biti donesena i dokumentovana odluka o podržanim formatima za MVP.
- Odabrani formati  moraju biti prezentovani timu i usvojeni od strane članova tima.
- Dokument mora biti postavljen na zajedničkom repozitoriju. 

### US-6. Istraživanje RAG i LLM servisa

**Backlog referenca:** Backlog #6 – Istraživanje RAG i LLM servisa  
**Tip:** Research  
**Prioritet:** High  
**Status:** In Progress  

**Opis:**
Kao developer, želim da istražim dostupne embedding modele, vektorske baze podataka i LLM API servise, kako bih odabrao najprikladniju tehnološku osnovu za RAG arhitekturu chatbota.

**Poslovne vrijednosti:**
Odabir ispravnih tehnologija za RAG direktno utiče na tačnost odgovora chatbota, troškove izvodjenja i prilagodljivost sistema.

**Pretpostavke i otvorena pitanja:**
- Tim ima osnovno znanje o RAG (Retrieval Augmented Generation) arhitekturi.
- Postoji budžet za testiranje LLM API servisa.
- Istraživanje uključuje i procjenu troškova za produkcijsko okruženje.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-1 (Istraživanje domene) i US-5 (Istraživanje ulaznih formata).
- Rezultati direktno utiču na US-27 (Izgradnja baze znanja) i US-21 (Skeleton projekta).

**Acceptance criteria:**
- Tim mora istražiti i porediti najmanje 2 LLM API servisa (npr. OpenAI, Mistral).
- Tim mora istražiti i porediti najmanje 2 vektorske baze podataka (npr. Pinecone, Chroma).
- Tim mora istražiti i porediti najmanje 2 embedding modele za generisanje vektora iz teksta.
- Findings moraju biti dokumentovani u obliku uporedne tabele s kriterijima odabira.
- Mora biti donesena i dokumentovana konačna odluka o odabranom tehnološkom stacku.
- Dokument mora biti dostupan svim članovima tima.


### US-7. Definisanje MVP opsega

**Backlog referenca:** Backlog #7 – Definisanje MVP opsega  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** Done  

**Opis:**
Kao product owner, želim da precizno definišem koje funkcionalnosti ulaze u MVP a koje su post-MVP, kako bi tim imao jasan fokus i mogao isporučiti vrijednost u najkraćem mogućem roku.

**Poslovne vrijednosti:**
Jasno razgraničenje MVP-a sprječava stalno dodavanje novih zahtjeva ili funkcionalnosti koje nisu planirane, a tim ih mora uraditi, fokusira tim na ključne funkcionalnosti i omogućava brzu isporuku radnog sistema koji se može validirati sa stakeholderima.

**Pretpostavke i otvorena pitanja:**
- Product Vision (US-3) je definisana i prihvaćena.
- Stakeholder mapa (US-2) je završena.
- MVP opseg je usklađen s raspoloživim resursima i vremenskim okvirom.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-3 (Product Vision) i US-2 (Mapiranje stakeholdera).
- Sastavni dio Product Vision deliverable-a.
- Utiče na prioritizaciju svih ostalih backlog stavki.

**Acceptance criteria:**
- Dokument mora jasno nabrojati sve funkcionalnosti koje ulaze u MVP.
- Dokument mora jasno nabrojati sve funkcionalnosti koje su izvan MVP opsega.
- Svaka stavka mora imati kratko obrazloženje zašto ulazi ili ne ulazi u MVP.
- MVP opseg mora biti odobren od strane svih stakeholdera na prezentaciji.
- Dokument mora biti integrisan u Product Vision i dostupan svim članovima tima.


### US-8. Početni Product Backlog

**Backlog referenca:** Backlog #8 – Početni Product Backlog  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** Done  

**Opis:**
Kao product owner, želim da kreiram inicijalni product backlog sa svim tehničkim i funkcionalnim zadacima projekta, kako bi tim imao strukturiran pregled rada i mogao planirati sprintove.

**Poslovne vrijednosti:**
Strukturiran backlog je temelj Scrum procesa – bez njega tim nema jasnu sliku šta treba biti urađeno i ne može efikasno planirati rad.

**Pretpostavke i otvorena pitanja:**
- Product Vision (US-3) i MVP opseg (US-7) su definirani.
- Tim je upoznat sa Scrum procesom i formatom backlog stavki.
- Backlog se ažurira na kraju svakog sprinta.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-3 (Product Vision), US-7 (MVP opseg).
- Deliverable koji se ažurira svaki sprint – veza s US-12 (Ažuriranje backloga).

**Acceptance criteria:**
- Backlog mora sadržavati sve identifikovane stavke s ID-om, nazivom, kratkim opisom, tipom, prioritetom, procjenom i statusom.
- Svaka stavka mora biti dovoljno precizna da se može realizovati u jednom sprintu.
- Backlog mora biti postavljen na zajedničkom repozitoriju i dostupan svim članovima tima.
- Inicijalni backlog mora biti prezentovan timu i odobren na sprint planiranju.
- Format backlog stavki mora biti stalan kroz cijeli projekat.


### US-9. User Stories

**Backlog referenca:** Backlog #9 – User Stories  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** In Progress  

**Opis:**
Kao product owner, želim da napišem jasne, precizne i provjerljive user stories za sve uloge u sistemu (krajnji korisnik, agent,  administrator), kako bi razvojni tim imao jasno definisane funkcionalne zahtjeve.

**Poslovne vrijednosti:**
User stories prevode poslovne zahtjeve u konkretne, mjerljive zadatke koje developer tim može implementirati i testirati, čime se smanjuje nejasnoća i povećava kvalitet isporuke.

**Pretpostavke i otvorena pitanja:**
- Stakeholder mapa (US-2) i Product Vision (US-3) su završeni.
- Tim je upoznat s formatom user stories (Ko / Šta / Zašto).
- Stories se prepravljaju i dorađuju tokom sprinta na osnovu dogovora tima.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-2, US-3, US-7, US-8.
- Usko povezano s US-10 (Acceptance Criteria) – svaki story mora imati acceptance kriterije.

**Acceptance criteria:**
- Svaki user story mora sadržavati: opis (kao [uloga] želim [akcija] kako bih [cilj]), poslovne vrijednosti, prioritet, pretpostavke, zavisnosti i acceptance kriterije.
- Stories moraju biti napisani za sve uloge: krajnji korisnik, agent, administrator, developer.
- Svaki story mora biti precizan i spreman na implementaciju unutar jednog sprinta.
- Stories moraju biti provjerljivi – jasno je kada su gotovi.
- Dokument mora imati verzije u slučaju korekcija i dostupan svim članovima tima.

### US-10. Acceptance Criteria

**Backlog referenca:** Backlog #10 – Acceptance Criteria  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** In Progress  

**Opis:**
Kao product owner, želim da za svaki user story definišem mjerljive i provjerljive acceptance kriterije, kako bi razvojni tim i QA (osiguranje kvaliteta) imali jasnu definiciju kada je svaka funkcionalnost ispravno implementirana.

**Poslovne vrijednosti:**
Jasni acceptance kriteriji eliminišu subjektivnost pri ocjeni završenosti zadatka, olakšavaju testiranje i smanjuju broj ispravki nakon implementacije.

**Pretpostavke i otvorena pitanja:**
- User stories (US-9) su napisani i dostupni.
- Tim je upoznat s principima pisanja kriterija (Given/When/Then ili lista provjera) koji se mogu testirati.
- Acceptance kriteriji se mogu dopuniti tokom sprinta ukoliko se pojave novi slučajevi.

**Veza sa drugim storijima ili zavisnostima:**
- Direktno zavisi od US-9 (User Stories).
- Koriste se kao osnova za US-19 (Testne strategije).

**Acceptance criteria:**
- Svaki user story mora imati najmanje 3 acceptance kriterija.
- Svaki kriterij mora biti konkretan, mjerljiv i da ima mogućnost testiranja.
- Kriteriji moraju pokriti i pozitivne scenarije i negativne slučajeve.
- Acceptance kriteriji moraju biti integrisani direktno unutar svakog user story-a.
- Tim mora odobriti kriterije na sprint planiranju prije početka implementacije.


### US-11. Nefunkcionalni zahtjevi

**Backlog referenca:** Backlog #11 – Nefunkcionalni zahtjevi  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** In Progress 

**Opis:**
Kao product owner, želim da definišem nefunkcionalne zahtjeve sistema s opisom, kategorijom, načinom provjere i prioritetom, kako bi razvojni tim vodio računa o performansama, sigurnosti i dostupnosti tokom implementacije.

**Poslovne vrijednosti:**
Nefunkcionalni zahtjevi osiguravaju da sistem ne samo da radi ispravno, nego i da radi dovoljno brzo, sigurno i pouzdano da zadovolji realne potrebe korisnika u produkcijskom okruženju.

**Pretpostavke i otvorena pitanja:**
- Product Vision (US-3) je definisana.
- Tim razumije razliku između funkcionalnih i nefunkcionalnih zahtjeva.
- NFR-ovi se prepravljaju tokom projekta po potrebi.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-3 (Product Vision) i US-2 (Stakeholder mapa).
- NFR-ovi se primjenjuju na sve funkcionalne user stories (US-13 do US-35).

**Acceptance criteria:**
- Dokument mora sadržavati najmanje 8 nefunkcionalnih zahtjeva pokrivajući: performanse, prilagodljivost rastu, dostupnost, upotrebljivost, auditabilnost, održavanje, tačnost i transparentnost.
- Svaki NFR mora imati: ID, kategoriju, opis, način provjere, prioritet i napomenu.
- NFR-7: Sistem mora odgovoriti na upit u roku od 3 sekunde u 95% slučajeva.
- NFR-9: Sistem mora biti dostupan najmanje 99% vremena.
- NFR-13: Chatbot mora davati relevantne odgovore u najmanje 85% testiranih slučajeva.
- Dokument mora biti odobren od tima i postavljen na zajedničkom repozitoriju.


### US-12. Ažuriranje backloga

**Backlog referenca:** Backlog #12 – Ažuriranje backloga  
**Tip:** Documentation  
**Prioritet:** Medium  
**Status:** In Progress  

**Opis:**
Kao product owner, želim da redovno analiziram i ažuriram sve stavke backloga po poslovnoj vrijednosti i tehničkim zavisnostima, kako bi backlog uvijek odražavao trenutne prioritete i stanje projekta.

**Poslovne vrijednosti:**
Ažuran backlog osigurava da tim uvijek radi na stavkama s najvećom poslovnom vrijednošću i da planiranja sprintova budu efikasna i relevantna.

**Pretpostavke i otvorena pitanja:**
- Inicijalni backlog (US-8) je kreiran.
- Ažuriranje se vrši na kraju svakog sprinta ili po potrebi.
- Svi članovi tima mogu predlagati izmjene, ali product owner donosi konačnu odluku.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-8 (Početni backlog).
- Utiče na sve ostale stavke backloga.

**Acceptance criteria:**
- Backlog mora biti ažuriran na kraju svakog sprinta.
- Svaka stavka mora imati ažurirani status (Not Started / In Progress / Done).
- Prioriteti stavki moraju biti prepravljani na osnovu novih saznanja i promjena u projektu.
- Nove stavke moraju biti dodane u backlog čim budu identifikovane.
- Ukloniti ili označiti kao nevažeće sve stavke koje više nisu relevantne.
- Ažurirana verzija backloga mora biti dostupna timu prije svakog planiranja sprinta.


### US-13. Konverzija audio zapisa u transkript

**Backlog referenca:** Backlog #13 – Konvertovanje iz audio zapisa u transkript  
**Tip:** Research  
**Prioritet:** Medium   
**Status:** In Progress  

**Opis:**
Kao administrator, želim da istražim i integriram API servis za automatsku konverziju audio zapisa poziva u tekstualni transkript, kako ne bih morao ručno transkriptovati snimke i tako ubrzavam unos podataka u sistem.

**Poslovne vrijednosti:**
Automatska audio-to-text konverzija značajno ubrzava proces pripreme podataka za treniranje chatbota i smanjuje mogućnost grešaka pri ručnoj transkripciji.

**Pretpostavke i otvorena pitanja:**
- Postoje audio zapisi poziva u prihvatljivim formatima (.mp3, .wav, .m4a).
- Tim je istražio dostupne speech-to-text API servise (OpenAI, Cloude, Whisper, Azure).
- API servis podržava bosanski/hrvatski/srpski jezik ili engleski.

**Veza sa drugim storijima ili zavisnostima:**
- Utiče na US-18 (Upload transkripata) – audio upload kao dodatni ulazni kanal.
- Zavisi od US-5 (Istraživanje ulaznih formata).
- Konvertovani transkript prolazi kroz US-23 (Priprema za obradu).

**Acceptance criteria:**
- Tim mora istražiti i porediti najmanje 2 speech-to-text API servisa po kriterijima: tačnost, cijena, podrška za jezik, kašnjenje u reakciji sistema.
- Mora biti donesena dokumentovana odluka o odabranom API servisu.
- Administrator mora moći uploadovati audio fajl putem interfejsa.
- Sistem mora automatski pokrenuti konverziju nakon uploada i prikazati status obrade.
- Generisani transkript mora biti dostupan za pregled i editovanje prije unosa u bazu.
- Sistem mora prikazati jasnu poruku greške ukoliko konverzija nije uspjela.
- Konvertovani transkript mora proći iste korake obrade kao ručno uneseni (US-23, US-25, US-26).


### US-14. Plan baze podataka

**Backlog referenca:** Backlog #14 – Plan baze podataka   
**Tip:** Technical   
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao developer, želim da dizajniram shemu baze podataka za pohranu audio zapisa, transkripata, korisničkih računa, pitanja, odgovora i metapodataka, kako bi sistem imao stabilan i prilagodljiv temelj za pohranu podataka.

**Poslovne vrijednosti:**
Dobro dizajnirana baza podataka je temelj cijelog sistema – loš dizajn na ovom nivou uzrokuje skupo preuređivanje u kasnijim fazama razvoja.

**Pretpostavke i otvorena pitanja:**
- Funkcionalni zahtjevi (US-9, US-10) su dovoljno definirani da se može pristupiti dizajnu baze.
- Tim je usaglasio izbor sistema za upravljanje bazom podataka (SQL/NoSQL).
- Baza mora podržavati i relacijske podatke (korisnici, transkripti) i vektorske podatke (embedding).

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-9 (User Stories) i US-11 (Nefunkcionalni zahtjevi).
- Utiče na US-21 (Skeleton projekta), US-18 (Upload transkripata), US-27 (Baza znanja).

**Acceptance criteria:**
- Dizajn mora obuhvatiti sve ključne entitete: korisnici (uloge), transkripti, konverzacije, pitanja, odgovori, logovi, prijave grešaka.
- ER dijagram mora biti kreiran i dostupan svim članovima tima.
- Moraju biti definisane sve relacije između entiteta (one-to-many, many-to-many).
- Dizajn mora biti usklađen s nefunkcionalnim zahtjevima (performanse, prilagodljivost).
- Plan mora biti pregledan i odobren od strane tima prije implementacije.
- Dizajn mora predvidjeti pohranu vektorskih embeddinga za RAG komponentu.

### US-15. Ocjena odgovora chatbota od strane korisnika

**Backlog referenca:** Backlog #15 – Ocjena odgovora chatbota   
**Tip:** Research/Feature   
**Prioritet:** High   
**Status:** In Progress  

**Opis:**
Kao krajnji korisnik, želim da ocijenim odgovor chatbota nakon svake interakcije, kako bi sistem dobio povratnu informaciju o kvalitetu i tačnosti odgovora.

**Poslovne vrijednosti:**
Korisničke ocjene su primarni izvor informacija za identifikaciju netačnih odgovora i stalno unapređenje modela bez potrebe za ručnim pregledom svake konverzacije.

**Pretpostavke i otvorena pitanja:**
- Korisnik je postavio pitanje i primio odgovor od chatbota.
- Sistem evidentira i čuva sve ocjene s vremenskom oznakom (NFR-11).
- Negativna ocjena automatski kreira zapis u sistemu za praćenje problema.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-22 (Chat UI – korisnik mora imati interfejs za interakciju).
- Negativne ocjene vidljive administratoru kroz US-35 (Pregled prijavljenih problema).
- Utiče na US-32 (Potvrda i obrada netačnog odgovora).

**Acceptance criteria:**
- Sistem mora prikazati opciju za ocjenu (pozitivna/negativna) uz svaki odgovor chatbota.
- Kada korisnik pošalje negativnu ocjenu, sistem mora prikazati opciju za dodavanje komentara.
- Sistem mora evidentirati svaku ocjenu u bazi logova s ID-om konverzacije, ocjenom i vremenskom oznakom.
- Sistem mora korisniku potvrditi prijem ocjene kratkom porukom.
- Sistem ne smije tražiti prijavu/registraciju od korisnika za davanje ocjene.
- Negativno ocijenjeni odgovori moraju biti dostupni administratoru na pregledu.


### US-16. Risk Register

**Backlog referenca:** Backlog #16 – Risk Register  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** Not Started 

**Opis:**
Kao product owner, želim da identifikujem i dokumentujem ključne projektne i tehničke rizike s vjerovatnoćom pojave, uticajem i strategijom smanjivanja rizika, kako bi tim mogao preventivno upravljati rizicima tokom projekta.

**Poslovne vrijednosti:**
Preventivno upravljanje rizicima smanjuje vjerovatnoću da neočekivani događaji ugroze isporuku projekta na vrijeme i u budžetu.

**Pretpostavke i otvorena pitanja:**
- Tim ima dovoljno uvida u tehnički i poslovni kontekst projekta za identifikaciju rizika.
- Risk Register se ažurira na kraju svakog sprinta.
- Svaki član tima može predlagati nove rizike.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-1 (Istraživanje domene), US-6 (RAG istraživanje), US-3 (Product Vision).
- Utiče na sve tehničke odluke tokom razvoja.

**Acceptance criteria:**
- Dokument mora sadržavati tabelu s najmanje 8 identifikovanih rizika.
- Za svaki rizik mora biti definirano: ID, opis, kategorija, vjerovatnoća (1-5), uticaj (1-5), ukupna ocjena, strategija smanjenja rizika i vlasnik rizika.
- Rizici moraju pokriti: tehničke, projektne, pravne i poslovne kategorije.
- Register mora biti odobren od strane tima i pohranjen na zajedničkom repozitoriju.
- Register mora biti ažuriran na kraju svakog sprinta s novim rizicima i promjenama statusa.

### US-17. Use Case Model

**Backlog referenca:** Backlog #17 – Use Case Model  
**Tip:** Documentation   
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao developer, želim da kreiram UML use case dijagram koji prikazuje sve aktere sistema i njihove interakcije, kako bi tim imao vizuelni pregled funkcionalnih zahtjeva i odnosa između uloga.

**Poslovne vrijednosti:**
Use case model pruža jednoznačnu vizuelnu komunikaciju između tehničkih i netehničkih članova tima i služi kao referentni dokument za implementaciju.

**Pretpostavke i otvorena pitanja:**
- User stories (US-9) su dovoljno definisani da se može pristupiti modeliranju.
- Tim je upoznat s UML notacijom za use case dijagrame.
- Model se ažurira kada se dodaju novi zahtjevi.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-9 (User Stories) i US-2 (Stakeholder mapa).
- Alternativa ili dopuna domain modelu.

**Acceptance criteria:**
- Dijagram mora prikazati sve aktere sistema: krajnji korisnik, agent, administrator, (menadžment, developer).
- Dijagram mora prikazati sve ključne use case-ove za MVP.
- Moraju biti prikazane relacije između aktera i use case-ova (include, extend gdje je moguće primijeniti).
- Dijagram mora biti kreiran u odgovarajućem alatu 
- Model mora biti pregledan i odobren od strane tima.
- Dijagram mora biti pohranjen u repozitoriju u formatu koji se može editovati.

### US-18. Upload i unos transkripata

**Backlog referenca:** Backlog #18 – Upload i unos transkripata  
**Tip:** Feature  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao administrator, želim da uploadujem transkripte razgovora iz call centra u sistem, kako bi se ti podaci obradili i koristili za treniranje i poboljšanje chatbota.

**Poslovne vrijednosti:**
Unos transkripata je primarni izvor podataka za cijeli sistem – bez ovog koraka chatbot ne može imati bazu znanja niti davati relevantne odgovore.

**Pretpostavke i otvorena pitanja:**
- Administrator je prijavljen u sistem s odgovarajućim privilegijama.
- Transkripti su dostupni u podržanim formatima definiranim u US-5.
- Sistem ima implementiranu logiku za validaciju i obradu fajlova (US-23).

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-14 (Plan baze podataka), US-5 (Ulazni formati), US-21 (Skeleton projekta).
- Pokreće lanac obrade: US-23 (Priprema) → US-24 (Parser) → US-25 (Normalizacija) → US-26 (Maskiranje) → US-27 (Baza znanja).

**Acceptance criteria:**
- Sistem mora prikazati interfejs za upload fajlova s podržanim formatima.
- Sistem mora podržavati upload više fajlova istovremeno.
- Sistem mora validirati format i veličinu fajlova te prikazati grešku za nepodržane formate.
- Nakon uspješnog uploada, sistem mora automatski pokrenuti niz koraka obrade (US-23).
- Administrator mora primiti potvrdu o uspješnom uploadovanju s imenom fajla i vremenskom oznakom.
- Sistem ne smije prihvatiti fajl veći od definisanog limita bez upozorenja.
- Uploadovani transkripti moraju biti vidljivi u pregledu (US-33).

### US-19. Osmišljavanje testnih strategija

**Backlog referenca:** Backlog #19 – Osmisliti testne strategije  
**Tip:** Research  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao QA inženjer / developer, želim da definišem testnu strategiju projekta koja pokriva vrste testova, ciljeve testiranja i načine evidentiranja rezultata, kako bi tim imao sistematičan pristup osiguranju kvaliteta sistema.

**Poslovne vrijednosti:**
Jasna testna strategija smanjuje broj kvarova u produkciji, osigurava da acceptance kriteriji budu provjereni i pruža timu povjerenje u ispravnost sistema.

**Pretpostavke i otvorena pitanja:**
- Acceptance Criteria (US-10) su definirani.
- Tim ima resurse za implementaciju automatizovanih testova.
- Testiranje se provodi tokom cijelog razvoja, ne samo na kraju.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-10 (Acceptance Criteria) i US-11 (NFR).
- Utiče na implementaciju svih funkcionalnih stavki.

**Acceptance criteria:**
- Dokument mora definisati vrste testova koje će se koristiti: unit, integracijski, end-to-end, load testovi.
- Mora biti definisano šta je cilj svakog tipa testiranja i koji dijelovi sistema pokriva.
- Mora biti definisan format evidentiranja rezultata testova (izvještaji, dashboardi).
- Strategija mora biti usklađena s NFR zahtjevima (NFR-7, NFR-8, NFR-13).
- Dokument mora biti odobren od tima i postavljen na zajedničkom repozitoriju.
- Strategija mora definisati minimalan procenat pokrivenosti koda testovima.

### US-20. Definition of Done

**Backlog referenca:** Backlog #20 – Definition of Done   
**Tip:** Documentation  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao Scrum tim, želimo da usvojimo zajedničku definiciju kada je backlog stavka smatrana završenom, kako bi svi članovi tima imali isti standard kvaliteta i ne dolazilo do nesporazuma pri zatvaranju zadataka.

**Poslovne vrijednosti:**
DoD eliminira subjektivnost pri ocjeni završenosti rada, osigurava konzistentan kvalitet isporuke i smanjuje dug tokom projekta.

**Pretpostavke i otvorena pitanja:**
- Tim je upoznat s Scrum procesom i konceptom DoD-a.
- DoD se primjenjuje na sve stavke backloga od trenutka usvajanja.
- DoD se može prepravljati uz saglasnost tima 

**Veza sa drugim storijima ili zavisnostima:**
- Utiče na sve ostale backlog stavke – primjenjuje se na svaki task.
- Usklađen s US-10 (Acceptance Criteria) i US-19 (Testne strategije).

**Acceptance criteria:**
- DoD dokument mora navesti jasne i mjerljive kriterije završenosti za kod (npr. code review, testovi prolaze, nema otvorenih bugova).
- DoD mora pokriti kriterije za dokumentacijske isporuke (formatiran, odobren, pohranjen).
- DoD mora biti odobren uz saglasnost cijelog tima.
- DoD mora biti pohranjen na vidljivom i dostupnom mjestu za sve članove tima.
- Primjena DoD-a mora biti provjeravana na svakom pregledu sprinta.

### US-21. Osnovni skeleton projekta

**Backlog referenca:** Backlog #21 – Osnovni skeleton projekta   
**Tip:** Technical Task  
**Prioritet:** High  
**Status:** Not Started

**Opis:**
Kao developer, želim da postavim tehnički skeleton sistema koji uključuje GitHub repozitorij, strukturu foldera, konfiguraciju alata i osnovni CI/CD niz koraka, kako bi cijeli tim mogao početi razvijati na konzistentnoj osnovi.

**Poslovne vrijednosti:**
Skeleton projekta eliminiša tehničke prepreke na početku razvoja i osigurava da svi developeri rade u identičnom okruženju s dosljednom strukturom koda.

**Pretpostavke i otvorena pitanja:**
- Tehnološki stack je odabran (US-6).
- Tim ima pristup GitHub repozitoriju i deployment okruženju.
- Svi developeri imaju instalirane potrebne alate lokalno.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-6 (RAG istraživanje – odabir stacka) i US-14 (Plan baze podataka).
- preduslov za sve implementacijske stavke: US-18, US-22, US-23, US-24, US-25, US-26, US-27.

**Acceptance criteria:**
- GitHub repozitorij mora biti kreiran s definisanom branch strategijom (main, develop, feature branches).
- Struktura foldera mora biti uspostavljena i dokumentovana u README fajlu.
- Osnovna konfiguracija backend frameworka mora biti postavljena i pokrenuta lokalno.
- Konfiguracija baze podataka mora biti postavljena (lokalno i testno okruženje).
- Svi developeri moraju biti u stanju pokrenuti projekt lokalno ako slijede README upute.
- Skeleton mora biti pregledan i odobren od tima prije početka implementacije.

### US-22. Chat UI – Interfejs za krajnjeg korisnika

**Backlog referenca:** Backlog #22 – Chat UI  
**Tip:** Feature  
**Prioritet:** High 
**Status:** Not Started 

**Opis:**
Kao krajnji korisnik, želim da imam jednostavan chat interfejs s poljem za unos teksta i prikazom odgovora chatbota, kako bih mogao komunicirati s AI asistentom i dobiti odgovore na pitanja vezana uz usluge call centra.

**Poslovne vrijednosti:**
Chat UI je primarna tačka kontakta između korisnika i sistema – njen kvalitet direktno utiče na korisničko iskustvo i stopu prihvatanja sistema.

**Pretpostavke i otvorena pitanja:**
- Skeleton projekta (US-21) je postavljen.
- Backend API za chatbot (US-27) je implementiran.
- UI mora biti dostupan na web i mobilnim uređajima.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-21 (Skeleton projekta) i US-27 (Baza znanja – backend).
- US-15 (Ocjena odgovora) i US-31 (Preusmjeravanje na agenta) integrišu se u ovaj UI.

**Acceptance criteria:**
- Interfejs mora prikazivati polje za unos teksta i dugme za slanje poruke.
- Interfejs mora prikazivati historiju razgovora u toku aktivnog sastanka.
- Na početku svake konverzacije mora biti prikazana poruka da korisnik komunicira s AI asistentom (NFR-14).
- Sistem mora prikazati indikator učitavanja dok čeka na odgovor chatbota.
- Odgovor mora biti prikazan u roku od 3 sekunde u 95% slučajeva (NFR-7).
- Sistem ne smije dozvoliti slanje prazne poruke.
- UI mora biti reaktivan i funkcionalan na desktop i mobilnim uređajima.
- Interfejs mora sadržavati opciju za ocjenu odgovora (US-15).

### US-23. Priprema za obradu transkripata

**Backlog referenca:** Backlog #23 – Priprema za obradu transkripata  
**Tip:** Technical Task  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao developer, želim da implementiram niz koraka za pripremu transkripata koji uključuje normalizaciju teksta, razdvajanje po ulogama i maskiranje osjetljivih podataka, kako bi sirovi transkripti bili u formatu pogodnom za izgradnju baze znanja.

**Poslovne vrijednosti:**
Kvalitet pripreme transkripata direktno utiče na kvalitet baze znanja i tačnost odgovora chatbota – loša priprema podataka rezultira netačnim i odgovorima koji nisu relevantni.

**Pretpostavke i otvorena pitanja:**
- Ulazni formati transkripata su definirani (US-5).
- Skeleton projekta (US-21) je postavljen.
- Pipeline je modularan: svaki korak (normalizacija, parser, maskiranje) može se pokrenuti nezavisno.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-18 (Upload transkripata), US-21 (Skeleton).
- Sastavljen od od US-24 (Parser), US-25 (Normalizacija), US-26 (Maskiranje).
- preduslov za US-27 (Izgradnja baze znanja).

**Acceptance criteria:**
- Niz koraka mora biti automatski pokrenut nakon svakog uspješnog uploada transkripta i mora izvršiti sve tri faze: normalizaciju, razdvajanje uloga i maskiranje – u definisanom redoslijedu.
- Obrađeni transkript mora biti pohranjen u bazu s metapodacima o procesu obrade.
- Sistem mora zabilježiti svaki korak obrade i eventualne greške.
- Obrada ne smije prekinuti rad sistema za ostale korisnike (NFR-8).
- Pipeline mora biti testiran na primjerima transkripata s različitim formatima.

### US-24. Parser za razdvajanje uloga u transkriptu

**Backlog referenca:** Backlog #24 – Parser za razdvajanje uloga  
**Tip:** Technical  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao developer, želim da implementiram parser koji automatski detektuje i razdvaja redove agenta i korisnika u transkriptu, kako bi sistem znao ko govori i mogao pravilno indeksirati sadržaj za RAG.

**Poslovne vrijednosti:**
Razlikovanje uloga u transkriptu je ključno za kvalitetno indeksiranje – RAG sistem treba znati razliku između pitanja korisnika i odgovora agenta da bi generisao relevantne odgovore.

**Pretpostavke i otvorena pitanja:**
- Transkripti imaju konzistentan format označavanja uloga (npr. 'Agent:', 'Korisnik:').
- Edge case-ovi (nejasni redovi, više govornika) su identifikovani i dokumentovani.
- Parser podržava formate definirane u US-5.

**Veza sa drugim storijima ili zavisnostima:**
- Dio pipeline-a US-23 (Priprema za obradu).
- Zavisi od US-5 (Istraživanje ulaznih formata) i US-21 (Skeleton).
- Izlaz parsera se koristi u US-25 (Normalizacija) i US-27 (Baza znanja).

**Acceptance criteria:**
- Parser mora ispravno detektovati i razdvojiti redove agenta i korisnika u 95% slučajeva na testnom skupu.
- Parser mora kreirati strukturisani izlaz (JSON ili sličan format) s jasno označenim ulogama.
- Parser mora evidentirati redove koje nije mogao jasno kategorisati.
- Parser mora biti pokriven unit testovima s primjerima različitih formata.
- Performanse parsera moraju biti zadovoljavajuće (obrada transkripta u manje od 5 sekundi).
- Parser mora biti integrisan u pipeline US-23.

## US-25. Normalizacija teksta transkripata

**Backlog referenca:** Backlog #25 – Normalizacija teksta  
**Tip:** Technical  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao developer, želim da implementiram modul za normalizaciju teksta koji uklanja šum, standardizuje interpunkciju i format transkripata, kako bi tekst bio u konzistentnom obliku koji je pogodan za generisanje embeddinga.

**Poslovne vrijednosti:**
Normalizovani tekst poboljšava kvalitet embeddinga, što direktno utiče na relevantnost odgovora chatbota.

**Pretpostavke i otvorena pitanja:**
- Definirani su konkretni tipovi šuma koji se javljaju u transkriptima (npr. oznake za pauzu).
- Normalizacija ne smije mijenjati značenje rečenica.
- Modul se može prilagoditi novim vrstama šuma.

**Veza sa drugim storijima ili zavisnostima:**
- Dio pipeline-a US-23 (Priprema za obradu).
- Zavisi od US-24 (Parser – prethodni korak u pipeline-u).
- Izlaz se koristi u US-26 (Maskiranje) i US-27 (Baza znanja).

**Acceptance criteria:**
- Modul mora ukloniti definisane tipove šuma iz teksta (verbalni tikovi, oznake pauze, višestruki razmaci).
- Modul mora standardizovati interpunkciju prema definisanim pravilima.
- Normalizacija mora očuvati izvorno značajne informacije iz originalnog teksta.
- Modul mora biti pokriven unit testovima s primjerima normalnog i šumovitog teksta.
- Modul mora biti integrisan u pipeline US-23 kao drugi korak.

### US-26. Maskiranje osjetljivih podataka u transkriptima

**Backlog referenca:** Backlog #26 – Maskiranje osjetljivih podataka  
**Tip:** Technical  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao developer, želim da implementiram modul koji automatski detektuje i maskira osjetljive lične podatke (ime, telefon, JMBG, email) u transkriptima prije pohrane i obrade, kako bi sistem bio usklađen s pravnim propisima o zaštiti privatnosti.

**Poslovne vrijednosti:**
Maskiranje osjetljivih podataka je pravna i etička obaveza (GDPR i lokalni propisi) – propust u ovom koraku može rezultirati pravnom odgovornošću organizacije.

**Pretpostavke i otvorena pitanja:**
- Definisana je lista tipova osjetljivih podataka koji se maskiraju.
- Maskiranje se vrši prije pohrane u bazu – podaci nikada ne smiju biti pohranjeni nemaskirani.
- Korisnik je obaviješten da su njegovi podaci zaštićeni (NFR-14).

**Veza sa drugim storijima ili zavisnostima:**
- Dio pipeline-a US-23 (Priprema za obradu).
- Treći korak u pipeline-u, izvršava se nakon US-24 i US-25.
- Usklađen s pravnim zahtjevima definisanim u US-3 (Product Vision – ograničenja).

**Acceptance criteria:**
- Modul mora detektovati i maskirati: puna imena, telefonske brojeve, JMBG, email adrese, adrese.
- Maskirani podaci moraju biti zamijenjeni odgovarajućim placeholderima (npr. [IME], [TELEFON]).
- Modul mora biti testiran na skupu od najmanje 20 primjera s različitim tipovima osjetljivih podataka.
- Udio detekcije mora biti najmanje 95% na testnom skupu.
- Modul mora biti integrisan u pipeline US-23 kao završni korak prije pohrane.
- Niti jedan nemaskirani osjetljivi podatak ne smije dospjeti u vektorsku bazu podataka.

### US-27. Izgradnja baze znanja chatbota

**Backlog referenca:** Backlog #27 – Izgradnja baze znanja  
**Tip:** Feature  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao administrator, želim da pokrenem proces izgradnje baze znanja chatbota koji generišu embedding vektore iz obrađenih transkripata i pohranjuje ih u vektorsku bazu, kako bi chatbot mogao davati relevantne odgovore baziran na stvarnim podacima call centra.

**Poslovne vrijednosti:**
Baza znanja je srž cijelog sistema – bez nje chatbot nema informacije na osnovu kojih može odgovarati na pitanja korisnika.

**Pretpostavke i otvorena pitanja:**
- Obrađeni transkripti su dostupni u sistemu (US-23, US-24, US-25, US-26 završeni).
- LLM i embedding servis su odabrani i konfigurisani (US-6).
- Vektorska baza podataka je postavljena (US-14, US-21).

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-23 (Priprema za obradu), US-6 (Odabir RAG stacka), US-14 (Baza podataka), US-21 (Skeleton).
- Preduvjet za US-22 (Chat UI) – chatbot ne može odgovarati bez baze znanja.

**Acceptance criteria:**
- Sistem mora generisati embedding vektore iz svakog obrađenog segmenta transkripta.
- Embedding-i moraju biti pohranjeni u vektorsku bazu s odgovarajućim metapodacima.
- Retrieval mehanizam mora biti implementiran i testiran – mora vraćati relevantne odgovore za dato pitanje.
- Administrator mora moći pokrenuti proces izgradnje/ažuriranja baze znanja bez prekida rada sistema (NFR-12).
- Sistem mora prikazati status procesa izgradnje u realnom vremenu.
- Sistem mora evidentirati datum i opseg posljednjeg ažuriranja baze znanja.
- Chatbot mora davati relevantne odgovore u najmanje 85% testiranih slučajeva (NFR-13).


### US-28. Prijava netačnog odgovora od strane agenta

**Backlog referenca:** Backlog #28 – Prijava netačnog odgovora   
**Tip:** Technical Task  
**Prioritet:** Medium  
**Status:** Not Started  

**Opis:**
Kao agent call centra, želim da prijavim odgovor chatbota koji je netačan ili neprikladan, kako bi administrator mogao pregledati grešku i koristiti je za poboljšanje modela.

**Poslovne vrijednosti:**
Agenti su stručnjaci u domeni call centra i mogu pružiti visokokvalitetan feedback koji direktno poboljšava tačnost chatbota.

**Pretpostavke i otvorena pitanja:**
- Agent je prijavljen u sistem sa svojom ulogom.
- Agent ima pristup konverzacijama koje su preusmjerene s chatbota ili logovima interakcija.
- Prijavljena greška kreira zapis koji je vidljiv administratoru.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-31 (Preusmjeravanje na agenta) i US-22 (Chat UI).
- Prijave vidljive u US-35 (Pregled prijavljenih problema – admin).
- Obrađuje se kroz US-32 (Potvrda i obrada netačnog odgovora).

**Acceptance criteria:**
- Sistem mora agentima prikazati listu konverzacija iz chatbota koje su im preusmjerene ili dostupne za pregled.
- Agent mora moći označiti konkretan odgovor chatbota kao netačan.
- Agent mora imati opciju dodavanja komentara (opis greške ili ispravak).
- Sistem mora korisniku potvrditi prijem prijave vidljivom porukom.
- Prijavljena interakcija mora biti dostupna administratoru unutar jednog minuta od podnošenja prijave.
- Sistem ne smije dozvoliti slanje prijave bez označene specifične interakcije.


### US-29. Korisnička dokumentacija

**Backlog referenca:** Backlog #29 – Korisnička dokumentacija  
**Tip:** Documentation  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao developer, želim da kreiram korisničku dokumentaciju koja obuhvata upute za korištenje chatbota, admin panela i unosa transkripata, kako bi krajnji korisnici, agenti i administratori mogli samostalno koristiti sistem bez dodatne obuke.

**Poslovne vrijednosti:**
Dobra korisnička dokumentacija smanjuje troškove podrške, ubrzava proces upoznavanja novih korisnika i povećava stopu samoposluge u sistemu.

**Pretpostavke i otvorena pitanja:**
- Ključne funkcionalnosti sistema su implementirane i stabilne.
- Dokumentacija se ažurira pri svakoj značajnijoj izmjeni sistema.
- Dokumentacija mora biti razumljiva korisnicima bez tehničkog predznanja.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od implementacije svih funkcionalnih stavki: US-18, US-22, US-27, US-33, US-34, US-35.
- Usklađena s NFR-10 (Upotrebljivost).

**Acceptance criteria:**
- Dokumentacija mora sadržavati vodič za krajnjeg korisnika: kako koristiti chatbot i prijaviti netačan odgovor.
- Dokumentacija mora sadržavati vodič za agenta: kako pregledati konverzacije i prijaviti grešku.
- Dokumentacija mora sadržavati vodič za administratora: unos transkripata, pregled logova, upravljanje bazom znanja.
- Svaki vodič mora sadržavati screenshotove ili vizualne korake.
- Dokumentacija mora biti objavljena na dostupnom i vidljivom mjestu (wiki, portal, PDF).
- Dokumentacija mora biti provjerena s krajnjim korisnicima – korisnik mora moći završiti zadatak slijedeći uputstvo.

### US-30. Izgradnja razvojnog okruženja

**Backlog referenca:** Backlog #30 – Izgradnja razvojnog okruženja  
**Tip:** Feature  
**Prioritet:** Medium  
**Status:** Not Started  

**Opis:**
Kao developer, želim da podesim razvojno okruženje koje uključuje pakovanje aplikacije i svih njenih zavisnosti u izolovani, prenosivi kontejner, konfiguraciju baze podataka i backend framework, kako bi svi developeri imali identično i pouzdano okruženje za razvoj.

**Poslovne vrijednosti:**
Konzistentno razvojno okruženje eliminiše probleme tipa 'radi na mom računaru, ne radi na tvom', ubrzava onboarding novih developera i pojednostavljuje dostupnost korisnicima .

**Pretpostavke i otvorena pitanja:**
- Tehnološki stack je odabran (US-6).
- Svi developeri imaju instaliran Docker (za pakovanje aplikacije i svih njenih zavisnosti u izolovani, prenosivi kontejner).
- Okruženje mora podržavati lokalni razvoj i testno puštanje aplikacije.

**Veza sa drugim storijima ili zavisnostima:**
- Dio US-21 (Skeleton projekta) ili direktni preduslov za njega.
- Preduslov za sve implementacijske stavke.

**Acceptance criteria:**
- Docker Compose konfiguracija mora pokrenuti sve potrebne servise jednom komandom.
- Baza podataka mora biti konfigurisana s inicijalnim podacima i migracijom sheme.
- Backend servis mora biti pokrenut i dostupan lokalno s jednom komandom.
- README mora sadržavati jasne upute za postavljanje okruženja.
- Okruženje mora biti testirano na Windows, macOS i Linux platformama.
- Staging okruženje mora biti konfigurisano za testiranje prije puštanja softvera na produkciju.

### US-31. Preusmjeravanje na agenta kada chatbot ne može odgovoriti

**Backlog referenca:** Backlog #31 – Odgovor kada nema sigurnog responsea  
**Tip:** Feature  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao krajnji korisnik, želim da budem obavješten kada chatbot ne može dati siguran odgovor i da imam opciju preusmjeravanja na live agenta, kako moj upit ne bi ostao bez odgovora.

**Poslovne vrijednosti:**
Fallback mehanizam osigurava da niti jedan korisnički upit ne ostane bez odgovora, čime se štiti korisničko iskustvo i povjerenje u sistem.

**Pretpostavke i otvorena pitanja:**
- Definisan je prag sigurnosti ispod kojeg chatbot ne treba dati odgovor.
- Postoji mehanizam za preusmjeravanje na agenta (ticketing, live chat).
- Ovakvi slučajevi se zapisuju za analizu (NFR-11).

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-22 (Chat UI) i US-27 (Baza znanja).
- Pokrenuti za agenta US-28 (Prijava netačnog odgovora).

**Acceptance criteria:**
- Sistem mora prikazati jasnu i razumljivu poruku korisniku kada chatbot ne može dati siguran odgovor.
- Sistem mora ponuditi opciju preusmjeravanja na agenta ili kontaktnog obrasca.
- Sistem mora pratiti sve slučajeve fallback-a u logovima s pitanjem korisnika i vremenskom oznakom (NFR-11).
- Sistem ne smije prikazati netačan odgovor kao tačan ukoliko je nivo sigurnosti ispod definisanog praga.
- Poruka mora biti prikazana u roku od 3 sekunde od detekcije niske sigurnosti (NFR-7).
- Preusmjereni slučajevi moraju biti vidljivi agentima u njihovom interfejsu.

### US-32. Potvrda i obrada prijavljenih netačnih odgovora

**Backlog referenca:** Backlog #32 – Potvrda i obrada netačnog odgovora  
**Tip:** Technical Task  
**Prioritet:** Medium  
**Status:** Not Started  

**Opis:**
Kao administrator, želim da pregledam prijavljene netačne odgovore, potvrdim greške i označim ih za korištenje u idućem procesu nadogradnje chatbota, kako bi sistem mogao redovno unaprijediti tačnost svojih odgovora.

**Poslovne vrijednosti:**
Zatvaranje feedback petlje između korisnika/agenta i sistema za treniranje je ključno za dugoročno poboljšanje kvaliteta chatbota.

**Pretpostavke i otvorena pitanja:**
- Postoje prijavljene greške od korisnika (US-15) i agenata (US-28).
- Administrator je prijavljen u sistem.
- Odobrene greške se automatski dodaju u niz koraka za trening.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-15 (Ocjena korisnika), US-28 (Prijava agenta), US-35 (Pregled prijavljenih problema).
- Obrađene greške utiču na US-27 (Ažuriranje baze znanja).

**Acceptance criteria:**
- Administrator mora moći pregledati detalje svake prijave: pitanje, odgovor chatbota, ocjena, komentar.
- Administrator mora moći označiti prijavu kao: Potvrđena greška / Lažna prijava / U obradi.
- Potvrđene greške moraju biti automatski ili ručno dodane u listu za novo treniranje.
- Sistem mora prikazati ukupan broj neobrađenih prijava na admin interfejs.
- Nakon obrade prijave, sistem mora evidentirati ko je i kada obradio prijavu.
- Sistem ne smije dozvoliti brisanje prijave bez potvrde administratora.

### US-33. Pregled unesenih transkripata

**Backlog referenca:** Backlog #33 – Pregled unesenih transkripata  
**Tip:** Feature  
**Prioritet:** High  
**Status:** Not Started  

**Opis:**
Kao administrator, želim da vidim tabelu svih uploadovanih transkripata s nazivom fajla, datumom unosa i statusom obrade, kako bih mogao pratiti koje su datoteke uspješno obrađene i koje imaju problem.

**Poslovne vrijednosti:**
Pregled transkripata pruža administratoru transparentnost i kontrolu nad procesom unosa podataka koji je temelj kvaliteta chatbota.

**Pretpostavke i otvorena pitanja:**
- Administrator je prijavljen u sistem.
- Postoji barem jedan transkript unesen u sistem (US-18).
- Status obrade se ažurira u realnom vremenu.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-18 (Upload transkripata) i US-23 (Pipeline obrade).

**Acceptance criteria:**
- Sistem mora prikazati tabelu transkripata s kolonama: naziv fajla, datum uploada, veličina, status obrade.
- Status obrade mora imati jasne oznake: Na čekanju / U obradi / Obrađen / Greška.
- Administrator mora moći filtrirati transkripte po statusu i sortirati po datumu.
- Administrator mora moći pregledati detalje greške za transkripte s neuspješnom obradom.
- Sistem ne smije prikazati nemaskirane osjetljive podatke u tabeli.
- Sistem mora prikazati ukupan broj transkripata i distribuciju po statusima.
- Sistem mora prikazati poruku ukoliko nema unesenih transkripata.

### US-34. Pregled postavljenih pitanja i odgovora

**Backlog referenca:** Backlog #34 – Pregled postavljenih pitanja i odgovora  
**Tip:** Feature  
**Prioritet:** High  
**Status:** Not Started

**Opis:**
Kao administrator, želim da vidim sve interakcije korisnika s chatbotom uključujući pitanja, odgovore i ocjene, kako bih mogao analizirati kvalitet chatbota i donositi odluke o poboljšanjima.

**Poslovne vrijednosti:**
Uvid u stvarne konverzacije omogućava data-driven poboljšanje chatbota i identifikaciju sistematskih slabosti modela.

**Pretpostavke i otvorena pitanja:**
- Administrator je prijavljen u sistem.
- Sistem čuva logove svih interakcija (NFR-11).
- Lični podaci korisnika su maskirani u logovima.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-22 (Chat UI), US-15 (Ocjena odgovora), US-27 (Baza znanja).

**Acceptance criteria:**
- Sistem mora prikazati listu konverzacija s: datumom, pitanjem korisnika, odgovorom chatbota i ocjenom (ako postoji).
- Administrator mora moći pretraživati konverzacije po sadržaju i filtrirati po datumu ili ocjeni.
- Sistem ne smije prikazati lične podatke korisnika koji su maskirani u procesu obrade.
- Administrator mora moći vidjeti izvor odgovora (koji dio transkripta je korišten za odgovor).
- Sistem mora prikazati ukupne statistike: broj konverzacija, prosječna ocjena, postotak negativnih ocjena.
- Sistem mora prikazati poruku ukoliko nema evidentiranih konverzacija.

### US-35. Pregled prijavljenih problema

**Backlog referenca:** Backlog #35 – Pregled prijavljenih problema  
**Tip:** Feature  
**Prioritet:** Medium  
**Status:** Not Started  

**Opis:**
Kao administrator, želim da vidim listu svih odgovora koje su korisnici ili agenti prijavili kao netačne, kako bi ih mogao pregledati, obraditi i koristiti za poboljšanje chatbota.

**Poslovne vrijednosti:**
Pregled svih prijava zatvara feedback petlju između korisnika/agenta i sistema za treniranje, što je ključno za dugoročno unapređenje tačnosti modela.

**Pretpostavke i otvorena pitanja:**
- Administrator je prijavljen u sistem.
- Postoje prijavljene greške od korisnika (US-15) ili agenta (US-28).
- Prijave se ažuriraju u realnom vremenu.

**Veza sa drugim storijima ili zavisnostima:**
- Zavisi od US-15 (Ocjena korisnika) i US-28 (Prijava agenta).
- Veza s US-32 (Potvrda i obrada netačnog odgovora).

**Acceptance criteria:**
- Sistem mora prikazati tabelu prijavljenih problema sa: pitanjem, odgovorom chatbota, ocjenom, komentarom, datumom i statusom obrade.
- Administrator mora moći filtrirati prijave po statusu: Novo / U obradi / Riješeno.
- Administrator mora moći sortirati prijave po datumu ili tipu izvora (korisnik / agent).
- Sistem mora prikazati ukupan broj neriješenih prijava
- Sistem ne smije dozvoliti trajno brisanje prijave bez potvrde.
- Sistem mora prikazati poruku ukoliko nema aktivnih prijava.


