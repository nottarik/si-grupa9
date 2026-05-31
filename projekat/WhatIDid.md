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
