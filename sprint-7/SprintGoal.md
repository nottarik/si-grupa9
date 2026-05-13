
# Sprint Goal — Sprint 7

## Cilj sprinta

Sprint 7 fokusiran je na stabilizaciju i unapređenje preprocessing pipeline-a koji predstavlja osnovu za obradu i zaštitu transkripata unutar sistema. Nakon što je Sprint 6 omogućio administratoru potpunu kontrolu nad podacima i validaciju unosa, ovaj sprint uvodi granularnu obradu transkripata, zaštitu osjetljivih podataka (PII), audit logging i automatizovano testiranje cijelog toka obrade.

Cilj sprinta je osigurati da sistem može sigurno i pouzdano obrađivati stvarne korisničke transkripte bez curenja osjetljivih informacija, uz jasnu podjelu preprocessing logike u modularne cjeline koje su lakše za održavanje, proširenje i testiranje.

Na kraju sprinta sistem podržava kompletnu preprocessing obradu: normalizaciju teksta, prepoznavanje govornika, detekciju i maskiranje osjetljivih podataka, segmentaciju sadržaja i kreiranje Q&A zapisa za bazu znanja, uz dokaz da cijeli pipeline funkcioniše kroz unit i integracione testove.

---

## Šta ovaj sprint isporučuje

**Refaktorisanje preprocessing pipeline-a** predstavlja centralnu tehničku stavku sprinta. Postojeća logika razdvojena je u zasebne module (`normalize`, `speakers`, `chunking`, `pii/recognizers`, `pii/masker`, `token_store`, `audit`, `speakers_llm`) kako bi sistem bio pregledniji, održiviji i spreman za dalje proširenje.

**Detekcija i maskiranje PII podataka** uvedeni su kako bi se spriječilo curenje osjetljivih korisničkih informacija. Sistem sada prepoznaje i maskira JMBG, email adrese, telefone, IBAN i druge osjetljive podatke prije nego što tekst bude dalje obrađivan ili poslan eksternim servisima.

**LLM speaker labeling** unaprijeđen je dodatnim sigurnosnim pravilima. Sistem koristi maskiranu verziju teksta prilikom komunikacije s eksternim API servisima, čime se osigurava da originalni PII podaci nikada ne napuštaju sistem.

**Audit logging i token store** omogućavaju sigurnije praćenje rada sistema. Audit logovi više ne sadrže sirove korisničke podatke, dok token store omogućava sigurnu pohranu i rekonstrukciju maskiranih vrijednosti.

**Automatizovano testiranje pipeline-a** značajno je prošireno. Uvedeni su unit testovi za svaki preprocessing modul pojedinačno, kao i end-to-end integracioni test koji validira kompletan tok od ulaznog transkripta do kreiranja segmenata i Q&A zapisa u bazi znanja.

---

## Stavke uključene u sprint

| ID | Naziv | Prioritet |
|----|-------|-----------|
| PB-45 | Refaktorisanje preprocessing pipeline-a | High |
| PB-46 | Normalizacija i segmentacija transkripata | High |
| PB-47 | Detekcija i maskiranje PII podataka | High |
| PB-48 | Audit logging bez curenja osjetljivih podataka | High |
| PB-49 | LLM speaker labeling i fallback logika | Medium |
| PB-50 | Token store i zaštita mapiranja PII vrijednosti | Medium |
| PB-51 | End-to-end pipeline integracioni test | High |
| PB-52 | Unit testovi preprocessing modula | High |

---

## Kriterij uspjeha

Sprint se smatra uspješnim ako:

- preprocessing pipeline obrađuje transkripte bez greške kroz sve faze obrade
- sistem uspješno detektuje i maskira osjetljive podatke prije dalje obrade
- nijedan PII podatak ne curi prema logovima, segmentima ili eksternim API servisima
- LLM speaker labeling koristi fallback strategiju bez rušenja sistema u slučaju greške
- svi unit i integracioni testovi prolaze bez greške
- sistem uspješno kreira segmente i Q&A zapise u bazi znanja iz obrađenih transkripata
- modularna struktura preprocessing logike omogućava lakše održavanje i buduće proširenje sistema

---

## Rizici i zavisnosti

Glavni rizik ovog sprinta je mogućnost curenja osjetljivih podataka ukoliko maskiranje ili audit logging nisu implementirani dosljedno kroz cijeli pipeline.

Postoji i rizik da refaktorisanje uvede regresije u postojeće funkcionalnosti ukoliko testiranje ne pokrije sve ključne tokove obrade.

Zavisnosti uključuju stabilnost postojećeg sistema za unos i upravljanje transkriptima iz Sprinta 6, kao i ispravnu integraciju preprocessing modula s bazom podataka i AI servisima.


