# AI Usage Log – Claude Code

## AI Usage Log – Zapis 31

**Datum:** 20/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji brisanja pojedinačnih chat sesija putem kontekstnog menija.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji funkcionalnosti koja korisniku omogućava brisanje pojedinih razgovora iz historije chata desnim klikom miša. Fokus je bio na kaskadnom brisanju svih podataka vezanih za sesiju uz poštovanje FK ograničenja u bazi, kao i na optimističnom uklanjanju stavke iz prikaza bez čekanja na potvrdu servera.

**Šta je AI predložio ili generisao:**
- kontekstni meni (context menu) koji se pojavljuje pri desnom kliku na stavku historije
- `DELETE /api/v1/chat/sessions/{session_id}` backend endpoint sa kaskadnim brisanjem
- redoslijed brisanja koji poštuje cirkularne FK veze između `Poruka` i `Odgovor` tabela
- nullifikaciju referenci u `Anomalija` tabeli prije brisanja poruka i odgovora
- optimistično uklanjanje sesije iz liste na frontend strani
- zatvanje context menija klikom van menija ili otvaranjem drugog

**Šta je tim prihvatio:**
- kontekstni meni vezan za desni klik na stavku historije
- kaskadni redoslijed brisanja: nullify Anomalija → delete Feedback → break circular FK → delete Odgovor → delete Poruka → delete Eskalacija → delete ChatSesija
- optimistično uklanjanje sesije iz UI-a bez potrebe za reloadom liste
- zatvaranje context menija klikom van područja menija

**Šta je tim izmijenio:**
- dodan je import `Eskalacija` modela i brisanje eskalacije vezane za sesiju, jer je inicijalni prijedlog uzrokovao FK violation grešku
- pozicioniranje context menija prilagođeno je za `position: fixed` radi ispravnog prikaza

**Šta je tim odbacio:**
- dialog za potvrdu brisanja kao dodatni korak koji usporava tok
- batch brisanje sesija kroz isti meni u ovoj fazi

**Rizici, problemi ili greške koje su uočene:**
- FK violation greška pri brisanju sesije koja ima aktivnu eskalaciju; riješeno eksplicitnim brisanjem eskalacije u ispravnom redoslijedu
- brisanje je nepovratno i zahtijeva ispravnu provjeru vlasništva nad sesijom na backend strani

---

## AI Usage Log – Zapis 32

**Datum:** 21/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri optimizaciji performansi backend AI servisa bez narušavanja postojeće funkcionalnosti.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri poboljšanju brzine odgovaranja chatbota kroz tri pristupa: uvođenje singleton instanci AI servisa, paralelno pokretanje klasifikacije upita i generisanja embeddinga, te pametno preskakanje prepisivanja upita za jednostavne slučajeve.

**Šta je AI predložio ili generisao:**
- singleton pattern za `LLMService`, `EmbeddingService` i `VectorStoreService` kroz module-level varijable i getter funkcije
- `asyncio.gather(return_exceptions=True)` za paralelno izvršavanje `classify_intent` i `embed` koraka
- regex patern `_CONTEXT_REF_RE` i `_needs_rewrite()` funkciju za detekciju kada je prepisivanje upita zaista potrebno
- ponovnu upotrebu pretprikupljenog embeddinga ako upit nije rewritean
- smanjenje `max_tokens` za LLM pozive sa 512 na 350 za domenski odgovor i sa 256 na 150 za odgovor bez konteksta

**Šta je tim prihvatio:**
- singleton instance za sve tri AI servisne klase kako bi se izbjeglo višekratno učitavanje modela
- paralelno pokretanje klasifikacije i embeddinga kroz `asyncio.gather`
- heuristiku za preskakanje prepisivanja upita kod kratkih ili samostalnih pitanja
- smanjenje `max_tokens` radi bržih odgovora

**Šta je tim izmijenio:**
- singleton getter funkcije su premještene ispod definicija klasa kako bi se izbjegla greška forward reference
- sve reference na direktno instanciranje servisa u `knowledge.py` i `main.py` zamijenjene su getter pozivima

**Šta je tim odbacio:**
- Redis keširanje embeddinga u ovoj fazi
- uvođenje posebnog background workera samo za AI servis

**Rizici, problemi ili greške koje su uočene:**
- singleton instanca je thread-safe za `Groq`, `QdrantClient` i `SentenceTransformer`, ali je to potrebno verificirati pri promjeni biblioteka
- preskakanje prepisivanja upita može dovesti do lošijeg retrieval-a za kratke ali kontekstualne upite

---

## AI Usage Log – Zapis 33

**Datum:** 21/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri implementaciji korisničkog menija za podešavanja dostupnog klikom na avatar ikonu.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri implementaciji `UserMenu` komponente koja se prikazuje klikom na avatar u gornjem desnom uglu i nudi korisniku opcije za promjenu prikazanog imena, brisanje svih razgovora, brisanje naloga i odjavu. Fokus je bio na jasnoj navigaciji između pogleda unutar dropdowna, ispravnoj povratnoj informaciji korisniku i radu na svim stranicama gdje je ikona vidljiva.

**Šta je AI predložio ili generisao:**
- `UserMenu` komponentu sa internim view stanjem (`main`, `rename`, `confirmHistory`, `confirmAccount`)
- `PATCH /me` backend endpoint za promjenu punog imena korisnika
- `DELETE /me/history` endpoint za kaskadno brisanje svih sesija korisnika
- `DELETE /me` endpoint za potpuno brisanje naloga uz nullifikaciju agent referenci i brisanje svih korisničkih podataka
- pozicioniranje dropdowna kroz `getBoundingClientRect()` i `position: fixed` radi ispravnog prikaza
- zatvanje dropdowna klikom van oblasti menija kroz `mousedown` event listener

**Šta je tim prihvatio:**
- višepoglednu strukturu dropdowna sa inline formom za preimenovanje i potvrdnim ekranima za destruktivne akcije
- backend endpointe za promjenu imena, brisanje historije i brisanje naloga
- `position: fixed` sa koordinatama iz `getBoundingClientRect()` za prikaz dropdowna
- ažuriranje prikazanog imena bez reloada stranice kroz `refreshUser` callback

**Šta je tim izmijenio:**
- `UserMenu` je integrisan i na `HomePage` i u `ChatWindow` s istim setom opcija
- inicijali korisnika se prikazuju u skladu sa funkcijom koja podržava jednodijelna i višedijelna imena

**Šta je tim odbacio:**
- poseban modal za promjenu lozinke koji nije bio u scope-u sprinta
- slanje e-mail potvrde pri brisanju naloga

**Rizici, problemi ili greške koje su uočene:**
- brisanje naloga je nepovratno i zahtijeva jasnu korisničku potvrdu prije izvršavanja
- `DELETE /me/history` mora kaskadno brisati sve sesije uz poštovanje istog FK redoslijeda kao brisanje pojedinačne sesije

---

## AI Usage Log – Zapis 34

**Datum:** 22/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri dijagnostici i ispravci problema s prikazivanjem UserMenu dropdowna koji se pojavljivao ispod elemenata chat interfejsa.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za dijagnostiku uzroka zbog kojeg se UserMenu dropdown prikazivao ispod chat poruka unatoč postavljenom `z-index: 9999` i `position: fixed`. Cilj je bio pronaći izvorni uzrok i implementirati ispravku koja radi u svim dijelovima aplikacije.

**Šta je AI predložio ili generisao:**
- identifikaciju uzroka: `glass-header` CSS klasa koristi `backdrop-filter: blur(18px)` koji kreira novi CSS stacking context i zarobljava sve `position: fixed` potomke unutar njega bez obzira na `z-index`
- korištenje `ReactDOM.createPortal` za renderovanje dropdowna direktno u `document.body`, van DOM stabla header elementa
- potvrdu da portal element nije više potomak `glass-header` elementa pa `z-index` funkcioniše globalno

**Šta je tim prihvatio:**
- `createPortal(dropdown, document.body)` kao ispravku koja garantuje prikaz dropdowna iznad svih elemenata
- zadržavanje `position: fixed` i koordinata iz `getBoundingClientRect()` unutar portala

**Šta je tim izmijenio:**
- dodan import `createPortal` iz `react-dom` u `UserMenu.tsx`
- dropdown `div` omotan je pozivom `createPortal(..., document.body)`

**Šta je tim odbacio:**
- povećanje `z-index` vrijednosti kao privremeno rješenje koje ne rješava temeljni uzrok
- premještanje dropdowna van header-a na razini DOM strukture bez portala

**Rizici, problemi ili greške koje su uočene:**
- elementi renderirani kroz portal nisu vidljivi u React DevTools stablu na uobičajen način
- `mousedown` listener za zatvaranje menija mora pravilno identificirati i portal element kako bi se izbjeglo nenamjerno zatvaranje

---

## AI Usage Log – Zapis 35

**Datum:** 23/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri prikazivanju komentara iz ocjenjivanja u admin Ratings sekciji i naznačavanju kometiranih sesija u agent MyHistory prikazu.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za pomoć pri proširenju postojećeg sistema ocjenjivanja. Na strani admina dodana je sekcija „Recent User Comments" koja prikazuje komentare korisnika uz ocjenu, datum i pitanje. Na strani agenta, sesije koje sadrže komentar vizuelno su istaknute u listi historije, a komentar je prikazan u razvijenom redu sesije.

**Šta je AI predložio ili generisao:**
- proširenje `GET /chat/ratings` endpointa za dohvat posljednjih 20 komentara (Feedback JOIN Odgovor JOIN Poruka)
- prikaz `recent_comments` kartice u admin `Ratings.tsx` sa ocjenom zvjezdicama, datumom i citatom komentara
- proširenje `GET /escalation/my-history` endpointa za dohvat Feedback zapisa vezanog za sesiju eskalacije
- `sesija_feedback` polje u `EscalationItem` tipu na frontendu
- zlatnu `✦` ikonu u Topic koloni `MyHistory` tabele za sesije s komentarom uz tooltip sa tekstom komentara
- prikaz ocjene i komentara u razvijenom redu sesije u `MyHistory` komponenti

**Šta je tim prihvatio:**
- `recent_comments` sekciju u admin Ratings s ocjenom, datumom, komentarom i pitanjem
- `sesija_feedback` polje u agent MyHistory s prikazom ocjene i komentara u razvijenom redu
- vizuelnu oznaku (zlatna ikonica) u listi historije kada sesija ima komentar

**Šta je tim izmijenio:**
- `recent_comments` query koristi `outerjoin` jer ne postoji feedback za sve odgovore
- ikonica i tooltip implementirani su inline bez uvođenja nove komponente

**Šta je tim odbacio:**
- filtriranje historije agenta samo na sesije s komentarima
- prikaz komentara u posebnom modalnom prozoru na agent strani

**Rizici, problemi ili greške koje su uočene:**
- feedback može biti vezan za odgovor ili za sesiju u zavisnosti od toka ocjenjivanja; query mora pokrivati oba slučaja
- komentar može biti prazan string; backend mora filtrirati i `komentar != ""`

---

## AI Usage Log – Zapis 36

**Datum:** 24/05/2026

**Sprint broj:** Sprint 9

**Alat koji je korišten:** Claude Code

**Svrha korištenja:**
Pomoć pri ispravci prikaza chat sesije vezane za komentar u admin panelu i pri ispravci zaštite rute `/agent` od pristupa admin korisnika.

**Kratak opis zadatka ili upita:**
Claude Code je korišten za rješavanje dva problema: (1) dugme „View in Chat Logs" otvaralo je listu svih logova filtriranu po tekstu pitanja umjesto da prikaže konkretnu sesiju; (2) admin korisnik mogao je pristupiti `/agent` ruti direktno, što nije bilo namijenjeno.

**Šta je AI predložio ili generisao:**
- dodavanje `sesija_id` polja u `recent_comments` odgovor backend endpointa
- novi admin endpoint `GET /api/v1/chat/admin/sessions/{session_id}/messages` bez provjere vlasništva nad sesijom
- modalni prozor u `Ratings.tsx` koji prikazuje razgovor specifične sesije umjesto navigacije u Chat Logs
- promjenu u `App.tsx` da `/agent` ruta koristi `requiredRole="agent"` umjesto `requiredRole={["admin", "agent"]}`
- uklanjanje „Agent" linka iz skupa linkova vidljivih admin korisniku u `ChatWindow.tsx`

**Šta je tim prihvatio:**
- modalni prikaz sesije direktno u Ratings sekciji bez navigacije na drugu stranicu
- admin endpoint koji ne provjerava vlasništvo nad sesijom, ali zahtijeva admin rolu
- restrikciju `/agent` rute isključivo na `agent` rolu
- uklanjanje „Agent" navigacijskog linka za admin korisnike

**Šta je tim izmijenio:**
- `onGoToChat` prop i `chatLogsPreset` state su uklonjeni iz `AdminShell` jer više nisu potrebni
- `Ratings` komponenta više ne prima props; modal logika je interna

**Šta je tim odbacio:**
- navigaciju prema Chat Logs s predfiltriranim parametrima kao rješenje
- zadržavanje „Agent" linka za admin rolu u bilo kom obliku

**Rizici, problemi ili greške koje su uočene:**
- admin endpoint za sesiju ne provjerava vlasništvo, što je namjerno ali zahtijeva striktnu provjeru admin role
- modalni prikaz ne prikazuje metapodatke sesije (datum, status) pa je potrebno provjeriti da li je to dovoljno za administrativne potrebe

---
