# Sprint Goal — Sprint 7

## Cilj sprinta

Sprint 7 fokusira se na implementaciju ključnih funkcionalnosti za obradu transkripata i izgradnju baze znanja. Fokusiraćemo se na normalizaciju i razdvajanje transkripata po ulogama, zaštitu osjetljivih podataka kroz maskiranje, te pohranu generiranih embeddinga u vektorsku bazu podataka. Pored ovoga, Sprint 7 uključuje prikaz statusa obrade transkripata u administratorskom UI-u, čime omogućavamo administratoru da prati napredak obrade i uoči moguće greške u procesu.

Na kraju ovog sprinta, sistem će biti sposoban automatski normalizirati transkripte, odvojiti ih po ulogama, maskirati osjetljive podatke, generirati embeddinge i pohraniti ih u vektorsku bazu podataka. Administrator će moći pratiti status obrade transkripata i uočiti greške u procesu, čime će dobiti bolji uvid u funkcionalnost sistema.

---

## Šta ovaj sprint isporučuje

**Normalizacija transkripata** je u ovom sprintu uvedena kako bi se tekstualni podaci pripremili za dalju obradu i pohranu. Sistem će automatski ukloniti nepotrebne razmake, standardizirati kapitalizaciju i zamijeniti nevalidne znakove bez mijenjanja semantičkog značenja teksta.

**Razdvajanje transkripata po ulogama (Agent/Korisnik)** omogućava administratoru da jasno vidi ko je govorio u transkriptima. Sistem će automatski razdvojiti tekst po ulogama, a kada oznake nisu jasno definirane, pokušat će inferirati uloge.

**Maskiranje osjetljivih podataka** (JMBG, telefon, ime) će zaštititi privatnost korisnika. Sistem će automatski detektirati i zamijeniti ove podatke prije obrade, čime se osigurava poštovanje propisa o zaštiti podataka.

**Generisanje embeddinga i pohrana u vektorsku bazu** omogućava chatbotu da koristi semantičku pretragu za pružanje relevantnih odgovora. Embeddingi će biti povezani s odgovarajućim transkriptima i pohranjeni u vektorsku bazu podataka (Qdrant).

**Prikaz statusa obrade transkripata** daje administratoru uvid u tok procesa obrade podataka. Sistem će prikazivati statuse kao što su `Pending`, `Processing`, `Completed` ili `Failed`, te će administrator moći vidjeti greške koje nastanu tokom obrade.

---

## Stavke uključene u sprint

| ID   | Naziv stavke                             | Kratak opis                                                                                         | Tip            | Prioritet | Procjena napora | Status   |
|------|------------------------------------------|----------------------------------------------------------------------------------------------------|----------------|-----------|-----------------|----------|
| PB-23 | Priprema za obradu transkripata          | Normalizacija teksta i razdvajanje po ulogama                                                       | Technical Task | High      | 13              | Završeno |
| PB-26 | Maskiranje osjetljivih podataka          | Detekcija i zamjena ličnih podataka prije obrade                                                   | Technical Task | High      | 5               | Završeno |
| PB-27 | Izgradnja baze znanja                   | Generisanje embeddinga, pohrana u vektorsku bazu                                                   | Feature        | High      | 13              | Završeno |
| PB-46 | Prikaz statusa obrade transkripata       | Prikaz statusa obrade i grešaka u administratorskom UI-u                                            | Feature        | Medium    | 5               | Završeno |

---

## Kriterij uspjeha

Sprint se smatra uspješnim ako:

- Transkripti budu pravilno normalizirani i razdvojeni po ulogama bez grešaka.
- Osjetljivi podaci budu uspješno maskirani prije obrade i korisnicima će biti prikazana obavještenja o zamjeni tih podataka.
- Embeddinzi će biti uspješno generisani i pohranjeni u vektorsku bazu, sa svim povezanim transkriptima.
- Administratorski UI će prikazivati tačne statuse obrade transkripata, uključujući greške ako se pojave.



