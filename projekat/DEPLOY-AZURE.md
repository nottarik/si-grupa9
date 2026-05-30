# Single-click deploy to Azure

The whole app deploys to Azure with **one command: `azd up`**. The backend runs on
**Azure Container Apps** (1 vCPU / 2 GiB, always warm) and the frontend on **Azure
Static Web Apps** (Free). The database, vector store and LLM stay on the existing
managed services (Supabase, Qdrant Cloud, Groq) — only their connection secrets are
injected at deploy time.

Both services get a **permanent HTTPS URL** that survives redeploys, so there's no
more cloudflared tunnel to re-wire.

## Prerequisites (one time)

```powershell
winget install Microsoft.Azd     # restart the terminal afterwards
azd version                      # confirm it's installed
azd auth login                   # opens a browser; sign in to your Azure account
```

> **Docker Desktop IS required** and must be running: free-trial subscriptions block
> ACR cloud builds ("TasksOperationsNotAllowed"), so azd builds the image locally and
> pushes it to the registry. Install: https://aka.ms/azure-dev/docker-install
> Confirm your subscription is the **Free Trial** ($200 credit), not Pay-As-You-Go,
> before deploying.

## Configure (one time, per environment)

Create an environment and set the secrets. Values come from `backend/.env`.
They are stored under `.azure/` (git-ignored) — **nothing secret is committed.**

```powershell
azd env new chatbot
azd env set AZURE_LOCATION westeurope

azd env set DATABASE_URL          "<DATABASE_URL from backend/.env>"
azd env set QDRANT_URL            "<QDRANT_URL>"
azd env set QDRANT_API_KEY        "<QDRANT_API_KEY>"
azd env set GROQ_API_KEY          "<GROQ_API_KEY>"
azd env set SUPABASE_URL          "<SUPABASE_URL>"
azd env set SUPABASE_SERVICE_KEY  "<SUPABASE_SERVICE_KEY>"

# IMPORTANT: reuse the EXISTING value — a new key makes already-masked PII undecryptable.
azd env set TOKEN_MAP_KEY         "<existing TOKEN_MAP_KEY>"

# Google Drive batch import (service-account JSON on a single line, single-quoted):
azd env set GOOGLE_SERVICE_ACCOUNT_JSON '<service account json>'
azd env set GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID "<drive folder id>"
```

`SECRET_KEY` and `INTERNAL_API_KEY` are generated automatically — don't set them.
`REDIS_URL` is intentionally omitted (the Redis cache layer is optional and unused).

## Deploy — the "single click"

```powershell
azd up
```

This provisions the infra (`infra/main.bicep`), builds `backend/Dockerfile` in the
cloud, builds the Vite frontend with `VITE_API_URL` pointed at the new backend, and
deploys both. When it finishes it prints `BACKEND_URI` and `WEB_URI`.

To redeploy after code changes: `azd deploy`. To change infra: `azd provision`.

## Verify

1. `curl <BACKEND_URI>/health` → `200`.
2. Open `WEB_URI`, log in, send a chat message → you get a RAG answer.
3. **In the browser Network tab, confirm API/WS calls go to `*.azurecontainerapps.io`,
   NOT `onrender.com`.** If you see `onrender.com`, the build used the stale URL from
   `frontend/.env.production` instead of the injected one — see Troubleshooting below.
4. Agent/escalation views connect over `wss://` (check the Network tab).
5. No CORS errors in the browser console (the backend's `ALLOWED_ORIGINS` is wired
   to the Static Web App URL automatically).

## Troubleshooting

**Frontend calls the old `onrender.com` backend.** azd didn't pass `VITE_API_URL` into
the build. Fix by baking the real URL in and redeploying just the frontend:

```powershell
# put the value azd printed as BACKEND_URI here, then rebuild + redeploy web
"VITE_API_URL=<BACKEND_URI>" | Out-File -Encoding utf8 frontend/.env.production
azd deploy web
```

## Tear down (stop spending credit)

```powershell
azd down --purge
```

## After deploying

- **Rotate the Google service-account key** in Google Cloud Console — the previous
  key was shared in plaintext and should be considered compromised.
- Optional: attach a **custom domain** (free managed TLS on the Static Web App) if
  you want a branded URL instead of the default `*.azurestaticapps.net`.
