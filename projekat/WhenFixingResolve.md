# When Fixing Resolve → Submit to Knowledge Base

Context on how "Submit agent answer to Knowledge Base" currently
works in the Escalation Queue, plus what I want to change.

## How it works now

1. **Escalation Queue → Resolve form** (`frontend/src/components/escalation/ChatPanel.tsx`)
   - Checking "Submit agent answer to Knowledge Base (pending approval)" reveals a textarea
     for the agent answer.
   - On **Confirm Resolve** it sends `POST /escalation/{id}/resolve` with:
     - `submit_to_kb: true`
     - `odgovor_agenta`: the textarea content
     - `pitanje_korisnika`: auto-filled from the **first user message** in the thread
       (`item.razgovor.find(m => m.role === "user")?.content`)

2. **Backend** (`backend/app/services/escalation/service.py` → `resolve_escalation`, ~line 144)
   - Marks the escalation `Rijesena`, frees the agent, notifies the user.
   - Only if `submit_to_kb AND pitanje AND odgovor` are all truthy, inserts a new
     `UnosBazeZnanja` row with `status_aprovacije="NaCekanju"`, `aktivan=True`,
     `verzija_broj=1`. `pregledano` defaults to `False`, `vector_id` is null.

3. **Result:** the row shows up in **Knowledge → Pending** (moderation list) but is **NOT**
   searchable yet — it only goes live (embedded into Qdrant) after a separate
   **Approve** step (`POST /knowledge/{id}/approve`), which sets `status_aprovacije="Odobren"`,
   `pregledano=True`, and indexes it.

## What I want to change (TODO tomorrow)

**The submitted chat answer should automatically go into the knowledge base** (be approved
and live/searchable immediately on resolve) — no separate manual approval step needed.

**But it should still show up in the sidebar "Training dataset" admin section**, so the admin
can still **edit** or **delete** it afterwards if they want. So: auto-publish, but keep it
visible and manageable in the admin UI.

## Existing gotchas to also fix while in here

1. **Silent no-op if the answer textarea is empty.** Frontend gates `odgovor_agenta` on the
   checkbox but never checks it's non-empty. If you check the box but leave the answer blank,
   the escalation resolves fine but `if submit_to_kb and pitanje and odgovor` quietly fails —
   nothing is added, no error. → Disable Confirm Resolve / show a hint when checked but empty.

2. **`pitanje_korisnika` is the first user message, which may be wrong.** It grabs the first
   user turn. If the customer opened with "hi" / "I need help", the KB entry gets a useless
   question paired with the agent's answer, hurting future retrieval. → Let the agent edit the
   auto-filled question (editable field instead of silently using the first message).

## What I want for the question (TODO tomorrow)

- **Fix `pitanje_korisnika` to be the REAL question**, not just the first user message. The
  first turn is often a greeting ("hi" / "I need help"), so pairing it with the agent answer
  pollutes the KB. Pick the actual question the customer asked.
- **Put the question in an editable field** in the resolve form so the agent can correct/edit
  it before it gets imported into the knowledge base.
- **Stretch idea:** instead of one auto-picked question, show each user message in the chat
  with its own checkbox, so the agent can tick which question(s) should be imported to the
  knowledge base (paired with the agent answer) and which should NOT. Per-question control over
  what becomes a KB entry.

## Files involved

- `frontend/src/components/escalation/ChatPanel.tsx` — resolve form
- `frontend/src/api/escalation.ts` — `EscalationResolvePayload`, `resolve()`
- `backend/app/api/v1/routes/escalation.py` — `POST /{escalation_id}/resolve`
- `backend/app/services/escalation/service.py` — `resolve_escalation()`
- `backend/app/api/v1/routes/knowledge.py` — `approve_item()` shows what "go live" requires
  (set `Odobren` + `pregledano=True` + `embed_and_index_item`)
- Training dataset admin: `frontend/src/components/admin/sections/Training.tsx`
