# Sprint Goal — Sprint 8

## Cilj sprinta

U Sprintu 8 fokus je na tome da sistem postane stvarno upotrebljiv za sve aktere — korisnika, agenta i administratora. Nakon što je Sprint 7 izgradio pipeline za obradu transkripata i napunio bazu znanja, ovaj sprint tu bazu stavlja u upotrebu: chatbot sada klasificira upite, odgovara iz baze znanja kada ima relevantan sadržaj, a kada nema — ne izmišlja, već korisnika upućuje na agenta. Uvodi se kompletna real-time komunikacija između korisnika i agenta putem WebSocketa, zasebni agent panel s vlastitim Live Queue-om i pristupom bazi znanja, te niz funkcionalnosti koje poboljšavaju svakodnevno korisničko iskustvo: historija razgovora, glasovni unos i upload audio fajlova s automatskom transkripcijom.

Na kraju ovog sprinta sistem je funkcionalan end-to-end — korisnik postavlja pitanje, chatbot odgovara iz baze znanja ili eskalira na agenta, agent prihvata razgovor i komunicira u realnom vremenu, a cijela sesija se čisto zatvara kada korisnik ili agent završe razgovor.

---

## Šta ovaj sprint isporučuje

**RAG retrieval i LLM klasifikacija** su centralna tehnička isporuka sprinta. Svaki korisnički upit prolazi kroz klasifikaciju — ako postoji relevantan sadržaj u bazi znanja, chatbot odgovara iz nje; ako ne, LLM generira odgovor ili korisnika upućuje na agenta. Chatbot odgovara na pozdrave i općenita pitanja prirodno, bez nepotrebnih eskalacija, a za specifične upite call centra koje ne može pokriti — jasno obavještava korisnika i nudi vezu s agentom.

**Escalation queue i WebSocket komunikacija** zatvaraju loop između korisnika i agenta. Kada korisnik pristane na povezivanje, upit se pojavljuje u escalation queue-u u admin panelu. Agent prihvata upit, otvara se live chat s punom historijom razgovora s chatbotom, a poruke se razmjenjuju u realnom vremenu. Kada korisnik izađe iz razgovora, agent automatski dobija obavijest da je korisnik završio konverzaciju i sesija se zatvara — nema ostavljenih otvorenih konekcija.

**Agent panel** je nova zasebna sekcija, potpuno odvojena od admin panela. Agent vidi samo svoje aktivne sesije u Live Queue-u, može pretraživati bazu znanja tokom razgovora s korisnikom i ima pristup vlastitoj historiji. Admin i dalje vidi sve agente i sve sesije, ali svaki agent radi samo s vlastitim podacima.

**Korisničko iskustvo** je poboljšano kroz tri nove funkcionalnosti: historija razgovora omogućava korisniku pregled svih prethodnih interakcija, glasovni unos omogućava diktiranje pitanja umjesto tipkanja, a upload audio fajlova u admin panelu s automatskom transkripcijom ubrzava punjenje baze znanja snimljenim pozivima bez ručnog prepisivanja.

**Resolving chatova** zaokružuje upravljanje razgovorima — agent označava završene razgovore kao riješene čime se sesija čisto zatvara s obje strane, a razgovor ostaje vidljiv u historiji s odgovarajućim statusom.

---

## Stavke uključene u sprint

| ID | Naziv | Prioritet |
|----|-------|-----------|
| PB-13 | Konvertovanje iz audio zapisa u transkript | High |
| PB-22 | Chat UI — glasovni unos (Dictate) | High |
| PB-48 | Escalation queue u admin panelu | High |
| PB-49 | Historija razgovora korisnika | Medium |
| PB-50 | Automatsko obavještavanje agenta o završetku korisničke sesije | High |
| PB-51 | Agent panel s Live Queue i pristupom bazi znanja | High |
| PB-52 | RAG retrieval i LLM klasifikacija upita | High |
| PB-53 | Obrada osnovne komunikacije sa LLM | High |
| PB-54 | WebSocket komunikacija između korisnika i agenta | High |
| PB-55 | Resolving chatova | Medium |

---

## Kriterij uspjeha

Sprint se smatra uspješnim ako:

- chatbot klasificira upite i odgovara iz baze znanja kada postoji relevantan sadržaj, bez izmišljanja informacija
- chatbot prirodno odgovara na pozdrave i općenita pitanja bez nepotrebne eskalacije na agenta
- kada chatbot nema odgovor, korisnik dobija jasnu poruku i opciju povezivanja s agentom
- eskalirani upit se pojavljuje u escalation queue-u i agent ga može prihvatiti u realnom vremenu
- korisnik i agent razmjenjuju poruke putem WebSocketa bez kašnjenja i bez potrebe za refreshom stranice
- kada korisnik izađe iz razgovora, agent automatski dobija obavijest i sesija se zatvara čisto
- agent panel prikazuje samo sesije i upite dodijeljene prijavljenom agentu
- agent može pretraživati bazu znanja iz vlastitog panela tokom razgovora
- korisnik može pregledati historiju svih prethodnih razgovora
- glasovni unos pretvara govor u tekst i postavlja ga u input polje chata
- upload audio fajla pokreće automatsku transkripciju i transkript je dostupan administratoru na pregled prije pohrane
- agent može označiti razgovor kao riješen čime se sesija čisto zatvara s obje strane
