## Sprint 4 Review

# 1. Planirani sprint goal

Cilj Sprinta 4 bio je pripremiti projekat za početak implementacione faze kroz definisanje kriterija završetka rada, izradu početnog release plana, uspostavljanje tehničke osnove sistema, inicijalne strukture repozitorija i finalno usklađivanje modela sistema iz prethodnog sprinta.

---

# 2. Šta je završeno

Tim je uspješno realizovao planirane aktivnosti Sprinta 4 i postavio čvrst temelj za razvoj sistema u narednim sprintovima.

- **Definition of Done** – Definisani su jasni kriteriji kada se stavka smatra završenom, uključujući funkcionalnost, testiranje, kvalitet, dokumentaciju i spremnost za demonstraciju.   
- **AI-specifični Definition of Done kriteriji** – Dodani su posebni uslovi za AI funkcionalnosti poput chatbot odgovora, fallback mehanizma, obrade transkripata, privatnosti i auditabilnosti.  
- **Initial Release Plan** – Kreiran je inicijalni plan isporuke kroz inkremente od Sprinta 5 do Sprinta 12, sa jasno definisanim ciljevima i funkcionalnostima svakog inkrementa.   
- **Definisan MVP opseg** – Identifikovana je prva upotrebljiva verzija sistema sa osnovnim chatbot funkcionalnostima i unosom transkripata.  
- **Tehnički setup sistema** – Definisan kompletan tehnološki stack za frontend, backend, AI komponente, baze podataka i infrastrukturu.   
- **Inicijalna struktura repozitorija** – Kreiran repozitorij sa odvojenim direktorijima za frontend, backend, nginx konfiguraciju i CI/CD workflow-e.  
- **Docker Compose osnova** – Postavljena početna konfiguracija za pokretanje sistema kroz kontejnere.  
- **Use Case model dorade** – Prošireni use case dijagrami dodatnim slučajevima upotrebe vezanim za pripremu podataka, obradu transkripata i AI pipeline.  


---

# 3. Šta nije završeno


Sve predviđene aktivnosti za Sprint 4 su uspješno završene i nema zaostataka.

---

# 4. Demonstrirani artefakti

- Dokument **Definition of Done**  
- Dokument **Initial Release Plan**  
- Dokument **Tehnički setup sistema**  
- Struktura GitHub repozitorija i osnovni skeleton projekta   


---

# 5. Glavni problemi

- Bilo je potrebno uskladiti veliki broj tehnologija kako bi stack bio realan i izvodiv  
- Diskusija oko izbora backend frameworka, AI servisa i hosting infrastrukture  
- Potrebno dodatno razjasniti razliku između inkremenata razvoja i release verzija proizvoda  
- Usklađivanje MVP opsega sa realnim kapacitetom tima i rokovima

---

# 6. Ključne odluke donesene u sprintu

- Frontend će koristiti **React + Vite + Tailwind CSS**  
- Backend će koristiti **Python FastAPI**  
- AI modul koristi **LangChain + Groq API + RAG pristup**  
- Za transkripciju audio zapisa koristi se **faster-whisper**  
- Relacijska baza podataka je **PostgreSQL**, a vektorska baza **Qdrant**  
- Redis i Celery koriste se za asinhrone taskove  
- Deployment će koristiti **Docker Compose + Nginx**  
- Hosting planiran na **Oracle Cloud Always Free**  
- MVP release fokusiran je na osnovni chatbot, unos transkripata i fallback logiku

---

# 7. Povratna informacija Product Ownera



---

# 8. Zaključak za naredni sprint

U Sprintu 5 tim ulazi u implementacionu AI-enabled fazu razvoja projekta.

Fokus narednog sprinta biće na izradi prvog funkcionalnog inkrementa sistema, validaciji osnovnog implementacionog toka i povezivanju ključnih komponenti aplikacije.

Planirane aktivnosti uključuju:

- izradu Sprint Backloga
- implementaciju prvih korisničkih funkcionalnosti
- povezivanje frontend, backend i baze podataka
- početni chatbot tok i AI integraciju
- uspostavu AI Usage Log dokumenta
- uspostavu Decision Log dokumenta
- tehničku validaciju arhitekture sistema

Sprint 5 predstavlja prelazak sa planske i pripremne faze projekta na konkretnu realizaciju prve radne verzije sistema.
