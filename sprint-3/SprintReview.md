# Sprint Review Summary

## Sprint 3

---

# 1. Planirani sprint goal

Definisanje osnovne strukture sistema kroz analizu rizika, projektovanje domene i use-case scenarija, kao i postavljanje početnog arhitektonskog pravca i strategije testiranja, kako bi se osigurala stabilna osnova za dalji razvoj sistema.

---

# 2. Šta je završeno

Tim je uspješno izradio sve planirane deliverable-e za ovaj sprint:

- **Risk Register** – Dokumentovano je 30 rizika raspoređenih u šest grupa (rizici podataka, tehnički rizici, projektni i organizacioni rizici, rizici korisničkog iskustva i adopcije, rizici usklađenosti i etike, te operativni rizici). Svaki rizik sadrži opis, uzrok, vjerovatnoću, uticaj, prioritet i konkretan plan mitigacije. Identifikovano je 7 kritičnih, 12 visokih, 10 srednjih i 1 nizak rizik.

- **Use Case Model i Use Case Dijagram** – Definisano je 10 use-case scenarija za tri aktera: Korisnik call centra, Agent call centra i Administrator. Svaki scenarij uključuje cilj, preduslove, osnovni tok, alternativne tokove i ishod. Izrađen je use-case dijagram u alatu Visual Paradigm koji prikazuje sve aktere, slučajeve korištenja te `<<include>>` i `<<extend>>` relacije.

- **Architecture Overview** – Definisana je arhitektura sistema kao modularni monolit sa slojevitim pristupom (Presentation, Application i Data sloj). Opisano je 9 glavnih komponenti sistema, tokovi podataka (obrada transkripata, chatbot tok, feedback tok), ključne tehničke odluke (RAG pristup, vektorska baza, asinhrona obrada) te pregled arhitektonskih rizika i otvorenih pitanja.

- **Non-Functional Requirements (NFR)** – Definisano je 14 mjerljivih i testabilnih NFR stavki pokrivajući kategorije: sigurnost, privatnost, pouzdanost, performanse, skalabilnost, dostupnost, upotrebljivost, auditabilnost, održavanje, tačnost i transparentnost. Svaka stavka sadrži konkretan opis, način provjere i prioritet.

- **Test Strategy** – Definisana je strategija testiranja koja obuhvata sedam nivoa: unit, integraciono, sistemsko, prihvatno (UAT), regresiono, penetracijsko i UI testiranje. Dokumentovana je pokrivenost testiranjem po funkcionalnim oblastima, veza sa acceptance kriterijima user storyja, te top 10 rizika kvaliteta sa strategijama ublažavanja.

---

# 3. Šta nije završeno

Sve planirane stavke za Sprint 3 su uspješno završene.

---

# 4. Demonstrirane funkcionalnosti ili artefakti

Svi urađeni artefakti su uspješno predstavljeni Product Owneru. Pri tome je urađeno:

- **Prezentacija Risk Registra** – Objašnjenje metodologije prioritizacije rizika (vjerovatnoća × uticaj), prikaz distribucije po grupama i prioritetima, te ključni kritični rizici (halucinacije AI modela, sigurnosne ranjivosti, kršenje GDPR-a, loša kvaliteta podataka).
- **Prezentacija Use Case dijagrama** – Objašnjenje toka rada sistema za sve tri korisničke uloge (Korisnik, Agent, Administrator), uključujući scenarije eskalacije i preusmjeravanja na ljudskog agenta.
- **Pregled arhitekture** – Demonstracija kako odabrana slojevita arhitektura s RAG pristupom rješava zahtjeve definisane u projektnoj viziji, uz obrazloženje zašto je modularni monolit odabran umjesto mikroservisa.
- **Prezentacija Test Strategije** – Pregled svih sedam nivoa testiranja, alata koji će se koristiti (Jest, PyTest, Playwright, k6, OWASP ZAP i dr.) te veze test slučajeva sa acceptance kriterijima.
- **Pregled NFR zahtjeva** – Demonstracija mjerljivih kriterija za svaki zahtjev, uz pojašnjenje načina provjere u kasnijim fazama projekta.

---

# 5. Glavni problemi i blokeri

- **Obuhvat Risk Registra** – Izazov je bio odrediti granicu između projektnih i tehničkih rizika te izbjeći preklapanja. Problem je riješen grupisanjem rizika u šest jasno definisanih kategorija s jedinstvenim ID-ovima.
- **Usklađivanje arhitekture s AI fazom** – U ovoj ranoj fazi dizajna bilo je teško precizno predvidjeti sve potrebe AI komponenti (LLM, embeddingi, vektorska baza). Problem je riješen planiranjem modularne arhitekture s apstraktnim slojem koji olakšava zamjenu ili nadogradnju eksternih AI servisa.
- **Definisanje mjerljivih NFR zahtjeva** – Inicijalne NFR stavke bile su preširoko formulisane i nisu bile direktno testabilne. Zahtjevi su refinovani uvođenjem konkretnih pragova (npr. P95 odziv < 3s, tačnost ≥ 85%, maskiranje u roku od 24h).
- **Pokrivenost Use Case scenarija** – Postojala je dilema oko granularnosti scenarija i koje interakcije tretirati kao zasebne use case-ove nasuprot alternativnim tokovima. Problem je riješen konzistentnom primjenom UML smjernica i mapiranjem na user stories.

---

# 6. Ključne odluke donesene u sprintu

- **Odabir arhitektonskog stila** – Odlučeno je za slojevitu (Layered) arhitekturu unutar modularnog monolita radi bržeg razvoja MVP-a, lakšeg testiranja i manje operativne kompleksnosti. Migracija na mikroservise planirana je u kasnijim fazama.
- **RAG pristup za chatbot** – Potvrđeno je da sistem koristi Retrieval-Augmented Generation pristup koji ograničava odgovore na sadržaj baze znanja i smanjuje halucinacije, bez potrebe za treniranjem modela od nule.
- **Penetracijsko testiranje kao obavezni nivo** – Odlučeno je da penetracijsko testiranje (OWASP ZAP, Burp Suite) bude obavezan dio strategije testiranja s obzirom na osjetljivu prirodu podataka i tri različite korisničke uloge s RBAC kontrolom.
- **Privacy-by-design princip** – Usvojen je princip maskiranja PII podataka kao obaveznog koraka u processing pipelineu, uz automatsko brisanje originalnih transkripata u roku od 24 sata (u skladu s GDPR-om i lokalnim propisima).
- **Fokus na automatizovano testiranje** – Dogovoreno je pisanje unit testova paralelno s razvojem funkcionalnosti u narednim sprintovima, uz CI/CD integraciju za regresijsko testiranje.

---

# 7. Povratna informacija Product Ownera

*(Nije zabilježena)*

---

# 8. Zaključak za naredni sprint

Na osnovu završenog trećeg sprinta, za Sprint 4 (posljednji u "human-first" fazi) planira se sljedeće:

- Definisanje Definition of Done (DoD).
- Izrada Initial Release Plan-a.
- Postavljanje tehničkog skeletona sistema i repozitorija.
- Završna validacija dizajna sistema prije prelaska na AI-enabled fazu razvoja.
