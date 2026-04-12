1. Postavljanje pitanja chatbotu

Glavni akter: Korisnik call centra
Učesnici: Korisnik, AI chatbot sistem, po potrebi agent call centra
Cilj: Korisnik želi dobiti odgovor na svoje pitanje.

Preduslovi:

chatbot sistem je dostupan
korisnik ima pristup interfejsu za komunikaciju

Osnovni tok:

Korisnik otvara chatbot interfejs.
Unosi pitanje.
Sistem provjerava i maskira osjetljive podatke ako postoje.
Sistem obrađuje korisnički upit.
Chatbot vraća odgovor korisniku.
Korisnik vidi odgovor u razgovoru.

Alternativni tokovi:

korisnik može postaviti pitanje glasovnim unosom, a sistem ga prvo pretvara u tekst
ako pitanje sadrži osjetljive podatke, sistem ih zamjenjuje prije obrade
ako chatbot ne može dati pouzdan odgovor, razgovor se preusmjerava ljudskom agentu

Ishod:

korisnik dobije odgovor od chatbota
ili
pitanje bude eskalirano agentu
2. Pregled historije razgovora

Glavni akter: Korisnik call centra
Učesnici: Korisnik, AI chatbot sistem
Cilj: Korisnik želi vidjeti prethodne razgovore sa chatbotom.

Preduslovi:

u sistemu postoje prethodne interakcije korisnika

Osnovni tok:

Korisnik otvara sekciju historije razgovora.
Sistem učitava sačuvane poruke i odgovore.
Sistem prikazuje historiju hronološki.

Alternativni tokovi:

ako nema sačuvane historije, sistem prikazuje poruku da nema prethodnih razgovora
korisnik može iz historije pokrenuti dodatnu akciju, npr. brisanje razgovora

Ishod:

korisnik vidi svoju prethodnu komunikaciju sa sistemom
3. Brisanje historije razgovora

Glavni akter: Korisnik call centra
Učesnici: Korisnik, AI chatbot sistem
Cilj: Korisnik želi ukloniti dio ili cijelu historiju razgovora.

Preduslovi:

korisnik ima postojeću historiju razgovora
korisnik je otvorio pregled historije

Osnovni tok:

Korisnik otvara historiju razgovora.
Odabire zapis ili više zapisa za brisanje.
Sistem traži potvrdu.
Korisnik potvrđuje brisanje.
Sistem uklanja odabrane zapise iz historije.

Alternativni tokovi:

korisnik odustane od brisanja
sistem ne nalazi odabrani zapis jer je već uklonjen
korisnik briše samo jedan zapis ili više zapisa odjednom

Ishod:

odabrani razgovori više nisu vidljivi u historiji
4. Ocjena odgovora

Glavni akter: Korisnik call centra
Učesnici: Korisnik, AI chatbot sistem
Cilj: Korisnik želi dati povratnu informaciju o kvalitetu chatbot odgovora.

Preduslovi:

korisnik je već dobio odgovor od chatbota

Osnovni tok:

Sistem prikazuje opciju za ocjenu odgovora.
Korisnik bira ocjenu.
Sistem pohranjuje ocjenu uz adekvatan odgovor.

Alternativni tokovi:

korisnik uz ocjenu može ostaviti i komentar
korisnik ne želi ostaviti komentar, već samo ocjenu
korisnik daje negativnu ocjenu, pa potom prijavljuje odgovor kao netačan

Ishod:

odgovor chatbota dobija sačuvanu korisničku ocjenu
5. Prijava netačnog odgovora

Glavni akter: Korisnik call centra
Učesnici: Korisnik, AI chatbot sistem, administrator
Cilj: Korisnik želi prijaviti odgovor koji smatra netačnim, nejasnim ili nerelevantnim.

Preduslovi:

chatbot je prethodno dao odgovor
korisnik je uočio problem u odgovoru

Osnovni tok:

Korisnik bira opciju prijave problema.
Sistem otvara formu za prijavu.
Korisnik unosi opis problema i po potrebi bira kategoriju.
Sistem sprema prijavu i povezuje je s konkretnim odgovorom.

Alternativni tokovi:

korisnik prijavu pravi nakon negativne ocjene
korisnik može prijaviti problem bez dodatnog komentara, samo odabirom kategorije
korisnik odustane prije slanja prijave

Ishod:

problematičan odgovor ulazi u listu prijavljenih problema za administraciju
6. Pregled prijavljenih problema

Glavni akter: Administrator
Učesnici: Administrator, AI chatbot sistem
Cilj: Administrator želi analizirati prijave korisnika kako bi uočio slabosti sistema.

Preduslovi:

postoje evidentirane prijave problema

Osnovni tok:

Administrator otvara modul prijavljenih problema.
Sistem prikazuje listu svih prijava.
Administrator pregleda detalje pojedinačne prijave.
Administrator može promijeniti status prijave.

Alternativni tokovi:

administrator može filtrirati prijave po statusu, datumu ili vrsti problema
ako nema prijava, sistem prikazuje poruku da nema prijavljenih problema

Ishod:

administrator dobija pregled stanja prijava i može pratiti njihovu obradu
7. Upravljanje transkriptima

Glavni akter: Administrator
Učesnici: Administrator, AI chatbot sistem
Cilj: Administrator želi unijeti i pripremiti transkripte za rad i unapređenje sistema.

Preduslovi:

administrator ima pristup modulu za transkripte

Osnovni tok:

Administrator pristupa modulu za transkripte.
Unosi novi transkript.
Sistem validira unesene podatke.
Sistem priprema tekst za dalju obradu.
Transkript se pohranjuje.

Alternativni tokovi:

administrator može unijeti transkript iz fajla
administrator može ručno unijeti transkript
administrator može uploadati audio koji se pretvara u tekst
sistem može prepoznati grešku u formatu ili neispravne podatke pa odbiti unos

Ishod:

transkript je sačuvan i spreman za pregled ili dalju upotrebu
8. Pregled neodgovorenih pitanja

Glavni akter: Agent call centra
Učesnici: Agent, AI chatbot sistem
Cilj: Agent želi vidjeti pitanja na koja chatbot nije mogao odgovoriti.

Preduslovi:

postoje eskalirana ili neodgovorena pitanja

Osnovni tok:

Agent otvara modul neodgovorenih pitanja.
Sistem prikazuje listu pitanja koja čekaju obradu.
Agent bira jedno pitanje za pregled.

Alternativni tokovi:

ako nema takvih pitanja, sistem prikazuje odgovarajuću poruku
agent može pregledati samo pitanja određenog statusa ili datuma

Ishod:

agent dobija uvid u pitanja koja zahtijevaju ljudsku intervenciju
9. Odgovor agenta na neodgovoreno pitanje

Glavni akter: Agent call centra
Učesnici: Agent, AI chatbot sistem, korisnik call centra
Cilj: Agent želi dati tačan odgovor kada chatbot nije uspio.

Preduslovi:

postoji neodgovoreno pitanje u sistemu
agent je otvorio detalje pitanja

Osnovni tok:

Agent bira pitanje iz liste neodgovorenih pitanja.
Sistem prikazuje sadržaj pitanja i kontekst.
Agent unosi odgovor.
Sistem sprema odgovor.
Status pitanja se mijenja u odgovoreno.
Korisnik dobija odgovor.

Alternativni tokovi:

agent može dopuniti ili ispraviti odgovor prije slanja
agent može odgoditi odgovor i ostaviti pitanje u čekanju

Ishod:

korisnik dobija ljudski odgovor na pitanje koje chatbot nije riješio
10. Poboljšanje baze znanja chatbota

Glavni akter: Administrator
Učesnici: Administrator, AI chatbot sistem, indirektno agent
Cilj: Administrator želi unaprijediti chatbot korištenjem kvalitetnih agentovih odgovora.

Preduslovi:

agent je već dao odgovor na neodgovoreno pitanje
administrator ima pristup tim odgovorima

Osnovni tok:

Administrator pregleda agentove odgovore.
Označava odgovor kao koristan za unapređenje sistema.
Sistem dodaje odobreni sadržaj u bazu znanja ili dataset za dalje poboljšanje.

Alternativni tokovi:

administrator može odbiti agentov odgovor ako nije dovoljno kvalitetan
administrator može tražiti dodatnu doradu prije uključivanja u bazu znanja

Ishod:

chatbot baza znanja je unaprijeđena na osnovu stvarnih slučajeva iz prakse