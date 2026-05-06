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
