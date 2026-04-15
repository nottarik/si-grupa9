# Domain Model — AI Chatbot Asistent za Call Centar

Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu transkripata poziva

---

## 1. Glavni entiteti

* **Korisnik:** Svaka osoba koja pristupa sistemu, s definisanom ulogom (RBAC). Uloge uključuju: Administrator, Agent, Supervizor i KrajnjiKorisnik, koje određuju i kontrolišu nivo pristupa
* **Transkript:** Zapis telefonskog poziva koji predstavlja ulazni sirovi podatak sistema. Može biti učitan kao audio zapis, tekstualni transkript ili manualni unos
* **SegmentTeksta:** Chunk transkripta koji se koristi za RAG retrieval i embedding. Predstavlja obrađenu, kategorizovanu jedinicu teksta pripremljenu za semantičko pretraživanje
* **BazaZnanja:** Kurirani par pitanje–odgovor koji chatbot direktno koristi pri generisanju odgovora. Može biti izveden iz segmenta transkripta ili manualno unesen
* **Kategorija:** Logička grupacija sadržaja baze znanja (npr. Fakturisanje, Tehnička podrška). Podržava hijerarhijsku strukturu s podkategorijama
* **ChatSesija:** Jedna konverzacija između korisnika i chatbota. Prati kanal pristupa, status sesije i mogućnost eskalacije agentu
* **Poruka:** Pojedinačna poruka unutar sesije — može biti od korisnika, chatbota ili agenta. Bilježi latenciju, korišćeni model i retrievane unose
* **Feedback:** Ocjena kvaliteta chatbot odgovora od strane korisnika ili admina, s mogućnošću označavanja tipa problema
* **MaskiranjeLog:** Evidencija PII maskiranje nad svakim transkriptom. Čuva pozicije i zamjenske tokene za sve otkrivene osjetljive podatke
* **AuditLog:** Neizmjenjiva evidencija svih izmjena nad bazom znanja. Bilježi ko je izvršio akciju, nad kojim entitetom i kada

---

## 2. Ključni atributi

| Entitet | Atributi |
| :--- | :--- |
| **Korisnik** | korisnikId, ime, prezime, email, lozinkaHash, uloga (Administrator / Agent / Supervizor / KrajnjiKorisnik), aktivan, datumKreiranja, posljednjaAktivnost |
| **Transkript** | transkriptId, ucitaoKorisnikId, nazivFajla, izvor (AudioZapis / TekstualniTranskript / ManualniUnos), statusObrade, siroviTekst, trajanjeSekundi, jezikKoda, kvalitetOcjena, maskiran, datumPoziva, datumUploada |
| **SegmentTeksta** | segmentId, transkriptId, kategorijaId, sadrzaj, redoslijedUTranskriptu, tipSadrzaja (Pitanje / Odgovor / SmjenaGovornika / Mješovito), govornik, embedding (Vector 1536), odobrioAdminId, statusAprovacije, datumKreiranja |
| **BazaZnanja** | unos_id, kategorijaId, izvorSegmentId, kreiraoKorisnikId, pitanje, odgovor, embedding (Vector 1536), status (Aktivan / Nacrt / Arhiviran), pouzdanostOcjena, brojKoriscenja, datumKreiranja, datumIzmjene |
| **Kategorija** | kategorijaId, naziv, opis, roditeljKategorijaId, aktivna, datumKreiranja |
| **ChatSesija** | sesijaId, korisnikId, datumPocetka, datumZavrsetka, status (Aktivna / Zatvorena / EskaliranaAgentu), eskaliraoKorisnikId, kanal (Web / MobilnaAplikacija / API), ukupnoPoruka, ipAdresa |
| **Poruka** | porukaId, sesijaId, sadrzaj, uloga (Korisnik / Chatbot / Agent), redoslijed, timestamp, latencijaMs, korisceniModelId, retrievaniUnosiIds, retrieval_score |
| **Feedback** | feedbackId, porukaId, autorId, ocjena (Pozitivan / Negativan / Neutralan), komentar, tipProblema (NetačanOdgovor / NepotpunOdgovor / HaluciniraniPodatak / NeprikladanTon), obradjeno, timestamp |
| **MaskiranjeLog** | logId, transkriptId, tipEntiteta (ImePrezime / BrojTelefona / Email / JMBG / BrojRačuna / Adresa), originalnaVrijednost (enc.), maskToken, pozicijaPocetak, pozicijaKraj, algoritam, timestamp |
| **AuditLog** | auditId, korisnikId, entitetTip, entitetId, akcija (Kreiranje / Izmjena / Brisanje / Odobravanje / Odbijanje / Arhiviranje), staraVrijednost, novaVrijednost, timestamp, ipAdresa |

---

## 3. Veze između entiteta

* **Korisnik – Transkript (1:N):** Jedan korisnik može uploadovati više transkripata; svaki transkript ima tačno jednog uploadera
* **Transkript – SegmentTeksta (1:N):** Jedan transkript se dijeli na više segmenata tokom obrade; segment uvijek pripada jednom transkriptu
* **SegmentTeksta – BazaZnanja (1:0..1):** Segment može biti izvor za tačno jedan kurirani unos u bazi znanja; unos može biti i manualan (bez izvora)
* **Kategorija – SegmentTeksta (1:N):** Svaki segment dobija jednu kategoriju (automatsku ili manualnu); kategorija grupiše neograničen broj segmenata
* **Kategorija – BazaZnanja (1:N):** Svaki unos u bazi znanja mora imati tačno jednu kategoriju radi organizacije i retrievala
* **Kategorija – Kategorija (1:N, self):** Hijerarhijska struktura — kategorija može imati podkategorije; root kategorije nemaju roditelja
* **Korisnik – ChatSesija (1:N):** Korisnik može imati više sesija; sesija može biti i anonimna (null korisnikId)
* **ChatSesija – Poruka (1:N):** Sesija sadrži uređeni niz poruka; poruka pripada tačno jednoj sesiji
* **Poruka – BazaZnanja (N:M):** Jedan chatbot odgovor može biti zasnovan na više unosa iz baze znanja; isti unos može biti korišten u više odgovora
* **Poruka – Feedback (1:0..1):** Jedna chatbot poruka može imati najviše jedan feedback unos od korisnika
* **Transkript – MaskiranjeLog (1:N):** Jedan transkript može imati više maskiranih entiteta; svaki zapis log-a vezan je za tačno jedan transkript
* **Korisnik – AuditLog (1:N):** Svaka izmjena se pripisuje korisniku koji ju je izvršio; korisnik može imati neograničen broj audit zapisa

---

## 4. Poslovna pravila važna za model

1. **Obavezno maskiranje prije pohrane:** Transkript se ne smije proslijediti retrieval koraku niti pohraniti u SegmentTeksta dok polje `maskiran = true` nije postavljeno, čime se garantuje privatnost osjetljivih podataka iz poziva.
2. **Aprobacija segmenata:** Segment teksta sa `statusAprovacije = Na_čekanju` ne ulazi u embedding indeks niti bazu znanja bez eksplicitnog odobrenja administratora. Automatski odobreni segmenti imaju `odobrioAdminId = null`.
3. **Prag pouzdanosti odgovora:** Ako `retrieval_score` najboljeg rezultata padne ispod konfigurabilnog praga (default 0.65), sistem mora vratiti standardiziranu poruku o neizvjesnosti umjesto generisanog odgovora, čime se ograničavaju halucinacije.
4. **Eskalizacija sesije:** Sesija sa `status = EskaliranaAgentu` mora imati popunjen `eskaliraoKorisnikId`. Agent koji preuzme sesiju mora imati ulogu Agent ili Supervizor.
5. **Nepromjenjivost AuditLog-a:** Zapisi u AuditLog tabeli su append-only — ni jedan zapis se ne smije ažurirati niti brisati, čime se osigurava auditabilnost svih izmjena baze znanja.
6. **RBAC pristup bazi znanja:** Samo korisnici s ulogom Administrator mogu mijenjati ili brisati unose u BazaZnanja. Agent može predložiti izmjenu (`status = Nacrt`), ali finalizacija zahtijeva adminsku aprobaciju. KrajnjiKorisnik ne pristupa admin sučelju.
7. **Integritet kvaliteta transkripta:** Transkripti sa `kvalitetOcjena < 0.4` automatski dobivaju `statusObrade = Greška` i ne prolaze kroz pipeline ekstrakcije segmenata bez manualnog pregleda administratora.
8. **Feedback loop:** Feedback sa `tipProblema = HaluciniraniPodatak` automatski spušta `pouzdanostOcjena` na vezanom BazaZnanja unosu i postavlja ga u status Nacrt, blokirajući daljnje korišćenje dok admin ne pregleda unos.
