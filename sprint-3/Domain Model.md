Domain Model — AI Chatbot Asistent za Call Centar
Sistem za treniranje i implementaciju AI chatbot asistenta na osnovu transkripata poziva

1. Glavni entiteti
Korisnik
Korisnik
Svaka osoba koja pristupa sistemu, s definisanom ulogom (RBAC)
PK korisnikId	UUID	Primarni ključ
ime	String	Ime korisnika
prezime	String	Prezime korisnika
email	String	Jedinstvena email adresa, koristi se za prijavu
lozinkaHash	String	Bcrypt hash lozinke, nikad plain text
uloga	Enum	Administrator Agent Supervizor KrajnjiKorisnik
aktivan	Boolean	Soft-delete: neaktivni korisnici ne mogu se prijaviti
datumKreiranja	DateTime	Timestamp kreiranja naloga
posljednjaAktivnost	DateTime	Timestamp posljednje uspješne prijave
Transkript
Transkript
Zapis telefonskog poziva — ulazni sirovi podatak sistema
PK transkriptId	UUID	Primarni ključ
FK ucitaoKorisnikId	UUID	Korisnik koji je uploadovao transkript
nazivFajla	String	Originalno ime uploadovanog fajla
izvor	Enum	AudioZapis TekstualniTranskript ManualniUnos
statusObrade	Enum	CekaNaObradu UObradi Obrađen Greška
siroviTekst	Text	Puni tekst transkripta (može biti i STT izlaz)
trajanjeSekundi	Integer	Dužina poziva u sekundama (null za tekstualni unos)
jezikKoda	String	ISO 639-1 kod (npr. bs, sr, hr, en)
kvalitetOcjena	Float	0.0–1.0 automatska ocjena kvaliteta transkripta
maskiran	Boolean	Da li su PII podaci maskirani u tekstu
datumPoziva	Date	Datum originalnog poziva (može biti stariji od uploada)
datumUploada	DateTime	Timestamp unosa u sistem
SegmentTeksta
SegmentTeksta
Chunk transkripta koji se koristi za RAG retrieval i embedding
PK segmentId	UUID	Primarni ključ
FK transkriptId	UUID	Transkript iz kojeg je segment izdvojen
FK kategorijaId	UUID	Automatski ili manualno dodijeljena kategorija
sadrzaj	Text	Tekst segmenta (obično 200–500 tokena)
redoslijedUTranskriptu	Integer	Pozicija chunkа unutar transkripta
tipSadrzaja	Enum	Pitanje Odgovor SmjenaGovornika Mješovito
govornik	Enum	Agent Korisnik Nepoznato
embedding	Vector(1536)	Numerički embedding vektor za semantičko pretraživanje
odobrioAdminId	UUID / null	Admin koji je odobrio segment za bazu znanja (null = automatski)
statusAprovacije	Enum	Na_čekanju Odobreno Odbijeno
datumKreiranja	DateTime	Timestamp ekstrakcije segmenta
BazaZnanja
BazaZnanja
Kurirani par pitanje–odgovor koji chatbot direktno koristi
PK unos_id	UUID	Primarni ključ
FK kategorijaId	UUID	Kategorija pitanja
FK izvorSegmentId	UUID / null	Segment iz kojeg je unos izveden (null = manualni unos)
FK kreiraoKorisnikId	UUID	Korisnik (admin/agent) koji je unos kreirao ili odobrio
pitanje	Text	Kanonska formulacija pitanja
odgovor	Text	Kurirani odgovor koji chatbot koristi
embedding	Vector(1536)	Embedding pitanja za retrieval
status	Enum	Aktivan Nacrt Arhiviran
pouzdanostOcjena	Float	0.0–1.0 ocjena pouzdanosti odgovora
brojKoriscenja	Integer	Koliko puta je ovaj unos vraćen kao rezultat retrievala
datumKreiranja	DateTime	Timestamp prvog unosa
datumIzmjene	DateTime	Timestamp posljednje izmjene
Kategorija
Kategorija
Logička grupacija sadržaja baze znanja
PK kategorijaId	UUID	Primarni ključ
naziv	String	Naziv kategorije (npr. Fakturisanje, Tehnička podrška)
opis	Text	Opis tipa pitanja koja se svrstavaju u ovu kategoriju
roditeljKategorijaId	UUID / null	Roditeljska kategorija za hijerarhijsko grananje (null = root)
aktivna	Boolean	Neaktivne kategorije su skrivene u retrieval koraku
datumKreiranja	DateTime	Timestamp kreiranja
ChatSesija
ChatSesija
Jedna konverzacija između korisnika i chatbota
PK sesijaId	UUID	Primarni ključ
FK korisnikId	UUID / null	Prijavljeni korisnik (null = anonimna sesija)
datumPocetka	DateTime	Timestamp otvaranja sesije
datumZavrsetka	DateTime / null	Timestamp zatvaranja (null = aktivna sesija)
status	Enum	Aktivna Zatvorena EskaliranaAgentu
eskaliraoKorisnikId	UUID / null	Agent/supervizor koji je preuzeo sesiju (null = nije eskalirano)
kanal	Enum	Web MobilnaAplikacija API
ukupnoPoruka	Integer	Denormalizovani broj razmijenjenih poruka (radi efikasnosti)
ipAdresa	String / null	IP adresa klijenta (čuva se za sigurnosni audit)
Poruka
Poruka
Pojedinačna poruka unutar sesije (pitanje ili odgovor)
PK porukaId	UUID	Primarni ključ
FK sesijaId	UUID	Sesija kojoj poruka pripada
sadrzaj	Text	Tekst poruke
uloga	Enum	Korisnik Chatbot Agent
redoslijed	Integer	Redni broj poruke u sesiji
timestamp	DateTime	Tačno vrijeme slanja
latencijaMs	Integer / null	Trajanje generisanja odgovora u ms (samo za Chatbot uloge)
korisceniModelId	String / null	Identifikator LLM modela korišćenog za generisanje (npr. gpt-4o)
retrievaniUnosiIds	UUID[]	Lista ID-eva BazaZnanja unosa vraćenih retrieval korakom
retrieval_score	Float / null	Cosine similarity skor najboljeg retrievanog dokumenta
Feedback
Feedback
Ocjena kvaliteta chatbot odgovora od strane korisnika ili admina
PK feedbackId	UUID	Primarni ključ
FK porukaId	UUID	Chatbot odgovor koji se ocjenjuje
FK autorId	UUID / null	Korisnik koji je ostavio feedback (null = anoniman)
ocjena	Enum	Pozitivan Negativan Neutralan
komentar	Text / null	Opcioni tekstualni komentar uz ocjenu
tipProblema	Enum / null	NetačanOdgovor NepotpunOdgovor HaluciniraniPodatak NeprikladanTon
obradjeno	Boolean	Da li je admin pregledao i reagovao na ovaj feedback
timestamp	DateTime	Timestamp ostavljanja feedbacka
MaskiranjeLog
MaskiranjeLog
Evidencija PII maskiranje nad svakim transkriptom
PK logId	UUID	Primarni ključ
FK transkriptId	UUID	Transkript koji je maskiran
tipEntiteta	Enum	ImePrezime BrojTelefona Email JMBG BrojRačuna Adresa
originalnaVrijednost	String (enc.)	Enkripcijom zaštićena originalna vrijednost (za audit svrhe)
maskToken	String	Zamjenski token u tekstu (npr. [OSOBA_1], [TELEFON_2])
pozicijaPocetak	Integer	Char offset u sirovom tekstu (početak)
pozicijaKraj	Integer	Char offset u sirovom tekstu (kraj)
algoritam	String	Naziv NER modela ili regex pravila korišćenog za detekciju
timestamp	DateTime	Timestamp maskiranje operacije
AuditLog
AuditLog
Neizmjenjiva evidencija svih izmjena nad bazom znanja
PK auditId	UUID	Primarni ključ
FK korisnikId	UUID	Ko je izvršio akciju
entitetTip	String	Naziv entiteta nad kojim je akcija (npr. BazaZnanja, Kategorija)
entitetId	UUID	ID konkretnog zapisa koji je izmijenjen
akcija	Enum	Kreiranje Izmjena Brisanje Odobravanje Odbijanje Arhiviranje
staraVrijednost	JSONB / null	Snapshot entiteta prije izmjene
novaVrijednost	JSONB / null	Snapshot entiteta nakon izmjene
timestamp	DateTime	Timestamp akcije (indeksiran za efikasno pretraživanje)
ipAdresa	String	IP adresa s koje je akcija izvršena
2. Veze između entiteta
Korisnik – Transkript	1 : N Jedan korisnik može uploadovati više transkripata; svaki transkript ima tačno jednog uploadera
Transkript – SegmentTeksta	1 : N Jedan transkript se dijeli na više segmenata tokom obrade; segment uvijek pripada jednom transkriptu
SegmentTeksta – BazaZnanja	1 : 0..1 Segment može biti izvor za tačno jedan kurirani unos u bazi znanja; unos može biti i manualan (bez izvora)
Kategorija – SegmentTeksta	1 : N Svaki segment dobija jednu kategoriju (automatsku ili manualnu); kategorija grupiše neograničen broj segmenata
Kategorija – BazaZnanja	1 : N Svaki unos u bazi znanja mora imati tačno jednu kategoriju radi organizacije i retrievala
Kategorija – Kategorija	1 : N (self) Hijerarhijska struktura: kategorija može imati podkategorije; root kategorije nemaju roditelja
Korisnik – ChatSesija	1 : N Korisnik može imati više sesija; sesija može biti i anonimna (null korisnikId)
ChatSesija – Poruka	1 : N Sesija sadrži uređeni niz poruka; poruka pripada tačno jednoj sesiji
Poruka – BazaZnanja	N : M Jedan chatbot odgovor može biti zasnovan na više unosa iz baze znanja (retrievaniUnosiIds); isti unos može biti korišten u više odgovora
Poruka – Feedback	1 : 0..1 Jedna chatbot poruka može imati najviše jedan feedback unos od korisnika
Transkript – MaskiranjeLog	1 : N Jedan transkript može imati više maskiranih entiteta; svaki zapis log-a vezan je za tačno jedan transkript
Korisnik – AuditLog	1 : N Svaka izmjena se pripisuje korisniku koji ju je izvršio; korisnik može imati neograničen broj audit zapisa
3. Poslovna pravila važna za model
P1
Obavezno maskiranje prije pohrane: Transkript se ne smije proslijediti retrieval koraku niti pohraniti u SegmentTeksta dok polje maskiran = true nije postavljeno, čime se garantuje privatnost osjetljivih podataka iz poziva.
P2
Aprobacija segmenata: Segment teksta s statusAprovacije = Na_čekanju ne ulazi u embedding indeks niti bazu znanja bez eksplicitnog odobrenja administratora. Automatski odobreni segmenti imaju odobrioAdminId = null.
P3
Prag pouzdanosti odgovora: Ako retrieval_score najboljeg rezultata padne ispod konfigurabilnog praga (default 0.65), sistem mora vratiti standardiziranu poruku o neizvjesnosti umjesto generisanog odgovora, čime se ograničavaju halucinacije.
P4
Eskalizacija sesije: Sesija s status = EskaliranaAgentu mora imati popunjen eskaliraoKorisnikId. Agent koji preuzme sesiju mora imati ulogu Agent ili Supervizor.
P5
Nepromjenjivost AuditLog-a: Zapisi u AuditLog tabeli su append-only — ni jedan zapis se ne smije ažurirati niti brisati, čime se osigurava auditabilnost svih izmjena baze znanja.
P6
RBAC pristup bazi znanja: Samo korisnici s ulogom Administrator mogu mijenjati ili brisati unose u BazaZnanja. Agent može predložiti izmjenu (status = Nacrt), ali finalizacija zahtijeva adminsku aprobaciju. KrajnjiKorisnik ne pristupa admin sučelju.
P7
Integritet kvaliteta transkripta: Transkripti s kvalitetOcjena < 0.4 automatski dobivaju statusObrade = Greška i ne prolaze kroz pipeline ekstrakcije segmenata bez manualnog pregleda administratora.
P8
Feedback loop: Feedback s tipProblema = HaluciniraniPodatak automatski spušta pouzdanostOcjena na vezanom BazaZnanja unosu i postavlja ga u status Nacrt, blokirajući daljnje korišćenje dok admin ne pregleda unos.