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

---

## Zaključak

Sprint 10 označava operativnu zrelost sistema — sa ovim sprintom, sistem nije samo funkcionalan i stabilan, već je i autonoman, skalabilan i produkcijski spreman na svakom nivou: od automatske obrade podataka, kroz cloud deployment, do optimizovanog razvojnog i CI/CD procesa.

Batch procesiranje i scheduled pipeline postavljaju osnovu za trajno ažurnu bazu znanja bez operativnog opterećenja, dok single-click deployment osigurava da buduće verzije sistema mogu biti isporučene brzo i pouzdano. Optimizacija build procesa direktno ubrzava sve buduće iteracije razvoja.

Za naredne faze razvoja važno je nastaviti pratiti pouzdanost scheduled pipeline obrade u produkcijskom okruženju, posebno pri promjenama u eksternim izvorima podataka. Dokumentovanje infrastrukturnih komponenti i deployment procesa treba biti prioritet kako bi tim mogao efikasno upravljati sistemom dugoročno.
