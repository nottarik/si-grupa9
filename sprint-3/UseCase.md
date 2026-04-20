# Use Case Modeli – AI Chatbot Sistem

---

## 1. Postavljanje pitanja chatbotu

**Akter:** Korisnik call centra  
**Naziv use casea:** Postavljanje pitanja chatbotu

**Kratak opis:**  
Korisnik postavlja pitanje chatbotu kako bi dobio odgovor zasnovan na obrađenim unosima iz baze znanja.

**Preduslovi:**
- Chatbot sistem je dostupan
- Korisnik ima pristup chat interfejsu
- Baza znanja je dostupna za pretragu ili je omogućen fallback odgovor

**Glavni tok:**
1. Korisnik otvara chat interfejs
2. Korisnik unosi pitanje
3. Sistem provjerava sadržaj poruke
4. Sistem obrađuje korisnički upit
5. Sistem generiše ili pronalazi odgovor
6. Sistem prikazuje odgovor korisniku

**Alternativni tokovi:**
- Korisnik može postaviti pitanje glasovnim unosom, a sistem ga prvo pretvara u tekst
- Ako poruka sadrži osjetljive podatke, sistem ih maskira prije dalje obrade
- Ako sistem ne pronađe dovoljno pouzdan odgovor, generiše fallback odgovor i može pokrenuti eskalaciju
- Ako dođe do greške pri obradi, sistem prikazuje poruku o grešci

**Ishod:**
Korisnik dobija odgovor chatbota ili fallback odgovor sa eventualnom eskalacijom.

---

## 2. Pregled historije razgovora

**Akter:** Korisnik call centra  
**Naziv use casea:** Pregled historije razgovora

**Kratak opis:**  
Korisnik pregledava prethodne poruke i odgovore iz ranijih chat sesija.

**Preduslovi:**
- U sistemu postoje prethodne chat sesije korisnika
- Korisnik ima pristup modulu za historiju

**Glavni tok:**
1. Korisnik otvara sekciju historije razgovora
2. Sistem dohvaća prethodne sesije i poruke
3. Sistem prikazuje historiju hronološki
4. Korisnik pregledava ranije razgovore

**Alternativni tokovi:**
- Ako nema prethodnih razgovora, sistem prikazuje prazno stanje
- Ako dođe do greške pri učitavanju, sistem prikazuje poruku o grešci

**Ishod:**
Korisniku je prikazana historija razgovora ili odgovarajuća poruka o praznom stanju.

---

## 3. Brisanje historije razgovora

**Akter:** Korisnik call centra  
**Naziv use casea:** Brisanje historije razgovora

**Kratak opis:**  
Korisnik uklanja jedan ili više zapisa iz vlastite historije razgovora.

**Preduslovi:**
- Korisnik ima postojeću historiju razgovora
- Modul za historiju je dostupan

**Glavni tok:**
1. Korisnik otvara historiju razgovora
2. Korisnik odabire zapis ili više zapisa za brisanje
3. Sistem traži potvrdu brisanja
4. Korisnik potvrđuje akciju
5. Sistem uklanja odabrane zapise iz prikaza historije

**Alternativni tokovi:**
- Korisnik odustaje od potvrde i sistem ne vrši brisanje
- Odabrani zapis više ne postoji pa sistem prikazuje poruku o grešci
- Korisnik briše samo jedan zapis ili više zapisa odjednom

**Ishod:**
Odabrani zapisi su uklonjeni iz historije razgovora.

---

## 4. Ocjena odgovora

**Akter:** Korisnik call centra  
**Naziv use casea:** Ocjena odgovora

**Kratak opis:**  
Korisnik ocjenjuje kvalitet dobijenog odgovora kako bi sistem prikupio povratnu informaciju.

**Preduslovi:**
- Korisnik je prethodno dobio odgovor od chatbota
- Odgovor postoji u sistemu

**Glavni tok:**
1. Sistem prikazuje opciju za ocjenu odgovora
2. Korisnik bira ocjenu
3. Sistem pohranjuje ocjenu uz konkretan odgovor
4. Sistem potvrđuje uspješno spremanje ocjene

**Alternativni tokovi:**
- Korisnik može uz ocjenu ostaviti komentar
- Korisnik ne želi ostaviti komentar, već samo ocjenu
- Ako spremanje ne uspije, sistem prikazuje poruku o grešci

**Ishod:**
Odgovor dobija sačuvan feedback korisnika.

---

## 5. Prijava netačnog odgovora

**Akter:** Korisnik call centra  
**Naziv use casea:** Prijava netačnog odgovora

**Kratak opis:**  
Korisnik prijavljuje odgovor koji smatra netačnim, nejasnim ili nerelevantnim.

**Preduslovi:**
- Chatbot je prethodno dao odgovor
- Korisnik je uočio problem u odgovoru

**Glavni tok:**
1. Korisnik bira opciju za prijavu problema
2. Sistem otvara formu za prijavu
3. Korisnik unosi opis problema i po potrebi bira kategoriju
4. Sistem povezuje prijavu s konkretnim odgovorom
5. Sistem sprema prijavu
6. Sistem prikazuje potvrdu uspješnog slanja

**Alternativni tokovi:**
- Korisnik prijavu pokreće nakon negativne ocjene
- Korisnik odustaje prije slanja prijave
- Ako forma nije validno popunjena, sistem ne dozvoljava spremanje

**Ishod:**
Problematičan odgovor je evidentiran za dalju analizu.

---

## 6. Pregled prijavljenih problema

**Akter:** Administrator  
**Naziv use casea:** Pregled prijavljenih problema

**Kratak opis:**  
Administrator pregledava prijavljene netačne odgovore kako bi pratio kvalitet rada sistema.

**Preduslovi:**
- Postoje evidentirane prijave problema
- Administrator ima pristup modulu za pregled prijava

**Glavni tok:**
1. Administrator otvara modul prijavljenih problema
2. Sistem prikazuje listu svih prijava
3. Administrator bira pojedinačnu prijavu
4. Sistem prikazuje detalje prijave
5. Administrator pregleda sadržaj prijave

**Alternativni tokovi:**
- Administrator može filtrirati prijave po statusu, datumu ili vrsti problema
- Ako nema prijava, sistem prikazuje poruku da nema prijavljenih problema
- Ako dođe do greške pri učitavanju, sistem prikazuje poruku o grešci

**Ishod:**
Administrator ima pregled prijavljenih problema i njihovih detalja.

---

## 7. Upravljanje transkriptima

**Akter:** Administrator  
**Naziv use casea:** Upravljanje transkriptima

**Kratak opis:**  
Administrator unosi, pregleda i priprema transkripte za dalju obradu i izgradnju baze znanja.

**Preduslovi:**
- Administrator ima pristup modulu za transkripte
- Podržani su tekstualni i/ili audio formati

**Glavni tok:**
1. Administrator otvara modul za transkripte
2. Administrator pokreće unos novog transkripta
3. Sistem validira ulazne podatke
4. Sistem pokreće pripremu transkripta za obradu
5. Sistem pohranjuje transkript i dodjeljuje mu status
6. Administrator može pregledati sačuvani transkript

**Alternativni tokovi:**
- Administrator unosi transkript putem fajla
- Administrator transkript unosi ručno
- Administrator uploaduje audio zapis koji sistem pretvara u tekst
- Ako je format neispravan ili je sadržaj nevalidan, sistem odbija unos

**Ishod:**
Transkript je evidentiran u sistemu i spreman za dalju obradu ili pregled.

---

## 8. Pregled neodgovorenih pitanja

**Akter:** Agent call centra  
**Naziv use casea:** Pregled neodgovorenih pitanja

**Kratak opis:**  
Agent pregledava pitanja na koja chatbot nije mogao dati pouzdan odgovor.

**Preduslovi:**
- U sistemu postoje eskalirana ili neodgovorena pitanja
- Agent ima pristup modulu za pregled takvih pitanja

**Glavni tok:**
1. Agent otvara modul neodgovorenih pitanja
2. Sistem prikazuje listu pitanja koja čekaju obradu
3. Agent bira jedno pitanje za pregled
4. Sistem prikazuje detalje pitanja i kontekst razgovora

**Alternativni tokovi:**
- Ako nema takvih pitanja, sistem prikazuje prazno stanje
- Agent može filtrirati listu po statusu ili datumu
- Ako dođe do greške pri učitavanju, sistem prikazuje poruku o grešci

**Ishod:**
Agent dobija uvid u pitanja koja zahtijevaju ljudsku intervenciju.

---

## 9. Odgovor agenta na neodgovoreno pitanje

**Akter:** Agent call centra  
**Naziv use casea:** Odgovor agenta na neodgovoreno pitanje

**Kratak opis:**  
Agent daje odgovor na pitanje koje chatbot nije uspio riješiti.

**Preduslovi:**
- Postoji neodgovoreno pitanje u sistemu
- Agent je otvorio detalje pitanja

**Glavni tok:**
1. Agent bira pitanje iz liste neodgovorenih pitanja
2. Sistem prikazuje sadržaj pitanja i kontekst
3. Agent unosi odgovor
4. Sistem sprema odgovor
5. Sistem mijenja status pitanja u odgovoreno
6. Sistem prikazuje odgovor korisniku ili ga evidentira za dalju upotrebu

**Alternativni tokovi:**
- Agent može dopuniti ili ispraviti odgovor prije slanja
- Agent može odgoditi odgovor i ostaviti pitanje u čekanju
- Ako spremanje ne uspije, sistem prikazuje poruku o grešci

**Ishod:**
Korisnik dobija ljudski odgovor ili je odgovor evidentiran kao obrađen slučaj.

---

## 10. Poboljšanje baze znanja chatbota

**Akter:** Administrator  
**Naziv use casea:** Poboljšanje baze znanja chatbota

**Kratak opis:**  
Administrator koristi kvalitetne odgovore i obrađene segmente kako bi unaprijedio bazu znanja chatbota.

**Preduslovi:**
- U sistemu postoje agentovi odgovori ili validirani segmenti
- Administrator ima pristup modulu za upravljanje bazom znanja

**Glavni tok:**
1. Administrator otvara modul za unapređenje baze znanja
2. Sistem prikazuje dostupne prijedloge za unos ili ažuriranje
3. Administrator pregleda sadržaj prijedloga
4. Administrator potvrđuje unos ili izmjenu
5. Sistem ažurira bazu znanja i evidentira promjenu

**Alternativni tokovi:**
- Administrator može odbiti prijedlog
- Administrator može tražiti dodatnu doradu prije odobravanja
- Ako dođe do greške pri ažuriranju, sistem prikazuje poruku o grešci

**Ishod:**
Baza znanja je proširena ili ažurirana novim odobrenim sadržajem.

---

## 11. Upload transkripta putem fajla

**Akter:** Administrator  
**Naziv use casea:** Upload transkripta putem fajla

**Kratak opis:**  
Administrator učitava tekstualni transkript iz podržanog fajla kako bi ga pohranio i pripremio za obradu.

**Preduslovi:**
- Administrator je otvorio modul za unos transkripata
- Fajl postoji na uređaju korisnika
- Sistem podržava format odabranog fajla

**Glavni tok:**
1. Administrator bira opciju za upload fajla
2. Administrator odabire fajl sa svog uređaja
3. Sistem učitava sadržaj fajla
4. Sistem provjerava format i osnovnu validnost sadržaja
5. Sistem pohranjuje transkript kao novi zapis
6. Sistem prikazuje potvrdu uspješnog uploada

**Alternativni tokovi:**
- Ako fajl nije podržanog formata, sistem prikazuje grešku
- Ako je fajl oštećen ili prazan, sistem odbija unos
- Ako administrator odustane od procesa, sistem prekida upload

**Ishod:**
Tekstualni transkript je uspješno učitan ili je administrator obaviješten o problemu.

---

## 12. Ručni unos transkripta

**Akter:** Administrator  
**Naziv use casea:** Ručni unos transkripta

**Kratak opis:**  
Administrator ručno unosi sadržaj transkripta putem forme.

**Preduslovi:**
- Administrator ima pristup formi za unos transkripta
- Obavezna polja su definisana u sistemu

**Glavni tok:**
1. Administrator otvara formu za ručni unos transkripta
2. Administrator unosi tražene podatke i sadržaj razgovora
3. Administrator potvrđuje spremanje
4. Sistem validira unesene podatke
5. Sistem sprema transkript
6. Sistem prikazuje potvrdu o uspješnom unosu

**Alternativni tokovi:**
- Ako obavezna polja nisu popunjena, sistem označava greške
- Ako su podaci neispravni, sistem ne dozvoljava spremanje
- Ako dođe do greške pri spremanju, sistem prikazuje poruku o grešci

**Ishod:**
Transkript je ručno unesen i evidentiran u sistemu.

---

## 13. Konverzija audio zapisa u transkript

**Akter:** Administrator  
**Naziv use casea:** Konverzija audio zapisa u transkript

**Kratak opis:**  
Administrator uploaduje audio zapis poziva, a sistem ga automatski pretvara u tekstualni transkript.

**Preduslovi:**
- Administrator ima pristup modulu za upload audio zapisa
- Audio fajl postoji i podržan je od sistema
- Servis za transkripciju je dostupan

**Glavni tok:**
1. Administrator bira opciju za upload audio fajla
2. Administrator odabire audio zapis
3. Sistem provjerava format i pokreće transkripciju
4. Sistem generiše tekstualni transkript
5. Sistem prikazuje rezultat administratoru
6. Administrator potvrđuje spremanje transkripta
7. Sistem pohranjuje transkript u sistem

**Alternativni tokovi:**
- Ako je audio format nepodržan, sistem prikazuje grešku
- Ako je kvalitet zvuka prenizak, sistem prikazuje upozorenje
- Ako transkripcija ne uspije, sistem evidentira grešku i prekida proces

**Ishod:**
Audio zapis je pretvoren u transkript ili je administrator obaviješten o problemu.

---

## 14. Normalizacija teksta transkripta

**Akter:** Sistem  
**Naziv use casea:** Normalizacija teksta transkripta

**Kratak opis:**  
Sistem automatski čisti i standardizuje tekst transkripta kako bi ga pripremio za dalju obradu.

**Preduslovi:**
- Transkript je prethodno učitan u sistem
- Tekst transkripta je dostupan za obradu

**Glavni tok:**
1. Sistem preuzima tekst transkripta
2. Sistem uklanja nepotrebne razmake i tehnički šum
3. Sistem standardizuje format teksta i interpunkciju
4. Sistem evidentira da je normalizacija završena
5. Sistem prosljeđuje transkript u narednu fazu obrade

**Alternativni tokovi:**
- Ako tekst sadrži nečitljive ili nevalidne znakove, sistem ih uklanja ili označava
- Ako obrada ne uspije, sistem evidentira grešku i označava transkript za ručni pregled

**Ishod:**
Transkript je normalizovan i spreman za naredne korake obrade.

---

## 15. Maskiranje osjetljivih podataka u transkriptu

**Akter:** Sistem  
**Naziv use casea:** Maskiranje osjetljivih podataka u transkriptu

**Kratak opis:**  
Sistem automatski detektuje i zamjenjuje osjetljive podatke u transkriptu prije dalje obrade i korištenja.

**Preduslovi:**
- Transkript je dostupan u tekstualnom obliku
- Pravila za detekciju osjetljivih podataka su definisana

**Glavni tok:**
1. Sistem analizira sadržaj transkripta
2. Sistem detektuje osjetljive podatke poput imena, telefona i JMBG-a
3. Sistem zamjenjuje ili maskira osjetljive vrijednosti
4. Sistem evidentira da je zaštita privatnosti izvršena
5. Sistem prosljeđuje obrađeni transkript u narednu fazu

**Alternativni tokovi:**
- Ako osjetljivi podaci nisu pronađeni, sistem nastavlja obradu bez izmjena
- Ako dođe do greške pri maskiranju, sistem označava transkript za ručni pregled

**Ishod:**
Transkript je očišćen od osjetljivih podataka i spreman za sigurnu obradu.

---

## 16. Razdvajanje transkripta po ulogama i segmentacija

**Akter:** Sistem  
**Naziv use casea:** Razdvajanje transkripta po ulogama i segmentacija

**Kratak opis:**  
Sistem razdvaja dijalog na uloge govornika i izdvaja relevantne segmente razgovora.

**Preduslovi:**
- Transkript je prethodno normalizovan
- Tekst transkripta je dostupan za parsiranje

**Glavni tok:**
1. Sistem analizira strukturu transkripta
2. Sistem prepoznaje oznake govornika ili inferira uloge
3. Sistem razdvaja dijelove razgovora na agenta i korisnika
4. Sistem segmentira transkript na manje logičke cjeline
5. Sistem sprema segmente uz referencu na izvorni transkript

**Alternativni tokovi:**
- Ako oznake govornika nisu jasne, sistem označava segment kao nepoznat
- Ako segmentacija ne uspije u potpunosti, sistem kreira djelimične segmente i označava transkript za dodatni pregled

**Ishod:**
Transkript je razdvojen po ulogama i pretvoren u segmente spremne za dalju obradu.

---

## 17. Kategorizacija segmenata i priprema za bazu znanja

**Akter:** Sistem  
**Naziv use casea:** Kategorizacija segmenata i priprema za bazu znanja

**Kratak opis:**  
Sistem dodjeljuje kategorije segmentima i priprema validne segmente za moguću promociju u bazu znanja.

**Preduslovi:**
- Segmenti su prethodno izdvojeni iz transkripta
- U sistemu postoje definisane kategorije

**Glavni tok:**
1. Sistem učitava izdvojene segmente
2. Sistem analizira sadržaj svakog segmenta
3. Sistem dodjeljuje odgovarajuću kategoriju segmentu
4. Sistem procjenjuje pouzdanost i validnost segmenta
5. Sistem označava segmente kao validne, nevalidne ili na čekanju
6. Sistem priprema validne segmente za pregled i promociju u bazu znanja

**Alternativni tokovi:**
- Ako sistem ne može pouzdano odrediti kategoriju, segment označava za ručni pregled
- Ako segment ne zadovoljava pravila kvaliteta, sistem ga ne predlaže za bazu znanja

**Ishod:**
Segmenti su kategorizirani i pripremljeni za dalji proces odobravanja ili odbacivanja.

---

## 18. Pregled transkripata i predlaganje segmenata

**Akter:** Agent call centra  
**Naziv use casea:** Pregled transkripata i predlaganje segmenata

**Kratak opis:**  
Agent call centra pregledava postojeće transkripte i predlaže korisne segmente za dalju obradu i eventualno uključivanje u bazu znanja.

**Preduslovi:**
- Transkripti postoje u sistemu
- Agent ima pristup modulu za pregled transkripata

**Glavni tok:**
1. Agent otvara modul za pregled transkripata
2. Sistem prikazuje listu dostupnih transkripata
3. Agent bira transkript za pregled
4. Sistem prikazuje detalje transkripta i pripadajuće segmente
5. Agent označava relevantne segmente i predlaže ih za dalju obradu
6. Sistem sprema prijedlog segmenta

**Alternativni tokovi:**
- Ako nema dostupnih transkripata, sistem prikazuje prazno stanje
- Ako segment nije dovoljno jasan, agent odustaje od prijedloga
- Ako spremanje prijedloga ne uspije, sistem prikazuje poruku o grešci

**Ishod:**
Relevantni segmenti su predloženi za pregled i eventualnu promociju u bazu znanja.

---

## 19. Odobravanje unosa u bazu znanja

**Akter:** Administrator  
**Naziv use casea:** Odobravanje unosa u bazu znanja

**Kratak opis:**  
Administrator pregleda pripremljene segmente i odobrava njihov unos u bazu znanja.

**Preduslovi:**
- U sistemu postoje validni ili predloženi segmenti
- Administrator ima pristup modulu za bazu znanja

**Glavni tok:**
1. Administrator otvara modul za pregled prijedloga za bazu znanja
2. Sistem prikazuje listu segmenata i pripadajućih kategorija
3. Administrator pregleda sadržaj i kvalitet prijedloga
4. Administrator odobrava segment za unos u bazu znanja
5. Sistem kreira novi unos baze znanja i povezuje ga s izvornim segmentom
6. Sistem evidentira status odobrenja

**Alternativni tokovi:**
- Administrator odbija segment i sistem evidentira odbijanje
- Ako transkript ima nizak kvalitet, sistem traži ručni pregled prije promocije
- Ako segment nema kategoriju, sistem ne dozvoljava odobravanje

**Ishod:**
Segment je odobren i promovisan u bazu znanja ili je odbijen uz evidentiran status.

---

## 20. Pregled anomalija i feedbacka

**Akter:** Agent call centra  
**Naziv use casea:** Pregled anomalija i feedbacka

**Kratak opis:**  
Agent call centra (ljudski agent) pregledava sistemske anomalije i prikupljeni feedback radi nadzora kvaliteta odgovora i obrade transkripata.

**Preduslovi:**
- U sistemu postoje evidentirane anomalije ili feedback zapisi
- Agent call centra ima pravo pristupa modulu za nadzor kvaliteta

**Glavni tok:**
1. Agent call centra otvara modul za anomalije i feedback
2. Sistem prikazuje listu anomalija i listu feedback zapisa
3. Agent call centra bira zapis za detaljan pregled
4. Sistem prikazuje povezane poruke, odgovore i status anomalije
5. Agent call centra analizira kvalitet i eventualne probleme

**Alternativni tokovi:**
- Ako nema anomalija ili feedbacka, sistem prikazuje prazno stanje
- Agent call centra može filtrirati prikaz po statusu, tipu ili datumu
- Ako dođe do greške pri učitavanju, sistem prikazuje poruku o grešci

**Ishod:**
Agent call centra dobija pregled kvaliteta rada sistema i evidentiranih problema.

---

## 21. Generisanje fallback odgovora i anomalije

**Akter:** Sistem  
**Naziv use casea:** Generisanje fallback odgovora i anomalije

**Kratak opis:**  
Kada sistem ne pronađe dovoljno pouzdan odgovor, generiše fallback odgovor i kreira anomaliju radi daljeg praćenja.

**Preduslovi:**
- Korisničko pitanje je obrađeno
- Sistem nije pronašao odgovor dovoljne pouzdanosti ili nije pronašao odgovor uopšte

**Glavni tok:**
1. Sistem procjenjuje skor pouzdanosti generisanog ili pronađenog odgovora
2. Sistem utvrđuje da je skor ispod definisanog praga ili da odgovor ne postoji
3. Sistem generiše standardni fallback odgovor
4. Sistem kreira anomaliju i povezuje je s porukom i odgovorom
5. Sistem prikazuje fallback odgovor korisniku
6. Sistem po potrebi označava slučaj za eskalaciju agentu

**Alternativni tokovi:**
- Ako je skor pouzdanosti dovoljno visok, sistem ne generiše anomaliju i vraća standardni odgovor
- Ako kreiranje anomalije ne uspije, sistem evidentira internu grešku i ipak korisniku vraća fallback odgovor

**Ishod:**
Korisnik dobija fallback odgovor, a problematičan slučaj se evidentira kao anomalija.

---

## 22. Verzionarno ažuriranje unosa baze znanja

**Akter:** Sistem / Administrator  
**Naziv use casea:** Verzionarno ažuriranje unosa baze znanja

**Kratak opis:**  
Sistem prilikom izmjene odobrenog unosa baze znanja kreira novu verziju unosa i arhivira prethodnu verziju radi auditabilnosti.

**Preduslovi:**
- U bazi znanja postoji odobren unos
- Administrator je pokrenuo izmjenu unosa

**Glavni tok:**
1. Administrator otvara postojeći unos baze znanja
2. Administrator unosi izmjene
3. Sistem provjerava da je unos prethodno odobren
4. Sistem kreira novu verziju unosa
5. Sistem arhivira staru verziju
6. Sistem sprema novu aktivnu verziju i evidentira izmjenu

**Alternativni tokovi:**
- Ako unos nije odobren, sistem sprema izmjene bez verzionog arhiviranja ili traži dodatnu potvrdu, prema pravilima sistema
- Ako dođe do greške pri arhiviranju stare verzije, sistem prekida izmjenu i prikazuje poruku o grešci

**Ishod:**
Nova verzija unosa baze znanja je sačuvana, a prethodna verzija arhivirana.
