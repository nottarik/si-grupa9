# Sprint Review Summary

**Datum pregleda:** 19. maj 2026

---

## Pregled sprinta

Sprint 7 bio je fokusiran na implementaciju funkcionalnosti za obradu transkripata i izgradnju baze znanja koja predstavlja osnovu za budući rad chatbot sistema i semantičke pretrage. Tokom sprinta implementirane su funkcionalnosti za normalizaciju i obradu transkripata, maskiranje osjetljivih podataka, generisanje embeddinga i pohranu podataka u vektorsku bazu, kao i prikaz statusa obrade u administratorskom interfejsu.

Sve planirane stavke za ovaj sprint su završene i demonstrirane tokom sprint review sastanka.

---

## Isporučene stavke

| ID | Naziv stavke | Tip | Prioritet | Procjena napora | Status |
|----|--------------|-----|-----------|-----------------|--------|
| PB-23 | Priprema za obradu transkripata | Technical Task | High | 13 | Završeno |
| PB-26 | Maskiranje osjetljivih podataka | Technical Task | High | 5 | Završeno |
| PB-27 | Izgradnja baze znanja | Feature | High | 13 | Završeno |
| PB-46 | Prikaz statusa obrade transkripata | Feature | Medium | 5 | Završeno |

---

## Istaknuta dostignuća

### Normalizacija i razdvajanje transkripata (PB-23)

Implementirana je priprema transkripata za dalju obradu kroz normalizaciju teksta i razdvajanje sadržaja po ulogama Agent/Korisnik. Sistem sada automatski uklanja nepotrebne razmake, standardizuje tekst i organizuje poruke prema učesnicima razgovora, što omogućava stabilniju i precizniju obradu podataka u narednim koracima pipeline-a.

### Maskiranje osjetljivih podataka (PB-26)

Dodana je funkcionalnost za automatsku detekciju i maskiranje osjetljivih podataka kao što su JMBG, brojevi telefona i lični podaci prije dalje obrade transkripata. Time je unaprijeđena zaštita privatnosti korisnika i smanjen rizik od obrade osjetljivih informacija unutar sistema.

### Generisanje embeddinga i pohrana u vektorsku bazu (PB-27)

Implementiran je proces generisanja embeddinga iz obrađenih transkripata te njihova pohrana u vektorsku bazu podataka Qdrant. Ovim je postavljena osnova za buduću semantičku pretragu i rad AI funkcionalnosti koje će koristiti bazu znanja za generisanje relevantnih odgovora.

### Prikaz statusa obrade transkripata (PB-46)

Administratorski interfejs proširen je prikazom statusa obrade transkripata. Administrator sada može pratiti stanje obrade kroz statuse poput Pending, Processing, Completed i Failed, kao i uočiti eventualne greške tokom procesa obrade podataka.

---

## Demonstrirane funkcionalnosti

Tokom sprint review sastanka demonstrirane su sljedeće funkcionalnosti:

- Normalizacija tekstualnih transkripata
- Razdvajanje transkripata po ulogama Agent/Korisnik
- Automatsko maskiranje osjetljivih podataka
- Generisanje embeddinga za transkripte
- Pohrana embeddinga u Qdrant vektorsku bazu
- Prikaz statusa obrade transkripata u administratorskom UI-u
- Prikaz grešaka tokom obrade transkripata

---

## Glavni izazovi tokom sprinta

Najveći izazov tokom sprinta bio je povezivanje pipeline-a za obradu transkripata sa vektorskom bazom podataka i osiguravanje pravilnog toka obrade između više koraka sistema. Posebna pažnja bila je potrebna prilikom validacije i maskiranja podataka kako bi se osiguralo da obrada ne utiče na semantičko značenje transkripata.

Dodatni izazov predstavljalo je pravilno prikazivanje statusa obrade i grešaka u administratorskom interfejsu u realnom vremenu.

---

## Povratna informacija Product Ownera

Product Owner je pozitivno ocijenio napredak ostvaren u oblasti obrade transkripata i izgradnje baze znanja, posebno implementaciju maskiranja osjetljivih podataka i prikaza statusa obrade.

Tokom review sastanka savjetovano je da tim pojača rad na projektu, odnosno ubrza realizaciju većeg broja user storija i Product Backlog stavki u okviru jednog sprinta kako bi se povećao ukupni tempo razvoja projekta.

---

## Zaključak

Sprint 7 uspješno je postavio tehničku osnovu za dalji razvoj AI i RAG funkcionalnosti sistema kroz obradu transkripata, generisanje embeddinga i izgradnju baze znanja. Sve planirane stavke sprinta su završene, a sistem sada posjeduje osnovne mehanizme potrebne za semantičku pretragu i dalju obradu podataka.

Naredni sprintovi fokusiraće se na dalje unapređenje AI pipeline-a, optimizaciju pretrage i proširenje funkcionalnosti administratorskog interfejsa.
