# Sprint 11 — Zadnji sprint (Završna isporuka)

Cilj zadnjeg sprinta je stabilizacija finalne verzije i kompletna završna isporuka, tako da se sistem
može **pokrenuti, deployati, koristiti, testirati i evaluirati bez neformalnih objašnjenja tima**.

**Live aplikacija:** <https://purple-field-0d55d8003.7.azurestaticapps.net/>
**Hosting:** Azure free tier (Container Apps + Static Web Apps), deploy preko `azd` + GitHub Actions.

## Obavezni artefakti

| # | Artefakt | Fajl |
|---|----------|------|
| — | Sprint Goal | [`SprintGoal.md`](./SprintGoal.md) |
| 1 | Dokumentovanje rada (završni izvještaj) | [`ZavrsniIzvjestaj.md`](./ZavrsniIzvjestaj.md) |
| 2 | Deployment procedura | [`DeploymentProcedura.md`](./DeploymentProcedura.md) |
| 3 | Continuous Deployment skripta / pipeline | [`CD-Pipeline.md`](./CD-Pipeline.md) |
| 4 | User Manual | [`UserManual.md`](./UserManual.md) |
| 5 | Finalni Product Backlog status | [`ProductBacklog.md`](./ProductBacklog.md) |
| 6 | Release Notes | [`ReleaseNotes.md`](./ReleaseNotes.md) |
| 7 | Test Summary / QA izvještaj | [`TestSummary.md`](./TestSummary.md) |
| 8 | Architecture / Technical Overview | [`ArchitectureOverview.md`](./ArchitectureOverview.md) |
| 9 | Final AI Usage Summary | [`AIUsageSummary.md`](./AIUsageSummary.md) |
| 10 | Known Issues / Limitations | [`KnownIssues.md`](./KnownIssues.md) |

## Demo kredencijali

| Uloga | Email | Lozinka |
|---|---|---|
| Admin | `admin@test.com` | `admin123` |
| Agent | `agent@test.com` | `Agent1234` |
| User | `user@test.com` | `User1234` |

## Brzi start

```bash
# Lokalno (sve odjednom)
cd projekat && docker-compose up

# Testovi
cd projekat/backend && pytest -q        # 223 testa

# Cloud deploy (Azure)
cd projekat && azd up
```

Detalji: vidi `DeploymentProcedura.md`.
