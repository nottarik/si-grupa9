# Sprint 10 — Preostale User Stories

| # | User Story | Kao | Želi | Kako bi |
|---|-----------|-----|------|---------|
| US-1 | Batch procesiranje fajlova sa web lokacije | Administrator | Unese Google Drive Folder ID i pokrene batch uvoz audio/txt/pdf fajlova | Masovno popunio bazu znanja bez ručnog upload-a |
| US-2 | CHAT dugme u header-u (Admin i Agent) | Administrator ili agent | Klikne na "Chat" link u gornjem desnom uglu i bude preusmjeren na `/chat` | Brzo prešao iz admin/agent panela na chatbot interfejs |
| US-3 | Poboljšanje deployment pipeline-a i ubrzanje build vremena | Developer | CI/CD pipeline brže završi i svaki korak builde bude optimizovan | Smanjio čekanje pri svakom deploy-u i poboljšao razvojni tok |
| US-4 | Filtriranje issues-a u pregledu baze znanja | Administrator | Lista issues ne prikazuje duplikate, pozive agenta, pozdrave ni eksplicitne zahtjeve | Dobio čišći i relevantniji pregled stvarnih problema bez šuma |
| US-5 | Prikaz "Top Rated Responses" | Administrator | Sekcija "Top Rated Responses" prikazuje odgovore s najvišim prosječnim ocjenama | Vidio koji odgovori su korisnicima bili najkorisniji |
| US-6 | Poboljšanje UI-a eskalacijske queue | Korisnik ili agent | Sučelje eskalacijske queue prikazuje jasne i pregledne informacije | Znao status zahtjeva za eskalacijom i imao bolji uvid u tijek čekanja |

---

## US-1: Batch procesiranje fajlova sa web lokacije (on-demand)

**Kao** administrator,  
**želim** da unesem Google Drive folder ID i pokrenem batch uvoz svih audio/txt/pdf fajlova,  
**kako bih** mogao masovno popuniti bazu znanja bez ručnog upload-a fajl po fajl.

**Kriteriji prihvatanja:**
- Admin unese Google Drive Folder ID u UI polje
- Klikne "Pokreni sada" → sistem poziva `POST /transcripts/batch-drive`
- Sistem preuzme listu fajlova iz foldera (podržani tipovi: mp3, wav, mp4, txt, pdf)
- Duplikati se preskače (provjera po nazivu fajla unutar istog folder ID-a)
- Svaki novi fajl prolazi kroz postojeći pipeline (normalizacija → PII masking → embedding → Qdrant)
- Response vraća `{ queued, skipped, folder_id }`
- Status kartica u UI-u pokazuje zadnji run, broj obrađenih, broj na čekanju, broj grešaka

---

## US-2: CHAT dugme u header-u (Admin i Agent)

**Kao** administrator ili agent,  
**želim** da kliknem na "Chat" link u gornjem desnom uglu i budem preusmjeren na `/chat` stranicu,  
**kako bih** brzo prešao iz admin/agent panela na chatbot interfejs.

**Kriteriji prihvatanja:**
- U `AdminShell` header-u: link "Chat" vodi na `/chat` 
- U `AgentShell` header-u: dodan link "Chat" koji vodi na `/chat` 
- Link je vizualno konzistentan s ostalim header elementima (isti stil kao u AdminShell)

---

## US-3: Poboljšanje deployment pipeline-a i ubrzanje build vremena

**Kao** developer,  
**želim** da CI/CD pipeline brže završi i da svaki korak builde bude optimizovan,  
**kako bih** smanjio čekanje pri svakom deploy-u i poboljšao razvojni tok.

**Kriteriji prihvatanja:**
- Docker build koristi layer caching za svaki servis
- GitHub Actions workflow koristi caching za `pip`, `npm` i Docker layers između runova
- Build time za frontend i backend smanjeni za mjerljiv procenat u odnosu na trenutno stanje
- Pipeline koraci su paralelizovani gdje je moguće
- Neiskorišteni koraci i provjere su uklonjeni iz workflow fajlova

---

## US-4: Filtriranje issues-a u pregledu baze znanja

**Kao** administrator,  
**želim** da lista issues u pregledu baze znanja ne prikazuje duplikate, pozive agenta, pozdrave ni eksplicitne zahtjeve,  
**kako bih** dobio čišći i relevantniji pregled stvarnih problema bez šuma.

**Kriteriji prihvatanja:**
- Duplikati se ne prikazuju — prikazuje se samo jedna instanca
- Unosi koji su samo poziv agenta (npr. "Halo", "Jeste li tu?") se filtriraju
- Pozdravne poruke (npr. "Dobro jutro", "Hvala", "Doviđenja") se ne listaju
- Eksplicitni zahtjevi za agentom (npr. "Prebacite me na agenta") se isključuju iz liste
- UI pokazuje samo filtrirani rezultat

---

## US-5: Prikaz "Top Rated Responses"

**Kao** administrator,  
**želim** da sekcija "Top Rated Responses" prikazuje odgovore s najvišim prosječnim ocjenama,  
**kako bih** mogao vidjeti koji odgovori su korisnicima bili najkorisniji.

**Kriteriji prihvatanja:**
- Lista je sortirana silazno po prosječnoj ocjeni, a ne po broju feedbacka ili datumu
- Prikazuje se minimalno 5 odgovora ako postoji dovoljno podataka
- Odgovori s manje od 3 feedbacka se ne uzimaju u obzir
- Prikaz uključuje: tekst odgovora, prosječnu ocjenu, broj ocjena

---

## US-6: Poboljšanje UI-a eskalacijske queue u toku razgovora s agentom

**Kao** korisnik ili agent,  
**želim** da sučelje eskalacijske queue prikazuje jasne i pregledne informacije dok je razgovor u toku,  
**kako bih** znao status zahtjeva za eskalacijom i imao bolji uvid u tijek čekanja.

**Kriteriji prihvatanja:**
- Queue panel prikazuje poziciju u redu čekanja i estimirano vrijeme čekanja ako je dostupno
- Status eskalacije (čekanje / agent preuzeo / odbijeno) je vizualno jasno razlikovan bojom ili ikonom
- Tokom aktivnog razgovora s agentom, chat i queue panel ne preklapaju se niti blokiraju jedan drugi
- Tranzicije stanja (npr. agent se pridružio) praćene su vidljivom notifikacijom unutar UI-a
- Ispravno se prikazuje i na manjim ekranima
