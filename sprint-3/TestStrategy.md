# Test Strategy

## Cilj testiranja

Cilj testiranja je osigurati da AI chatbot sistem funkcioniše ispravno, pouzdano i sigurno u svim ključnim scenarijima korištenja. Testiranjem se provjerava da li sistem pravilno obrađuje transkripte, generiše relevantne odgovore i u slučaju nesigurnosti preusmjerava komunikaciju na ljudskog agenta.  

Također, cilj je potvrditi da su osjetljivi podaci adekvatno zaštićeni, da sistem zadovoljava performanse i stabilnost, te da ispunjava definisane acceptance kriterije i nefunkcionalne zahtjeve za MVP verziju.

---

## Ciljevi testiranja

| Cilj | Obim | Kriterij uspjeha |
|------|------|------------------|
| Verifikacija unosa i uploada transkripata | Validacija formata fajla, ručni unos i pohrana transkripata | Ispunjeni svi acceptance kriteriji iz US-01 i US-02: validan fajl se uspješno učitava i pohranjuje, a nevalidan se odbija uz odgovarajuću poruku |
| Validacija obrade i pripreme transkripata | Parsiranje, normalizacija i maskiranje osjetljivih podataka | Svi lični podaci su maskirani, tekst je pravilno strukturiran i spreman za korištenje u sistemu |
| Verifikacija chatbot odgovora | Generisanje odgovora na osnovu baze znanja | Chatbot daje relevantan odgovor u skladu sa definisanim kriterijima tačnosti (NFR-13) |
| Validacija fallback mehanizma | Preusmjeravanje na agenta kada chatbot nije siguran | Sistem uspješno prepoznaje nesigurnost i preusmjerava razgovor bez gubitka konteksta (NFR-5) |
| Provjera administratorskih funkcionalnosti | Pregled, validacija i upravljanje transkriptima i prijavljenim problemima | Administrator može pregledati, validirati i upravljati podacima bez grešaka |
| Validacija prijave netačnih odgovora | Korisnički feedback i obrada prijavljenih problema | Sistem omogućava prijavu netačnog odgovora i pravilno ga evidentira |
| Provjera sigurnosti i privatnosti podataka | Zaštita podataka i kontrola pristupa | Svi podaci su zaštićeni (HTTPS, RBAC), a lični podaci maskirani prije obrade (NFR-1, NFR-2, NFR-3) |
| Testiranje performansi sistema | Vrijeme odziva i rad pod opterećenjem | Sistem odgovara u roku < 3 sekunde u 95% slučajeva i podržava minimalno 100 korisnika (NFR-7, NFR-8) |
| Validacija pouzdanosti sistema | Stabilnost rada i ponašanje u greškama | Sistem ne generiše netačne odgovore i pravilno reaguje u slučaju greške (NFR-5, NFR-6) |
| Provjera upotrebljivosti sistema | Jednostavnost korištenja UI-a | Korisnici mogu koristiti sistem bez dodatne obuke i bez poteškoća (NFR-10) |

## Nivoi testiranja 
### Unit testiranje

Unit testiranje provjerava ispravnost individualnih komponenti sistema izolovano od ostatka aplikacije. Fokus je na poslovnoj logici unutar pojedinih modula.

| Atribut | Opis |
|--------|------|
| Cilj | Verificirati ispravnost pojedinačnih funkcija i klasa unutar modula |
| Ko testira | Developeri (tokom razvoja) |
| Kada | Kontinuirano tokom svakog sprinta, prije commita koda |
| Alati | Jest (JavaScript/TypeScript), PyTest (Python backend) |
| Pokrivenost | Cilj: minimalno 80% code coverage za poslovnu logiku |

---

### Integraciono testiranje

Integraciono testiranje verificira ispravnost komunikacije i razmjene podataka između više modula sistema koji zajedno ostvaruju određenu funkcionalnost.

| Atribut | Opis |
|--------|------|
| Cilj | Verificirati da moduli ispravno komuniciraju i razmjenjuju podatke |
| Ko testira | Developeri / QA tim |
| Kada | Nakon završetka razvoja modula, na kraju svakog sprinta |
| Alati | Supertest (API testiranje), Postman / Newman (automatizacija API testova) |

---

### Sistemsko testiranje

Sistemsko testiranje verificira kompletan sistem kao cjelinu u okruženju što bližem produkcijskom. Pokriva end-to-end tokove i nefunkcionalne zahtjeve.

| Atribut | Opis |
|--------|------|
| Cilj | Verificirati cjelokupni sistem u realističnom okruženju – funkcionalni i nefunkcionalni zahtjevi |
| Ko testira | QA tim / tester |
| Kada | U fazi stabilizacije sistema (Sprint 11) |
| Alati | Playwright / Cypress (E2E), k6 / JMeter (load testing) |

---

### Prihvatno testiranje (UAT)

Prihvatno testiranje provode krajnji korisnici ili njihovi predstavnici kako bi potvrdili da sistem zadovoljava njihove potrebe i poslovne zahtjeve prije puštanja u produkciju.

| Atribut | Opis |
|--------|------|
| Cilj | Potvrditi da sistem ispunjava poslovne zahtjeve i da je spreman za produkciju |
| Ko testira | Predstavnici krajnjih korisnika (korisnik call centra, agent, administrator) |
| Kada | Na kraju razvojnog ciklusa, neposredno prije završne demonstracije (Sprint 12-13) |
| Alati | Ručno testiranje uz predefinisane test scenarije zasnovane na user stories |

---

## Šta se testira i na kojem nivou

Tabela prikazuje pokrivenost testiranjem po funkcionalnim oblastima.  
Legenda:
- **Da** → primarni nivo testiranja  
- **Djelimično** → sekundarni nivo  
- **-** → nije primjenjivo  

| Funkcionalna oblast / User Story | Unit | Integraciono | Sistemsko | Prihvatno |
|--------------------------------|------|-------------|-----------|-----------|
| US-25/26: Prijava i odjava iz sistema | Da | Da | Da | Da |
| US-1: Upload transkripata (fajl) | Da | Da | Da | Da |
| US-2: Ručni unos transkripata | Da | Djelimično | Da | Da |
| US-3: Validacija transkripata | Da | Da | Djelimično | - |
| US-4 (ID27): Konverzija audio u transkript | Djelimično | Da | Da | Da |
| US-4/5: Pregled i detalji transkripta | - | Djelimično | Da | Da |
| US-6: Pretraga i filtriranje transkripta | Da | Djelimično | Da | Djelimično |
| US-27: Normalizacija teksta | Da | Da | Djelimično | - |
| US-28: Razdvajanje po ulogama | Da | Da | Djelimično | - |
| US-8: Maskiranje osjetljivih podataka | Da | Da | Da | Djelimično |
| US-7: Postavljanje pitanja chatbotu (tekst) | Da | Da | Da | Da |
| US-9: Glasovni unos (Dictate) | Djelimično | Da | Da | Da |
| US-10: Pregled historije razgovora | - | Djelimično | Da | Da |
| US-11: Brisanje historije razgovora | Da | Djelimično | Da | Da |
| US-12: Admin pregled svih pitanja i odgovora | - | Djelimično | Da | Da |
| US-13: Ocjena odgovora chatbota | Da | Da | Da | Da |
| US-14: Komentar uz ocjenu | Da | Djelimično | Da | Da |
| US-15: Pregled prosječne ocjene (admin) | Da | Djelimično | Da | Djelimično |
| US-16: Prijava netačnog odgovora | Da | Da | Da | Da |
| US-17: Kategorizacija prijavljenog problema | Da | Djelimično | Da | Da |
| US-18/19 | - | Djelimično | Da | Da |
| US-20: Promjena statusa prijave | Da | Djelimično | Da | Da |
| US-21: Filtriranje prijavljenih problema | Da | Djelimično | Da | Djelimično |
| US-22: Pregled neodgovorenih pitanja (agent) | - | Djelimično | Da | Da |
| US-23: Unos agentovog odgovora | Da | Da | Da | Da |
| US-24: Upotreba agentovog odgovora za poboljšanje chatbota | Da | Da | Da | Da |
| Izgradnja baze znanja (embedding, RAG) | Da | Da | Da | - |
| Preusmjeravanje na ljudskog agenta | Da | Da | Da | Da |
| NFR: Sigurnost i HTTPS/TLS | - | Da | Da | - |
| NFR: Performanse (odziv <3s, 100 korisnika) | - | - | Da | - |
| NFR: Dostupnost 99%, rad 24/7 | - | - | Da | - |
| NFR: Tačnost chatbota (>= 85%) | - | - | Da | Da |

## Veza sa acceptance kriterijima


## Način evidentiranja rezultata testiranja

Rezultati testiranja će se evidentirati kroz strukturirane test slučajeve (test case-ove) koji su direktno povezani sa user story-ima i njihovim acceptance kriterijima.

Za svaki test slučaj bilježit će se:
- ID testa  
- opis scenarija testiranja  
- povezani acceptance kriterij i user story  
- očekivani rezultat  
- stvarni rezultat  
- status testa (Passed / Failed)  
- napomena ili opis greške (ukoliko postoji)

Rezultati testiranja će se voditi u tabelarnom obliku, dok će se uočene greške evidentirati kao posebne stavke u backlogu.

Za automatizovane testove (unit i integraciono testiranje) koristit će se izvještaji iz testnih alata, dok će se za UI i sistemsko testiranje po potrebi priložiti dodatni dokazi kao što su screenshotovi ili opis izvršenih scenarija.

Ovakav pristup omogućava jasnu sljedivost između zahtjeva, testova i rezultata, te olakšava praćenje kvaliteta sistema kroz razvoj.

---

## Glavni rizici kvaliteta

Testiranjem sistema mogu se identificirati sljedeći ključni rizici kvaliteta:

- **Netačni ili nepouzdani odgovori chatbot-a**  
  Postoji rizik da chatbot generiše netačne ili izmišljene odgovore, posebno za pitanja koja nisu pokrivena bazom znanja.

- **Neispravno maskiranje osjetljivih podataka**  
  Lični podaci iz transkripata mogu ostati neadekvatno zaštićeni, što predstavlja sigurnosni i pravni rizik.

- **Neispravan fallback mehanizam**  
  Sistem može neuspješno prepoznati situacije nesigurnosti ili ne preusmjeriti razgovor na agenta, što utiče na korisničko iskustvo.

- **Greške u obradi i pohrani transkripata**  
  Nepravilna validacija ili obrada transkripata može dovesti do gubitka ili pogrešnog prikaza podataka.

- **Neautorizovan pristup administratorskom dijelu sistema**  
  Nedovoljno osigurana autentifikacija i autorizacija mogu omogućiti pristup osjetljivim funkcionalnostima neovlaštenim korisnicima.

- **Pad performansi sistema pod opterećenjem**  
  Sistem može postati spor ili nestabilan pri većem broju istovremenih korisnika.

- **Nedovoljna upotrebljivost korisničkog interfejsa**  
  Nejasan ili nepraktičan UI može otežati korištenje sistema krajnjim korisnicima i administratorima.

- **Regresije nakon izmjena sistema**  
  Nove funkcionalnosti mogu nenamjerno pokvariti postojeće funkcionalnosti ukoliko se ne provodi adekvatno regresiono testiranje.
