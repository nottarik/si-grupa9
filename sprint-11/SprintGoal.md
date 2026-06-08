# Sprint Goal — Sprint 11 

## Cilj sprinta

Cilj zadnjeg sprinta je **stabilizovati finalnu verziju sistema i pripremiti kompletnu završnu
isporuku**. Fokus nije na dodavanju novih funkcionalnosti, nego na tome da projekat bude
**razumljiv, pokretljiv, deployabilan, testiran i evaluabilan bez ikakvih neformalnih objašnjenja
tima**.

Konkretno, Sprint 11 isporučuje:

- završnu **procesnu i tehničku dokumentaciju** (završni izvještaj o radu tima),
- **provjerljivu deployment proceduru** kojom druga osoba može pokrenuti sistem prateći napisane korake,
- **automatizovan i ponovljiv deployment** putem CD pipeline-a (GitHub Actions + Azure Developer CLI),
- **korisnički priručnik (User Manual)** pisan za krajnjeg korisnika,
- **finalni Product Backlog status** koji prikazuje stvarno stanje projekta,
- **Release Notes** koji razdvajaju isporučeno od planiranog-ali-nezavršenog,
- **Test Summary / QA izvještaj** sa konkretnim i provjerljivim dokazima testiranja,
- **Architecture / Technical Overview** za osobu koja prvi put gleda projekat,
- **Final AI Usage Summary** koji transparentno prikazuje korištenje AI alata,
- **Known Issues / Limitations** —  listu poznatih problema i ograničenja.

## Kontekst

Sistem (RAG-zasnovan AI chatbot za podršku call centru) je kroz sprintove 1–10 dosegao
produkcijsku zrelost: kompletan transcript→knowledge base pipeline, RAG chat sa eskalacijom na
stvarnog agenta, admin i agent paneli, automatizovan import sa Google Drive-a, scheduled pipeline,
te single-click cloud deployment na Azure. Sprint 11 ne mijenja funkcionalni opseg — on
**zaključava** isporuku i čini je provjerljivom.

## Hosting

Produkcija se hostuje na **Azure free tieru**:

- **Frontend (Vite SPA):** Azure Static Web App (Free SKU) — live na
  <https://purple-field-0d55d8003.7.azurestaticapps.net/>
- **Backend (FastAPI):** Azure Container App (1 vCPU / 2 GiB, uvijek topla 1 replika)
- Provisioning i deploy: Azure Developer CLI (`azd`) iz `infra/main.bicep`, automatizovan kroz
  GitHub Actions (`.github/workflows/azure-dev.yml`).

Eksterni servisi (Supabase Postgres + Storage, Qdrant Cloud, Groq API) ostaju van Azure-a i u
deployment se injektuju samo kao secret konekcije.

## Kriterij uspjeha (Definition of Done za sprint)

Sprint se smatra uspješnim ako:

- dokumentacija je konkretna za stvarno razvijeni projekat,
- deployment procedura je detaljna i provjerljiva — druga osoba može pokrenuti sistem bez pitanja upućenih timu,
- CD pipeline omogućava ponovljiv deployment kompletnog sistema na Azure,
- korisnički priručnik je razumljiv krajnjem korisniku i sadrži demo kredencijale,
- Product Backlog prikazuje stvarno stanje projekta (Done / Partially Done / Not Done / Deferred),
- testiranje je jasno dokumentovano, povezano s funkcionalnostima i provjerljivo (223 testa, pytest),
- tehnička arhitektura je objašnjena razumljivo (komponente, dijagram, komunikacija, sigurnost),
- AI korištenje je transparentno opisano,
- poznata ograničenja su jasno navedena bez prikrivanja,
- svi dokumenti su međusobno konzistentni i tim ih može odbraniti.

## Obavezni artefakti 

| # | Artefakt | Fajl |
|---|----------|------|
| 1 | Dokumentovanje rada (završni izvještaj) | `ZavrsniIzvjestaj.md` |
| 2 | Deployment procedura | `DeploymentProcedura.md` |
| 3 | Continuous Deployment skripta / pipeline | `CD-Pipeline.md` |
| 4 | User Manual | `UserManual.md` |
| 5 | Finalni Product Backlog status | `ProductBacklog.md` |
| 6 | Release Notes | `ReleaseNotes.md` |
| 7 | Test Summary / QA izvještaj | `TestSummary.md` |
| 8 | Architecture / Technical Overview | `ArchitectureOverview.md` |
| 9 | Final AI Usage Summary | `AIUsageSummary.md` |
| 10 | Known Issues / Limitations | `KnownIssues.md` |
