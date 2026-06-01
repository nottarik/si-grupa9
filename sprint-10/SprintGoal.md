# Sprint Goal — Sprint 10

## Cilj sprinta

U Sprintu 10 fokus je na automatizaciji, skalabilnosti i produkcijskoj spremnosti sistema. Nakon što je Sprint 9 stabilizovao sistem, poboljšao kvalitet podataka i isporučio završne funkcionalnosti korisničkog iskustva, ovaj sprint je podigao sistem na viši nivo operativne zrelosti: uvodi se automatska obrada podataka iz eksternih izvora, scheduled pipeline izvršavanje, cloud deployment infrastruktura i optimizacija build procesa.

Centralni tehnički fokus sprinta je automatizacija toka podataka — od preuzimanja transkripata iz eksternih izvora poput Google Drive-a i S3 storage-a, kroz kompletnu obradu pipeline-a, sve do automatskog ažuriranja baze znanja bez administratorske intervencije za svaki fajl posebno. Ovo direktno smanjuje operativno opterećenje i omogućava sistemu da kontinuirano ostaje ažuran s novim podacima.

Paralelno s automatizacijom podataka, sprint uvodi produkcijsku deployment infrastrukturu. Kompletan sistem može biti deployovan na Azure/AWS cloud okruženje jednim komandnim pozivom, što eliminišeručne korake pri postavljanju produkcijskog okruženja i osigurava konzistentan, ponovljiv proces isporuke. Uz to, Docker build proces se radikalno optimizuje kroz cache mehanizme i CPU-only ML dependency layere, čime se vrijeme rebuildanja smanjuje sa više od 25 minuta na svega 10–15 sekundi za cached rebuildove.

Na strani administratorskog iskustva, sprint donosi pregled live napretka pipeline obrade u realnom vremenu, čime administrator dobija pun uvid u status automatskih operacija bez potrebe za ručnom provjerom logova.

Sprint 10 zaokružuje sistem kao cjelinu — ne dodaje nove korisničke funkcionalnosti, već osigurava da sistem koji je izgrađen kroz prethodnih devet sprintova može biti efikasno isporučen, automatski održavan i trajno skaliran u produkcijskom okruženju.

---

## Šta ovaj sprint isporučuje

**Batch procesiranje fajlova iz eksternih izvora** uvodi mogućnost automatskog importa većeg broja transkripata iz Google Drive-a, S3 i sličnih eksternih storage servisa. Administrator pokreće batch import unosom folder URL-a ili ID-a, a sistem samostalno preuzima sve podržane fajlove i provlači ih kroz postojeći transcript pipeline. Implementirana je deduplikacija kako bi već obrađeni fajlovi bili preskočeni, dok se izmijenjene verzije automatski re-importuju. Greška jednog fajla ne blokira obradu ostalih, čime se osigurava robustnost procesa.

**Scheduled pipeline obrada i automatsko ažuriranje baze znanja** uvode autonomni rad sistema bez potrebe za ručnim pokretanjem. Administrator konfiguriše frekvenciju izvršavanja (hourly, daily ili weekly), nakon čega sistem automatski pokreće kompletan pipeline: import transkripata, transkripciju, ekstrakciju Q&A parova, generisanje embeddinga i ažuriranje baze znanja. Status svakog izvršavanja, uključujući posljednje pokretanje i rezultat obrade, vidljiv je u admin panelu.

**Live prikaz napretka pipeline obrade** daje administratoru uvid u tok automatske obrade u realnom vremenu. UI automatski osvježava status svih faza pipeline-a bez potrebe za reload-om stranice, prikazuje trenutno obrađivani fajl te status posljednjeg uspješnog scheduled runa.

**Single-click cloud deployment** omogućava isporuku kompletnog sistema na Azure/AWS infrastrukturu jednim komandnim pozivom. Backend i frontend se automatski deployaju, cloud infrastruktura se automatski provisionira, a rezultat deploya su trajni HTTPS endpointi dostupni odmah po završetku procesa. Ovim se eliminišu ručni koraci i osigurava ponovljiv, konzistentan deployment proces.

**Optimizacija build procesa i CI/CD performansi** dramatično skraćuje trajanje Docker rebuildova uvođenjem cache mehanizama za dependency pakete i CPU-only ML dependency layera. Rebuild koji je prethodno trajao više od 25 minuta sada se izvršava za 10–15 sekundi na cached rebuildovima, čime se ubrzava razvojni ciklus i CI/CD pipeline bez ikakvih promjena u runtime ponašanju aplikacije.

---

## Stavke uključene u sprint

| ID | Naziv | Prioritet |
|----|-------|-----------|
| PB-66 | Batch procesiranje fajlova iz eksternih izvora | High |
| PB-67 | Scheduled pipeline obrada i automatsko ažuriranje baze znanja | High |
| PB-68 | Single-click cloud deployment | High |
| PB-69 | Optimizacija build procesa i CI/CD performansi | High |

---

## Kriterij uspjeha

Sprint se smatra uspješnim ako:

- administrator može pokrenuti batch import iz eksternog izvora (Google Drive, S3) unosom folder URL-a ili ID-a
- sistem automatski preskače već obrađene fajlove i re-importuje izmijenjene verzije
- greška jednog fajla pri batch importu ne prekida obradu preostalih fajlova u skupu
- scheduled pipeline se izvršava prema konfiguriranom rasporedu bez ručnog pokretanja
- pipeline pokriven svim fazama: import, transkripcija, ekstrakcija Q&A, generisanje embeddinga, ažuriranje baze znanja
- administrator vidi live status pipeline obrade u admin panelu bez potrebe za reload-om
- kompletan sistem se deploya na cloud infrastrukturu jednim komandnim pozivom
- deploy automatski provisionira infrastrukturu i generiše trajne HTTPS endpointe
- cached Docker rebuild traje značajno kraće u odnosu na prethodnu implementaciju (ciljno 10–15 sekundi)
- optimizacija build procesa ne mijenja runtime ponašanje niti produkcijsku funkcionalnost aplikacije
