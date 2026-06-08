# Continuous Deployment — Pipeline i skripta

Ovaj dokument pokazuje da se deployment kompletnog sistema može izvršiti **ponovljivo i provjerivo**,
a ne samo opisati. Deployment je automatizovan kroz **GitHub Actions** + **Azure Developer CLI
(`azd`)** koji čita infrastrukturu iz **Bicep** definicije. Ručni ekvivalent (`azd up`) opisan je u
`DeploymentProcedura.md`, sekcija 10.

---

## 1. Gdje se skripta/pipeline nalazi

| Fajl | Uloga |
|---|---|
| `.github/workflows/azure-dev.yml` | **Glavni CD pipeline** — provision + deploy na Azure pri push-u na `main` |
| `.github/workflows/ci.yml` | CI — pokreće `pytest` na svaki push/PR prema `main` |
| `.github/workflows/release.yml` | Release okidač na git tag (`v*.*.*`) — poziva `ci.yml` |
| `projekat/azure.yaml` | `azd` manifest — definiše dva servisa: `backend` (Container App) i `web` (Static Web App) |
| `projekat/infra/main.bicep` | Infrastruktura kao kod (ACR, Container Apps env, Container App, Static Web App, identity, Log Analytics) |
| `projekat/backend/Dockerfile` | Build backend image-a |
| `projekat/frontend/Dockerfile` | Build frontend image-a (lokalni/tunnel scenariji); na Azure-u se radi `npm run build` → Static Web App |

---

## 2. Šta CD pipeline obuhvata

CD pipeline (`azure-dev.yml` → `azd provision` + `azd deploy`) pokriva sve tražene korake:

1. **Build backend aplikacije** — `azd` buildi `backend/Dockerfile` i push-a image u Azure Container Registry.
2. **Build frontend aplikacije** — `azd` pokreće `npm run build` (Vite) i objavljuje `dist/` na Static Web App.
3. **Priprema / povezivanje baze** — baza je Supabase Postgres (eksterna); konekcija se injektuje kao secret `DATABASE_URL`.
4. **Primjena migracija** — Alembic migracije se primjenjuju nad Supabase bazom (`alembic upgrade head`); shema je dijeljena, pa redovan deploy ne zahtijeva re-provisioning baze.
5. **Postavljanje environment varijabli** — sve tajne (`GROQ_API_KEY`, `QDRANT_*`, `SUPABASE_*`, `TOKEN_MAP_KEY`, `DATABASE_URL`, `GOOGLE_*`) prosljeđuju se iz GitHub Secrets-a kao Container App secrets (vidi `main.bicep`).
6. **Deployment backend-a** — Container App `backend` (1 vCPU / 2 GiB, uvijek topla replika).
7. **Deployment frontend-a** — Static Web App `web` (Free SKU).
8. **Povezivanje frontenda sa backend API-jem** — `VITE_API_URL` se baked u frontend build iz `BACKEND_URI` outputa Bicep-a (FQDN backenda). Nije potrebno ručno editovanje.
9. **Osnovna provjera dostupnosti** — `GET /health` i `/heartbeat` na backendu; otvaranje `WEB_URI` frontenda.

---

## 3. Kako se pokreće

### Automatski (CD)
`azure-dev.yml` se pokreće:
- na **push na `main`** koji dira `projekat/**` ili sam workflow (pushevi koji diraju samo dokumentaciju/sprintove se ignorišu — `paths` filter),
- ručno preko **workflow_dispatch**.

```yaml
on:
  workflow_dispatch:
  push:
    branches: [ main ]
    paths:
      - 'projekat/**'
      - '.github/workflows/azure-dev.yml'
```

Koraci joba (`build`, radni direktorij `projekat/`):
1. `actions/checkout`
2. `Azure/setup-azd` — instalira `azd`
3. **Login bez tajni (OIDC / federated credentials):** `azd auth login --federated-credential-provider github` koristeći `AZURE_CLIENT_ID` / `AZURE_TENANT_ID`
4. `azd provision --no-prompt` — kreira/ažurira infrastrukturu
5. `azd deploy --no-prompt` — buildi i deploya backend + frontend

### CI (na svaki push/PR)
`ci.yml` pokreće backend testove prije/uz deploy:

```yaml
- name: Run tests
  env:
    APP_ENV: test
    DATABASE_URL: sqlite+aiosqlite:///./test.db
    GROQ_API_KEY: test-key
    ...
  run: pytest -q
```

### Ručni ekvivalent (lokalno)
```bash
cd projekat
azd up        # provision + build + deploy u jednoj komandi
```

---

## 4. Koje preduvjete pipeline zahtijeva

- **Azure pretplata** (free tier) i resource group kreiran kroz `azd`.
- **Federated credentials (OIDC)** između GitHub repozitorija i Azure App Registration-a — pipeline koristi `permissions: id-token: write` i ne čuva Azure lozinke/secret-e za login.
- **Docker daemon** na runneru/lokalno — backend image se buildi lokalno pa push na ACR (ACR Tasks su blokirani na free-trial: „TasksOperationsNotAllowed").
- Konfigurisani **GitHub Actions Variables** i **Secrets** (sekcija 5).

---

## 5. Koje varijable i secrets pipeline koristi

### GitHub Actions **Variables** (`vars.*`, ne-tajno)
`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_ENV_NAME`, `AZURE_LOCATION`,
`AZURE_STATIC_WEB_APP_LOCATION`, `SERVICE_BACKEND_IMAGE_NAME`, `GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID`.

### GitHub Actions **Secrets** (`secrets.*`, tajno)
`DATABASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY`, `GROQ_API_KEY`, `SUPABASE_URL`,
`SUPABASE_SERVICE_KEY`, `TOKEN_MAP_KEY`, `GOOGLE_SERVICE_ACCOUNT_JSON_BASE64`.

Ove se u `azd provision`/`azd deploy` koraku prosljeđuju kao env i dalje upisuju kao **Container App
secrets** (`main.bicep` → `secrets[]` blok). `SECRET_KEY` i `INTERNAL_API_KEY` se **automatski
generišu po deployu** (`newGuid()`), pa ih ne treba čuvati.

---

## 6. Šta se tačno deploya

| Komponenta | Izvor | Cilj |
|---|---|---|
| Backend (FastAPI) | `backend/Dockerfile` → ACR image | Container App `backend` |
| Frontend (Vite SPA) | `npm run build` → `dist/` | Static Web App `web` |
| Infrastruktura | `infra/main.bicep` | Resource group (ACR, Container Apps env, identity, Log Analytics, SWA) |

Backend i frontend su **odvojeni servisi**; povezani su tako što frontend build dobije backend FQDN
kroz `VITE_API_URL`, a backend dozvoljava CORS origin frontenda kroz `ALLOWED_ORIGINS` (postavljen na
domenu Static Web App-a u `main.bicep`). WebSocket (chat/escalation) radi jer Container App ingress
koristi `transport: auto` (WSS upgrade).

---

## 7. Gdje se provjerava rezultat deploymenta

- Outputi `azd`-a / Actions logova: `WEB_URI`, `BACKEND_URI`, `VITE_API_URL`, `AZURE_CONTAINER_REGISTRY_ENDPOINT`.
- **Live frontend:** <https://purple-field-0d55d8003.7.azurestaticapps.net/>
- **Backend health:** `GET <BACKEND_URI>/health` → `{"status":"ok"}`; `GET <BACKEND_URI>/heartbeat` → `{"ok":true}`.
- **Swagger:** `<BACKEND_URI>/docs`.
- **Logovi:** Log Analytics workspace (Container Apps logovi).

---

## 8. Stepen automatizacije i ručni koraci

Deployment je u najvećoj mjeri **automatizovan**: jedan push na `main` (ili `azd up`) provisionira
infrastrukturu, buildi obje aplikacije, injektuje konfiguraciju i deploya sistem do trajnih HTTPS
endpointa.

Jedini opravdani ručni preduvjet je **jednokratni setup**: kreiranje Azure App Registration-a sa
federated credentials i unošenje GitHub Variables/Secrets. Nakon toga je deployment ponovljiv bez
neformalnih koraka. Image se buildi lokalno/na runneru (zbog free-trial ograničenja ACR Tasks-a), ali
to je dio automatizovanog `azd` toka, ne ručni korak.
