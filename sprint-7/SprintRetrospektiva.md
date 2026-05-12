# Sprint Retrospektiva

---

## Šta je išlo dobro

- Preprocessing pipeline je u potpunosti refaktorisan u zasebne module, a svaki modul ima vlastite unit testove — to je konkretno povećanje kvaliteta koda, ne samo cleanup.
- 37 novih testova prolazi bez greške, uključujući end-to-end integracioni test koji verificira čitav tok od teksta do baze.
- Privacy boundary između pipeline-a i Groq API-ja je implementiran i verificiran testom — PII nikad ne napušta sistem u čistom tekstu.
- Tim je usvojio naviku iz retrospektive Sprinta 6: stavke su se zatvarale uz kratku provjeru toka, ne samo provjeru da li se kompajlira.

---

## Refleksija na tim i proces

Sprint 7 je bio tehnički najzahtjevniji do sada — nije bila u pitanju nova funkcionalna stavka, nego potpuni refaktoring postojećeg servisa uz istovremeno uvođenje novih sigurnosnih slojeva (PII masking, Fernet enkriptovanje, LLM privacy boundary). Činjenica da je to isporučeno s punim testnim pokrivanjem govori da tim razumije razliku između "radi" i "radi ispravno".

Ipak, uočavamo nekoliko otvorenih pitanja koja zaslužuju pažnju u narednom sprintu.

Prvo: `TOKEN_MAP_KEY` nije konfigurisan u produkcijskom okruženju. Kada ključ nije postavljen, sistem generuje efemerni ključ koji nestaje s restartom — što znači da se nijedna pohranjena token mapa ne može dekriptovati nakon restarta. Ovo nije teorijski rizik, to je produkcijska greška koja čeka da se desi. Potrebno je ili postaviti stabilan ključ ili eksplicitno definisati politiku za slučaj gubitka.

Drugo: embedding je odgođen do koraka odobravanja, ali korak odobravanja još nije implementiran kao workflow. Unosi koji čekaju odobravanje nisu pretraživi u Qdrantu — što znači da RAG trenutno ne vidi nijedan novi transkript. Ovo nije propust ovog sprinta, ali mora biti vidljivo u backlogu kao prioritet, ne kao detalj.

Treće: LLM fallback za audio transkripte radi, ali nema nikakve metrike o tome koliko transkripata prolazi tim putem nasuprot pattern detekciji. Bez te informacije ne možemo procijeniti ni kvalitet labelovanja ni opterećenje Groq API-ja.

---

## Zaključak

Tehnički temelj za obradu transkripata je sada čvrst — modularan, testiran i privatan po dizajnu. Ono što sljedeći sprint treba riješiti su operativne praznine koje su ostale otvorene: konfiguracija produkcijskog ključa, approval workflow koji triggeruje embedding i osnovno praćenje ponašanja pipeline-a u produkciji. Isporučiti dobar kod koji ostaje neupotrebljiv zbog manjkave konfiguracije nije uspjeh — to je zadnji korak koji se ne smije preskočiti.
