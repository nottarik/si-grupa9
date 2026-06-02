# Sprint Retrospektiva — Sprint 10

---

## Šta je išlo dobro

- Sve četiri planirane stavke sprinta su uspješno implementirane i isporučene bez kritičnih blokatora, čime je sprint završen s punim opsegom isporuke.
- Optimizacija build procesa pokazala je izuzetne rezultate — smanjenje build vremena sa više od 25 minuta na 10–15 sekundi za cached rebuildove direktno je uticalo na produktivnost tima tokom cijelog sprinta.
- Single-click deployment skripta prošla je kroz višestruka testiranja na čistim okruženjima i pokazala visok nivo pouzdanosti i konzistentnosti, bez potrebe za ručnim intervenisanjem.
- Uvođenje scheduled pipeline obrade i batch importa prošlo je glatko zahvaljujući dobro postavljenoj osnovi iz prethodnih sprintova — postojeći transcript pipeline ostao je nepromijenjen i integrisan bez regresija.

---

## Refleksija na tim i proces

Sprint 10 bio je tehnički i infrastrukturno najzahtjevniji sprint do sada, s fokusom koji se značajno razlikovao od prethodnih sprintova. Umjesto dodavanja korisničkih funkcionalnosti, tim je radio na automatizaciji, DevOps infrastrukturi i optimizaciji — oblastima koje zahtijevaju drukčiji pristup planiranju, testiranju i provjeri isporuke.

Poseban izazov predstavljalo je testiranje scheduled pipeline obrade — validacija autonomnog ponašanja sistema zahtijeva simulaciju vremenskih uslova i eksternih izvora, što je uvelo novu dimenziju u testnu strategiju tima. Tim je ovaj izazov riješio kroz kombinaciju unit testova za pojedinačne pipeline faze i integracionih testova koji su simulirali kompletan flow na testnim podacima.

Batch procesiranje i deduplikacija fajlova zahtijevali su pažljivo upravljanje rubnim slučajevima — posebno oko verzionisanja izmijenjenih fajlova i ponašanja sistema pri djelimično prekinutom batch importu. Ovo je dovelo do nekoliko iteracija i revizija acceptance criterija tokom sprinta, što je produljilo implementaciju, ali je rezultiralo znatno robusnijim rješenjem.

Komunikacija unutar tima ostala je efikasna i u ovom sprintu, posebno pri usklađivanju backend pipeline komponenti s frontend prikazom live statusa obrade. WebSocket integracija za live prikaz napretka zahtijevala je koordinaciju između backend i frontend dijela tima, ali je implementirana bez značajnih kašnjenja.

Uz infrastrukturne stavke, sprint je uključivao i tri funkcionalnosti usmjerene na integritet podataka, administratorsku efikasnost i korisničko iskustvo. Implementacija prevencije duplih unosa u bazu znanja zahtijevala je pažljivo definisanje graničnih slučajeva — posebno oko toga koji se unosi tretiraju kao identični i kako se ponašanje razlikuje ovisno o izvoru unosa. Bulk brisanje razgovora iz Chat Logs implementirano je konzistentno s već postojećim obrascem na stranici transkripata, što je ubrzalo razvoj i osiguralo konzistentno korisničko iskustvo u admin panelu. Standardizacija poruka o greškama zahtijevala je pregled svih tačaka gdje sistem komunicira s korisnikom — rezultat je konzistentno, jasno korisničko iskustvo bez izlaganja internih tehničkih detalja.

---

## Zaključak

Sprint 10 označava operativnu zrelost sistema — sa ovim sprintom, sistem nije samo funkcionalan i stabilan, već je i autonoman, skalabilan i produkcijski spreman na svakom nivou: od automatske obrade podataka, kroz cloud deployment, do optimizovanog razvojnog i CI/CD procesa. Prevencija duplikata, bulk administracija i ujednačene poruke o greškama dodatno podižu kvalitet sistema na korisnički i operativni nivo.

Batch procesiranje i scheduled pipeline postavljaju osnovu za trajno ažurnu bazu znanja bez operativnog opterećenja, dok single-click deployment osigurava da buduće verzije sistema mogu biti isporučene brzo i pouzdano. Optimizacija build procesa direktno ubrzava sve buduće iteracije razvoja.

Za naredne faze razvoja fokus treba biti na stabilizaciji sistema, kvalitetu i testiranju, zatvaranju ključnih funkcionalnih rupa te pripremi za završnu demonstraciju.
