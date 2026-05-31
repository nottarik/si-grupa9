# AI Usage Log – Claude Code

## AI Usage Log – Zapis 1

**Datum:** 25/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri implementaciji backend autentifikacije korisnika.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten kao pomoć pri implementaciji registracije i prijave korisnika, uključujući validaciju ulaznih podataka, provjeru korisnika u bazi, hashiranje lozinke i generisanje autentifikacijskog tokena.

**Šta je AI predložio ili generisao:**  
- strukturu backend ruta za registraciju i prijavu korisnika
- logiku za provjeru postojećeg korisnika po email adresi
- način hashiranja lozinke prije spremanja u bazu
- primjer generisanja i vraćanja tokena nakon uspješne prijave
- obradu grešaka za neispravne podatke, pogrešnu lozinku i nepostojećeg korisnika

**Šta je tim prihvatio:**  
- osnovnu logiku registracije i prijave korisnika
- provjeru korisnika prije kreiranja novog naloga
- princip da se lozinke ne čuvaju u plain text obliku
- vraćanje jasnih statusa i poruka greške prema frontend-u

**Šta je tim izmijenio:**  
- validacije su prilagođene pravilima projekta
- nazivi polja su usklađeni sa modelom korisnika u bazi
- format odgovora backend-a je usklađen sa ostatkom API-ja

**Šta je tim odbacio:**  
- generičke dijelove koda koji nisu odgovarali postojećoj strukturi backend-a
- nepotrebne dodatne biblioteke za funkcionalnost koja se mogla implementirati postojećim alatima

**Rizici, problemi ili greške koje su uočene:**  
- autentifikacija zahtijeva dodatnu sigurnosnu provjeru i testiranje
- frontend i backend validacije moraju ostati usklađene
- AI može predložiti funkcionalan kod koji ipak nije dovoljno siguran bez ručne provjere

---

## AI Usage Log – Zapis 2

**Datum:** 25/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri implementaciji frontend formi za registraciju i prijavu korisnika.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri izradi login i register formi na frontend dijelu aplikacije, uključujući validaciju inputa, prikaz grešaka, slanje zahtjeva prema backend-u i obradu odgovora.

**Šta je AI predložio ili generisao:**  
- strukturu login i register komponenti
- validaciju obaveznih polja u formama
- način prikaza grešaka korisniku
- povezivanje forme sa API funkcijama za login i registraciju
- osnovno rukovanje loading stanjem tokom slanja zahtjeva

**Šta je tim prihvatio:**  
- osnovnu strukturu autentifikacijskih formi
- prikaz validacijskih poruka korisniku
- povezivanje formi sa backend endpointima
- loading stanje prilikom slanja podataka

**Šta je tim izmijenio:**  
- vizuelni izgled formi je prilagođen dizajnu aplikacije
- poruke grešaka su prilagođene bosanskom jeziku
- struktura komponenti je usklađena sa postojećim frontend folderima

**Šta je tim odbacio:**  
- prijedloge koji su uvodili prekomplikovan state management
- dodatne UI efekte koji nisu bili potrebni za trenutni sprint

**Rizici, problemi ili greške koje su uočene:**  
- moguće neslaganje između frontend i backend validacijskih pravila
- potrebno je testirati ponašanje forme kod neuspješne prijave i registracije
- greške iz backend-a moraju biti jasno prikazane korisniku

---

## AI Usage Log – Zapis 3

**Datum:** 26/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri povezivanju frontend aplikacije sa backend API rutama.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri povezivanju frontend stranica i komponenti sa backend endpointima za autentifikaciju, chat funkcionalnost, transkripte i bazu znanja.

**Šta je AI predložio ili generisao:**  
- organizaciju API poziva u posebne frontend fajlove
- konfiguraciju HTTP klijenta za komunikaciju sa backend-om
- način slanja login/register zahtjeva
- način slanja pitanja chatbotu
- obradu loading i error stanja na frontend strani

**Šta je tim prihvatio:**  
- izdvajanje API logike iz UI komponenti
- korištenje zasebnih funkcija za pozive prema backend-u
- osnovnu strukturu komunikacije između frontend-a i backend-a
- prikaz grešaka korisniku na frontend strani

**Šta je tim izmijenio:**  
- nazivi API funkcija su prilagođeni postojećoj strukturi projekta
- poruke grešaka su prilagođene korisnicima aplikacije
- način čuvanja tokena i stanja korisnika je usklađen sa ostatkom aplikacije

**Šta je tim odbacio:**  
- rješenja koja su uvodila nepotrebnu dodatnu biblioteku
- prekomplikovan pristup za API sloj koji nije bio potreban za trenutni obim aplikacije

**Rizici, problemi ili greške koje su uočene:**  
- moguća neusklađenost URL ruta između frontend-a i backend-a
- CORS greške mogu spriječiti komunikaciju između aplikacija
- potrebno je testirati ponašanje aplikacije kod neuspješnih API poziva

---

## AI Usage Log – Zapis 4

**Datum:** 27/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri implementaciji obrade transkripata poziva iz call centra.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri implementaciji toka obrade transkripata, uključujući upload transkripta, normalizaciju teksta, izdvajanje segmenata i pripremu podataka za kasnije korištenje u bazi znanja.

**Šta je AI predložio ili generisao:**  
- tok obrade transkripta od uploada do spremanja u sistem
- primjer strukture za spremanje transkripta i njegovih segmenata
- način označavanja segmenata kao pitanje, odgovor ili kontekst
- provjeru statusa obrade transkripta
- povezivanje transkripta sa segmentima i potencijalnim unosima baze znanja

**Šta je tim prihvatio:**  
- osnovni tok obrade transkripta
- ideju da se transkript dijeli na manje segmente
- korištenje statusa obrade radi praćenja procesa
- povezivanje segmenata sa bazom znanja

**Šta je tim izmijenio:**  
- struktura segmenata je prilagođena postojećem modelu baze
- nazivi statusa i tipova segmenata su usklađeni sa projektnim pravilima
- pojedini koraci obrade su pojednostavljeni zbog obima sprinta

**Šta je tim odbacio:**  
- napredne prijedloge za automatsku klasifikaciju koji nisu bili potrebni u ovoj fazi
- dodatne AI funkcionalnosti koje bi povećale kompleksnost implementacije

**Rizici, problemi ili greške koje su uočene:**  
- transkripti mogu sadržavati nejasne, nepotpune ili pogrešno formatirane podatke
- postoji rizik pogrešne segmentacije razgovora
- potreban je dodatni pregled kvaliteta obrađenih segmenata

---

## AI Usage Log – Zapis 5

**Datum:** 27/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri implementaciji baze znanja i pripremi podataka za RAG funkcionalnost.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri implementaciji funkcionalnosti za kreiranje i upravljanje unosima baze znanja koji se koriste kao izvor informacija za chatbot asistenta.

**Šta je AI predložio ili generisao:**  
- strukturu unosa baze znanja sa pitanjem, odgovorom, kategorijom i statusom
- način povezivanja unosa baze znanja sa segmentima transkripta
- logiku za kreiranje, izmjenu i dohvat unosa baze znanja
- prijedlog statusa za odobravanje ili deaktiviranje unosa
- osnovnu validaciju podataka prije spremanja u bazu

**Šta je tim prihvatio:**  
- osnovnu CRUD logiku za unose baze znanja
- povezivanje unosa sa segmentima kao izvorom podataka
- korištenje statusa odobravanja radi kontrole kvaliteta
- validaciju obaveznih polja prije spremanja

**Šta je tim izmijenio:**  
- nazivi atributa su usklađeni sa postojećim modelom baze
- logika statusa je prilagođena potrebama projekta
- dio implementacije je pojednostavljen radi lakšeg testiranja

**Šta je tim odbacio:**  
- kompleksno verzioniranje unosa koje nije bilo potrebno u trenutnoj fazi
- prijedloge koji bi uvodili dodatne tabele mimo dogovorenog modela

**Rizici, problemi ili greške koje su uočene:**  
- nekvalitetni unosi baze znanja mogu negativno uticati na odgovore chatbota
- potrebno je provjeriti da li su svi unosi pravilno povezani sa izvorima
- promjene u strukturi baze znanja mogu uticati na RAG logiku

---

## AI Usage Log – Zapis 6

**Datum:** 28/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri implementaciji RAG logike i generisanju odgovora chatbota.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri implementaciji retrieval-augmented generation pristupa, gdje chatbot koristi relevantne unose iz baze znanja kako bi odgovorio na pitanje agenta call centra.

**Šta je AI predložio ili generisao:**  
- osnovni tok RAG procesa
- način pretrage relevantnih unosa iz baze znanja
- logiku povezivanja korisničkog pitanja sa najrelevantnijim segmentima
- strukturu odgovora chatbota sa skorom pouzdanosti
- fallback odgovor kada sistem nema dovoljno pouzdan kontekst

**Šta je tim prihvatio:**  
- princip retrieval-a prije generisanja odgovora
- vraćanje odgovora zajedno sa informacijom o pouzdanosti
- fallback odgovor za slučajeve niske sigurnosti
- povezivanje odgovora sa izvorom iz baze znanja

**Šta je tim izmijenio:**  
- prag pouzdanosti je prilagođen potrebama projekta
- struktura odgovora je usklađena sa frontend prikazom
- retrieval logika je pojednostavljena radi lakše implementacije i testiranja

**Šta je tim odbacio:**  
- prijedloge koji bi zahtijevali kompleksniju AI infrastrukturu nego što je planirano
- napredne optimizacije retrieval procesa koje nisu bile potrebne u trenutnom sprintu

**Rizici, problemi ili greške koje su uočene:**  
- chatbot može dati netačan odgovor ako retrieval vrati pogrešan kontekst
- potrebno je testirati ponašanje sistema kod pitanja za koja ne postoji odgovor u bazi znanja
- postoji rizik oslanjanja na AI odgovor bez provjere izvora

---

## AI Usage Log – Zapis 7

**Datum:** 28/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri implementaciji korisničkog interfejsa za chat funkcionalnost.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri izradi frontend chat komponente, uključujući unos pitanja, slanje upita backend-u, prikaz odgovora chatbota, historiju poruka u sesiji i osnovno rukovanje greškama.

**Šta je AI predložio ili generisao:**  
- strukturu chat komponente
- način čuvanja poruka u lokalnom stanju komponente
- prikaz korisničkih i chatbot poruka
- loading stanje dok se čeka odgovor backend-a
- osnovni prikaz greške ako odgovor nije uspješno generisan

**Šta je tim prihvatio:**  
- osnovnu strukturu chat interfejsa
- prikaz historije poruka u jednoj sesiji
- loading indikator tokom slanja pitanja
- jednostavan prikaz greške korisniku

**Šta je tim izmijenio:**  
- vizuelni stil komponenti je prilagođen dizajnu projekta
- tekstovi u interfejsu su prilagođeni bosanskom jeziku
- struktura poruka je usklađena sa backend odgovorom

**Šta je tim odbacio:**  
- kompleksnije funkcionalnosti koje nisu bile u scope-u sprinta
- dodatne animacije i UI efekte koji nisu bili neophodni

**Rizici, problemi ili greške koje su uočene:**  
- moguće je da se poruke ne prikažu pravilno ako backend vrati neočekivan format
- potrebno je testirati ponašanje kod praznog pitanja ili prekida konekcije
- korisnički interfejs treba ostati jednostavan i razumljiv za agente call centra

---

## AI Usage Log – Zapis 8

**Datum:** 29/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri pisanju i organizaciji backend testova.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri pisanju testova za backend funkcionalnosti, uključujući autentifikaciju, API rute, obradu transkripata, bazu znanja i chat/RAG tok.

**Šta je AI predložio ili generisao:**  
- prijedloge unit testova za servisnu logiku
- prijedloge integracijskih testova za API rute
- testiranje validacije korisničkih podataka
- testiranje slanja pitanja chatbotu
- testiranje fallback odgovora kod niske pouzdanosti
- smjernice za korištenje odvojenog testnog okruženja

**Šta je tim prihvatio:**  
- testiranje autentifikacije i API ruta
- testiranje osnovnih slučajeva za chat funkcionalnost
- testiranje grešaka i edge case scenarija
- princip da se testiranje ne radi nad produkcionom bazom

**Šta je tim izmijenio:**  
- testovi su prilagođeni trenutno implementiranim funkcionalnostima
- nedovršene funkcionalnosti nisu uključene u obavezne testove
- testni scenariji su pojednostavljeni radi lakšeg održavanja

**Šta je tim odbacio:**  
- testiranje funkcionalnosti koje još nisu implementirane
- previše detaljne testove koji nisu potrebni za trenutni sprint
- prijedloge koji bi zahtijevali dodatnu infrastrukturu izvan scope-a projekta

**Rizici, problemi ili greške koje su uočene:**  
- moguće razlike između testnog i stvarnog okruženja
- potrebno je održavati testove nakon promjena u API rutama
- AI može generisati testove koji prolaze sintaksno, ali ne provjeravaju stvarnu poslovnu logiku

---

## AI Usage Log – Zapis 9

**Datum:** 29/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri podešavanju frontend testnog okruženja i pisanju testova za komponente.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri konfiguraciji frontend testnog okruženja i pisanju testova za glavne komponente aplikacije, posebno login, register i chat komponente.

**Šta je AI predložio ili generisao:**  
- instalaciju i konfiguraciju potrebnih paketa za frontend testiranje
- podešavanje testnog okruženja za React/Vite aplikaciju
- primjere testova za login i register forme
- testiranje prikaza grešaka i loading stanja
- mockovanje API poziva i browser funkcionalnosti

**Šta je tim prihvatio:**  
- konfiguraciju osnovnog testnog okruženja
- testove za autentifikacijske forme
- pristup mockovanju API poziva
- testiranje korisničkog feedback-a u UI komponentama

**Šta je tim izmijenio:**  
- testovi su prilagođeni stvarnoj strukturi komponenti
- uklonjeni su testovi za funkcionalnosti koje još nisu implementirane
- mock podaci su usklađeni sa formatom backend odgovora

**Šta je tim odbacio:**  
- testiranje placeholder komponenti
- testove za nedovršene dijelove aplikacije
- nepotrebno kompleksne testne scenarije koji nisu bili u scope-u sprinta

**Rizici, problemi ili greške koje su uočene:**  
- frontend testovi mogu zavisiti od pravilnog mockovanja API odgovora
- promjene u strukturi komponenti mogu zahtijevati česte izmjene testova
- potrebno je paziti da testovi provjeravaju stvarno ponašanje korisničkog interfejsa, a ne samo renderovanje komponenti

---

## AI Usage Log – Zapis 10

**Datum:** 30/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri unapređenju frontend navigacije i dashboard prikaza podataka.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten kao pomoć pri rješavanju problema navigacije u sidebaru (reset liste transkripata) i unapređenju dashboarda kroz prikaz stvarnih podataka umjesto hardkodiranih vrijednosti.

**Šta je AI predložio ili generisao:**  
- ideju korištenja key/state promjene za forsiranje remounta komponente  
- način resetovanja interne state logike komponente prilikom navigacije  
- prijedlog da se hardkodirani podaci zamijene API pozivima  
- organizaciju dashboard kartica sa dinamičkim podacima  

**Šta je tim prihvatio:**  
- princip da klik na sidebar sekciju resetuje stanje komponente  
- korištenje state promjene (counter) za remount komponente  
- zamjenu hardkodiranih podataka stvarnim API podacima  
- prikaz broja korisnika i transkripata kroz backend pozive  

**Šta je tim izmijenio:**  
- implementacija je prilagođena postojećoj strukturi AdminShell komponente  
- nazivi funkcija i API poziva su usklađeni sa projektom  
- dashboard kartice su vizuelno prilagođene dizajnu aplikacije  

**Šta je tim odbacio:**  
- kompleksnije state management pristupe  
- dodatne statistike koje backend trenutno ne podržava  

**Rizici, problemi ili greške koje su uočene:**  
- forsirani remount može uticati na performanse ako se koristi prečesto  
- dashboard zavisi od dostupnosti backend endpointa  
- placeholder podaci mogu zbuniti korisnika ako nisu jasno označeni  

---

## AI Usage Log – Zapis 11

**Datum:** 30/04/2026  

**Sprint broj:** Sprint 5  

**Alat koji je korišten:** Claude Code  

**Svrha korištenja:**  
Pomoć pri validaciji formata transkripata na backend i frontend strani.

**Kratak opis zadatka ili upita:**  
Claude Code je korišten za pomoć pri implementaciji validacije formata transkripta kako bi se osiguralo da svaki unos sadrži pravilno označene AGENT i KORISNIK linije.

**Šta je AI predložio ili generisao:**  
- validator funkciju za provjeru strukture transkripta  
- način parsiranja linija i provjere prefiksa (AGENT:, KORISNIK:)  
- prikaz validacijskih grešaka na frontend strani  
- sinhronizaciju validacije između backend i frontend dijela  

**Šta je tim prihvatio:**  
- validaciju formata transkripta prije spremanja  
- prikaz greške korisniku u realnom vremenu  
- isti princip validacije na frontend i backend strani  

**Šta je tim izmijenio:**  
- poruke grešaka su prilagođene korisnicima aplikacije  
- validacija je pojednostavljena za trenutni format  

**Šta je tim odbacio:**  
- kompleksnije NLP validacije strukture razgovora  
- automatsko ispravljanje formata transkripta  

**Rizici, problemi ili greške koje su uočene:**  
- korisnici mogu imati validan tekst koji ne prati striktan format  
- potrebno je jasno definisati očekivani format unosa  
- moguće neslaganje između frontend i backend validacije  

---
 ## AI Usage Log – Zapis 12

**Datum:** 30/04/2026

**Sprint broj:** Sprint 6

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri doradi funkcionalnosti za upload i unos transkripata.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri provjeri i doradi postojećeg toka za upload i unos transkripata. Fokus nije bio na ponovnoj implementaciji osnovne funkcionalnosti iz prethodnog sprinta, već na njenom poboljšanju, povezivanju sa ostatkom aplikacije i otklanjanju uočenih problema u radu.

**Šta je AI predložio ili generisao:**
- provjeru toka od unosa transkripta do prikaza u aplikaciji
- prijedloge za jasnije rukovanje greškama pri uploadu
- provjeru da li su frontend i backend očekivanja usklađena
- prijedloge za validaciju unesenog transkripta
- smjernice za testiranje uspješnog i neuspješnog unosa

**Šta je tim prihvatio:**
- doradu toka za upload i unos transkripata
- jasnije razdvajanje uspješnog i neuspješnog scenarija
- provjeru podataka prije slanja prema backend-u
- bolje povezivanje postojeće funkcionalnosti sa korisničkim interfejsom

**Šta je tim izmijenio:**
- nazivi i struktura dijelova koda su prilagođeni postojećem projektu
- poruke prema korisniku su usklađene sa načinom komunikacije u aplikaciji
- pojedini prijedlozi su pojednostavljeni kako bi odgovarali trenutnom obimu sprinta

**Šta je tim odbacio:**
- prijedloge koji bi uvodili novu kompleksnu obradu transkripata izvan Sprinta 6
- dodatne AI funkcionalnosti koje nisu bile potrebne za stabilizaciju postojećeg toka

**Rizici, problemi ili greške koje su uočene:**
- upload može pasti ako format transkripta nije očekivan
- frontend i backend moraju imati usklađena pravila validacije
- potrebno je dodatno provjeriti ponašanje kod praznog ili nepotpunog transkripta

---

## AI Usage Log – Zapis 13

**Datum:** 01/05/2026

**Sprint broj:** Sprint 6

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri doradi validacije i resetovanja transkripata.

**Kratak opis zadatka ili upita:**
Claude Code je korišten kao pomoć pri provjeri validacijskih pravila i funkcionalnosti resetovanja transkripata. Cilj je bio osigurati da aplikacija pravilno prepoznaje neispravne ili nepotpune podatke i da korisnik može vratiti transkript u odgovarajuće stanje kada je to potrebno.

**Šta je AI predložio ili generisao:**
- validacijske scenarije za transkripte sa nedostajućim podacima
- prijedloge za jasniju obradu grešaka
- logiku za provjeru stanja transkripta prije resetovanja
- scenarije u kojima reset treba biti dozvoljen ili blokiran
- prijedloge za testiranje validacije i reset funkcionalnosti

**Šta je tim prihvatio:**
- provjeru validacijskih pravila za unos i obradu transkripata
- ideju da reset funkcionalnost mora imati jasno definisano ponašanje
- obradu grešaka u slučajevima kada transkript nije moguće resetovati
- dodatnu provjeru rubnih slučajeva

**Šta je tim izmijenio:**
- pravila validacije su prilagođena postojećoj poslovnoj logici
- poruke grešaka su prilagođene korisnicima aplikacije
- reset logika je usklađena sa postojećim statusima i tokom rada aplikacije

**Šta je tim odbacio:**
- generičku reset logiku koja ne uzima u obzir stanje transkripta
- dodatne statuse koji nisu bili dio dogovorenog workflow-a

**Rizici, problemi ili greške koje su uočene:**
- reset transkripta može dovesti do gubitka prethodno unesenih podataka ako nije jasno kontrolisan
- potrebno je osigurati da se ne resetuju pogrešni zapisi
- validacija mora ostati usklađena sa backend pravilima

---

## AI Usage Log – Zapis 14

**Datum:** 02/05/2026

**Sprint broj:** Sprint 6

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri doradi dashboarda, sidebara i navigacije kroz aplikaciju.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri doradi korisničkog interfejsa, posebno dashboarda, sidebara i navigacije. Fokus je bio na tome da korisnik lakše pristupa glavnim dijelovima sistema i da se postojeće stranice bolje povežu u jednu cjelinu.

**Šta je AI predložio ili generisao:**
- prijedloge za organizaciju navigacijskih linkova
- doradu sidebara radi jasnijeg kretanja kroz aplikaciju
- poboljšanje rasporeda elemenata na dashboard stranici
- prijedloge za prikaz ključnih informacija korisniku
- provjeru UI problema koji mogu otežati korištenje aplikacije

**Šta je tim prihvatio:**
- doradu sidebara i navigacije
- poboljšanje dashboard prikaza
- jasnije povezivanje stranica unutar aplikacije
- ispravke UI problema koji su primijećeni tokom pregleda

**Šta je tim izmijenio:**
- raspored elemenata je prilagođen stvarnom sadržaju aplikacije
- nazivi linkova i tekstovi su usklađeni sa projektnim jezikom
- vizuelni stil je prilagođen postojećem dizajnu

**Šta je tim odbacio:**
- prijedloge za kompleksniji layout koji nije bio potreban
- dodatne animacije i efekte koji nisu doprinosili funkcionalnosti
- promjene koje bi značajno mijenjale dogovoreni izgled aplikacije

**Rizici, problemi ili greške koje su uočene:**
- nekonzistentna navigacija može zbuniti korisnike
- dashboard mora prikazivati relevantne informacije bez previše opterećenja
- UI promjene mogu uticati na postojeće komponente ako nisu pažljivo urađene

---

## AI Usage Log – Zapis 15

**Datum:** 03/05/2026

**Sprint broj:** Sprint 6

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri ispravci report issues funkcionalnosti i dodatnih UI problema.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri refaktoringu i ispravci problema vezanih za report issues funkcionalnost, navigaciju, dashboard i druge uočene UI nedostatke. Cilj je bio stabilizovati već implementirane dijelove aplikacije i učiniti ih spremnijim za demonstraciju u Sprint Review-u.

**Šta je AI predložio ili generisao:**
- analizu mogućih uzroka UI problema
- prijedloge za refaktoring dijelova interfejsa
- provjeru navigacije između stranica
- doradu prikaza grešaka i korisničkih poruka
- smjernice za provjeru dashboard prikaza nakon izmjena

**Šta je tim prihvatio:**
- ispravke u navigaciji
- doradu report issues prikaza i ponašanja
- poboljšanje dashboard korisničkog iskustva
- refaktoring dijelova koda radi bolje preglednosti

**Šta je tim izmijenio:**
- prijedlozi su prilagođeni postojećoj strukturi frontend aplikacije
- tekstovi i poruke su usklađeni sa bosanskim jezikom
- izmjene su ograničene na ono što je bilo potrebno za Sprint 6

**Šta je tim odbacio:**
- veće promjene arhitekture frontend-a
- dodavanje novih funkcionalnosti koje nisu bile dio Sprinta 6
- nepotrebno kompleksne obrasce za prikaz grešaka

**Rizici, problemi ili greške koje su uočene:**
- refaktoring može nenamjerno uticati na već funkcionalne dijelove aplikacije
- report issues funkcionalnost mora biti jasna korisniku
- potrebno je ručno provjeriti navigaciju nakon UI izmjena

---

## AI Usage Log – Zapis 16

**Datum:** 04/05/2026

**Sprint broj:** Sprint 6

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri završavanju prijevoda stranica i doradi landing page-a.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri provjeri i doradi tekstova na frontend stranama aplikacije. Fokus je bio na završavanju prijevoda stranica, usklađivanju terminologije i doradi landing page-a kako bi aplikacija djelovala konzistentnije i profesionalnije.

**Šta je AI predložio ili generisao:**
- prijedloge za prevod i usklađivanje UI tekstova
- doradu opisa i naslova na landing page-u
- provjeru konzistentnosti terminologije kroz aplikaciju
- prijedloge za jasnije formulacije korisničkih poruka
- provjeru da li su tekstovi razumljivi ciljnoj grupi korisnika

**Šta je tim prihvatio:**
- završavanje prijevoda stranica
- doradu landing page sadržaja
- usklađivanje terminologije kroz aplikaciju
- jasnije korisničke poruke na frontend-u

**Šta je tim izmijenio:**
- tekstovi su prilagođeni stvarnom kontekstu projekta
- pojedine formulacije su skraćene radi boljeg prikaza u UI-u
- landing page je usklađen sa funkcionalnostima koje aplikacija stvarno nudi

**Šta je tim odbacio:**
- marketinški preširoke opise koji nisu odgovarali stvarnom obimu projekta
- generičke tekstove koji nisu dovoljno jasno opisivali sistem
- dodatne sekcije koje nisu bile potrebne za trenutnu verziju aplikacije

**Rizici, problemi ili greške koje su uočene:**
- loš ili nedosljedan prevod može smanjiti jasnoću aplikacije
- landing page ne smije obećavati funkcionalnosti koje nisu implementirane
- UI tekstovi moraju ostati kratki i razumljivi

---

## AI Usage Log – Zapis 17

**Datum:** 06/05/2026

**Sprint broj:** Sprint 6

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri dodavanju i provjeri unit, integracijskih i CI testova.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri dodavanju i provjeri testova za Sprint 6. Fokus je bio na testovima koji potvrđuju stabilnost postojećih funkcionalnosti, uključujući autentifikaciju, pipeline, transkripte i dijelove aplikacije koji su mijenjani tokom sprinta.

**Šta je AI predložio ili generisao:**
- prijedloge unit testova za izolovanu backend logiku
- prijedloge integracijskih testova za tokove povezane sa autentifikacijom, pipeline-om i transkriptima
- smjernice za organizaciju testova u repozitoriju
- provjeru pytest konfiguracije
- smjernice za CI testove i dokaz testiranja

**Šta je tim prihvatio:**
- dodavanje Sprint 6 testova
- provjeru autentifikacije, pipeline-a i transkripata kroz testove
- korištenje postojećeg testnog okruženja
- dokumentovanje dokaza testiranja nakon lokalnog pokretanja

**Šta je tim izmijenio:**
- testovi su prilagođeni stvarnoj implementaciji
- dio testova je pojednostavljen da provjerava najvažnije poslovne scenarije
- konfiguracija je prilagođena postojećem pytest setup-u

**Šta je tim odbacio:**
- testove za funkcionalnosti koje nisu bile završene ili nisu bile dio Sprinta 6
- previše detaljne testove koji bi otežali održavanje
- prijedloge koji bi zahtijevali dodatne servise samo radi testiranja

**Rizici, problemi ili greške koje su uočene:**
- testovi moraju provjeravati stvarnu poslovnu logiku, a ne samo tehničko izvršavanje
- promjene u API rutama mogu zahtijevati ažuriranje integracijskih testova
- CI testovi mogu padati ako okruženje nije isto kao lokalno

---

## AI Usage Log – Zapis 18

**Datum:** 06/05/2026

**Sprint broj:** Sprint 6

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri završnoj provjeri builda, pokretanja testova i dokumentovanju dokaza testiranja.

**Kratak opis zadatka ili upita:**
Claude Code je korišten kao podrška pri završnoj provjeri Sprint 6 izmjena. Cilj je bio potvrditi da se aplikacija može buildati i da testovi prolaze prije nego što se promjene dokumentuju i predstave u Sprint Review-u.

**Šta je AI predložio ili generisao:**
- komande za lokalno pokretanje testova
- provjeru značenja pytest rezultata
- objašnjenje razlike između unit testova i testova koji zavise od Docker okruženja
- prijedlog načina dokumentovanja dokaza testiranja
- smjernice za završnu provjeru prije pushanja izmjena

**Šta je tim prihvatio:**
- lokalno pokretanje testova prije završetka sprinta
- dokumentovanje rezultata testiranja
- provjeru da unit testovi ne zahtijevaju Docker
- pripremu dokaza da su testovi uspješno prošli

**Šta je tim izmijenio:**
- komande su prilagođene stvarnoj strukturi projekta
- dokumentacija je napisana u skladu sa formatom koji tim već koristi
- u AI Usage Log su uključene samo aktivnosti vezane za implementaciju, ispravke, deploy i testiranje

**Šta je tim odbacio:**
- ponavljanje zapisa iz Sprinta 5
- dokumentovanje aktivnosti koje nisu vezane za implementaciju ili testiranje
- detalje koji nisu direktno povezani sa Sprint 6 promjenama

**Rizici, problemi ili greške koje su uočene:**
- uspješno lokalno testiranje ne garantuje automatski uspješan production deploy
- potrebno je posebno provjeriti produkcijske varijable i hosting konfiguraciju
- dokumentacija mora jasno razlikovati šta je urađeno u Sprintu 6 u odnosu na prethodni sprint
---

## AI Usage Log – Zapis 19

**Datum:** 07/05/2026

**Sprint broj:** Sprint 7

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri refaktoringu monolitnog preprocessing servisa u zasebne module.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri razdvajanju postojeće pipeline logike na odvojene module: `normalize`,
`speakers`, `chunking`, `pii/recognizers`, `pii/masker`, `pii/token_store`, `audit` i `speakers_llm`. Cilj je bio
povećati testabilnost i jasnoću odgovornosti svakog dijela.

**Šta je AI predložio ili generisao:**
- strukturu direktorija za preprocessing modul
- interfejse između modula (ulaz/izlaz po modulu)
- dataclass modele `Turn`, `Chunk`, `PipelineResult` u `models.py`
- `run_pipeline()` kao centralni orkestratorski korak
- strukturu `audit` modula za logovanje bez curenja teksta

**Šta je tim prihvatio:**
- podjelu na zasebne module sa jasnim odgovornostima
- dataclass modele za prenos podataka između koraka
- `audit.safe_log()` koji ne loguje raw tekst ni PII vrijednosti
- orkestracijsku ulogu `run_pipeline()` bez direktne poslovne logike

**Šta je tim izmijenio:**
- naziv i strukturu pojedinih modula prilagođeni su imenima u projektu
- `run_pipeline()` je dopunjen specifičnom logikom filtriranja Q&A parova
- konfiguracija je zadržana kroz postojeći `settings` objekt

**Šta je tim odbacio:**
- prijedloge koji su uvodili apstrakcije nepotrebne za trenutni obim
- automatsko registrovanje modula u plugin arhitekturi

**Rizici, problemi ili greške koje su uočene:**
- prevelika granularnost modula može otežati praćenje toka za novog developera
- potrebno je paziti da `run_pipeline()` ostane jedino mjesto gdje se vrši DB upis

---

## AI Usage Log – Zapis 20

**Datum:** 08/05/2026

**Sprint broj:** Sprint 7

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji PII detekcije, maskiranja i enkriptovane token mape.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji logike koja prepoznaje lične podatke u tekstu transkripta (JMBG,
telefon, email, IBAN, SSN), zamjenjuje ih placeholderima i čuva originalno mapiranje enkriptovano u bazi.

**Šta je AI predložio ili generisao:**
- regex patterne za svaki tip PII entiteta
- JMBG checksum algoritam za matematičku validaciju (ne samo regex)
- logiku dodjele konzistentnih placeholdera za isti PII u tekstu
- `encrypt_token_map` / `decrypt_token_map` korištenjem Fernet simetričnog šifrovanja
- upozorenje u logovima kada `TOKEN_MAP_KEY` nije postavljen u okolini

**Šta je tim prihvatio:**
- checksum provjeru za JMBG kako bi se smanjio broj lažnih pozitiva
- princip da isti PII uvijek dobija isti placeholder u jednom dokumentu
- Fernet enkriptovanje token mape prije upisa u bazu
- fallback na efemerni ključ ako `TOKEN_MAP_KEY` nije konfigurisan

**Šta je tim izmijenio:**
- regex za telefon prošireni su na bosanske i regionalne formate
- struktura `Span` dataclassa prilagođena je postojećim modelima

**Šta je tim odbacio:**
- Presidio biblioteku kao previše tešku zavisnost za ovaj obim
- eksternalnu enkripcijsku uslugu u korist lokalne Fernet implementacije

**Rizici, problemi ili greške koje su uočene:**
- regex PII detekcija može propustiti nestandardne formate
- nepostavljanje `TOKEN_MAP_KEY` znači da se token mape ne mogu dekriptovati nakon restarta

---

## AI Usage Log – Zapis 21

**Datum:** 09/05/2026

**Sprint broj:** Sprint 7

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji LLM speaker labeling-a sa privacy boundary-em.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji fallback mehanizma koji koristi Groq LLM za labelovanje govornika
u audio transkriptima koji nemaju jasne prefiks oznake (Agent:/Korisnik:). Poseban naglasak je bio na tome da se Groq
API-ju šalje isključivo maskirani tekst.

**Šta je AI predložio ili generisao:**
- strukturu system prompta koji traži JSON odgovor sa rolama
- logiku pozivanja `label_speakers_llm()` samo kada `split_turns` vrati sve `unknown` role
- fallback koji vraća `[]` pri svakom izuzetku bez prekida pipeline-a
- `asyncio.to_thread` za pokretanje sinhronog Groq klijenta unutar asinhronog konteksta
- validaciju odgovora (provjera dozvoljenih rola, filtriranje praznih turnova)

**Šta je tim prihvatio:**
- privacy boundary kao strogi uslov: LLM uvijek prima samo maskirani tekst
- graceful fallback na prazan rezultat kod nedostupnosti Groqa
- JSON response format za predvidive odgovore modela
- temperature=0.0 za determinističko labelovanje

**Šta je tim izmijenio:**
- system prompt je dopunjen pravilima specifičnim za call centar
- validacija rola je proširena jer LLM ponekad vraća nestandardne vrijednosti

**Šta je tim odbacio:**
- streaming odgovore koji nisu potrebni za kratke transkripte
- keširanje LLM odgovora u ovoj fazi projekta

**Rizici, problemi ili greške koje su uočene:**
- Groq API može biti nedostupan u produkciji i pipeline mora to preživjeti
- LLM može pogrešno labelovati govornika u kratkim ili dvosmislenim transkriptima
- potrebno je pratiti koliko transkripata prolazi kroz LLM fallback

---

## AI Usage Log – Zapis 22

**Datum:** 10/05/2026

**Sprint broj:** Sprint 7

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri pisanju granularnih unit testova za sve preprocessing module.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri pisanju `test_preprocessing.py` koji pokriva svaki preprocessing modul u
izolaciji: normalizator, speaker splitter, PII recognizers, masker, token store, chunker i audit logger.

**Šta je AI predložio ili generisao:**
- strukturu test fajla podijeljenu po sekcijama prema modulu
- fixture sa sintetičkim ali validnim PII podacima (JMBG sa ispravnim checksumom)
- `test_mask_token_map_invertible` koji potvrđuje idempotentnost maskiranja
- `test_no_pii_leak_in_masked_output` koji iterira po svim PII vrijednostima
- mock pristup za Groq u testovima `speakers_llm` (bez stvarnog API poziva)
- `test_llm_speaker_never_receives_raw_pii` koji hvata pozive prema Groq klijentu

**Šta je tim prihvatio:**
- podjelu testova po sekcijama sa komentarima
- upotrebu `caplog` za testiranje audit logiranja
- fixture sa validnim JMBG checksumom kako bi test bio pouzdan
- mock pristup koji simulira i uspješan i neuspješan Groq poziv

**Šta je tim izmijenio:**
- PII vrijednosti u fixture-u zamijenjene vlastitim validiranim vrijednostima
- dio asserta za `mask_roundtrip` prilagođen zbog space normalizacije telefona

**Šta je tim odbacio:**
- property-based testiranje (hypothesis) kao previše kompleksno za ovaj sprint
- testove koji zahtijevaju stvarni Groq API ključ

**Rizici, problemi ili greške koje su uočene:**
- mock testovi potvrđuju privacy boundary na nivou koda, ali ne i u produkciji
- testovi ovise o internom formatu placeholdera (`[JMBG_1]`) koji se može promijeniti

---

## AI Usage Log – Zapis 23

**Datum:** 11/05/2026

**Sprint broj:** Sprint 7

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri pisanju end-to-end integracionog testa pipeline-a nad testnom bazom.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri pisanju `test_pipeline_integration.py` koji pokreće `run_pipeline()` nad SQLite
testnom bazom i verificira da su ispravno kreirani `Segment`, `UnosBazeZnanja` i `TokenMapRecord` zapisi, te da PII ne
curi ni u jedan od tih zapisa.

**Šta je AI predložio ili generisao:**
- async test koji koristi `setup_test_db` fixture
- kreiranje `Transkript` objekta direktno u testnoj bazi
- asercije koje provjeravaju broj segmenata, Q&A parova i entiteta
- provjeru da `encrypted_blob` ne sadrži PII u čistom tekstu
- provjeru da ni jedno `pitanje` u `UnosBazeZnanja` ne sadrži maskirani PII

**Šta je tim prihvatio:**
- provjeru sva četiri izlaza pipeline-a u jednom testu
- no-leak aserciju nad `TokenMapRecord.encrypted_blob`
- korištenje sesijskog fixture-a radi dijeljenja baze između testova

**Šta je tim izmijenio:**
- transkript tekst je prilagođen da garantira barem 2 Q&A para
- minimalni pragovi asercija (`>= 2`, `>= 4`) odabrani su konzervativno

**Šta je tim odbacio:**
- zasebni testovi za svaki korak pipeline-a (pokriveni unit testovima)
- testiranje Qdrant integracije (embedding se ne radi pri uploadu)

**Rizici, problemi ili greške koje su uočene:**
- test ovisi o tome da `_is_procedural_qa` propusti dovoljno parova iz fixture teksta
- SQLite se ponaša drugačije od PostgreSQL-a u rubnim slučajevima

---
## AI Usage Log – Zapis 24

**Datum:** 17/05/2026

**Sprint broj:** Sprint 8

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji glasovnog unosa u chatu i automatske transkripcije audio fajlova.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji funkcionalnosti koje omogućavaju korisniku da diktira pitanje u chat, te administratoru ili agentu da uploaduje audio fajl i dobije transkript prije konačnog spremanja u sistem. Fokus je bio na tome da se audio transkript pregleda prije pohrane, da se podrže validni audio formati i da se nakon potvrde transkript obradi kroz postojeći pipeline.

**Šta je AI predložio ili generisao:**
- strukturu endpointa za transcribe preview nad audio fajlom
- tok potvrde transkripta prije konačnog spremanja
- validaciju audio fajla, uključujući prazan ili nepodržan fajl
- integraciju transkribovanog teksta sa postojećim tokom obrade transkripata
- frontend logiku za upload audio fajla i prikaz generisanog transkripta
- korištenje browser Web Speech API-ja za glasovni unos pitanja u chat

**Šta je tim prihvatio:**
- preview-before-save pristup za audio transkripciju
- obaveznu provjeru transkripta prije spremanja u bazu
- prikaz jasnih grešaka za nevalidan, prazan ili oštećen audio fajl
- glasovni unos koji popunjava chat input i omogućava korisniku da pitanje potvrdi prije slanja

**Šta je tim izmijenio:**
- podržani formati i poruke grešaka prilagođeni su postojećem upload modulu
- transkribovani audio zapis povezan je sa istim pipeline-om kao i ručno uneseni transkript
- frontend tok je usklađen sa postojećim dizajnom ChatWindow i UploadSection komponenti

**Šta je tim odbacio:**
- automatsko spremanje transkripta bez ručne potvrde korisnika
- kompleksniji player/editor audio fajla koji nije bio potreban za trenutni sprint
- implementaciju posebnog servisa za transkripciju izvan postojećeg backend-a

**Rizici, problemi ili greške koje su uočene:**
- transkripcija može biti nepotpuna ako je kvalitet audio fajla loš
- browser podrška za glasovni unos nije jednaka u svim browserima
- potrebno je jasno naglasiti korisniku da prije spremanja pregleda automatski generisani tekst

---

## AI Usage Log – Zapis 25

**Datum:** 17/05/2026

**Sprint broj:** Sprint 8

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji RAG retrieval-a, LLM klasifikacije upita i sigurnog fallback-a prema agentu.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri doradi toka odgovaranja u chat servisu. Cilj je bio da chatbot prvo prepozna da li je upit općenit, pozdrav ili domenski upit, zatim da za domenske upite koristi bazu znanja i Qdrant retrieval, a da u slučaju nedovoljne sigurnosti korisniku jasno ponudi povezivanje s agentom umjesto izmišljanja odgovora.

**Šta je AI predložio ili generisao:**
- tok klasifikacije upita na pozdrav, općeniti upit, RAG upit ili upit za eskalaciju
- korištenje confidence praga za odluku da li je odgovor dovoljno pouzdan
- prompt pravila koja zabranjuju izmišljanje odgovora izvan baze znanja
- uključivanje historije razgovora u chat payload radi boljeg konteksta
- fallback poruku koja korisniku objašnjava zašto se predlaže agent
- osnovnu logiku za reindeksiranje odobrenih unosa baze znanja

**Šta je tim prihvatio:**
- kombinovani RAG/LLM tok umjesto oslanjanja samo na generativni odgovor
- confidence threshold kao uslov za automatsku eskalaciju
- jasnu poruku korisniku kada chatbot nema dovoljno siguran odgovor
- prirodne odgovore na pozdrave i jednostavna općenita pitanja bez nepotrebne eskalacije

**Šta je tim izmijenio:**
- system prompt je prilagođen call-centar kontekstu aplikacije
- granica pouzdanosti i tekst fallback odgovora prilagođeni su stvarnom ponašanju sistema
- retrieval i reindex tok usklađeni su s postojećom bazom znanja i Qdrant integracijom

**Šta je tim odbacio:**
- davanje odgovora bez izvora kada RAG ne pronađe relevantan sadržaj
- keširanje vektorskih pretraga u Redisu u ovom sprintu
- kompleksnije podešavanje promptova koje bi otežalo stabilizaciju MVP-a

**Rizici, problemi ili greške koje su uočene:**
- kratki upiti mogu biti pogrešno klasificirani kao pozdrav ili općeniti razgovor
- kvalitet odgovora i dalje zavisi od kvaliteta baze znanja i embeddinga
- prag pouzdanosti može zahtijevati dodatno podešavanje nakon ručnog testiranja

---

## AI Usage Log – Zapis 26

**Datum:** 17/05/2026

**Sprint broj:** Sprint 8

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji escalation queue-a i servisnog sloja za upravljanje eskaliranim razgovorima.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri definisanju i implementaciji `EscalationService` toka: kreiranje eskalacije, prikaz u queue-u, prihvatanje od strane agenta, sprečavanje dupliranja aktivnih eskalacija, vraćanje u queue, otkazivanje i označavanje razgovora kao riješenog ili napuštenog.

**Šta je AI predložio ili generisao:**
- model stanja eskalacije sa statusima `Cekanje`, `UToku`, `Rijesena` i `Napustena`
- idempotentnu logiku kreiranja eskalacije za istog korisnika
- metode za prihvatanje, oslobađanje, otkazivanje i rješavanje eskalacije
- povezivanje eskalacije sa historijom razgovora korisnika
- ažuriranje statusa agenta kroz stanja `Online`, `Zauzet` i `Offline`
- API rute i šeme potrebne za queue prikaz i akcije agenta

**Šta je tim prihvatio:**
- eksplicitni statusni model za eskalacije
- idempotentnost kod kreiranja aktivnog zahtjeva za istog korisnika
- prikaz historije razgovora agentu pri prihvatanju eskalacije
- ažuriranje statusa agenta nakon prihvatanja i zatvaranja razgovora

**Šta je tim izmijenio:**
- dodan je razlog eskalacije kako bi se razlikovala niska pouzdanost od eksplicitnog zahtjeva korisnika
- eksplicitni zahtjev korisnika dobio je viši prioritet u queue-u
- nazivi statusa i payload format usklađeni su sa ostatkom backend API-ja i frontend tipovima

**Šta je tim odbacio:**
- jednostavan boolean flag umjesto statusnog modela
- kreiranje novog queue zapisa pri svakom ponovljenom zahtjevu korisnika
- potpuno oslanjanje na frontend za sprečavanje duplih eskalacija

**Rizici, problemi ili greške koje su uočene:**
- servisni sloj smanjuje rizik duplog prihvatanja, ali bez baze-level lockinga ne rješava sve race condition scenarije
- statusi eskalacije moraju ostati usklađeni između backend modela, API odgovora i frontend prikaza
- potrebno je pažljivo testirati prijelaze stanja, posebno kod prekida konekcije

---

## AI Usage Log – Zapis 27

**Datum:** 18/05/2026

**Sprint broj:** Sprint 8

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji WebSocket infrastrukture za real-time komunikaciju korisnika i agenta.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri dizajnu i implementaciji `ConnectionManager` mehanizma koji upravlja aktivnim WebSocket vezama korisnika i agenata, rutira poruke u realnom vremenu i omogućava automatsko obavještavanje druge strane kada se sesija promijeni ili zatvori.

**Šta je AI predložio ili generisao:**
- `ConnectionManager` singleton sa odvojenim mapama korisničkih i agentskih veza
- metode za spajanje, odspajanje i slanje poruka korisniku ili agentu
- broadcast mehanizam za agente uz mogućnost izuzimanja pošiljaoca
- WebSocket kanale za korisnički chat i agentski escalation kanal
- detekciju i uklanjanje mrtvih veza pri neuspješnom slanju
- inicijalni queue sync kada se agent poveže na WebSocket kanal

**Šta je tim prihvatio:**
- centralizovano upravljanje WebSocket vezama kroz jedan manager
- automatsko čišćenje veza koje više nisu aktivne
- JWT provjeru pri uspostavljanju WebSocket konekcije
- odvojene kanale za korisnika i agenta

**Šta je tim izmijenio:**
- dodani su statusni kodovi za nevalidan token i nedozvoljenu ulogu
- reconnect logika je dopunjena tolerisanjem greške ako je prethodna veza već zatvorena
- poruke su formatirane tako da frontend može razlikovati korisničke, agentske i sistemske evente

**Šta je tim odbacio:**
- long polling kao zamjenu za WebSocket komunikaciju
- čuvanje privremenih poruka u memoriji kao dodatni fallback u ovom sprintu
- Redis pub/sub pristup jer MVP radi na jednoj aplikacijskoj instanci

**Rizici, problemi ili greške koje su uočene:**
- aktivne veze se gube pri restartu aplikacije
- horizontalno skaliranje bi zahtijevalo drugačije rješenje za distribuirano stanje
- WebSocket testiranje je složenije od standardnih HTTP testova

---

## AI Usage Log – Zapis 28

**Datum:** 18/05/2026

**Sprint broj:** Sprint 8

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji zasebnog agent panela s Live Queue-om, chat panelom i pretragom baze znanja.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji agent panela u React/TypeScript aplikaciji, odvojenog od globalnog admin panela. Panel omogućava agentu da vidi dodijeljene ili dostupne eskalacije, prihvati razgovor, komunicira s korisnikom u realnom vremenu i pretražuje bazu znanja tokom razgovora.

**Šta je AI predložio ili generisao:**
- strukturu `AgentShell` komponente za agent-specifični pogled
- `useEscalation` hook za održavanje WebSocket veze i queue stanja
- `AgentQueue` i `EscalationCard` komponente za prikaz eskaliranih upita
- `ChatPanel` komponentu za real-time chat, historiju i sistemske poruke
- API funkcije za prihvatanje, oslobađanje i rješavanje eskalacije
- prikaz rezultata pretrage baze znanja u agentovom toku rada

**Šta je tim prihvatio:**
- odvajanje agent panela od admin panela
- raspodjelu odgovornosti između hook-ova, API sloja i prezentacijskih komponenti
- Live Queue koji se ažurira bez reload-a stranice
- prikaz historije razgovora pri prihvatanju eskalacije

**Šta je tim izmijenio:**
- stilizacija je usklađena s postojećim Tailwind dizajnom aplikacije
- dodano je automatsko skrolanje na zadnju poruku u chat panelu
- queue prikaz je prilagođen stvarnim statusima i prioritetima eskalacije

**Šta je tim odbacio:**
- React Query za upravljanje WebSocket stanjem u ovom sprintu
- prikaz svih aktivnih sesija svim agentima
- dodatne analitičke metrike koje nisu bile dio MVP cilja

**Rizici, problemi ili greške koje su uočene:**
- hook mora pravilno čistiti event listenere pri unmount-u
- agent ne smije vidjeti sesije koje nisu njegove ili nisu dostupne za preuzimanje
- pretraga baze znanja mora ostati brza i razumljiva tokom live razgovora

---

## AI Usage Log – Zapis 29

**Datum:** 18/05/2026

**Sprint broj:** Sprint 8

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri doradi historije razgovora, zatvaranja sesija, resolving toka i agent locking ponašanja.

**Kratak opis zadatka ili upita:**
Claude Code je korišten kao pomoć pri završnom povezivanju razgovora kroz cijeli lifecycle: korisnik vidi prethodne razgovore, agent preuzima samo odgovarajuću sesiju, chatbot ne preuzima aktivni razgovor koji je već dodijeljen agentu, a razgovor se zatvara kada agent označi slučaj kao riješen ili korisnik napusti sesiju.

**Šta je AI predložio ili generisao:**
- logiku da se poruke aktivne agentske sesije usmjeravaju dodijeljenom agentu umjesto kroz RAG odgovor
- čuvanje poruka u historiji eskalacije radi prikaza u agent panelu i korisničkoj historiji
- sistemske poruke za preuzimanje, napuštanje i rješavanje razgovora
- provjeru da novi agent ne preuzme razgovor koji je već u toku kod drugog agenta
- doradu prikaza kako bi se uklonili dupli tekstovi i nejasne sistemske poruke

**Šta je tim prihvatio:**
- agent locking pristup za aktivne live sesije
- bypass RAG-a dok je korisnik povezan s agentom
- čuvanje razgovora s odgovarajućim statusom u historiji
- resolving akciju kojom agent čisto zatvara razgovor

**Šta je tim izmijenio:**
- tekstovi sistemskih poruka su skraćeni i usklađeni s UI-em
- routing poruka je prilagođen dodijeljenom agentu i broadcast prikazu
- frontend prikaz je doradjen da izbjegne dupliranje istih poruka

**Šta je tim odbacio:**
- mogućnost da više agenata istovremeno aktivno piše u istom razgovoru
- vraćanje razgovora u chatbot tok prije eksplicitnog zatvaranja agentske sesije
- prikaz neobrađene interne strukture eventa korisniku

**Rizici, problemi ili greške koje su uočene:**
- bez pažljivog zaključavanja može doći do konfuzije oko toga koji agent trenutno vodi razgovor
- duple poruke mogu nastati ako frontend istovremeno prikazuje lokalni optimistic update i WebSocket event
- zatvaranje sesije mora biti sinhronizovano između korisničkog i agentskog prikaza

---

## AI Usage Log – Zapis 30

**Datum:** 19/05/2026

**Sprint broj:** Sprint 8

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri pisanju i ispravci unit i integracionih testova za Sprint 8 funkcionalnosti.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri kreiranju i doradi testova za WebSocket infrastrukturu, escalation service, escalation API endpoint-e i scenarije real-time komunikacije. Poseban fokus bio je na izolovanom testiranju `ConnectionManager` logike, statusnih prijelaza eskalacije i osnovnog lifecycle-a razgovora između korisnika i agenta.

**Šta je AI predložio ili generisao:**
- unit testove za metode `ConnectionManager`-a koristeći mockovane WebSocket objekte
- servisne testove za kreiranje, prihvatanje, oslobađanje i rješavanje eskalacija
- integracione testove za HTTP endpoint-e escalation API-ja
- WebSocket testove za osnovne korisničke i agentske scenarije
- test fixture-e za korisnike različitih uloga i JWT tokene

**Šta je tim prihvatio:**
- podjelu testova na unit i integracione testove
- SQLite testnu bazu konzistentno s prethodnim sprintovima
- testiranje auth guardova i role-based pristupa
- dodatne edge case testove za reconnect i neaktivne veze

**Šta je tim izmijenio:**
- testovi su prilagođeni stvarnim rutama i statusnim kodovima aplikacije
- uklonjeni su timeout parametri koji su pravili probleme u sinhronom WebSocket test okruženju
- dodani su testovi za paralelne korisničke sesije i nezavisnost WebSocket veza

**Šta je tim odbacio:**
- testiranje stvarnog Groq API poziva u automatizovanim testovima
- potpuno mockovanje baze za servisne testove
- testove konkurentnosti koji zahtijevaju produkciono okruženje s više procesa

**Rizici, problemi ili greške koje su uočene:**
- WebSocket testovi ne simuliraju u potpunosti produkciono async okruženje
- race condition scenariji s dva agenta nisu u potpunosti pokriveni
- promjene u rutama ili statusima eskalacije mogu zahtijevati ažuriranje većeg broja testova

---
## AI Usage Log – Zapis 31

**Datum:** 20/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri poboljšanju PII maskiranja i ekstrakcije Q&A parova iz transkripata.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri doradi obrade podataka u pipeline-u, posebno za edge case formate JMBG-a, telefonskih brojeva i imena, kao i za strožiju ekstrakciju smislenih Q&A parova iz transkripata. Fokus je bio da baza znanja ne bude degradirana nepotpunim, pogrešno povezanim ili privatnim podacima.

**Šta je AI predložio ili generisao:**
- proširenje regex pravila za različite formate telefonskih brojeva i JMBG-a
- dodatne regresijske testove za prethodno neispravno maskirane formate
- pravila za odbacivanje praznih, prekratkih ili interpunkcijskih Q&A parova
- spajanje susjednih segmenata istog govornika prije kreiranja Q&A para
- logovanje grešaka ekstrakcije s identifikatorom transkripta
- provjeru da pitanje dolazi od korisnika, a odgovor od agenta

**Šta je tim prihvatio:**
- proširenje PII maskiranja na edge case formate iz testiranja
- strožija pravila za validaciju Q&A parova prije spremanja u bazu znanja
- regresijske testove za formate koji su ranije prolazili bez maskiranja
- odbacivanje niskokvalitetnih parova koji ne nose korisnu proceduru za RAG

**Šta je tim izmijenio:**
- pragovi za minimalnu dužinu i sadržaj Q&A para prilagođeni su postojećem pipeline-u
- poruke i logovi su usklađeni s postojećim načinom dijagnostike u backend-u
- testni primjeri su prilagođeni stvarnim formatima korištenim u projektu

**Šta je tim odbacio:**
- ručno popravljanje svakog lošeg Q&A para bez automatskih pravila
- dodavanje kompleksnog NLP modela samo za detekciju kvaliteta Q&A parova u ovom sprintu
- oslanjanje isključivo na frontend validaciju za zaštitu PII podataka

**Rizici, problemi ili greške koje su uočene:**
- preagresivno maskiranje može sakriti korisne informacije ako regex obuhvati preširok tekst
- strožija ekstrakcija može odbaciti neke kratke, ali legitimne odgovore
- pravila za PII i Q&A ekstrakciju moraju se održavati kroz regresijske testove

---

## AI Usage Log – Zapis 32

**Datum:** 20/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji ocjene razgovora i sistemskih obavijesti u chatbotu.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri zamjeni ranijeg thumbs-up/thumbs-down pristupa formom za ocjenu cijele sesije, kao i za uvođenje sistemskog banera koji administrator može aktivirati radi obavještavanja korisnika o poznatim problemima ili održavanju.

**Šta je AI predložio ili generisao:**
- formu za ocjenu sesije s ocjenom 1–5 i opcionalnim komentarom
- logiku da se forma ne prikazuje za razgovore bez korisničkih poruka
- pravilo da se ista sesija ne može ocijeniti više puta
- endpoint i UI tok za aktiviranje, izmjenu i deaktiviranje sistemske obavijesti
- prikaz banera na vrhu Chat UI-a kada je obavijest aktivna
- mogućnost zatvaranja banera za trajanje trenutne sesije

**Šta je tim prihvatio:**
- ocjenjivanje kompletne sesije umjesto ocjenjivanja svake pojedinačne poruke
- opcionalni komentar uz numeričku ocjenu
- administratorski kontrolisanu sistemsku obavijest
- baner koji informiše korisnika bez blokiranja upotrebe chata

**Šta je tim izmijenio:**
- tekstovi i pozicioniranje forme prilagođeni su postojećem Chat UI-u
- sistemska poruka je usklađena s postojećim stilom aplikacije
- backend provjere su dopunjene da spriječe duplo slanje feedback-a za istu sesiju

**Šta je tim odbacio:**
- zadržavanje thumbs-up/down kontrola po poruci kao primarnog feedback mehanizma
- obavezno ocjenjivanje prije zatvaranja chata
- modalnu sistemsku obavijest koja bi blokirala korisnika

**Rizici, problemi ili greške koje su uočene:**
- korisnik može zatvoriti formu bez ocjene, pa broj prikupljenih feedback zapisa može biti manji
- sistemske obavijesti moraju biti jasno deaktivirane kako se zastarjele poruke ne bi prikazivale korisnicima
- feedback model mora pravilno razlikovati sesijsku ocjenu od ranijih feedback zapisa vezanih za odgovor

---

## AI Usage Log – Zapis 33

**Datum:** 21/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji ručnog unosa, pregleda, izmjene i brisanja Q&A parova u bazi znanja.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri doradi modula baze znanja. Cilj je bio omogućiti administratoru da direktno doda validiran Q&A par bez transkripta, pregleda odobrene unose, izmijeni sadržaj, obriše nevažeće unose i da se promjene sinhronizuju s Qdrant vektorskom bazom.

**Šta je AI predložio ili generisao:**
- `GET /knowledge/categories` endpoint za dohvat aktivnih kategorija
- `POST /knowledge/manual` endpoint za ručni unos Q&A para
- `GET /knowledge/approved` endpoint za prikaz odobrenih unosa
- `PUT /knowledge/{id}` endpoint za izmjenu para uz ponovno embedovanje i reindeksiranje
- `DELETE /knowledge/{id}` endpoint za soft-delete i uklanjanje iz Qdranta
- Pydantic validaciju da pitanje i odgovor imaju najmanje 10 karaktera
- frontend komponente `KnowledgeManualEntry`, `KnowledgeApprovedList` i tabbed layout u `Training.tsx`
- razlikovanje ručnih unosa od unosa nastalih iz transkripta kroz `source_type` / `id_segmenta IS NULL`

**Šta je tim prihvatio:**
- ručni unos Q&A para koji se odmah embeduje i indeksira u Qdrant
- pregled odobrenih unosa s oznakom izvora
- inline edit i potvrđeno brisanje unosa iz baze znanja
- validaciju na backend i frontend strani
- engleske UI i API poruke u ovom modulu radi konzistentnosti interfejsa

**Šta je tim izmijenio:**
- tekstovi u `Training.tsx`, `KnowledgeManualEntry.tsx` i `KnowledgeApprovedList.tsx` prevedeni su na engleski za dosljednost modula
- backend poruke u `knowledge.py` usklađene su s novim validacijskim pravilima
- prikaz kartica i badge-ova prilagođen je postojećem frontend dizajnu

**Šta je tim odbacio:**
- automatsko dodavanje svih prijedloga u aktivnu bazu znanja bez administratorske kontrole
- trajno brisanje bez soft-delete ponašanja u ovoj fazi
- odvojeni ekran za ručne unose kada se isti tok mogao uklopiti u postojeći Training modul

**Rizici, problemi ili greške koje su uočene:**
- promjena Q&A para zahtijeva ponovno embedovanje i reindeksiranje, pa greška u Qdrantu može ostaviti nekonzistentno stanje
- ručno uneseni sadržaj mora biti kvalitetan jer odmah utiče na odgovore chatbota
- validacija mora ostati ista na frontend i backend strani kako korisnik ne bi dobijao kontradiktorne poruke

---

## AI Usage Log – Zapis 34

**Datum:** 21/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri optimizaciji performansi backend AI servisa i mjerenju latencije odgovora.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri smanjenju latencije chatbota kroz keširanje embeddinga, singleton instance AI servisa, paralelno izvršavanje nezavisnih koraka i preciznije mjerenje ukupnog vremena odgovora kroz cijeli pipeline.

**Šta je AI predložio ili generisao:**
- `@lru_cache(maxsize=512)` na module-level `_embed_cached()` funkciji u `embedding_service.py`
- singleton getter funkcije za `LLMService`, `EmbeddingService` i `VectorStoreService`
- paralelno pokretanje klasifikacije namjere i embedding koraka kroz `asyncio.gather`
- PERF logove po fazama: `intent_classify`, `embed`, `vector_search`, `llm_only` i `llm_generate`
- računanje `latencija_ms` od ulaska u `answer()` do završetka svih grana odgovaranja
- ponovno korištenje prethodno izračunatog embeddinga kada query rewrite nije potreban

**Šta je tim prihvatio:**
- keširanje identičnih embedding upita unutar procesa
- singleton servise kako se modeli i klijenti ne bi inicijalizirali pri svakom zahtjevu
- ukupno mjerenje latencije za sve request path-ove
- zadržavanje postojećeg retrieval modela kako optimizacija ne bi promijenila tačnost odgovora

**Šta je tim izmijenio:**
- getter funkcije su smještene nakon definicija klasa kako bi se izbjegli problemi s forward reference
- sve direktne instance u `knowledge.py` i `main.py` zamijenjene su pozivima getter funkcija
- logovi su prilagođeni postojećem formatu backend logiranja

**Šta je tim odbacio:**
- Redis keširanje embeddinga u ovom sprintu
- zaseban background worker samo za AI servis
- promjene retrieval logike koje bi mogle promijeniti relevantnost odgovora

**Rizici, problemi ili greške koje su uočene:**
- singleton instance dijele svi zahtjevi i zahtijevaju oprez ako se kasnije uvede mutable stanje
- keširanje po tekstu ne pomaže kod semantički istih, ali tekstualno različitih upita
- preskakanje query rewrite-a može lošije raditi za kratke, ali kontekstualne upite

---

## AI Usage Log – Zapis 35

**Datum:** 21/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji User Settings menija i korisničkih akcija nad nalogom i historijom.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji `UserMenu` komponente dostupne klikom na avatar, s opcijama za promjenu prikazanog imena, brisanje cijele historije razgovora, brisanje korisničkog naloga i odjavu.

**Šta je AI predložio ili generisao:**
- `UserMenu` komponentu s internim view stanjima za glavni meni, promjenu imena i potvrde destruktivnih akcija
- `PATCH /me` endpoint za promjenu korisničkog imena
- `DELETE /me/history` endpoint za kaskadno brisanje historije razgovora korisnika
- `DELETE /me` endpoint za brisanje naloga i povezanih podataka
- pozicioniranje dropdowna pomoću `getBoundingClientRect()` i `position: fixed`
- zatvaranje dropdowna klikom van menija kroz `mousedown` listener

**Šta je tim prihvatio:**
- User Settings meni dostupan kroz avatar ikonu
- inline promjenu korisničkog imena s trenutnim ažuriranjem UI-a
- potvrdu prije brisanja historije i prije brisanja naloga
- kaskadno brisanje podataka u backend-u uz poštovanje FK ograničenja

**Šta je tim izmijenio:**
- `UserMenu` je integrisan na mjestima gdje je avatar vidljiv, uključujući `HomePage` i `ChatWindow`
- prikaz inicijala prilagođen je jednodijelnim i višedijelnim imenima
- callback za osvježavanje korisnika usklađen je s postojećim auth stanjem aplikacije

**Šta je tim odbacio:**
- promjenu lozinke kroz isti meni jer nije bila dio scope-a sprinta
- e-mail potvrdu prije brisanja naloga
- automatsko brisanje bez eksplicitne potvrde korisnika

**Rizici, problemi ili greške koje su uočene:**
- brisanje naloga i historije je nepovratno i mora biti jasno označeno korisniku
- kaskadno brisanje mora pratiti isti redoslijed kao brisanje pojedinačne sesije
- dropdown mora raditi konzistentno u svim layoutima gdje se koristi

---

## AI Usage Log – Zapis 36

**Datum:** 21/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji brisanja pojedinačnih chat sesija iz historije.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji funkcionalnosti koja korisniku omogućava da obriše pojedinačan razgovor iz historije putem kontekstnog menija. Fokus je bio na sigurnom backend brisanju povezanih podataka i ažuriranju UI-a bez reloada.

**Šta je AI predložio ili generisao:**
- kontekstni meni koji se otvara desnim klikom na stavku historije
- `DELETE /api/v1/chat/sessions/{session_id}` endpoint
- redoslijed kaskadnog brisanja koji poštuje FK veze između `Poruka`, `Odgovor`, `Feedback`, `Anomalija`, `Eskalacija` i `ChatSesija`
- optimistično uklanjanje obrisane sesije iz liste historije
- zatvaranje kontekstnog menija klikom van njega ili otvaranjem drugog menija

**Šta je tim prihvatio:**
- brisanje pojedinačnog chata kroz kontekstni meni
- backend provjeru vlasništva nad sesijom prije brisanja
- kaskadno brisanje povezanih zapisa u ispravnom redoslijedu
- optimistično ažuriranje liste historije na frontend strani

**Šta je tim izmijenio:**
- dodano je eksplicitno brisanje `Eskalacija` zapisa vezanog za sesiju zbog FK violation problema
- pozicioniranje menija prilagođeno je kroz `position: fixed`
- tekstovi i poruke brisanja usklađeni su s postojećim User Settings akcijama

**Šta je tim odbacio:**
- bulk brisanje pojedinačnih sesija kroz checkbox selekciju
- vidljivo dugme za brisanje na svakoj stavci historije
- brisanje bez backend provjere vlasništva nad sesijom

**Rizici, problemi ili greške koje su uočene:**
- brisanje je nepovratno i mora biti jasno razumljivo korisniku
- touch uređaji nemaju klasičan desni klik, pa pristup može zahtijevati dodatnu UX doradu
- FK veze se mogu promijeniti u budućnosti i tada redoslijed brisanja treba ponovo provjeriti

---

## AI Usage Log – Zapis 37

**Datum:** 22/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri ispravci prikaza UserMenu dropdowna pomoću React Portala.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za dijagnostiku problema u kojem se `UserMenu` dropdown prikazivao ispod elemenata chat interfejsa iako je imao visoku `z-index` vrijednost. Cilj je bio pronaći stvarni CSS uzrok i riješiti problem bez narušavanja postojećeg dizajna.

**Šta je AI predložio ili generisao:**
- identifikaciju da `glass-header` sa `backdrop-filter` kreira novi CSS stacking context
- objašnjenje zašto povećanje `z-index` vrijednosti ne rješava problem
- korištenje `ReactDOM.createPortal` za renderovanje dropdowna direktno u `document.body`
- zadržavanje `position: fixed` koordinata iz `getBoundingClientRect()`
- prilagođavanje event listenera za zatvaranje menija kada je dropdown renderovan kroz portal

**Šta je tim prihvatio:**
- `createPortal(dropdown, document.body)` kao trajno rješenje
- zadržavanje postojećeg `glass-header` vizualnog efekta
- prikaz dropdowna iznad svih ostalih elemenata aplikacije

**Šta je tim izmijenio:**
- dodan je import `createPortal` iz `react-dom`
- dropdown wrapper je premješten u portal bez promjene vanjskog API-ja komponente
- logika zatvaranja klikom van menija prilagođena je portal elementu

**Šta je tim odbacio:**
- dodatno povećanje `z-index` vrijednosti
- uklanjanje `backdrop-filter` efekta iz headera
- ručnu DOM manipulaciju van React toka

**Rizici, problemi ili greške koje su uočene:**
- portal elementi mogu zbuniti developere jer nisu u istom DOM stablu kao roditeljska komponenta
- event handling mora uzeti u obzir element renderovan van headera
- potrebno je provjeriti ponašanje na svim mjestima gdje se `UserMenu` koristi

---

## AI Usage Log – Zapis 38

**Datum:** 23/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri prikazu komentara iz ocjenjivanja u admin i agent pogledima.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri proširenju sistema ocjenjivanja tako da admin vidi posljednje korisničke komentare u Ratings sekciji, a agent u svojoj historiji može prepoznati i pregledati sesije koje imaju komentar korisnika.

**Šta je AI predložio ili generisao:**
- proširenje `GET /chat/ratings` endpointa za dohvat posljednjih komentara korisnika
- `recent_comments` prikaz u admin `Ratings.tsx` komponenti
- prikaz ocjene, datuma, komentara i povezanog pitanja
- proširenje `GET /escalation/my-history` endpointa sa feedback podacima sesije
- `sesija_feedback` polje u frontend tipu za agent historiju
- vizuelnu oznaku za sesije koje imaju komentar i prikaz komentara u proširenom redu

**Šta je tim prihvatio:**
- sekciju za najnovije komentare u admin Ratings dijelu
- prikaz komentara i ocjene u agentovoj historiji
- vizuelnu oznaku za komentarisane sesije bez uvođenja posebnog modalnog prozora na agent strani

**Šta je tim izmijenio:**
- query koristi `outerjoin` jer ne postoji feedback za svaku sesiju ili odgovor
- komentari se filtriraju tako da prazni stringovi ne ulaze u listu prikaza
- ikonica i tooltip implementirani su inline radi brze integracije

**Šta je tim odbacio:**
- filtriranje agent historije samo na sesije s komentarom
- poseban ekran samo za komentare
- prikaz praznih feedback zapisa bez komentara

**Rizici, problemi ili greške koje su uočene:**
- feedback može biti vezan za sesiju ili odgovor, pa query mora pokriti oba toka
- komentari mogu sadržavati kratak ili neinformativan tekst
- admin prikaz mora jasno povezati komentar sa stvarnom chat sesijom

---

## AI Usage Log – Zapis 39

**Datum:** 24/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri ispravci pregleda konkretne sesije iz Ratings sekcije i ograničavanju `/agent` rute.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za rješavanje problema u kojem je dugme „View in Chat Logs" iz Ratings sekcije vodilo na listu svih logova filtriranu po tekstu, umjesto da prikaže konkretnu sesiju. U istom toku je ispravljena i zaštita `/agent` rute tako da admin više ne može pristupiti agentskom panelu direktno.

**Šta je AI predložio ili generisao:**
- dodavanje `sesija_id` polja u `recent_comments` response
- novi admin endpoint `GET /api/v1/chat/admin/sessions/{session_id}/messages`
- modal u `Ratings.tsx` koji prikazuje poruke konkretne sesije
- uklanjanje `chatLogsPreset` i `onGoToChat` toka iz `AdminShell`
- promjenu route guarda za `/agent` na isključivo `agent` ulogu
- uklanjanje „Agent" linka iz navigacije vidljive admin korisniku

**Šta je tim prihvatio:**
- modalni prikaz konkretne sesije direktno u Ratings komponenti
- admin endpoint koji zahtijeva admin rolu, ali ne provjerava vlasništvo nad sesijom
- strožiju RBAC zaštitu `/agent` rute
- uklanjanje agentskog linka iz admin navigacije

**Šta je tim izmijenio:**
- `Ratings` komponenta više ne prima props za navigaciju u Chat Logs
- modal logika je implementirana interno u Ratings sekciji
- endpoint vraća samo podatke potrebne za pregled sesije iz admin konteksta

**Šta je tim odbacio:**
- navigaciju prema Chat Logs sa predfiltriranim parametrima
- zadržavanje admin pristupa `/agent` ruti radi testiranja
- posebnu novu stranicu za detalje sesije

**Rizici, problemi ili greške koje su uočene:**
- admin endpoint mora ostati strogo ograničen na admin rolu
- modal ne prikazuje sve metapodatke koji postoje u Chat Logs pogledu
- promjena route guarda mora biti testirana da ne blokira prave agente

---

## AI Usage Log – Zapis 40

**Datum:** 24/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri ispravci WebSocket stabilnosti kroz keepalive poruke i replay eventa za prihvaćenu eskalaciju.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri ispravci problema gdje je korisnički WebSocket mogao propustiti informaciju da je agent već prihvatio sesiju, kao i problema s gašenjem idle WebSocket konekcija iza proxy-ja. Dodatno je dijagnosticiran uzrok mogućeg reconnect loop-a na agentskom WebSocket kanalu.

**Šta je AI predložio ili generisao:**
- provjeru aktivne `UToku` eskalacije odmah pri korisničkom WebSocket connect-u
- replay `agent_connected` eventa ako je agent prihvatio eskalaciju prije završetka WebSocket handshake-a
- background `asyncio.Task` koji šalje `{"type":"ping"}` svakih 25 sekundi na korisničkom WebSocketu
- isti keepalive obrazac za agentski queue WebSocket
- premještanje `disconnect_agent` poziva u `finally` blok
- dijagnostiku da paralelne `useEscalation` instance mogu zatvarati jedna drugoj WebSocket vezu

**Šta je tim prihvatio:**
- replay provjeru aktivne eskalacije pri korisničkom spajanju
- keepalive ping za korisnički i agentski WebSocket kanal
- čišćenje agentske veze kroz `finally` blok
- dokumentovanje potencijalnog problema s duplim `useEscalation` instancama

**Šta je tim izmijenio:**
- ping task se eksplicitno otkazuje u `finally` bloku pri prekidu veze
- provjera aktivne eskalacije koristi svježu DB sesiju pri connect-u
- keepalive payload je zadržan minimalan da ne opterećuje frontend logiku

**Šta je tim odbacio:**
- rješavanje svih reconnect scenarija kroz dodatni globalni frontend state u ovom sprintu
- oslanjanje samo na proxy timeout konfiguraciju bez aplikacijskog keepalive-a
- čuvanje WebSocket poruka u memoriji kao fallback mehanizam

**Rizici, problemi ili greške koje su uočene:**
- dva paralelna `useEscalation` hook-a mogu uzrokovati zatvaranje prethodne agentske veze
- keepalive smanjuje idle timeout problem, ali ne rješava sve mrežne prekide
- WebSocket stanje u memoriji i dalje nije pogodno za horizontalno skaliranje

---

## AI Usage Log – Zapis 41

**Datum:** 24/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri pisanju i dopuni testova za Sprint 9 funkcionalnosti.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri dopuni unit, integracionih i regresijskih testova koji pokrivaju kritične putanje Sprinta 9: PII maskiranje, Q&A ekstrakciju, ocjenu razgovora, knowledge CRUD, User Settings akcije, brisanje chatova, WebSocket stabilnost i role-based pristup.

**Šta je AI predložio ili generisao:**
- regresijske testove za PII edge case formate
- testove za odbacivanje nevalidnih Q&A parova
- testove za knowledge endpoint-e i validaciju minimalne dužine pitanja/odgovora
- testove za korisničke postavke i destruktivne akcije
- testove za brisanje pojedinačne chat sesije i kaskadni redoslijed brisanja
- testove za route guard `/agent` i admin-only endpoint za pregled sesije
- testove za WebSocket keepalive i replay eventa u osnovnim scenarijima

**Šta je tim prihvatio:**
- regresijske testove za prethodno uočene bugove
- provjeru auth i role-based guardova
- testiranje backend validacije umjesto oslanjanja samo na frontend
- zadržavanje SQLite testnog okruženja za servisne i integracione testove

**Šta je tim izmijenio:**
- testovi su prilagođeni stvarnim rutama i statusnim kodovima aplikacije
- dio testova je pojednostavljen da provjerava najvažnije poslovne scenarije
- scenariji koji zavise od eksternih API poziva mockovani su kako testovi ne bi zavisili od mreže

**Šta je tim odbacio:**
- testiranje stvarnih Groq i Qdrant servisa u automatizovanom CI toku
- E2E testove koji zahtijevaju potpuno produkciono okruženje u ovom sprintu
- testove za funkcionalnosti iz PreostaliUserStories koje nisu uključene u implementaciju Sprinta 9

**Rizici, problemi ili greške koje su uočene:**
- mock testovi ne garantuju potpuno isto ponašanje kao produkcijski servisi
- promjene u modelima baze mogu zahtijevati ažuriranje većeg broja testova
- WebSocket testovi i dalje ne simuliraju sve realne mrežne prekide

---
## AI Usage Log – Zapis 42

**Datum:** 25/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji batch importa transkripata iz Google Drive foldera i povezivanju u postojeći pipeline obrade.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji on-demand importa fajlova sa web lokacije, primarno Google Drive foldera, tako da administrator unese folder ID ili link, a sistem povuče podržane fajlove i obradi ih kroz isti tok koji se koristi za ručni upload transkripata. Fokus je bio da se import ne implementira kao poseban paralelni tok, nego da koristi postojeću logiku za klasifikaciju fajla, transkripciju, ekstrakciju teksta, kreiranje `Transkript` zapisa i pokretanje pipeline-a.

**Šta je AI predložio ili generisao:**
- `GoogleDriveService` servis za service-account autentifikaciju, paginirano listanje fajlova i download fajlova iz Drive foldera
- `POST /api/v1/transcripts/import-drive` endpoint koji validira konfiguraciju i pokreće FastAPI `BackgroundTask`
- `DriveImportRequest` i `DriveImportResponse` šeme za API komunikaciju
- zajednički `file_utils.py` modul za `classify_file`, `extract_pdf_text`, dozvoljene formate i maksimalnu veličinu fajla
- `import_drive_folder(folder_id, uploader_id)` task koji za svaki podržani fajl koristi isti upload/pipeline tok kao ručni unos
- frontend `importDriveTranscripts(folderId)` funkciju i novu Drive karticu u `UploadSection.tsx`
- prikaz statusa u UI-u nakon pokretanja importa i jasnu poruku kada Google konfiguracija nije postavljena

**Šta je tim prihvatio:**
- on-demand import Google Drive foldera kao prvi podržani remote batch import
- ponovno korištenje postojećeg transcript pipeline-a umjesto pravljenja odvojenog toka
- podršku za `.mp3`, `.wav`, `.m4a`, `.ogg`, `.txt` i `.pdf` fajlove
- BackgroundTask pristup kako API ne bi čekao završetak cijelog batch procesa
- idempotentno preskakanje već importovanih fajlova
- jasnu konfiguraciju kroz `GOOGLE_SERVICE_ACCOUNT_JSON` bez commitovanja tajni

**Šta je tim izmijenio:**
- logika klasifikacije fajlova izdvojena je iz upload rute u zajednički helper kako bi upload i Drive import koristili ista pravila
- Google biblioteke se importuju lazy pristupom kako se ne bi učitavale ako se Drive import ne koristi
- Drive tab u admin upload sekciji uklopljen je u postojeći UI tok umjesto kreiranja posebne stranice

**Šta je tim odbacio:**
- uvođenje Celery worker-a ili novog servisa samo za batch import
- posebnu baznu migraciju za Drive import u ovoj fazi
- automatski scheduled import kao obavezni dio ove implementacije
- podršku za S3 u ovom koraku, iako je pristup dokumentovan kao moguće proširenje

**Rizici, problemi ili greške koje su uočene:**
- service-account JSON mora ostati tajan i ne smije se commitovati
- ako Google Drive API nije konfigurisan, endpoint mora vratiti jasnu 503 poruku
- jedan loš fajl ne smije prekinuti cijeli batch import
- audio fajlovi mogu ponovo aktivirati transkripcijski API ako se reimportuju

---

## AI Usage Log – Zapis 43

**Datum:** 25/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri doradi Google Drive importa tako da prihvata pune URL-ove i reimportuje ažurirane fajlove na osnovu vremena izmjene.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za dopunu Drive import funkcionalnosti nakon što je ustanovljeno da administrator može zalijepiti puni Google Drive folder URL, a ne samo folder ID. Dodatno je implementirana logika koja prepoznaje kada je fajl u Drive folderu ažuriran i tada zamjenjuje staru verziju novom, bez dupliranja unosa u bazi znanja.

**Šta je AI predložio ili generisao:**
- `extractDriveId()` frontend helper koji prepoznaje `/folders/<id>`, `/d/<id>` i `?id=<id>` formate
- normalizaciju unosa tako da backend uvijek dobija čisti folder ID
- proširenje `GoogleDriveService.list_files` metode da dohvaća `modifiedTime`
- verzionisani naziv `gdrive:<folder>:<filename>::v::<modifiedTime>`
- `_drive_naziv` i `_parse_drive_naziv` helper funkcije za rad s version-aware ključevima
- `purge_transcript` helper koji briše staru verziju transkripta, segmente, unose baze znanja i Qdrant vektore
- pravilo da se stara verzija briše tek nakon što se nova uspješno preuzme i validira

**Šta je tim prihvatio:**
- podršku za puni Drive folder URL i bare folder ID
- deduplikaciju po folderu, imenu fajla i `modifiedTime`
- zamjenu stare verzije novom kada se isti fajl ažurira u Drive-u
- čuvanje korisnički čistog prikaza naziva fajla bez `::v::<modifiedTime>` sufiksa u UI-u
- siguran redoslijed zamjene gdje se prethodna validna verzija ne briše ako novi download ili validacija padnu

**Šta je tim izmijenio:**
- placeholder i help tekst u upload formi izmijenjeni su tako da jasno kažu da se može unijeti folder URL ili ID
- import-progress logika usklađena je sa prikaznim nazivom fajla bez tehničkog sufiksa
- preview/count logika u `/import-drive` ruti prilagođena je istom version-aware pravilu

**Šta je tim odbacio:**
- jednostavno preskakanje fajlova samo po imenu bez provjere da li je sadržaj ažuriran
- brisanje stare verzije prije provjere nove verzije
- čuvanje više aktivnih verzija istog Drive fajla u bazi znanja

**Rizici, problemi ili greške koje su uočene:**
- prvi import nakon uvođenja `modifiedTime` može jednom reimportovati ranije importovane fajlove bez verzije
- audio reimport može ponovo potrošiti transkripcijski API
- pogrešna interpretacija Drive URL-a mogla bi pokrenuti import nad pogrešnim folderom ako se ID ne izdvoji pažljivo

---

## AI Usage Log – Zapis 44

**Datum:** 25/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri optimizaciji backend Docker build procesa i smanjenju vremena rebuilda.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za analizu sporog backend Docker builda i za predlaganje izmjena kojima se izbjegava ponovno skidanje velikih biblioteka pri svakom buildu. Poseban fokus bio je na tome da aplikacija koristi CPU-only embedding, ali je `torch` ranije povlačio veliki CUDA build i usporavao instalaciju dependency-ja.

**Šta je AI predložio ili generisao:**
- instalaciju CPU-only `torch` paketa u zasebnom Docker sloju prije `requirements.txt`
- korištenje PyTorch CPU wheel indexa kroz `--index-url https://download.pytorch.org/whl/cpu`
- BuildKit pip cache mount `RUN --mount=type=cache,target=/root/.cache/pip`
- `# syntax=docker/dockerfile:1` direktivu za BuildKit funkcionalnosti
- novi `backend/.dockerignore` koji iz build contexta izbacuje `.venv`, cache foldere, `*.db`, `.git` i `.env*`
- objašnjenje da prvi build i dalje može trajati duže, ali se naredni rebuildovi značajno ubrzavaju jer se dependency-ji ne skidaju ponovo

**Šta je tim prihvatio:**
- CPU-only torch kao siguran izbor jer aplikacija nema GPU i embedding se već izvršava na CPU-u
- izdvajanje torch instalacije u cache-friendly Docker layer
- BuildKit cache mount za pip download cache
- `.dockerignore` smanjenje build contexta
- dokumentovanje da prvi build može biti sporiji, ali da naredni buildovi nakon keširanja traju znatno kraće, u praksi oko 10–15 sekundi u odnosu na ranije buildove preko 25 minuta

**Šta je tim izmijenio:**
- Dockerfile je reorganizovan tako da runtime ponašanje ostane isto: isti paketi, isti spaCy model, isti `apt` paketi i isti start command
- `requirements.txt` je zadržan kao izvor istine za Python pakete
- dokumentacija je dopunjena napomenom da se pri problemu sa `--mount` mora eksplicitno uključiti BuildKit

**Šta je tim odbacio:**
- izbacivanje `sentence-transformers` biblioteke iz projekta samo radi brzine builda
- promjenu embedding modela u ovom sprintu
- uvođenje posebnog build servisa samo radi optimizacije Docker image-a

**Rizici, problemi ili greške koje su uočene:**
- ako BuildKit nije aktivan, `--mount` sintaksa može pasti pri buildu
- prvi build nakon promjene i dalje mora jednom popuniti cache
- različite Docker verzije mogu imati drugačije ponašanje cache-a
- treba paziti da `.dockerignore` ne izbaci fajlove koji su stvarno potrebni runtime-u

---

## AI Usage Log – Zapis 45

**Datum:** 25/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri pripremi single-click deployment toka na Azure infrastrukturu.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri dokumentovanju i pripremi deployment toka u kojem se kompletna aplikacija može podići jednom komandom `azd up`. Cilj je bio zamijeniti privremene tunele stabilnim HTTPS URL-ovima i postaviti backend i frontend na Azure servise, dok postojeći managed servisi za bazu, vektorsku bazu i LLM ostaju isti.

**Šta je AI predložio ili generisao:**
- `DEPLOY-AZURE.md` dokument sa koracima za `azd` instalaciju, autentifikaciju i deployment
- Azure arhitekturu: backend na Azure Container Apps, frontend na Azure Static Web Apps
- zadržavanje Supabase, Qdrant Cloud i Groq servisa uz injection secret-a u deploy okruženju
- `azd env new`, `azd env set` i `azd up` tok komandi
- napomenu da su `SECRET_KEY` i `INTERNAL_API_KEY` automatski generisani
- verifikacione korake nakon deploya: `/health`, login, chat poruka, Network tab i `wss://` konekcije
- troubleshooting za slučaj da frontend i dalje gađa stari `onrender.com` backend

**Šta je tim prihvatio:**
- single-click deploy pristup preko `azd up`
- Azure Container Apps za backend i Azure Static Web Apps za frontend
- trajne HTTPS URL-ove umjesto ručnog prevezivanja cloudflared tunela
- čuvanje tajni u `.azure/` okruženju koje je git-ignored
- obaveznu provjeru da frontend API/WS pozivi idu prema Azure backendu nakon deploya

**Šta je tim izmijenio:**
- deployment dokument je prilagođen studentskom/free-trial kontekstu i napominje da Docker Desktop mora biti pokrenut
- dodana je posebna napomena za `TOKEN_MAP_KEY` da se mora reuse-ati postojeća vrijednost
- dokumentovana je potreba za rotacijom Google service-account ključa nakon što je ranije dijeljen u plaintext obliku

**Šta je tim odbacio:**
- nastavak oslanjanja na cloudflared tunel kao glavni production deployment tok
- commitovanje secret vrijednosti u repozitorij
- migraciju Supabase, Qdrant i Groq servisa u Azure u ovom koraku

**Rizici, problemi ili greške koje su uočene:**
- pogrešan `TOKEN_MAP_KEY` čini ranije maskirane PII token mape nedekriptabilnim
- stale `frontend/.env.production` može prouzrokovati da frontend zove stari backend
- Azure Free Trial može blokirati neke cloud build opcije, pa je lokalni Docker build potreban
- deployment može napraviti troškove ako se resursi ne ugase nakon testiranja

---

## AI Usage Log – Zapis 46

**Datum:** 25/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri doradi admin pregleda ocjena, komentara i kompletnih chat razgovora.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za rješavanje problema u administratorskim pregledima gdje se nisu prikazivali svi dijelovi razgovora, posebno ljudsko-agentski dio eskalirane sesije. Dodatno je popravljeno prikazivanje session-level ratinga u Chat Logs i uklonjena mogućnost odabira `Manager` uloge iz User Management forme.

**Šta je AI predložio ili generisao:**
- spajanje `Poruka` redova sa porukama iz `Eskalacija.razgovor` JSON kolone u admin endpointu za poruke sesije
- deduplikaciju poruka po `(role, content)` da se bot poruke ne ponavljaju
- prikaz `role: "agent"` poruka kao "Agent" u Ratings modalu
- dopunu `/chat/logs` odgovora sa `session_id` vrijednošću
- dohvat pune sesije kada admin proširi Details u Chat Logs
- session-level rating subquery i `COALESCE` logiku za rating prikaz i `min_rating` filter
- uklanjanje `manager` iz selectable role liste u `UsersSection.tsx`, uz fallback prikaz postojeće uloge

**Šta je tim prihvatio:**
- kompletan prikaz bot + agent razgovora u Ratings → View Chat
- prikaz pune sesije u Chat Logs Details umjesto samo jednog exchange-a
- prikaz korisničkih ocjena ostavljenih na nivou sesije u Chat Logs
- uklanjanje Manager uloge iz dropdowna za dodjelu novih uloga
- fallback opciju da se postojeći manager korisnik ne prikaže pogrešno

**Šta je tim izmijenio:**
- modal i Chat Logs prikaz su usklađeni s postojećim labelama: User, Ambassador/Bot i Agent
- query logika koristi dodatne izvore poruka bez dupliciranja postojećih bot turnova
- frontend fallback prikaz zadržava badge mapiranje bez dopuštanja novog izbora Manager uloge

**Šta je tim odbacio:**
- prikaz samo bot poruka u admin modalima
- navigaciju iz Ratings sekcije na tekstualno filtriran Chat Logs kao jedini način pregleda
- ručno spajanje razgovora na frontend strani bez backend izvora istine
- zadržavanje Manager uloge kao standardne opcije za nove promjene u User Managementu

**Rizici, problemi ili greške koje su uočene:**
- poruke iz različitih tabela i JSON kolona moraju se pravilno sortirati i deduplicirati
- session-level i response-level feedback moraju ostati jasno razlikovani
- fallback prikaz postojeće Manager uloge ne smije omogućiti slučajno dodavanje novih managera

---

## AI Usage Log – Zapis 47

**Datum:** 25/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri dokumentovanju završnih promjena, verifikaciji kompajliranja i definisanju preostalih tehničkih ograničenja.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za sažimanje sesijskih promjena u pratećim dokumentima i za provjeru da su backend izmjene sintaksno ispravne kroz `py_compile`. Dokumentovani su deployment koraci, Drive import, build optimizacije, session/rating ispravke i ograničenja koja nisu riješena automatizovanim testovima.

**Šta je AI predložio ili generisao:**
- `SESSION_CHANGES.md` sa pregledom admin, ratings, chat logs i Drive import izmjena
- `DRIVE_IMPORT_AND_BUILD_NOTES.md` sa objašnjenjem Google Drive batch importa i build speed-up pristupa
- `DEPLOY-AZURE.md` sa single-click Azure deployment uputama
- jasnu napomenu da backend prolazi `py_compile`
- napomenu da test suite nije pokrenut zbog problema u pytest setup fixture-ima nevezanih za ove izmjene
- manuelne verifikacione korake za Ratings, Chat Logs i Drive import

**Šta je tim prihvatio:**
- dokumentovanje tehničkih promjena u odvojenim markdown fajlovima
- eksplicitno navođenje šta je implementirano, a šta je namjerno odgođeno
- naglašavanje build ubrzanja i objašnjenje zašto se biblioteke više ne skidaju svaki put
- zadržavanje iskrene napomene da kompletan test suite nije potvrđen ako fixture setup trenutno pada

**Šta je tim izmijenio:**
- dokumentacija je dopunjena objašnjenjem da prvi build može trajati duže, ali naredni buildovi koriste cache
- formulacije su prilagođene tome da se jasno vidi šta je stvarno urađeno u ovom sprintu
- deployment upute su prilagođene PowerShell okruženju koje tim koristi

**Šta je tim odbacio:**
- prikazivanje očekivanih funkcionalnosti kao da su implementirane ako su samo dokumentovane kao buduće proširenje
- sakrivanje činjenice da kompletan pytest suite nije pokrenut zbog nevezanih fixture problema
- miješanje tajnih vrijednosti i service-account JSON-a u repozitorijsku dokumentaciju

**Rizici, problemi ili greške koje su uočene:**
- dokumentacija mora ostati usklađena s kodom jer deployment i import koraci zavise od tačnih env varijabli
- manualna verifikacija ne zamjenjuje automatizovane testove
- ako se service-account key već dijelio u plaintextu, potrebno ga je rotirati prije produkcijske upotrebe

---
