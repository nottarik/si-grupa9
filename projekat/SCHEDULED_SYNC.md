# Scheduled Google Drive Sync — Implementation

How the **admin-controlled scheduled import** of Google Drive transcripts works, end to
end. The admin configures a recurring schedule from the app; the backend runs the import
automatically at those times, reusing the existing Drive-import pipeline.

> Companion docs: `DRIVE_IMPORT_AND_BUILD_NOTES.md` (the original on-demand import) and
> `DEPLOY-AZURE.md` (deployment).

---

## 1. What the user gets

**Admin → Pipeline → "Automatic schedule"** card:

- A toggle to **enable/disable** automatic import.
- **Frequency:** Hourly / Daily / Weekly.
- **Time:** day-of-week (weekly), hour (daily/weekly), and minute — all in **Bosnian
  time (Europe/Sarajevo)**.
- Read-outs for **Next run** and **Last run**.

The manual *"Run complete pipeline"* button is unchanged and still works alongside it.

---

## 2. Why an in-process scheduler (not an Azure cron job)

The backend is deployed on **Azure Container Apps with a single always-warm replica**
(`minReplicas: 1, maxReplicas: 1` in `infra/main.bicep`). That one fact drives the design:

- A **fixed Azure cron job** (or a Bicep `Microsoft.App/jobs` resource) bakes the schedule
  into infrastructure at deploy time — it **cannot** read a schedule the admin edits at
  runtime. Running both an infra cron *and* an app-controlled schedule would also
  **double-fire** the import.
- Because there is exactly **one** backend replica, an **in-process scheduler** (a single
  asyncio loop inside FastAPI) is safe — there's no second instance to fire the job a
  second time. It needs **no extra Azure resource and no new runtime dependency**.

So the schedule lives in the database (admin-editable) and an in-process loop executes it.
An earlier iteration used a Bicep cron job hitting an internal endpoint; that was removed
in favor of this. The internal endpoint (`POST /api/v1/internal/sync-drive`) is kept for a
manual/external trigger if ever needed.

---

## 3. Moving parts

```
Admin UI (DriveScheduleCard)
        │  GET/PUT /api/v1/schedule/drive
        ▼
schedule route ───────────►  drive_sync_schedule  (1-row config table)
                                      ▲
                                      │ reads every 60s
        scheduler_loop (asyncio, started from FastAPI lifespan)
                                      │ when next_run_at is due
                                      ▼
                       import_drive_folder(folder, admin_id)   ← existing pipeline
```

### Backend

| File | Role |
|---|---|
| `app/db/models/schedule.py` | `DriveSyncSchedule` ORM model — the single-row config. |
| `alembic/versions/005_drive_sync_schedule.py` | Migration that creates + seeds the table. |
| `app/schemas/schedule.py` | Pydantic `DriveScheduleRead` / `DriveScheduleUpdate` (validates ranges). |
| `app/services/schedule/scheduler.py` | `compute_next_run`, `ensure_table`, `scheduler_loop`, the tick logic. |
| `app/api/v1/routes/schedule.py` | Admin-only `GET`/`PUT /api/v1/schedule/drive`. |
| `app/main.py` (lifespan) | Starts `scheduler_loop` as a background task on boot. |
| `app/api/v1/router.py` | Registers the schedule router. |

### Frontend

| File | Role |
|---|---|
| `src/api/schedule.ts` | Typed `getDriveSchedule` / `updateDriveSchedule`. |
| `src/components/admin/sections/DriveScheduleCard.tsx` | The schedule UI. |
| `src/components/admin/sections/PipelineMonitor.tsx` | Renders the card in the Pipeline section. |

---

## 4. Data model

`drive_sync_schedule` is a **singleton** (always `id = 1`):

| Column | Meaning |
|---|---|
| `enabled` | Master on/off. |
| `frequency` | `hourly` \| `daily` \| `weekly`. |
| `hour` | 0–23, **Bosnian local time** (used by daily/weekly). |
| `minute` | 0–59. |
| `day_of_week` | Mon=0 … Sun=6 (used by weekly). |
| `last_run_at` | UTC timestamp of the last run (display). |
| `next_run_at` | UTC timestamp of the next due run — what the loop compares against. |

**No manual migration needed in prod.** Production has no automatic Alembic step, so
`ensure_table()` runs at startup and creates + seeds the table if it's missing
(`checkfirst=True`, idempotent). The Alembic migration is provided for the clean
`alembic upgrade head` path and for local/test parity.

---

## 5. The schedule loop

`scheduler_loop()` is launched from the FastAPI **lifespan** and ticks every **60 s**:

1. Read the singleton config. If `enabled` is false → do nothing.
2. If `next_run_at` is unset, compute it from the current settings and store it.
3. If `now (UTC) < next_run_at` → not due yet, wait.
4. **Due:** advance the schedule *first* (`last_run_at = now`, recompute `next_run_at`)
   and commit — so a slow import can't re-trigger itself — then run
   `import_drive_folder(folder_id, admin_id)`.

A few deliberate choices:

- **Who "uploaded" it?** A cron run has no logged-in user, but `transkript.id_korisnika_upload`
  is `NOT NULL`. The loop attributes the import to the **first administrator** user.
- **Idempotent imports.** `import_drive_folder` already skips files it has imported before
  (matched by Drive `modifiedTime`), so overlapping or repeated runs don't duplicate work.
- **Not configured?** If the schedule is enabled but `GOOGLE_SERVICE_ACCOUNT_JSON` /
  `GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID` aren't set, the loop logs a warning, advances the
  schedule, and skips — it never hot-loops.

---

## 6. Timezones (Bosnian time)

The admin thinks in **Bosnian local time**, but the scheduler must compare against UTC.

- `hour` / `minute` / `day_of_week` are stored as **Europe/Sarajevo wall-clock** values.
- `compute_next_run()` builds the candidate time in `ZoneInfo("Europe/Sarajevo")`, does the
  wall-clock arithmetic there, then converts the result to **UTC** for `next_run_at`.
- This is **DST-correct**: "daily at 02:00" is 02:00 Sarajevo all year — `00:00 UTC` in
  summer (CEST, +2), `01:00 UTC` in winter (CET, +1).
- `tzdata` is in `requirements.txt` so `zoneinfo` has the IANA database on any platform
  (slim containers / Windows don't always ship it).
- The UI shows `next_run_at` / `last_run_at` formatted in `Europe/Sarajevo` too, so the
  displayed clock matches what the admin entered.

---

## 7. API

Both endpoints are **admin-only**.

```
GET  /api/v1/schedule/drive   → DriveScheduleRead   (current config + next/last run)
PUT  /api/v1/schedule/drive   ← DriveScheduleUpdate (enabled, frequency, hour, minute, day_of_week)
                              → DriveScheduleRead
```

On `PUT`, the server recomputes `next_run_at` from the new settings (or clears it when
disabled). The loop picks up the change on its next tick (≤ 60 s) — no restart needed.

---

## 8. Testing / verification notes

- `compute_next_run` was validated against hourly/daily/weekly cases **including DST**
  boundaries (winter vs summer offsets).
- All backend modules byte-compile.
- Not yet run end-to-end here (backend deps / `tsc` / `az` not installed in the dev box);
  smoke-test with `uvicorn app.main:app` + the admin Pipeline page before relying on it.

## 9. How to change it later

- **Different timezone:** change `BOSNIA_TZ` in `app/services/schedule/scheduler.py`.
- **More frequencies / a raw cron field:** extend the `frequency` handling in
  `compute_next_run` and the `DriveScheduleUpdate` schema + the UI dropdown.
- **Multiple folders / sources:** the schedule is currently the single configured folder;
  generalizing would mean a row per source and a small `RemoteSource` interface.
