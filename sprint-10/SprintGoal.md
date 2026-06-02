# Sprint Goal — Sprint 10

## Cilj sprinta

U Sprintu 10 fokus je na automatizaciji, skalabilnosti i produkcijskoj spremnosti sistema. Nakon što je Sprint 9 stabilizovao sistem, poboljšao kvalitet podataka i isporučio završne funkcionalnosti korisničkog iskustva, ovaj sprint je podigao sistem na viši nivo operativne zrelosti: uvodi se automatska obrada podataka iz eksternih izvora, scheduled pipeline izvršavanje, cloud deployment infrastruktura i optimizacija build procesa.

Centralni tehnički fokus sprinta je automatizacija toka podataka — od preuzimanja transkripata iz eksternih izvora poput Google Drive-a, kroz kompletnu obradu pipeline-a, sve do automatskog ažuriranja baze znanja bez administratorske intervencije za svaki fajl posebno. Ovo direktno smanjuje operativno opterećenje i omogućava sistemu da kontinuirano ostaje ažuran s novim podacima.

Paralelno s automatizacijom podataka, sprint uvodi produkcijsku deployment infrastrukturu. Kompletan sistem može biti deployovan na Azure/AWS cloud okruženje jednim komandnim pozivom, što eliminišeručne korake pri postavljanju produkcijskog okruženja i osigurava konzistentan, ponovljiv proces isporuke. Uz to, Docker build proces se radikalno optimizuje kroz cache mehanizme i CPU-only ML dependency layere, čime se vrijeme rebuildanja smanjuje sa više od 25 minuta na svega 10–15 sekundi za cached rebuildove.

Na strani administratorskog iskustva, sprint donosi pregled live napretka pipeline obrade u realnom vremenu, čime administrator dobija pun uvid u status automatskih operacija bez potrebe za ručnom provjerom logova.

Uz infrastrukturne isporuke, sprint donosi i tri funkcionalnosti koje direktno unapređuju integritet podataka, administratorsku kontrolu i korisničko iskustvo. Uvodi se prevencija duplih unosa u bazu znanja na svim mjestima unosa, bulk brisanje razgovora iz Chat Logs, Transcripts i Issues pregleda, te sistemski konzistentne i korisnički razumljive poruke o greškama koje zamjenjuju sirove tehničke poruke kroz cijelu aplikaciju.

---

## Šta ovaj sprint isporučuje

**Batch procesiranje fajlova iz eksternih izvora** uvodi mogućnost automatskog importa većeg broja transkripata iz Google Drive-a. Administrator pokreće batch import unosom folder URL-a ili ID-a, a sistem samostalno preuzima sve podržane fajlove i provlači ih kroz postojeći transcript pipeline. Implementirana je deduplikacija kako bi već obrađeni fajlovi bili preskočeni, dok se izmijenjene verzije automatski re-importuju. Greška jednog fajla ne blokira obradu ostalih, čime se osigurava robustnost procesa.

**Scheduled pipeline obrada i automatsko ažuriranje baze znanja** uvode autonomni rad sistema bez potrebe za ručnim pokretanjem. Administrator konfiguriše frekvenciju izvršavanja (hourly, daily ili weekly), nakon čega sistem automatski pokreće kompletan pipeline: import transkripata, transkripciju, ekstrakciju Q&A parova, generisanje embeddinga i ažuriranje baze znanja. Status svakog izvršavanja, uključujući posljednje pokretanje i rezultat obrade, vidljiv je u admin panelu.

**Live prikaz napretka pipeline obrade** daje administratoru uvid u tok automatske obrade u realnom vremenu. UI automatski osvježava status svih faza pipeline-a bez potrebe za reload-om stranice, prikazuje trenutno obrađivani fajl te status posljednjeg uspješnog scheduled runa.

**Single-click cloud deployment** omogućava isporuku kompletnog sistema na Azure/AWS infrastrukturu jednim komandnim pozivom. Backend i frontend se automatski deployaju, cloud infrastruktura se automatski provisionira, a rezultat deploya su trajni HTTPS endpointi dostupni odmah po završetku procesa. Ovim se eliminišu ručni koraci i osigurava ponovljiv, konzistentan deployment proces.

**Optimizacija build procesa i CI/CD performansi** dramatično skraćuje trajanje Docker rebuildova uvođenjem cache mehanizama za dependency pakete i CPU-only ML dependency layera. Rebuild koji je prethodno trajao više od 25 minuta sada se izvršava za 10–15 sekundi na cached rebuildovima, čime se ubrzava razvojni ciklus i CI/CD pipeline bez ikakvih promjena u runtime ponašanju aplikacije.

**Prevencija duplih unosa u bazu znanja** štiti integritet baze znanja na svim mjestima unosa — ručni unos Q&A para, obrada transkripata, batch import iz eksternih izvora i spašavanje Q&A pri rješavanju eskalacije. Kod batch importa i obrade transkripata duplikati se automatski preskaču bez prekida obrade, dok kod ručnog unosa administrator dobija eksplicitnu poruku da pitanje već postoji u bazi znanja.

**Bulk brisanje razgovora iz Chat Logs, Transcripts, Issues** daje administratoru efikasnu kontrolu nad historijom razgovora. Dodat je checkbox po svakom redu u Chat Logs, Transcripts i Issues tabelama uz "select all" u zaglavlju. Dugme "Delete selected (N)" trajno briše sve označene razgovore zajedno s porukama, odgovorima, ocjenama i eskalacijama. Akcija je dostupna isključivo administratoru.

**Razumljive i korisnički prilagođene poruke o greškama** osiguravaju da nijedna akcija u sistemu ne prikazuje sirove tehničke poruke poput HTTP status kodova ili stack trace informacija. Sistem prikazuje jasne, kontekstualne poruke prilagođene konkretnoj akciji — upload transkripata, pipeline obrada, unos i izmjena baze znanja, brisanje — konzistentnog vizualnog prikaza kroz cijelu aplikaciju.

---

## Stavke uključene u sprint

| ID | Naziv | Prioritet |
|----|-------|-----------|
| PB-66 | Batch procesiranje fajlova iz eksternih izvora | High |
| PB-67 | Scheduled pipeline obrada i automatsko ažuriranje baze znanja | High |
| PB-68 | Single-click cloud deployment | High |
| PB-69 | Optimizacija build procesa i CI/CD performansi | High |
| PB-70 | Prevencija duplih unosa u bazu znanja | High |
| PB-71 | Bulk brisanje razgovora iz Chat Logs, Transcripts, Issues | Medium |
| PB-72 | Razumljive i korisnički prilagođene poruke o greškama | High |


---

## Kriterij uspjeha

Sprint se smatra uspješnim ako:

- administrator može pokrenuti batch import iz eksternog izvora (Google Drive) unosom folder URL-a ili ID-a
- sistem automatski preskače već obrađene fajlove i re-importuje izmijenjene verzije
- greška jednog fajla pri batch importu ne prekida obradu preostalih fajlova u skupu
- scheduled pipeline se izvršava prema konfiguriranom rasporedu bez ručnog pokretanja
- pipeline pokriven svim fazama: import, transkripcija, ekstrakcija Q&A, generisanje embeddinga, ažuriranje baze znanja
- administrator vidi live status pipeline obrade u admin panelu bez potrebe za reload-om
- kompletan sistem se deploya na cloud infrastrukturu jednim komandnim pozivom
- deploy automatski provisionira infrastrukturu i generiše trajne HTTPS endpointe
- cached Docker rebuild traje značajno kraće u odnosu na prethodnu implementaciju (ciljno 10–15 sekundi)
- optimizacija build procesa ne mijenja runtime ponašanje niti produkcijsku funkcionalnost aplikacije
- sistem sprječava dodavanje identičnih pitanja u bazu znanja na svim mjestima unosa
- kod batch importa i obrade transkripata duplikati se automatski preskaču bez prekida procesa
- kod ručnog unosa administrator dobija eksplicitnu poruku o već postojećem pitanju
- administrator može označiti više razgovora u Chat Logs, Transcripts i issues pregledima i obrisati ih jednom akcijom
- brisanje razgovora uklanja sve pridružene poruke, ocjene i eskalacije iz sistema
- nijedna akcija u sistemu ne prikazuje sirove tehničke poruke niti HTTP status kodove krajnjem korisniku
- sve poruke o greškama su konzistentnog vizualnog prikaza kroz cijelu aplikaciju
