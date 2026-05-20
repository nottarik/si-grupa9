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
