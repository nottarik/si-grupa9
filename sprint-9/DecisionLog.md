# Decision log

## **ID:** DL-23

**Datum:** 20/05/2026

**Naziv:** Kontekstni meni za brisanje pojedinačnih chat sesija

**Opis:**
Korisnici su trebali mogućnost brisanja pojedinih razgovora iz historije chata. Bilo je potrebno odlučiti kako izložiti tu akciju u korisničkom interfejsu bez narušavanja preglednosti liste i bez uvođenja previše koraka za jednostavnu radnju.

**Razmatrane opcije:**
- Dugme za brisanje vidljivo uz svaku stavku historije
- Kontekstni meni koji se pojavljuje desnim klikom
- Dugme za brisanje unutar otvorene chat sesije
- Grupno brisanje sesija kroz odabir s checkboxovima

**Odabrana opcija:**
Kontekstni meni pri desnom kliku na stavku historije.

**Razlog izbora:**
Desni klik je uobičajen obrazac za destruktivne akcije jer ne zauzima prostor u UI-u i ne ometa primarni tok korištenja historije. Korisnici koji žele brisati mogu to učiniti bez da im akcija smeta tokom normalnog pregledavanja razgovora. Grupno brisanje nije bilo potrebno u ovom sprintu jer je `Delete all history` već dostupno kroz korisnički meni.

**Posljedice odluke:**

**Pozitivne:**
- lista historije ostaje pregledna bez dodatnih kontrola
- destruktivna akcija nije dostupna slučajnim klikom
- kontekstni meni se može proširiti o dodatne opcije u budućim sprintovima

**Negativne:**
- korisnici na touch uređajima nemaju desni klik; akcija brisanja im nije dostupna ovim putem
- kontekstni meni mora biti pažljivo pozicioniran da ne izlazi van vidljivog područja

**Status odluke:**
Aktivna

---

## **ID:** DL-24

**Datum:** 21/05/2026

**Naziv:** Singleton instance AI servisa za eliminaciju višekratnog učitavanja modela

**Opis:**
Svaki poziv ka `RagService`, `EmbeddingService`, `LLMService` i `VectorStoreService` prethodno je kreirao novu instancu klase. To je uzrokovalo nepotrebno učitavanje `SentenceTransformer` modela i inicijalizaciju `QdrantClient` konekcije pri svakom zahtjevu, što je negativno uticalo na latenciju.

**Razmatrane opcije:**
- Kreiranje nove instance servisa pri svakom zahtjevu (dotadašnji pristup)
- Singleton instance kroz module-level varijable i getter funkcije
- Dependency injection kroz FastAPI `Depends` mehanizam sa cached instancama
- Eksternalizacija AI servisa na zasebni mikroservis

**Odabrana opcija:**
Singleton instance kroz module-level varijable i getter funkcije (`get_llm_service()`, `get_embedding_service()`, `get_vector_store()`).

**Razlog izbora:**
Module-level singleton je najednostavniji pristup koji ne zahtijeva promjenu potpisa API funkcija niti uvođenje novih FastAPI dependency-ja. `SentenceTransformer`, `QdrantClient` i `Groq` klijent su thread-safe za konkurentnu upotrebu kroz `asyncio.to_thread`, pa singleton ne uvodi race condition rizike. Eksternalizacija na mikroservis bila bi prerana optimizacija za trenutni obim projekta.

**Posljedice odluke:**

**Pozitivne:**
- model se učitava jednom pri prvom zahtjevu i ostaje u memoriji
- latencija odgovora smanjena eliminacijom ponovnog inicijaliziranja servisa
- manji memorijski pritisak jer postoji samo jedna instanca po servisu

**Negativne:**
- stanje singleton instance dijele svi zahtjevi; greška u inicijalizaciji blokira sve naredne pozive
- testovi koji zahtijevaju svježu instancu moraju eksplicitno resetovati modul-level varijablu

**Status odluke:**
Aktivna

---

## **ID:** DL-25

**Datum:** 22/05/2026

**Naziv:** React Portal za renderovanje UserMenu dropdowna van backdrop-filter stacking context-a

**Opis:**
UserMenu dropdown prikazivao se ispod elemenata chat sučelja unatoč `z-index: 9999` i `position: fixed`. Uzrok je bio u tome što `glass-header` CSS klasa koristi `backdrop-filter`, što po CSS specifikaciji kreira novi stacking context i zarobljava sve `position: fixed` potomke unutar njega bez obzira na `z-index` vrijednost.

**Razmatrane opcije:**
- Povećanje `z-index` vrijednosti na višu vrijednost
- Premještanje dropdown elementa u DOM izvan header elementa ručnom manipulacijom
- Uklanjanje `backdrop-filter` iz `glass-header` CSS klase
- Korištenje `ReactDOM.createPortal` za renderovanje dropdowna direktno u `document.body`

**Odabrana opcija:**
`ReactDOM.createPortal(dropdown, document.body)` za renderovanje dropdowna van DOM stabla header elementa.

**Razlog izbora:**
Portal je standardni React mehanizam za ovaj slučaj upotrebe. Uklanjanje `backdrop-filter` narušilo bi vizuelni identitet aplikacije. Ručna DOM manipulacija nije prihvatljiva u React aplikaciji. Povećanje `z-index`-a ne rješava temeljni uzrok jer CSS stacking context nije pitanje `z-index` vrijednosti nego CSS svojstava roditelja.

**Posljedice odluke:**

**Pozitivne:**
- dropdown se uvijek prikazuje iznad svih elemenata bez obzira na CSS stacking context roditelja
- rješenje radi na svim mjestima gdje se `UserMenu` koristi (`ChatWindow`, `HomePage`)
- vizuelni stil `glass-header` ostaje nepromijenjen

**Negativne:**
- element renderiran kroz portal nije vidljiv u React DevTools stablu na uobičajeni način
- event propagacija između portala i roditelja funkcioniše prema React pravilima, ali može zbuniti developere koji nisu upoznati s portalima

**Status odluke:**
Aktivna

---

## **ID:** DL-26

**Datum:** 24/05/2026

**Naziv:** Modalni prikaz konkretne chat sesije u admin Ratings umjesto navigacije na Chat Logs

**Opis:**
Dugme za pregled chata vezanog za komentar korisnika prethodno je navigiralo na Chat Logs stranicu s predfiltriranim parametrima (tekst pitanja i datum). Ovaj pristup prikazivao je sve logove koji odgovaraju filtru, a ne samo konkretnu sesiju za koju je komentar ostavljen.

**Razmatrane opcije:**
- Navigacija na Chat Logs s predfiltriranim parametrima (dotadašnji pristup)
- Modalni prozor koji prikazuje poruke konkretne sesije direktno u Ratings sekciji
- Nova zasebna stranica za prikaz detalja sesije
- Proširenje Chat Logs komponente da podržava direktan link na sesiju po ID-u

**Odabrana opcija:**
Modalni prozor unutar `Ratings` komponente koji dohvata i prikazuje poruke konkretne sesije.

**Razlog izbora:**
Navigacijom prema Chat Logs gubio se kontekst Ratings sekcije i prikazivali su se svi logovi koji odgovaraju filtru. Modalni prozor zadržava admina u Ratings sekciji i prikazuje tačno onaj razgovor za koji je komentar ostavljen, bez rizika pogrešne identifikacije sesije. Novi zasebni admin endpoint osigurava da se sesija dohvata po ID-u bez provjere vlasništva, što je odgovarajuće za admin ulogu.

**Posljedice odluke:**

**Pozitivne:**
- admin vidi tačno onaj razgovor koji je korisnik ocijenio
- kontekst Ratings sekcije se zadržava; nema navigacije amo-tamo
- prikaz je brži jer se dohvata samo jedna sesija umjesto liste svih logova

**Negativne:**
- modal ne prikazuje sve metapodatke sesije (status, kanal pristupa) koji su vidljivi u Chat Logs
- dodaje se novi admin endpoint koji zaobilazi provjeru vlasništva, što zahtijeva pažljivo održavanje RBAC provjere

**Status odluke:**
Aktivna

---
