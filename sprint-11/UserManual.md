# User Manual / Korisnički priručnik

Ovaj priručnik je pisan za **krajnjeg korisnika sistema**, ne za programera. Objašnjava kome je sistem
namijenjen, kako se prijaviti, koje uloge postoje i kako korak-po-korak obaviti najvažnije zadatke.

> **Live aplikacija:** <https://purple-field-0d55d8003.7.azurestaticapps.net/>

---

## 1. Kome je sistem namijenjen

**Call Centar Chatbot** je AI asistent za podršku call centru telekom/ISP operatera. Pomaže da se brzo
dođe do tačnih odgovora na pitanja o internetu, TV-u, mobilnim uslugama, naplati i tehničkoj podršci.
Sistem koriste tri vrste korisnika:

- **Korisnik (user)** — postavlja pitanja chatbotu i, kad treba, biva spojen s živim agentom.
- **Agent** — preuzima eskalirane razgovore, pretražuje bazu znanja i vodi živi chat s korisnikom.
- **Administrator (admin)** — upravlja transkriptima, bazom znanja, korisnicima, ocjenama i obavijestima.

(Postoji i uloga **manager** sa pravima nivoa administracije nad pregledima; u praksi se admin koristi
za sve administrativne radnje.)

---

## 2. Korisničke uloge i šta svaka može

| Uloga | Pristup | Glavne mogućnosti |
|---|---|---|
| `user` | `/chat`, `/home` | chat s botom, ocjena odgovora, historija razgovora, eskalacija na agenta, postavke naloga |
| `agent` | `/agent` (+ chat) | live queue eskalacija, vođenje razgovora s korisnikom, pretraga baze znanja, vlastita historija |
| `admin` | `/admin` (+ sve) | transkripti, baza znanja, korisnici, chat logovi, ocjene, issues, obavijesti, scheduled import |
| `manager` | pregledi nivoa admina | pregled i kontrola podataka |

---

## 3. Kako se korisnik prijavljuje

1. Otvori aplikaciju: <https://purple-field-0d55d8003.7.azurestaticapps.net/>
2. Na Landing stranici klikni **Prijava / Login** (vodi na `/login`).
3. Unesi email i lozinku → **Prijavi se**.
4. Nakon prijave sistem te vodi na ekran prema tvojoj ulozi (korisnik → chat/home, agent → agent panel, admin → admin panel).
5. Novi korisnik se može **registrovati** na login stranici (default uloga je `user`); ulogu kasnije mijenja administrator.

**Odjava:** preko korisničkog menija (UserMenu) u gornjem desnom uglu → **Odjava**.

---

## 4. Testni korisnici (demo kredencijali)

| Uloga | Email | Lozinka |
|---|---|---|
| Administrator | `admin@test.com` | `admin123` |
| Agent | `agent@test.com` | `Agent1234` |
| Korisnik | `user@test.com` | `User1234` |

---

## 5. Opis glavnih ekrana

| Ekran | Putanja | Sadržaj |
|---|---|---|
| Landing | `/` | Uvodna stranica s opisom i prijavom |
| Login | `/login` | Prijava i registracija |
| Chat | `/chat` | Razgovor s AI asistentom, ocjena, eskalacija |
| Home | `/home` | Početni pregled za prijavljenog korisnika |
| Admin panel | `/admin` | Dashboard, Transcripts, Knowledge, Users, Chat Logs, Ratings, Issues, Announcements, Scheduled import |
| Agent panel | `/agent` | Live Queue, aktivni razgovori, KB Lookup, My History |

---

## 6. Korak-po-korak: najvažniji korisnički tokovi

### 6.1 Korisnik — postavljanje pitanja chatbotu
1. Prijavi se kao `user` i otvori **Chat** (`/chat`).
2. U polje za unos upiši pitanje (npr. How do i reset router?") i pošalji.
3. **Očekivani rezultat:** asistent vraća odgovor zasnovan na bazi znanja. Ako je pouzdanost niska, odgovoru se dodaje napomena o nesigurnosti.
4. Ako sistem nema dovoljno siguran odgovor **ili** zatražiš agenta („i want to talk to an agent"), pokreće se **eskalacija** — dobićeš poruku da te spajamo s agentom i poziciju u redu čekanja.

### 6.2 Korisnik — ocjena odgovora
1. Nakon odgovora možeš ostaviti ocjenu (1–5) — na kraju razgovora prikazuje se forma za ocjenu sesije.
2. Možeš dodati komentar i, ako je odgovor netačan, označiti ga kao netačan.
3. **Očekivani rezultat:** ocjena je sačuvana; negativan feedback ili „netačan odgovor" se evidentira kao Issue koji admin može pregledati.

### 6.3 Korisnik — historija razgovora i postavke
1. U korisničkom meniju otvori **Historija** — vidiš ranije razgovore (sa botom i agentima).
2. Možeš obrisati pojedinačni razgovor ili cijelu historiju.
3. U **Postavkama naloga** možeš promijeniti ime, obrisati historiju ili obrisati vlastiti nalog.

### 6.4 Agent — preuzimanje eskalacije i live chat
1. Prijavi se kao `agent` i otvori **Agent panel** (`/agent`).
2. U **Live Queue** vidiš eskalirane upite (pozicija, prioritet, status). Notifikacija stiže kad uđe novi.
3. Klikni **Prihvati (Accept)** na upitu → ulaziš u live chat; status ti postaje „zauzet".
4. Razgovaraj s korisnikom u realnom vremenu (WebSocket). Po potrebi koristi **KB Lookup** za pretragu baze znanja.
5. Kad je problem riješen, klikni **Resolve** → razgovor se zatvara, a po potrebi se Q&A par predlaže za bazu znanja.
6. **Očekivani rezultat:** sesija je riješena, agent oslobođen, korisnik obaviješten ako je napustio razgovor.

### 6.5 Administrator — upload i obrada transkripta
1. Prijavi se kao `admin` i otvori **Admin panel** → **Transcripts / Upload**.
2. Uploaduj tekstualni transkript (format `Agent:` / `Korisnik:`) ili audio fajl.
   - Za audio: prvo se prikazuje **preview transkripta** koji potvrđuješ prije obrade.
3. Nakon potvrde, transkript prolazi kroz pipeline: normalizacija → maskiranje PII → detekcija govornika → chunking → ekstrakcija Q&A → embedding → upis u bazu znanja.
4. **Očekivani rezultat:** u **Pipeline Monitor** pratiš napredak po fazama u realnom vremenu; po završetku Q&A parovi čekaju odobrenje.
   *(Primjer: kao administrator, da bih odobrio prijedlog, otvorim Knowledge → Pending, pregledam par i kliknem Approve; sistem prikaže status i par uđe u bazu znanja.)*

### 6.6 Administrator — kuriranje baze znanja
1. **Admin panel → Knowledge.**
2. **Pending:** pregledaj predložene Q&A parove (iz transkripata, agentskih odgovora, eskalacija) → **Approve** ili **Reject**.
3. **Approved:** pregledaj/uredi/obriši postojeće unose.
4. **Ručni unos:** dodaj validiran Q&A par direktno (sistem generiše embedding i sprema u Qdrant). Duplikati se automatski sprječavaju.

### 6.7 Administrator — korisnici, ocjene, issues, obavijesti
- **Users:** dodjela/izmjena uloga, pregled i brisanje naloga.
- **Ratings:** prosječna ocjena, distribucija, trend, top-ocijenjeni odgovori, komentari.
- **Issues:** anomalije (niska pouzdanost, bez odgovora, negativan feedback) — pregled, status, brisanje (pojedinačno i bulk).
- **Announcements:** postavi baner s porukom o poznatim problemima/održavanju koji vide korisnici u chatu.
- **Chat Logs:** pregled razgovora; bulk brisanje označenih.

### 6.8 Administrator — automatski import sa Google Drive-a
1. **Admin panel → (Drive / Scheduled import).**
2. Pokreni batch import unosom Drive folder URL-a/ID-a, ili podesi raspored (hourly/daily/weekly).
3. **Očekivani rezultat:** sistem preuzima podržane fajlove, preskače duplikate i provlači ih kroz pipeline; status zadnjeg izvršavanja je vidljiv u panelu.

---

## 7. Očekivani rezultat nakon svake veće akcije (sažeto)

| Akcija | Očekivani rezultat |
|---|---|
| Slanje pitanja u chatu | Odgovor iz baze znanja (uz napomenu ako je nesiguran) ili eskalacija na agenta |
| Zahtjev za agentom | Poruka o spajanju + pozicija u redu čekanja |
| Ocjena odgovora | Ocjena sačuvana; negativan feedback → Issue za admina |
| Upload transkripta | Pipeline obrada s live statusom; Q&A parovi na čekanju za odobrenje |
| Approve Q&A para | Par uđe u bazu znanja (embedding + Qdrant) i postaje dostupan u odgovorima |
| Agent Resolve | Sesija zatvorena; korisnik obaviješten |
| Scheduled import | Novi transkripti obrađeni automatski; status izvršavanja prikazan |

---

## 8. Slike ekrana

> Mjesta za snimke ekrana (umetnuti pri finalnoj predaji):
> - `[slika: Login stranica]`
> - `[slika: Chat sa odgovorom i ocjenom]`
> - `[slika: Eskalacija — pozicija u redu]`
> - `[slika: Agent panel — Live Queue]`
> - `[slika: Admin — Pipeline Monitor]`
> - `[slika: Admin — Knowledge Pending/Approved]`

Aplikacija je vizuelno jednostavna i dostupna na linku iznad, pa se ekrani mogu i direktno pogledati.

---

## 9. Objašnjenje ograničenja sistema (šta korisnik NE može raditi)

- Chatbot odgovara **samo na pitanja iz domene** (internet, TV, mobilne usluge, naplata, tehnička podrška). Pitanja van domene dobijaju poruku da asistent ne može pomoći.
- Chatbot **ne izmišlja** odgovore — ako nema pouzdanog izvora u bazi znanja, **eskalira na agenta** umjesto da nagađa.
- **Obični korisnik** ne može pristupiti admin ni agent panelu, mijenjati uloge, niti vidjeti tuđe razgovore.
- **Agent** ne može administrirati korisnike ni bazu znanja kao admin (može predlagati Q&A iz razgovora).
- Sistem **ne prikazuje lične podatke** iz transkripata — PII (imena, telefoni, JMBG, email…) se maskira prije obrade i uklanja iz odgovora.
- Odgovori zavise od dostupnosti vanjskih servisa (Groq, Qdrant, baza); kratki prekidi tih servisa mogu privremeno smanjiti kvalitet/odziv.
- Jezik domene i UI-a je bosanski; chatbot razumije i bosanski i engleski unos.

Potpunija lista ograničenja: vidi `KnownIssues.md`.
