# What I Did

Work on the escalation / agent-chat flow.

## 1. Resolve → Knowledge Base (per `WhenFixingResolve.md`)
- Resolve form now lists each **customer question paired with the agent's reply** (the
  answer that followed it in chat), each with a **checkbox** and an **editable answer**.
- Greetings / "call agent" messages are filtered out of the import list.
- Selected questions are **formatted** (whitespace/capitalization/`?`) and **auto-published**
  to the KB on resolve (approved + embedded immediately), still editable/deletable in the
  admin **Training Dataset**.
- Fixed silent no-op: Confirm Resolve is blocked unless an answer + a question are provided.
- Fixed stale cache so new KB entries show in Training Dataset without a hard refresh.

## 2. Escalation cleanup bugs
- Admin/agent panel no longer lingers "open" on a dead chat; abandoning a chat now frees
  the assigned agent (backend `cancel_escalation`).

## 3. Presence (leave / re-enter)
- User goes Home/refreshes while connected → agent sees **"User left the chat."**
- User returns → agent sees **"User entered the chat again."** (WS reconnect on the user side).
- If the agent **resolved** while the user was away, returning shows the user a
  **session-ended** message (clean state, not a continuation).

## 4. 15-second grace + auto-end
- If the user leaves and doesn't return within **15s**, the chat is auto-ended:
  agent notified **"Chat ended — the user did not return."**, agent freed, session closed.
- The user's chat **history shows "Closed"** when the agent resolves or the chat times out
  (backend marks the session closed, not relying on the client).

## 5. One agent chat at a time
- Requesting an agent in a new chat while already talking to one returns a clear message:
  *"Već razgovarate sa agentom u drugom razgovoru…"* (HTTP 409).
- `/ask` no longer hijacks messages typed in a different chat into the active agent session.

## 6. "Chat ended" panel behavior
- When a chat ends (user left/timed out), the agent panel **stays open** labelled
  **"Chat Ended"** with the input replaced by a notice + **Close** button. **Resolve** stays
  available (so the agent can still save it to the KB). The panel only closes when the agent
  resolves or closes it — nothing auto-quits. Applied to both admin and agent consoles.

## 7. Dashboard / logs / upload polish
- **Chat Logs** now shows **one row per conversation**, titled with the **real
  question** — for escalated chats it's pulled from the agent transcript (users often
  just say "talk to an agent" to the bot and ask the real question after the agent
  connects); greetings/agent-call turns are skipped.
- **Top Rated Responses** now counts both per-answer thumbs **and** end-of-session
  ratings (was empty when users only rated the whole session); capped at **5**.
- **Upload → Drive**: shows a **"Recently used"** folder chip (click to refill the input).
- **Pipeline** view shows the **name of the configured Google Drive folder**
  (new `get_folder_name` + `/transcripts/drive-folder` endpoint).
- **Training Dataset**: removed the **Pending Review** tab (Knowledge Base only).
- **Login**: smaller "Forgot password?" font.
- **New agent call notification** now fires from **any** dashboard section once the
  agent/admin is **Online** (moved to a shared `useNewEscalationAlert` hook at the
  shell level; lifted the admin online state into `AdminShell`).

## 8. Fix: "Run complete pipeline" not working
- The Run button sent `null`, so it required `GOOGLE_DRIVE_TRANSCRIPTS_FOLDER_ID`; when
  unset it 400'd. Run now **falls back to the recently-used Drive folder** (from
  Upload → Drive) when no default is configured, and surfaces the backend error if there's
  no folder at all. (`components/admin/sections/PipelineMonitor.tsx`)

## Files touched
- **Backend:** `services/escalation/service.py`, `api/v1/routes/escalation.py`,
  `api/v1/routes/chat.py`, `api/v1/routes/transcripts.py`, `schemas/escalation.py`,
  `services/ws/connection_manager.py`, `services/storage/google_drive_service.py`
- **Frontend:** `components/escalation/ChatPanel.tsx`, `components/admin/sections/EscalationQueue.tsx`,
  `components/admin/sections/{ChatLogs,Ratings,Training,UploadSection,PipelineMonitor}.tsx`,
  `components/admin/AdminShell.tsx`, `components/agent/sections/AgentQueue.tsx`,
  `components/agent/AgentShell.tsx`, `components/admin/KnowledgeApprovedList.tsx`,
  `components/admin/KnowledgePendingList.tsx`, `pages/LoginPage.tsx`,
  `hooks/useChat.ts`, `hooks/useEscalation.ts`, `hooks/useNewEscalationAlert.ts` (new),
  `api/escalation.ts`, `api/transcripts.ts`

> Note: backend verified with `py_compile`; frontend lint/`tsc` not run (deps not installed
> in this checkout) — run `npm run lint` before committing.

---

# Session 2 — RAG, scheduled sync, responsive, build time

## 1. Escalation resolve: removed the resolution note (`napomena`)
- Dropped the agent-entered resolution note end-to-end: `EscalationResolve` schema, the
  resolve route/service param, the `EscalationResolvePayload`/`ChatPanel` payload, and the
  "Resolution Note" display in `MyHistory`. (Auto status reasons set by expire/cancel kept.)

## 2. Issues
- **Publishing a Q&A to the KB clears the originating Issue:** on resolve-with-`submit_to_kb`,
  anomalies for that chat session are deleted (`_clear_session_anomalies`).
- **No more JS `confirm` on delete** — single-row Issue delete (and later Transcript delete)
  happen immediately on click.

## 3. RAG — classify first, then retrieve (KB authoritative)
- Root cause: the intent classifier ran *before* retrieval and labelled in-KB questions
  (e.g. "How much are your agents paid?", AC-unit specs) `out_of_scope`, so the KB was never
  searched. Verified live: DB/Qdrant in sync (22/22), classifier mislabels confirmed.
- Fix: an `out_of_scope` verdict no longer short-circuits — the KB is still searched. Then made
  it **stricter** for a Telemach agent: off-topic content must clear a dedicated, env-tunable
  floor `RAG_OFFTOPIC_THRESHOLD` (default **0.5**) to answer; domain keeps the 0.35 floor.
  Prompt-injection stays a hard block. (`services/ai/rag_service.py`, `core/config.py`)

## 4. Scheduled Google Drive sync — admin-controlled from the UI
- **Admin → Pipeline → "Automatic schedule":** enable + frequency (hourly/daily/weekly) +
  time, all in **Bosnian time (Europe/Sarajevo)**, DST-correct (`zoneinfo` + `tzdata`).
- Singleton config `drive_sync_schedule` (model + Alembic `005`, self-creates at startup so
  prod needs no manual migration); admin-only `GET/PUT /api/v1/schedule/drive`.
- **In-process scheduler** (`services/schedule/scheduler.py`, started from lifespan) ticks each
  minute and runs `import_drive_folder` when due — safe because the backend is a single
  always-warm replica. Removed the fixed Bicep cron Job (would double-fire); kept
  `POST /internal/sync-drive` for manual/external triggers.
- Documented in `SCHEDULED_SYNC.md`.

## 5. Live progress shows imports happening (manual + scheduled)
- Unified a shared `running` flag (`services/schedule/runtime_state.py`) set by
  `import_drive_folder`, surfaced via the schedule endpoint.
- Pipeline **Live progress**: spinner + "Importing" pill, "checking the folder…" message,
  per-file **pulsing dot + real filename** (strips `gdrive:` prefix), live stage steppers.
  Auto-refreshes (no manual refresh), keeps polling for the whole run, ~5s detection,
  and a persistent **"Last scheduled run: <time> · <result>"** line.

## 6. Responsiveness
- **End-user pages:** Login/Landing/Home already largely responsive; centered + de-crowded
  the Chat/Home headers (laurels hidden on mobile, fluid sizing).
- **Admin & Agent dashboards:** sidebar → **overlay drawer on mobile** (backdrop, closes on
  nav tap), inline on desktop; condensed headers; wide `.tbl` tables scroll horizontally.

## 7. Backend build time
- Dropped the `apt build-essential/libpq-dev` layer (all deps have cp312 wheels;
  psycopg2-binary/asyncpg bundle libpq).
- Reverted an ML-layer split that made pip install latest transitive deps then
  uninstall/downgrade them; now a **single `pip install`** + **pinned langchain transitive
  deps** (`langchain-core==0.2.8`, `langchain-text-splitters==0.2.1`, `langsmith==0.1.81`)
  to stop resolver backtracking. Kept CPU-torch layer + cache mount.

## 8. Branding
- Centered **AMBASSADOR / CALL CENTER CHATBOT** on the chat header (3-column grid).
- Browser title → **"Ambassador — Call Center Chatbot"**; added a brand-matching gold "A"
  coin **favicon** (`public/favicon.svg`).

## Files touched (session 2)
- **Backend:** `services/ai/rag_service.py`, `core/config.py`, `services/escalation/service.py`,
  `api/v1/routes/{escalation,chat,schedule,internal}.py`, `schemas/{escalation,schedule}.py`,
  `db/models/schedule.py`, `alembic/versions/005_drive_sync_schedule.py`,
  `services/schedule/{scheduler,runtime_state}.py`, `tasks/transcript_tasks.py`, `main.py`,
  `api/v1/router.py`, `Dockerfile`, `requirements.txt`, `tests/conftest.py`
- **Frontend:** `components/chat/ChatWindow.tsx`, `pages/HomePage.tsx`,
  `components/admin/AdminShell.tsx`, `components/agent/AgentShell.tsx`,
  `components/admin/sections/{PipelineMonitor,DriveScheduleCard,Issues,TranscriptList,MyHistory}.tsx`
  (DriveScheduleCard new), `api/{escalation,schedule}.ts` (schedule new), `index.css`,
  `index.html`, `public/favicon.svg` (new)
- **Infra/docs:** `infra/main.bicep`, `DEPLOY-AZURE.md`, `DRIVE_IMPORT_AND_BUILD_NOTES.md`,
  `SCHEDULED_SYNC.md` (new)

> Verified with `py_compile` + a timezone/RAG date-math sanity test; frontend `tsc`/ESLint and
> `docker build` not run in this checkout — build before deploying. Backend changes need a redeploy.

---

# Session 3 — scheduled import timing, cancel, bulk delete, live titles

## 1. Scheduled import fires on time (not ~50s late)
- The in-process scheduler slept a flat 60s, so a `HH:MM` run was noticed up to a minute
  after the offset where the loop happened to start. Now the loop **sleeps to the top of the
  next minute**, so a run scheduled for `HH:MM` fires at `HH:MM:00` (≈sub-second).
  (`services/schedule/scheduler.py`)

## 2. Cancel a Drive import (manual + scheduled)
- Shared cancel via `runtime_state`: `request_cancel()`/`is_cancelling()` (+ `cancelling`
  flag in the snapshot). The import loop checks it **before each file and again right after
  the (slow) download**, so a cancel skips the rest of the batch and the current file's heavy
  processing — cooperative, so a file already mid-transcription finishes (Groq call can't be
  interrupted). New `POST /api/v1/schedule/drive/cancel` (admin).
- **UI:** Cancel button on the **DriveScheduleCard** (next to the running badge) and the
  **manual Drive panel** (`UploadSection`). Manual cancel updates the UI optimistically and
  fires the request without blocking, so it reacts instantly; the button is tracked by an
  `importing` flag so it stays visible for the **whole** active import (fixes it not showing
  when files processed faster than a poll tick).
- (`runtime_state.py`, `tasks/transcript_tasks.py`, `schemas/schedule.py`,
  `routes/schedule.py`, `api/schedule.ts`, `DriveScheduleCard.tsx`, `UploadSection.tsx`)

## 3. Live per-file titles on the scheduled progress
- `runtime_state` now carries a `files` list (`set_files`/`update_file`). The import seeds the
  **titles as soon as the folder is listed** (before any processing) and transitions each
  `pending → importing → imported` (or `skipped`/`failed`). Exposed as
  `DriveScheduleRead.files`; the card renders an "Importing N files" panel with live per-file
  status. Card poll tightened **5s → 1.5s** for faster appearance.

## 4. Bulk delete ("Delete selected") on Transcripts — like Issues
- New admin `POST /api/v1/transcripts/bulk-delete` (reuses `purge_transcript`:
  segments / KB entries / Qdrant vectors / token map, one commit). Checkbox column +
  select-all + "Delete selected (N)" toolbar button in `TranscriptList`.
- **No JS `confirm`** on either single or bulk transcript delete (deletes immediately).

## 5. Chat Logs title — skip greetings
- `_is_real` (the per-conversation title picker) now also rejects smalltalk via the existing
  `_is_smalltalk`, so a "Pozdrav/Zdravo" turn answered by retrieval no longer becomes the
  row title — the real question shows instead. (`routes/chat.py`)

## 6. Verified: Ratings "Score Trend — Last 14 Days"
- Reviewed the path (`/chat/ratings` builds `trend` from `Feedback.timestamp_fb` in the last
  14 days, grouped per day; `Ratings.tsx` renders the bars) — functionally correct. Note: it
  only emits days that have ratings (so <14 bars possible); empty window shows "No data".

## Files touched (session 3)
- **Backend:** `services/schedule/{scheduler,runtime_state}.py`, `tasks/transcript_tasks.py`,
  `schemas/{schedule,transcript}.py`, `api/v1/routes/{schedule,transcripts,chat}.py`
- **Frontend:** `api/{schedule,transcripts}.ts`,
  `components/admin/sections/{DriveScheduleCard,UploadSection,TranscriptList}.tsx`
- **Infra (unrelated recovery):** restored `docker-compose.yml`, which had been overwritten
  with non-YAML text (failed `docker-compose up`), from the last commit.

> Backend verified with `py_compile`/`ast` only; frontend `tsc`/ESLint not run (deps not
> installed in this checkout) — run `npm run lint` before committing. Backend needs a redeploy.
