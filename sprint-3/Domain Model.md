# Domain Model – AI Chatbot Asistent na osnovu Call Centar Poziva

---

## 1. Glavni entiteti

* **Korisnik:** Osoba koja pristupa sistemu. Uloga (Administrator, Call Centar Agent, Supervizor, Krajnji Korisnik) određuje nivo pristupa putem RBAC-a
* **Poziv/Transkript:** Izvorni snimak ili tekstualni transkript razgovora iz call centra koji služi kao sirovi podatak za izgradnju baze znanja
* **Segment:** Izdvojeni dio transkripta koji predstavlja jedan par pitanje–odgovor ili relevantnu tematsku cjelinu
* **BazaZnanja:** Kolekcija validiranih i obrađenih segmenata koji chatbot koristi za generisanje odgovora
* **Kategorija:** Tematska grupa kojoj pripada segment ili unos u bazi znanja (npr. reklamacije, fakturisanje, tehnička podrška)
* **ChatSesija:** Jedna sesija razgovora između krajnjeg korisnika i chatbot asistenta
* **Poruka:** Pojedinačna razmjena unutar chat sesije – korisnikovo pitanje ili chatbotov odgovor
* **Odgovor:** Generisani ili preuzeti odgovor chatbota, vezan za konkretnu poruku i izvor iz baze znanja
* **Feedback:** Ocjena ili komentar korisnika ili administratora vezan za kvalitet konkretnog odgovora
* **Anomalija:** Zapis koji sistem kreira kada chatbot ne može pronaći pouzdan odgovor ili kada je detektovana nedosljednost u podacima

---

## 2. Ključni atributi

| Entitet | Atributi |
| :--- | :--- |
| **Korisnik** | ID, Ime, Prezime, Email, Lozinka, Uloga (RBAC), DatumKreiranja, Aktivan |
| **Poziv/Transkript** | ID, Naziv, DatumPoziva, Trajanje, Format (audio/tekst), Status (Sirovi/Obrađen/Odbačen), ID_Korisnika_koji_je_uploadovao, DatumUploada, Jezik, Kvalitet (Visok/Srednji/Nizak) |
| **Segment** | ID, Tekst, TipSegmenta (Pitanje/Odgovor/Kontekst), PozicijaUTrasnskriptu, ID_Transkripta, Status (Validan/Nevalidan/NaCekanju), ID_Kategorije, PouzdanostScore, DatumEkstrakcije |
| **BazaZnanja** | ID, Naziv, Verzija, DatumKreiranja, Status (Aktivna/Arhivirana/NaCekanju), ID_Administratora, BrojUnosa |
| **UnosBazeZnanja** | ID, Pitanje, Odgovor, ID_BazeZnanja, ID_Kategorije, ID_Segmenta (izvor), StatusAprovacije (Odobren/Odbijen/NaCekanju), DatumKreiranja, DatumAzuriranja, TezinaPouzdanosti |
| **Kategorija** | ID, Naziv, Opis, NadređenaKategorija_ID, Aktivan |
| **ChatSesija** | ID, DatumPocetka, DatumZavrsetka, ID_Korisnika, KanalPristupa (web/mobile/API), Status (Aktivna/Zatvorena), BrojPoruka |
| **Poruka** | ID, Tekst, Tip (KorisnickoP/ChatbotOdgovor), Timestamp, ID_Sesije, ID_Odgovora |
| **Odgovor** | ID, TekstOdgovora, ID_UnosaBazeZnanja (izvor), MetodaGenerisanja (Retrieval/Generativno/Fallback), SkorPouzdanosti, Latencija_ms, ID_Poruke |
| **Feedback** | ID, Ocjena (1–5), Komentar, Tip (KorisnikOcjena/AdminReview), Timestamp, ID_Odgovora, ID_Korisnika |
| **Anomalija** | ID, Opis, Tip (NiskaP ouzdanost/BezOdgovora/KontradiktoranOdgovor/NevalidanPodatak), NivoOzbiljnosti (Kritična/Visoka/Niska), Status (Otvorena/Riješena/Ignorisana), DatumKreiranja, ID_Poruke, ID_Odgovora |

---

## 3. Veze između entiteta

* **Poziv – Segment (1:N):** Jedan transkript može biti razložen na više segmenata. Svaki segment pripada tačno jednom transkriptu
* **Segment – UnosBazeZnanja (1:0..1):** Segment može, ali ne mora biti promovisan u unos baze znanja. Svaki unos baze znanja ima tačno jedan izvorni segment
* **BazaZnanja – UnosBazeZnanja (1:N):** Jedna baza znanja sadrži više unosa, a svaki unos pripada tačno jednoj bazi znanja
* **Kategorija – Segment (1:N):** Svaki segment mora biti kategoriziran. Jedna kategorija može obuhvatati više segmenata
* **Kategorija – UnosBazeZnanja (1:N):** Svaki unos baze znanja mora imati kategoriju, što omogućava filtriranje i organizaciju
* **Kategorija – Kategorija (1:N, samo-referenca):** Kategorije mogu biti hijerarhijske – jedna nadređena kategorija može imati više podkategorija
* **Korisnik – ChatSesija (1:N):** Jedan korisnik može imati više chat sesija. Svaka sesija pripada tačno jednom korisniku
* **ChatSesija – Poruka (1:N):** Jedna sesija sadrži više poruka u hronološkom redoslijedu
* **Poruka – Odgovor (1:0..1):** Korisnikova poruka može rezultirati jednim chatbotovim odgovorom. Chatbotove poruke nemaju odgovor
* **Odgovor – UnosBazeZnanja (N:1):** Više odgovora može biti generisano na osnovu istog unosa iz baze znanja
* **Odgovor – Feedback (1:N):** Jedan odgovor može primiti feedback od više korisnika ili administratora
* **Odgovor – Anomalija (1:0..1):** Ako sistem detektuje problem pri generisanju odgovora, kreira se tačno jedna anomalija vezana za taj odgovor

---

## 4. Poslovna pravila važna za model

1. **Pravilo kvaliteta transkripta:** Transkript čiji je atribut Kvalitet označen kao Nizak ne smije biti automatski promovisan u bazu znanja bez ručnog pregleda i odobravanja od strane administratora

2. **Pravilo pouzdanosti odgovora:** Ako SkorPouzdanosti generisanog odgovora padne ispod definisanog praga (npr. 0.6), sistem automatski kreira entitet Anomalija tipa NiskaPouzdanost i odgovor se korisniku isporučuje s oznakom upozorenja

3. **Pravilo fallback odgovora:** Kada chatbot ne pronađe odgovarajući unos u bazi znanja, generira se standardni fallback odgovor, kreira se Anomalija tipa BezOdgovora, a sesija se opciono eskalira ka živom agentu

4. **RBAC ograničenje:** Samo korisnici s ulogom Administrator mogu odobravati, uređivati ili brisati unose iz baze znanja. Supervizor može pregledati anomalije i feedback, dok Call Centar Agent može jedino pregledavati transkripte i predlagati segmente

5. **Pravilo imutabilnosti feedbacka:** Feedback koji je jednom sačuvan ne može biti izbrisan, kako bi se osigurao integritet evaluacije kvaliteta sistema kroz vrijeme

6. **Pravilo verzioniranja baze znanja:** Svaka promjena na odobrenom unosu u bazi znanja kreira novu verziju tog unosa, a stara verzija se arhivira, čime se omogućava auditabilnost i rollback

7. **Pravilo privatnosti transkripta:** Transkripti se ne smiju direktno izlagati krajnjem korisniku. Chatbot odgovara isključivo na osnovu procesiranih unosa iz baze znanja, a ne sirovim sadržajem poziva

8. **Pravilo obavezne kategorizacije:** Segment ili unos baze znanja ne može biti sačuvan bez dodjeljene kategorije, čime se osigurava konzistentna organizacija znanja
