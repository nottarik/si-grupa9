# Risk Registar – Sistem za treniranje i implementaciju AI chatbot asistenta

**Projekt:** Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu poziva iz call centra  
---

## Risk Registar

### GRUPA 1 – Rizici podataka

---

#### RIZ-001 – Loša kvaliteta audio snimaka / transkripata

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-001 |
| **Opis rizika** | Snimljeni pozivi iz call centra mogu biti lošeg audiokvaliteta (šum, preklapanje govora, dijalekt, loša veza) ili transkripti mogu sadržavati greške transkripcije, što direktno narušava korisnost podataka za izgradnju baze znanja. |
| **Uzrok** | Stara oprema za snimanje, varijabilni uvjeti poziva, automatska transkripcija bez manualnih korekcija, različiti jezički registri agenata. |
| **Vjerovatnoća** | V |
| **Uticaj** | V |
| **Prioritet rizika** | Kritičan |
| **Plan mitigacije** | Uspostaviti pipeline za procjenu kvaliteta podataka (confidence score transkripcije, dužina poziva, omjer tišine). Definisati minimalne kriterije prihvatljivosti za svaki zapis. Implementirati manualni review uzorak za validaciju. Loši zapisi se označavaju i isključuju iz trening seta. |
| **Odgovorna osoba / uloga** | Data Engineer / ML inženjer |
| **Status** | Identificiran |

---

#### RIZ-002 – Nedovoljno podataka za izgradnju reprezentativne baze znanja

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-002 |
| **Opis rizika** | Dostupan skup poziva možda ne pokriva dovoljan broj kategorija pitanja ili ne sadrži dovoljno primjera po kategoriji, što rezultira chatbotom koji ne može odgovoriti na veliki dio korisničkih upita. |
| **Uzrok** | Ograničen period snimanja, sezonska distribucija poziva, fokus snimaka na određene produkte ili usluge. |
| **Vjerovatnoća** | S |
| **Uticaj** | V |
| **Prioritet rizika** | Kritičan |
| **Plan mitigacije** | Provesti analizu distribucije tema u ranoj fazi (Sprint 3). Definisati minimalni prag pokrivenih kategorija za MVP. Ako je skup mali, koristiti data augmentation ili ručno kreiranje Q&A parova od strane agenata. Transparentno komunikovati opseg chatbota krajnjim korisnicima. |
| **Odgovorna osoba / uloga** | Product Owner / Data Engineer |
| **Status** | Identificiran |

---

#### RIZ-003 – Prisustvo osjetljivih ličnih podataka u snimcima

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-003 |
| **Opis rizika** | Pozivi iz call centra mogu sadržavati lične podatke korisnika (JMBG, broj računa, adresa, zdravstveni podaci i sl.) koji podliježu zakonima o zaštiti privatnosti (GDPR, lokalni propisi BiH). Obrada ovih podataka bez adekvatnih mjera može dovesti do pravnih sankcija i gubitka povjerenja. |
| **Uzrok** | Priroda razgovora u call centru, nedostatak automatske anonimizacije u toku snimanja. |
| **Vjerovatnoća** | V |
| **Uticaj** | V |
| **Prioritet rizika** | Kritičan |
| **Plan mitigacije** | Implementirati automatski PII detection i redaction modul (regex + NER model) kao obavezni korak u pipeline-u prije bilo kakve obrade. Nikad ne čuvati originalne transkripte s PII podacima na produkcijskom serveru. Pribaviti pravno mišljenje o usklađenosti. Definisati Data Governance politiku. |
| **Odgovorna osoba / uloga** | Security / Compliance Officer / Tech Lead |
| **Status** | Identificiran |

---

#### RIZ-004 – Zastarijevanje baze znanja

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-004 |
| **Opis rizika** | Sadržaj u bazi znanja (politike, procedure, cijene, proizvodi) može zastarjeti ako ne postoji mehanizam redovnog ažuriranja. Chatbot bi tada davao netačne ili zastarjele odgovore korisnicima. |
| **Uzrok** | Promjene poslovnih politika, novih proizvoda/usluga, nedostatak procesa za ažuriranje znanja. |
| **Vjerovatnoća** | S |
| **Uticaj** | V |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Dizajnirati administrativni interfejs koji omogućava ažuriranje, dodavanje i povlačenje sadržaja iz baze znanja. Definisati SLA za pregled i ažuriranje sadržaja (npr. kvartalno). Implementirati verzioniranje baze znanja s audit logom. |
| **Odgovorna osoba / uloga** | Administrator sistema / Product Owner |
| **Status** | Identificiran |

---

#### RIZ-005 – Bias u podacima – pristranost agenata ili specifičnih perioda

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-005 |
| **Opis rizika** | Ako su pozivi prikupljeni samo od određenih agenata, u određenom periodu ili za određenu grupu korisnika, chatbot može razviti pristranosti koje ne odražavaju stvarne potrebe svih korisnika. |
| **Uzrok** | Selektivno snimanje, sezonske varijacije, razlike u stilu komunikacije između agenata. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Analizirati demografsku i vremensku distribuciju skupa podataka. Nastojati prikupiti reprezentativan uzorak iz različitih perioda i od različitih agenata. Redovno evaluirati odgovore chatbota na raznovrsnom test setu. |
| **Odgovorna osoba / uloga** | Data Engineer / QA |
| **Status** | Identificiran |

---

### GRUPA 2 – Tehnički rizici

---

#### RIZ-006 – Halucinacije i netačni odgovori AI modela

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-006 |
| **Opis rizika** | Upotrebljeni LLM / retrieval mehanizam može generisati odgovore koji zvuče uvjerljivo ali su faktički netačni, naročito za upite koji nisu dobro pokriveni bazom znanja. Korisnici mogu donijeti pogrešne odluke na osnovu takvih odgovora. |
| **Uzrok** | Inherentna priroda generativnih modela, slaba pokrivenost teme u bazi znanja, slabi retrieval mehanizam koji vraća irelevantne kontekste. |
| **Vjerovatnoća** | V |
| **Uticaj** | V |
| **Prioritet rizika** | Kritičan |
| **Plan mitigacije** | Implementirati RAG (Retrieval-Augmented Generation) pristup koji ograničava odgovore na sadržaj baze znanja. Dodati confidence threshold – ako sistem nije dovoljno siguran, korisnika uputiti na agenta. Prikazivati izvor odgovora (transparentnost). Implementirati feedback mehanizam za označavanje netačnih odgovora. |
| **Odgovorna osoba / uloga** | ML inženjer / Tech Lead |
| **Status** | Identificiran |

---

#### RIZ-007 – Loše performanse retrieval sistema pri velikom broju upita

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-007 |
| **Opis rizika** | Retrieval mehanizam (vektorska pretraga, BM25 ili hibridni pristup) može imati visoku latenciju ili biti nepouzdan pod opterećenjem, što degradira korisničko iskustvo. |
| **Uzrok** | Neoptimizovana vektorska baza podataka, neadekvatna infrastruktura, veliki embedding prostor. |
| **Vjerovatnoća** | N |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Odabrati odgovarajuću vektorsku bazu (npr. FAISS, Chroma, Qdrant) prilagođenu veličini podataka. Definisati NFR zahtjev za latenciju (npr. < 2s po upitu). Provesti load testing prije puštanja u produkciju. Implementirati caching za česte upite. |
| **Odgovorna osoba / uloga** | Backend Developer / DevOps |
| **Status** | Identificiran |

---

#### RIZ-008 – Prekid ili promjena API servisa eksternog modela

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-008 |
| **Opis rizika** | Ukoliko projekt koristi eksterni AI servis (npr. OpenAI, Anthropic, Azure OpenAI), promjena uslova korištenja, rast cijena, nedostupnost servisa ili gašenje API-ja mogu ugroziti funkcionisanje sistema. |
| **Uzrok** | Zavisnost o eksternom provideru, nedostatak fallback rješenja. |
| **Vjerovatnoća** | N |
| **Uticaj** | V |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Dizajnirati abstraction layer koji olakšava zamjenu modela. Dokumentovati alternativne provajdere. Pratiti promjene uslova eksternih servisa. Razmotriti open-source alternativu (npr. Llama, Mistral) kao fallback. Definisati SLA monitoring za dostupnost eksternog servisa. |
| **Odgovorna osoba / uloga** | Tech Lead / Arhitekt sistema |
| **Status** | Identificiran |

---

#### RIZ-009 – Sigurnosne ranjivosti (prompt injection, neovlašteni pristup)

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-009 |
| **Opis rizika** | Zlonamjerni korisnici mogu pokušati manipulisati chatbot putem prompt injection napada, izvući osjetljive informacije iz baze znanja ili dobiti neovlašteni pristup administrativnom interfejsu. |
| **Uzrok** | Nedostatak input validacije, neadekvatna autentifikacija za admin panel, javno dostupan chatbot bez ograničenja. |
| **Vjerovatnoća** | S |
| **Uticaj** | V |
| **Prioritet rizika** | Kritičan |
| **Plan mitigacije** | Implementirati input sanitizaciju i ograničenje karaktera na chatbot interfejsu. Koristiti system prompt hardening za sprečavanje prompt injection-a. Implementirati autentifikaciju i autorizaciju za admin panel. Redovne security review sesije. Logovati sve interakcije radi forenzike. |
| **Odgovorna osoba / uloga** | Security Engineer / Tech Lead |
| **Status** | Identificiran |

---

#### RIZ-010 – Problemi s integracijom audio-to-text pipeline-a

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-010 |
| **Opis rizika** | Ukoliko se koriste audio snimci umjesto gotovih transkripata, automatska transkripcija (ASR) može imati visoku stopu greške za lokalne dijalekte, šum u pozadini ili specifičnu terminologiju. |
| **Uzrok** | Modeli za transkripciju obučeni na standardnom jeziku slabije rade na lokalnim govorima; tehnički termini ili interni žargon call centra nisu u vokabularu modela. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Testirati više ASR rješenja (Whisper, Google STT, Azure STT) na uzorku lokalnih poziva i odabrati ono s najboljim WER. Implementirati post-processing korak za korekciju specifičnih termina. Razmotriti manualno kreiranje transkripata za ključne primjere. |
| **Odgovorna osoba / uloga** | ML inženjer / Data Engineer |
| **Status** | Identificiran |

---

#### RIZ-011 – Skalabilnost sistema pri rastu baze znanja

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-011 |
| **Opis rizika** | Kako baza znanja raste (veći broj dokumenata, kategorija, embedding vektora), sistem može postati sporiji ili manje precizan u retrieval-u bez pravovremene optimizacije arhitekture. |
| **Uzrok** | Inicijalni dizajn prilagođen MVP obimu koji nije skalabilan, neadekvatno indeksiranje. |
| **Vjerovatnoća** | N |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Definisati arhitekturu s horizontalnom skalabilnošću od početka. Koristiti vektorsku bazu s podrškom za inkrementalno dodavanje vektora. Testirati performanse na projektovanoj veličini podataka, ne samo MVP obimu. |
| **Odgovorna osoba / uloga** | Arhitekt sistema / Backend Developer |
| **Status** | Identificiran |

---

#### RIZ-026 – Namjerno ubacivanje zlonamjernih podataka u bazu znanja (Data Poisoning)

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-026 |
| **Opis rizika** | Zlonamjerni akter (interni ili eksterni) može namjerno ubaciti lažne, pristrasne ili štetne sadržaje u bazu znanja – putem kompromitovanog admin panela, lažnih transkripata u pipeline-u ili direktne manipulacije vektorskom bazom. Chatbot bi tada počeo davati sistematski pogrešne ili štetne odgovore korisnicima, a napad može dugo proći neopaženo. |
| **Uzrok** | Nedovoljna kontrola pristupa admin interfejsu, odsutnost validacije i sanity check-a za nove unose, nedostatak detekcije anomalija pri unosu sadržaja, povjerenje u interne aktere bez verifikacije. |
| **Vjerovatnoća** | N |
| **Uticaj** | V |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Implementirati strogi RBAC (Role-Based Access Control) za sve operacije pisanja u bazu znanja uz obavezan audit log. Svaki novi unos prolazi kroz review workflow (četiri-oka princip) prije aktivacije u produkciji. Implementirati anomaly detection koji upozorava na neobično velike ili tematski devijantne unose. Redovito provoditi integrity check uspoređivanjem hasha sadržaja baze s referentnim snimkom. Definisati rollback proceduru za vraćanje baze na prethodno stanje. |
| **Odgovorna osoba / uloga** | Security Engineer / Administrator sistema |
| **Status** | Identificiran |

---

#### RIZ-028 – Neovlašteno izbacivanje internih podataka putem chatbota (RAG leakage)

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-028 |
| **Opis rizika** | Napadač može putem pažljivo konstruisanih upita (prompt injection) navesti LLM da otkrije interne sadržaje iz baze znanja koji nisu namijenjeni javnom pristupu – npr. interne procedure, povjerljive cijene, informacije o korisnicima ili poslovni procesi koji su ušli u bazu kao dio transkripata. Ovo je drugačije od SQL injectiona: napadač ne napada bazu podataka direktno, nego manipuliše LLM-om da iz legitimno preuzetog konteksta izvuče i vrati podatke na način koji zaobilazi namjeravana ograničenja. |
| **Uzrok** | Nedovoljna granularnost pristupa sadržaju baze znanja (svi sadržaji dostupni svim korisnicima), odsustvo output filteringa koji prepoznaje strukturu internih dokumenata, retrieval koji vraća previše sirovog izvornog sadržaja LLM-u kao kontekst. |
| **Vjerovatnoća** | S |
| **Uticaj** | V |
| **Prioritet rizika** | Kritičan |
| **Plan mitigacije** | Klasificirati sadržaj baze znanja po razini osjetljivosti i implementirati access control na razini segmenata (javni / interni / povjerljivi). Chatbot korisniku nikad ne prikazuje sirove izvorne dokumente – isključivo sintetizovani odgovor. Implementirati output monitoring koji detektuje pokušaje ekstrakcije strukturiranih podataka. Provesti red team testiranje usmjereno na eksfiltraciju prije puštanja u produkciju. |
| **Odgovorna osoba / uloga** | Security Engineer / Tech Lead |
| **Status** | Identificiran |

---

#### RIZ-030 – Ovisnost o jednoj kritičnoj komponenti u RAG arhitekturi (Single Point of Failure)

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-030 |
| **Opis rizika** | RAG pipeline se sastoji od više zasebnih komponenti koje rade u nizu: embedding model pretvara upit u vektor → vektorska baza pretražuje relevantne dokumente → LLM generiše odgovor na osnovu pronađenog konteksta. Ako ijedna od ovih komponenti zakaže, cijeli pipeline prestaje funkcionisati jer svaka komponenta ovisi o izlazu prethodne. Sistem ne može preskočiti pokvarenu kariku niti se djelimično degradirati – chatbot je u potpunosti van funkcije dok se problem ne riješi, bez ikakvog fallbacka za korisnika. |
| **Uzrok** | Arhitekturalne odluke u ranoj fazi fokusirane na brzinu isporuke MVP-a nauštrb redundancije, izostanak definisanog fallback scenarija za svaki kritični element u lancu. |
| **Vjerovatnoća** | N |
| **Uticaj** | V |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Mapirati sve kritične komponente u arhitekturalnom dijagramu i za svaku definisati fallback strategiju. Implementirati circuit breaker pattern između komponenti kako bi kvar jedne bio izolovan i ne bi rušio ostatak sistema. Za MVP je prihvatljivo prikazati statički FAQ korisnicima ako vektorska baza nije dostupna. U kasnijim fazama razmotriti replikaciju kritičnih komponenti. Pratiti health check svake komponente odvojeno, a ne samo krajnjeg korisničkog endpointa. |
| **Odgovorna osoba / uloga** | Arhitekt sistema / DevOps |
| **Status** | Identificiran |

---

### GRUPA 3 – Projektni i organizacioni rizici

---

#### RIZ-012 – Scope creep – nekontrolisano proširivanje opsega

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-012 |
| **Opis rizika** | Stakeholderi ili tim mogu tokom semestra početi dodavati zahtjeve (višejezičnost, voice interface, CRM integracija i sl.) koji nisu dio definisanog MVP opsega, što može ugroziti isporuku temeljnih funkcionalnosti. |
| **Uzrok** | Nejasnо definisan MVP, entuzijazam tima, pritisak menadžmenta za dodatnim funkcijama. |
| **Vjerovatnoća** | V |
| **Uticaj** | S |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Jasno definisati i zaključati MVP opseg u Product Backlogu. Svaki novi zahtjev prolazi kroz formalni change request proces i ocjenu uticaja. Product Owner ima pravo veta na dodavanje u tekući sprint. Pratiti velocity i kapacitet tima. |
| **Odgovorna osoba / uloga** | Product Owner / Scrum Master |
| **Status** | Identificiran |

---

#### RIZ-013 – Nedovoljno angažovanje ili nedostupnost stakeholdera

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-013 |
| **Opis rizika** | Call centar agenti, menadžment ili IT odjel mogu biti nedovoljno angažovani u procesu pružanja povratnih informacija, validacije odgovora chatbota ili pružanja pristupa podacima, što usporava razvoj. |
| **Uzrok** | Operativne obaveze stakeholdera, nedovoljna komunikacija, nerazumijevanje vrijednosti projekta. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Uspostaviti redovne (sedmične) sync sesije sa stakeholderima. Kreirati jasan RACI model odgovornosti. Pripremiti kratke prezentacije vrijednosti sistema za motivaciju. Identificovati i ojačati vezu s "champion" osobom unutar call centra. |
| **Odgovorna osoba / uloga** | Product Owner / Project Manager |
| **Status** | Identificiran |

---

#### RIZ-014 – Nedostatak tehničkih kompetencija u timu

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-014 |
| **Opis rizika** | Tim može nemati dovoljno iskustva s NLP/LLM tehnologijama, vektorskim bazama podataka, RAG arhitekturama ili pipeline-ima za obradu podataka, što može dovesti do tehničkih grešaka ili kašnjenja. |
| **Uzrok** | Akademski kontekst projekta, ograničeno prethodno iskustvo s AI sistemima. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Provesti knowledge gap analizu na početku projekta. Organizovati interni tech spike (istraživačke iteracije) za nepoznate tehnologije. Koristiti dobro dokumentovane open-source alate i managed servise koji smanjuju kompleksnost. Razmotriti mentorstvo ili peer learning sesije. |
| **Odgovorna osoba / uloga** | Tech Lead / Scrum Master |
| **Status** | Identificiran |

---

#### RIZ-015 – Kašnjenje zbog zavisnosti o eksternim resursima ili odobrenjima

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-015 |
| **Opis rizika** | Pristup snimcima poziva, serverima, API ključevima ili odobrenjem pravnog/compliance odjela može biti spor, što blokira kritične razvojne aktivnosti. |
| **Uzrok** | Birokratski procesi, sigurnosne politike organizacije, nedostatak prethodno dogovorenih procedura pristupa. |
| **Vjerovatnoća** | S |
| **Uticaj** | V |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Identifikovati sve potrebne dozvole i pristupe na početku projekta (Sprint 1-2). Inicirati zahtjeve za pristup što ranije. Pripremiti alternativni sintetički ili javno dostupni dataset za razvoj dok se čeka pristup pravim podacima. |
| **Odgovorna osoba / uloga** | Project Manager / Product Owner |
| **Status** | Identificiran |

---

#### RIZ-016 – Fluktuacija članova tima

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-016 |
| **Opis rizika** | Napuštanje projekta od strane jednog ili više članova tima (zbog akademskih obaveza, zdravlja ili drugih razloga) može ugroziti kontinuitet razvoja i znanje o sistemu. |
| **Uzrok** | Akademski kontekst, konkurentske obaveze studenata. |
| **Vjerovatnoća** | N |
| **Uticaj** | S |
| **Prioritet rizika** | Nizak |
| **Plan mitigacije** | Redovito dokumentovati sve odluke, arhitekturne izbore i kodove (README, ADR). Implementirati code review praksu kako bi više članova razumjelo svaki dio sistema. Definisati jasne uloge ali i plan za zamjenu / redistribuciju zadataka. |
| **Odgovorna osoba / uloga** | Scrum Master / Team Lead |
| **Status** | Identificiran |

---

#### RIZ-027 – Neuočljive greške u kodu generisanom AI coding alatima

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-027 |
| **Opis rizika** | AI coding asistenti (npr. GitHub Copilot, Claude, Cursor) koji se koriste za razvoj web aplikacije mogu generisati kod koji se kompajlira, prolazi surface-level testove i izgleda ispravno, ali sadrži suptilne logičke greške, sigurnosne propuste ili rubne slučajeve koje developer nije uočio pri pregledu. Rizik je posebno visok jer tim tendencijski manje kritički čita AI-generisani kod nego vlastito pisani. |
| **Uzrok** | Preveliko povjerenje u AI alate bez sistematskog code reviewa, nedostatak iskustva tima u prepoznavanju karakterističnih grešaka AI-generisanog koda (npr. pogrešna pretpostavka o null safety, race conditions, off-by-one greške u paginaciji, nepotpuna error handling logika). AI modeli su trenirani na javnom kodu koji često sadrži loše prakse, te mogu reproducirati antipatterne koji nisu odmah vidljivi. |
| **Vjerovatnoća** | V |
| **Uticaj** | S |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Uspostaviti obavezan peer code review za sav AI-generisani kod, s posebnom pažnjom na: autentifikacijsku logiku, validaciju inputa, upravljanje sesijama i error handling. Koristiti statičke analizatore i lintere koji ne ovise o AI (npr. ESLint, Bandit, SonarQube) kao obavezan korak u CI/CD pipeline-u. Pisati unit i integration testove koji eksplicitno pokrivaju rubne slučajeve i ne koristiti AI za generisanje samih testova za isti kod koji se testira. Dokumentovati sve dijelove koda gdje je AI imao veći doprinos kako bi bili pod pojačanim nadzorom. |
| **Odgovorna osoba / uloga** | Tech Lead / QA Engineer |
| **Status** | Identificiran |

---

### GRUPA 4 – Rizici korisničkog iskustva i adopcije

---

#### RIZ-017 – Niska adopcija chatbota od strane krajnjih korisnika

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-017 |
| **Opis rizika** | Korisnici mogu preferirati direktan kontakt s agentom i ignorisati chatbot, čime se ne ostvaruje cilj rasterećenja call centra. |
| **Uzrok** | Loše korisničko iskustvo, nepovjerenje u AI, neadekvatni odgovori chatbota, loš UX dizajn interfejsa. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Provesti UX istraživanje i testiranje s realnim korisnicima tokom razvoja. Osigurati brzu i jasnu eskalaciju na agenta kada chatbot ne zna odgovor. Implementirati feedback mehanizam. Pratiti metrike adopcije (broj sesija, completion rate, handoff rate). |
| **Odgovorna osoba / uloga** | UX Designer / Product Owner |
| **Status** | Identificiran |

---

#### RIZ-018 – Otpor call centar agenata prema implementaciji sistema

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-018 |
| **Opis rizika** | Call centar agenti mogu doživjeti chatbot kao prijetnju njihovim radnim mjestima i aktivno ili pasivno sabotirati projekt (odbijanje pružanja feedback-a, minimalan doprinos validaciji sadržaja). |
| **Uzrok** | Strah od automatizacije, nedovoljna komunikacija o svrsi sistema, nedostatak uključenosti agenata u dizajn. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Jasno komunicirati da chatbot služi kao podrška agentima (smanjivanje repetitivnih poziva), ne kao zamjena. Uključiti agente kao aktivne saradnike u kreiranje i validaciju sadržaja baze znanja. Prezentovati im benefite (fokus na kompleksnije pozive). |
| **Odgovorna osoba / uloga** | Product Owner / Menadžment |
| **Status** | Identificiran |

---

#### RIZ-019 – Neadekvatno upravljanje situacijom kada chatbot "ne zna" odgovor

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-019 |
| **Opis rizika** | Ako sistem nema jasno definisan fallback mehanizam za pitanja izvan baze znanja, korisnici mogu dobiti generičke, zbunjujuće ili pogrešne odgovore, što narušava povjerenje u sistem. |
| **Uzrok** | Neimplementiran threshold za konfidencnost odgovora, nedostatak graceful degradation dizajna. |
| **Vjerovatnoća** | S |
| **Uticaj** | V |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Definisati i implementirati "I don't know" response pattern s jasnom porukom i opcijom eskalacije na agenta ili FAQ stranicu. Testirati sistem s out-of-scope upitima. Logirati sve "nisam siguran" situacije za kasniju analizu i dopunu baze znanja. |
| **Odgovorna osoba / uloga** | ML inženjer / UX Designer |
| **Status** | Identificiran |

---

#### RIZ-031 – Neintuitivan korisnički interfejs chatbota

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-031 |
| **Opis rizika** | Korisnički interfejs chatbota može biti dizajniran na način koji zbunjuje korisnike – nejasno gdje se unosi poruka, nepregledan prikaz historije razgovora, nejasne opcije za eskalaciju na agenta, ili interfejs koji ne odgovara očekivanjima korisnika naviklih na druge kanale (telefon, e-mail). Rezultat je odustajanje korisnika prije nego dobiju odgovor, povećanje broja poziva u call centar umjesto smanjenja, i negativna percepcija sistema. |
| **Uzrok** | Izostanak UX istraživanja s realnim korisnicima u ranoj fazi, razvoj interfejsa od strane tehničkog tima bez uključivanja dizajnera, pretpostavke o korisničkom ponašanju koje nisu validirane, prenošenje kompleksnosti backend sistema na frontend. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Provesti korisničko istraživanje (intervjui ili anketa) s reprezentativnim uzorkom krajnjih korisnika prije početka razvoja interfejsa. Kreirati i testirati wireframeove s najmanje 5 korisnika prije implementacije. Implementirati usability testiranje na kraju svakog sprinta koji uključuje UI promjene. Pratiti metrike poput abandon rate (odustajanje bez odgovora) i broj klikova do eskalacije na agenta kao indikatore UX problema. |
| **Odgovorna osoba / uloga** | UX Designer / Product Owner |
| **Status** | Identificiran |

---

### GRUPA 5 – Rizici usklađenosti i etike

---

#### RIZ-020 – Kršenje propisa o zaštiti podataka (GDPR / lokalno pravo)

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-020 |
| **Opis rizika** | Nedovoljna anonimizacija podataka, neovlaštena obrada ličnih podataka ili pohranjivanje osjetljivih informacija bez adekvatnih mjera zaštite može dovesti do kršenja GDPR-a i lokalnog Zakona o zaštiti ličnih podataka BiH. |
| **Uzrok** | Nedostatak privacy-by-design pristupa, propusti u anonimizaciji, nedefinisana politika retencije podataka. |
| **Vjerovatnoća** | S |
| **Uticaj** | V |
| **Prioritet rizika** | Kritičan |
| **Plan mitigacije** | Angažovati pravnog savjetnika ili DPO (Data Protection Officer) u fazi dizajna. Implementirati privacy-by-design principe. Definisati Data Retention Policy. Provesti Data Protection Impact Assessment (DPIA). Sve obrade podataka dokumentovati u registru obrada. |
| **Odgovorna osoba / uloga** | Compliance Officer / Tech Lead |
| **Status** | Identificiran |

---

#### RIZ-021 – Diskriminatorni ili uvredljivi odgovori chatbota

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-021 |
| **Opis rizika** | Chatbot može generisati odgovore koji su diskriminatorni, uvredljivi ili neprikladno personalizovani na osnovu biasa u podacima iz poziva (npr. različit tretman korisnika po demografskim karakteristikama). |
| **Uzrok** | Bias u trening podacima, nedostatak filtarskog sloja za output. |
| **Vjerovatnoća** | N |
| **Uticaj** | V |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Implementirati output filtering layer koji detektuje potencijalno uvredljiv sadržaj. Provesti bias audit nad skupom podataka i odgovorima chatbota. Definisati feedback mehanizam za prijavljivanje problematičnih odgovora. Redovito evaluirati odgovore s raznolikim test setom. |
| **Odgovorna osoba / uloga** | ML inženjer / Ethics Lead |
| **Status** | Identificiran |

---

#### RIZ-022 – Nedovoljna auditabilnost i transparentnost sistema

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-022 |
| **Opis rizika** | Bez adekvatnog logiranja interakcija, promjena u bazi znanja i administrativnih akcija, nije moguće revidirati greške, razumjeti zašto je chatbot dao određeni odgovor ili pratiti ko je napravio kakvu izmjenu. |
| **Uzrok** | Nedostatak audit log infrastrukture, nebrinutost o observability-u u ranoj fazi. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Implementirati centralizovani logging sistem od početka (sve korisničke interakcije, admin akcije, promjene baze znanja). Verzionirati bazu znanja. Kreirati administrativni dashboard s historijom promjena. Definisati politiku retencije logova. |
| **Odgovorna osoba / uloga** | Tech Lead / DevOps |
| **Status** | Identificiran |

---

### GRUPA 6 – Operativni rizici

---

#### RIZ-023 – Nedostupnost sistema (uptime i reliability)

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-023 |
| **Opis rizika** | Sistem može biti nedostupan uslijed pada servera, grešaka u deploymentu ili problema s eksternim servisima, što korisnicima onemogućuje pristup chatbotu upravo kada im je potreban. |
| **Uzrok** | Neadekvatna infrastruktura, nedostatak redundancije, greške u CI/CD pipeline-u. |
| **Vjerovatnoća** | N |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Definisati NFR zahtjev za dostupnost (npr. 99% uptime u radnom vremenu). Implementirati health check endpoint i monitoring. Definisati incident response proceduru. Koristiti cloud hosting s managed availability garancijama. Implementirati graceful degradation (ako AI servis pada, prikaži statičke FAQ). |
| **Odgovorna osoba / uloga** | DevOps / Tech Lead |
| **Status** | Identificiran |

---

#### RIZ-024 – Prekoračenje budžeta za cloud i AI API troškove

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-024 |
| **Opis rizika** | Troškovi korištenja eksternih AI API-ja (token-based pricing), cloud infrastrukture i vektorskih baza mogu premašiti planirani budžet, naročito pri rastu broja korisnika ili netačno procijenjenoj potrošnji tokena. |
| **Uzrok** | Nedovoljno precizna inicijalna procjena troškova, neočekivani rast korištenja, skupi modeli s visokim token troškovima. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Srednji |
| **Plan mitigacije** | Definisati budžetski limit i alert za cloud troškove. Implementirati caching odgovora za česte upite. Odabrati cost-efficient modele za retrieval i generisanje. Pratiti token consumption u realnom vremenu. Razmotriti open-source/self-hosted alternativu ako troškovi rastu. |
| **Odgovorna osoba / uloga** | Tech Lead / Project Manager |
| **Status** | Identificiran |

---

#### RIZ-025 – Neadekvatno testiranje i nedostatak QA procesa

| Atribut | Vrijednost |
|---------|------------|
| **ID** | RIZ-025 |
| **Opis rizika** | Bez sistematskog testiranja chatbota (unit, integration, end-to-end i evaluacijski testovi odgovora), greške mogu proći u produkciju, narušavajući pouzdanost sistema i povjerenje korisnika. |
| **Uzrok** | Pritisak rokova, nedostatak iskustva s evaluacijom NLP sistema, zanemarivanje QA u korist brzog razvoja funkcionalnosti. |
| **Vjerovatnoća** | S |
| **Uticaj** | S |
| **Prioritet rizika** | Visok |
| **Plan mitigacije** | Definisati test plan s minimalnim setom test slučajeva za svaki sprint. Kreirati "golden test set" – skup referentnih pitanja i očekivanih odgovora za regresijsko testiranje. Implementirati automatizovane evaluacijske metrike (precision, recall, BLEU/ROUGE za generisane odgovore). Uključiti UAT sesije s call centar agentima. |
| **Odgovorna osoba / uloga** | QA Engineer / Tech Lead |
| **Status** | Identificiran |

---

## Sažetak rizika

| ID | Naziv rizika | Vjerovatnoća | Uticaj | Prioritet |
|----|-------------|--------------|--------|-----------|
| RIZ-001 | Loša kvaliteta audio snimaka / transkripata | V | V | Kritičan |
| RIZ-002 | Nedovoljno podataka za bazu znanja | S | V | Kritičan |
| RIZ-003 | Osjetljivi lični podaci u snimcima | V | V | Kritičan |
| RIZ-004 | Zastarijevanje baze znanja | S | V | Visok |
| RIZ-005 | Bias u podacima | S | S | Srednji |
| RIZ-006 | Halucinacije i netačni AI odgovori | V | V | Kritičan |
| RIZ-007 | Loše performanse retrieval sistema | N | S | Srednji |
| RIZ-008 | Prekid eksternog AI API servisa | N | V | Visok |
| RIZ-009 | Sigurnosne ranjivosti (prompt injection) | S | V | Kritičan |
| RIZ-010 | Problemi s audio-to-text pipeline-om | S | S | Visok |
| RIZ-011 | Skalabilnost sistema | N | S | Srednji |
| RIZ-012 | Scope creep | V | S | Visok |
| RIZ-013 | Nedostupnost stakeholdera | S | S | Srednji |
| RIZ-014 | Nedostatak tehničkih kompetencija | S | S | Srednji |
| RIZ-015 | Kašnjenja zbog eksternih odobrenja | S | V | Visok |
| RIZ-016 | Fluktuacija članova tima | N | S | Srednji |
| RIZ-017 | Niska adopcija korisnika | S | S | Srednji |
| RIZ-018 | Otpor call centar agenata | S | S | Srednji |
| RIZ-019 | Loš fallback mehanizam | S | V | Visok |
| RIZ-020 | Kršenje propisa o zaštiti podataka | S | V | Kritičan |
| RIZ-021 | Diskriminatorni odgovori chatbota | N | V | Visok |
| RIZ-022 | Nedovoljna auditabilnost | S | S | Srednji |
| RIZ-023 | Nedostupnost sistema (uptime) | N | S | Srednji |
| RIZ-024 | Prekoračenje budžeta za AI/cloud | S | S | Srednji |
| RIZ-025 | Neadekvatno testiranje i QA | S | S | Visok |
| RIZ-026 | Data poisoning – namjerno trovanje baze znanja | N | V | Visok |
| RIZ-027 | Neuočljive greške u AI-generisanom kodu aplikacije | V | S | Visok |
| RIZ-028 | Eksfiltracija internih podataka putem chatbota (RAG leakage) | S | V | Kritičan |
| RIZ-030 | Single point of failure u RAG arhitekturi | N | V | Visok |
| RIZ-031 | Neintuitivan korisnički interfejs chatbota | S | S | Srednji |

---

## Distribucija rizika po prioritetu

| Prioritet | Broj rizika |
|-----------|-------------|
| Kritičan | 7 |
| Visok | 12 |
| Srednji | 10 |
| Nizak | 1 |
| **Ukupno** | **30** |

---
