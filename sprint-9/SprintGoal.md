# Sprint Goal — Sprint 9

## Cilj sprinta

U Sprintu 9 fokus je na stabilizaciji, kvalitetu podataka i pripremi sistema za produkcijsko okruženje. Nakon što je Sprint 8 isporučio funkcionalan end-to-end tok komunikacije između korisnika, chatbota i agenata, ovaj sprint se fokusira na ono što direktno utiče na pouzdanost i kvalitet korisničkog iskustva: precizniju obradu podataka, kvalitetniju bazu znanja, optimizaciju performansi i završno testiranje sistema.

Poseban fokus sprinta stavljen je na kvalitet baze znanja i sigurnost podataka. Poboljšava se maskiranje osjetljivih podataka kako bi svi edge case formati JMBG-a i telefonskih brojeva bili pravilno zaštićeni, dok se ekstrakcija Q&A parova dodatno unapređuje kako bi chatbot odgovarao isključivo na osnovu smislenih i validnih informacija. Paralelno s tim, uvodi se mogućnost ručnog upravljanja bazom znanja kroz unos, pregled i uklanjanje sadržaja.

Sprint također zaokružuje korisničko iskustvo. Korisnici sada mogu ocijeniti kompletan razgovor nakon završetka sesije, chatbot može prikazivati sistemske obavijesti o poznatim problemima ili održavanju, a Chat UI dobija vizualna i UX poboljšanja kako bi aplikacija djelovala profesionalnije i konzistentnije.

Na tehničkoj strani sprint donosi optimizaciju performansi chatbota i završno funkcionalno i regresijsko testiranje ključnih putanja sistema. Cilj je osigurati stabilan, brz i pouzdan sistem spreman za produkcijsku isporuku bez regresija i kritičnih grešaka.

---

## Šta ovaj sprint isporučuje

**Poboljšanje kvaliteta podataka i baze znanja** predstavlja centralni tehnički fokus sprinta. Sistem sada pouzdano maskira osjetljive podatke u svim poznatim formatima, uključujući edge case scenarije za JMBG i telefonske brojeve. Istovremeno se unapređuje ekstrakcija Q&A parova iz transkripata kako bi se eliminisali nepotpuni ili pogrešno povezani parovi koji degradiraju kvalitet odgovora chatbota.

**Upravljanje bazom znanja** dodatno proširuje administratorske mogućnosti. Administrator može ručno unositi validirane Q&A parove direktno u bazu znanja bez potrebe za obradom kompletnog transkripta, pregledati postojeće unose, uklanjati nevažeći sadržaj i kurirati prijedloge prije nego što postanu dio aktivne baze znanja.

**Poboljšanje korisničkog iskustva** uvodi novu formu za ocjenu razgovora po završetku sesije, čime se prikuplja kvalitetnija povratna informacija o radu sistema. Dodatno se uvode sistemske obavijesti kroz baner u chatbotu, dok korisnici dobijaju veću kontrolu nad vlastitim podacima kroz User Settings i upravljanje historijom razgovora.

**Pregled komentara uz ocjene razgovora** omogućava administratorima i agentima dodatni uvid u povratne informacije korisnika. Administrator ima pristup svim komentarima i ocjenama vezanim za razgovore u sistemu, dok agent vidi samo komentare povezane sa sesijama na koje je upravo on odgovorio.

**Optimizacija performansi i testiranje sistema** zatvaraju sprint kroz fokus na stabilnost i spremnost za produkciju. Latencija odgovora chatbota se smanjuje kroz optimizaciju retrieval i LLM procesa, dok se kompletan sistem prolazi kroz end-to-end i regresijsko testiranje kako bi se osiguralo da nove izmjene ne narušavaju postojeće funkcionalnosti.

---

## Stavke uključene u sprint

| ID | Naziv | Prioritet |
|----|-------|-----------|
| PB-56 | Poboljšanje maskiranja PII podataka i ekstrakcije Q&A parova | High |
| PB-57 | Ocjena razgovora po završetku sesije | High |
| PB-58 | Sistemske obavijesti u chatbotu | Medium |
| PB-59 | Mogućnost ručnog unosa Q&A para direktno u bazu znanja bez transkripata | High |
| PB-60 | Pregled i kuriranje sadržaja baze znanja | High |
| PB-61 | Optimizacija performansi chatbota | High |
| PB-62 | Prikaz komentara uz ocjene razgovora u admin i agent panelu | Medium |
| PB-63 | End-to-end i regresijsko testiranje sistema | High |
| PB-64 | User Settings | Medium |
| PB-65 | Brisanje pojedinačnog chata iz historije | Medium |

---

## Kriterij uspjeha

Sprint se smatra uspješnim ako:

- sistem ispravno maskira sve testirane formate JMBG-a, telefonskih brojeva i drugih PII podataka
- ekstrakcija Q&A parova generiše smislen i ispravno povezan sadržaj bez nepotpunih ili nevalidnih unosa
- administrator može ručno dodavati, pregledati i uklanjati sadržaj iz baze znanja
- chatbot koristi ažuriranu i kuriranu bazu znanja bez degradacije relevantnosti odgovora
- korisnik može ocijeniti cijeli razgovor po završetku sesije putem forme za ocjenu
- sistemske obavijesti se pravilno prikazuju korisnicima kada ih administrator aktivira
- Chat UI ima konzistentan i responzivan dizajn na desktop i mobilnim uređajima
- prosječno vrijeme odgovora chatbota bude unutar definisanih performansnih granica
- svi kritični tokovi sistema prolaze end-to-end testiranje bez kritičnih grešaka
- regresijski testovi automatski otkrivaju ponovno pojavljivanje prethodno ispravljenih grešaka
- svi testovi u CI/CD pipeline-u budu uspješni prije produkcijskog deploya