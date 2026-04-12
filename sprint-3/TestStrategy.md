# Test Strategy

## Cilj testiranja

Cilj testiranja je osigurati da AI chatbot sistem funkcioniše ispravno, pouzdano i sigurno u svim ključnim scenarijima korištenja. Testiranjem se provjerava da li sistem pravilno obrađuje transkripte, generiše relevantne odgovore i u slučaju nesigurnosti preusmjerava komunikaciju na ljudskog agenta.  

Također, cilj je potvrditi da su osjetljivi podaci adekvatno zaštićeni, da sistem zadovoljava performanse i stabilnost, te da ispunjava definisane acceptance kriterije i nefunkcionalne zahtjeve za MVP verziju.

---

## Ciljevi testiranja

| Cilj | Obim | Kriterij uspjeha |
|------|------|------------------|
| Verifikacija unosa i uploada transkripata | Validacija formata fajla, ručni unos i pohrana transkripata | Ispunjeni svi acceptance kriteriji iz US-01 i US-02: validan fajl se uspješno učitava i pohranjuje, a nevalidan se odbija uz odgovarajuću poruku |
| Validacija obrade i pripreme transkripata | Parsiranje, normalizacija i maskiranje osjetljivih podataka | Svi lični podaci su maskirani, tekst je pravilno strukturiran i spreman za korištenje u sistemu |
| Verifikacija chatbot odgovora | Generisanje odgovora na osnovu baze znanja | Chatbot daje relevantan odgovor u skladu sa definisanim kriterijima tačnosti (NFR-13) |
| Validacija fallback mehanizma | Preusmjeravanje na agenta kada chatbot nije siguran | Sistem uspješno prepoznaje nesigurnost i preusmjerava razgovor bez gubitka konteksta (NFR-5) |
| Provjera administratorskih funkcionalnosti | Pregled, validacija i upravljanje transkriptima i prijavljenim problemima | Administrator može pregledati, validirati i upravljati podacima bez grešaka |
| Validacija prijave netačnih odgovora | Korisnički feedback i obrada prijavljenih problema | Sistem omogućava prijavu netačnog odgovora i pravilno ga evidentira |
| Provjera sigurnosti i privatnosti podataka | Zaštita podataka i kontrola pristupa | Svi podaci su zaštićeni (HTTPS, RBAC), a lični podaci maskirani prije obrade (NFR-1, NFR-2, NFR-3) |
| Testiranje performansi sistema | Vrijeme odziva i rad pod opterećenjem | Sistem odgovara u roku < 3 sekunde u 95% slučajeva i podržava minimalno 100 korisnika (NFR-7, NFR-8) |
| Validacija pouzdanosti sistema | Stabilnost rada i ponašanje u greškama | Sistem ne generiše netačne odgovore i pravilno reaguje u slučaju greške (NFR-5, NFR-6) |
| Provjera upotrebljivosti sistema | Jednostavnost korištenja UI-a | Korisnici mogu koristiti sistem bez dodatne obuke i bez poteškoća (NFR-10) |

## Nivoi testiranja 


## Šta se testira i na kojem nivou


## Veza sa acceptance kriterijima


## Način evidentiranja rezultata testiranja

Rezultati testiranja će se evidentirati kroz strukturirane test slučajeve (test case-ove) koji su direktno povezani sa user story-ima i njihovim acceptance kriterijima.

Za svaki test slučaj bilježit će se:
- ID testa  
- opis scenarija testiranja  
- povezani acceptance kriterij i user story  
- očekivani rezultat  
- stvarni rezultat  
- status testa (Passed / Failed)  
- napomena ili opis greške (ukoliko postoji)

Rezultati testiranja će se voditi u tabelarnom obliku, dok će se uočene greške evidentirati kao posebne stavke u backlogu.

Za automatizovane testove (unit i integraciono testiranje) koristit će se izvještaji iz testnih alata, dok će se za UI i sistemsko testiranje po potrebi priložiti dodatni dokazi kao što su screenshotovi ili opis izvršenih scenarija.

Ovakav pristup omogućava jasnu sljedivost između zahtjeva, testova i rezultata, te olakšava praćenje kvaliteta sistema kroz razvoj.

---

## Glavni rizici kvaliteta

Testiranjem sistema mogu se identificirati sljedeći ključni rizici kvaliteta:

- **Netačni ili nepouzdani odgovori chatbot-a**  
  Postoji rizik da chatbot generiše netačne ili izmišljene odgovore, posebno za pitanja koja nisu pokrivena bazom znanja.

- **Neispravno maskiranje osjetljivih podataka**  
  Lični podaci iz transkripata mogu ostati neadekvatno zaštićeni, što predstavlja sigurnosni i pravni rizik.

- **Neispravan fallback mehanizam**  
  Sistem može neuspješno prepoznati situacije nesigurnosti ili ne preusmjeriti razgovor na agenta, što utiče na korisničko iskustvo.

- **Greške u obradi i pohrani transkripata**  
  Nepravilna validacija ili obrada transkripata može dovesti do gubitka ili pogrešnog prikaza podataka.

- **Neautorizovan pristup administratorskom dijelu sistema**  
  Nedovoljno osigurana autentifikacija i autorizacija mogu omogućiti pristup osjetljivim funkcionalnostima neovlaštenim korisnicima.

- **Pad performansi sistema pod opterećenjem**  
  Sistem može postati spor ili nestabilan pri većem broju istovremenih korisnika.

- **Nedovoljna upotrebljivost korisničkog interfejsa**  
  Nejasan ili nepraktičan UI može otežati korištenje sistema krajnjim korisnicima i administratorima.

- **Regresije nakon izmjena sistema**  
  Nove funkcionalnosti mogu nenamjerno pokvariti postojeće funkcionalnosti ukoliko se ne provodi adekvatno regresiono testiranje.
