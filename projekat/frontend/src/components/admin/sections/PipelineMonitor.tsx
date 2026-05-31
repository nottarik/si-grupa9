import { useEffect, useRef, useState } from "react";
import { getDriveFolder, importDriveTranscripts, listActiveTranscripts } from "../../../api/transcripts";
import { getDriveSchedule } from "../../../api/schedule";
import type { Transcript } from "../../../types";
import { StageStepper } from "../PipelineStage";
import DriveScheduleCard from "./DriveScheduleCard";

const RECENT_DRIVE_KEY = "recent_drive_folder";

// Accept a bare folder ID or a pasted Drive URL and return the ID.
function extractDriveId(input: string): string {
  const s = (input || "").trim();
  const patterns = [/\/folders\/([a-zA-Z0-9_-]+)/, /\/d\/([a-zA-Z0-9_-]+)/, /[?&]id=([a-zA-Z0-9_-]+)/];
  for (const re of patterns) {
    const m = s.match(re);
    if (m) return m[1];
  }
  return s;
}

function extractError(e: unknown): string {
  if (e && typeof e === "object" && "response" in e) {
    const resp = (e as { response?: { data?: { detail?: unknown } } }).response;
    const detail = resp?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg as string;
  }
  if (e instanceof Error) return e.message;
  return "An unexpected error occurred. Please try again.";
}

function fmtSchedTime(iso: string): string {
  return new Date(iso).toLocaleString("en-GB", {
    timeZone: "Europe/Sarajevo",
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Drive imports are stored as "gdrive:<folder>:<filename>" — show just the filename.
function displayName(naziv: string): string {
  if (naziv.startsWith("gdrive:")) {
    const second = naziv.indexOf(":", naziv.indexOf(":") + 1);
    if (second >= 0) return naziv.slice(second + 1);
  }
  return naziv;
}

export default function PipelineMonitor() {
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [active, setActive] = useState<Transcript[]>([]);
  const [folderName, setFolderName] = useState<string | null>(null);
  const [sched, setSched] = useState<{
    running: boolean;
    last_run_at: string | null;
    last_result: string | null;
  } | null>(null);
  const importRunning = sched?.running ?? false;

  useEffect(() => {
    getDriveFolder().then((f) => setFolderName(f.name)).catch(() => {});
  }, []);

  const pollRef = useRef<number | null>(null);
  const attemptsRef = useRef(0);
  const emptyStreakRef = useRef(0);
  // Mirrors sched.running for the poll loop: while an import is running we keep polling
  // even through empty gaps, so the file list stays live the whole time.
  const runningRef = useRef(false);

  function stopPolling() {
    if (pollRef.current !== null) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }

  async function poll() {
    attemptsRef.current += 1;
    try {
      const list = await listActiveTranscripts();
      setActive(list);
      // import-drive returns before rows exist, and files process sequentially, so /active
      // is briefly empty mid-run. Only stop after a run of empties, not the first one.
      emptyStreakRef.current = list.length === 0 ? emptyStreakRef.current + 1 : 0;
      // Stop only when idle AND no import is running — never abandon an in-progress run.
      if (emptyStreakRef.current >= 6 && !runningRef.current) stopPolling(); // ~15s idle
    } catch {
      // transient — keep trying
    }
    if (attemptsRef.current >= 240) stopPolling(); // ~10-min safety cap
  }

  function startPolling() {
    stopPolling();
    attemptsRef.current = 0;
    emptyStreakRef.current = 0;
    pollRef.current = window.setInterval(poll, 2500);
    void poll();
  }

  // Show anything already mid-pipeline on mount; the poll self-terminates if idle.
  useEffect(() => {
    startPolling();
    return () => stopPolling();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Watch the scheduled runner so a run triggered by the clock (not the button) is
  // visible: when it's running, surface a banner and keep the live-progress poll going.
  useEffect(() => {
    let alive = true;
    async function checkSchedule() {
      try {
        const s = await getDriveSchedule();
        if (!alive) return;
        setSched({ running: s.running, last_run_at: s.last_run_at, last_result: s.last_result });
        runningRef.current = s.running;
        if (s.running && pollRef.current === null) startPolling();
      } catch {
        /* ignore */
      }
    }
    checkSchedule();
    // Poll fairly often so a run that fires at the scheduled minute is reflected
    // promptly — and so the "last run" stamp updates within a few seconds.
    const id = window.setInterval(checkSchedule, 5_000);
    return () => {
      alive = false;
      clearInterval(id);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleRun() {
    setRunning(true);
    setError("");
    setMessage("");
    try {
      // Prefer the configured default folder; fall back to the last folder the admin
      // imported from (Upload → Drive) so Run works even without the env var set.
      let recent = "";
      try { recent = localStorage.getItem(RECENT_DRIVE_KEY) || ""; } catch { /* ignore */ }
      const folder = folderName ? null : recent ? extractDriveId(recent) : null;
      const res = await importDriveTranscripts(folder, "bs");
      setMessage(res.message);
      startPolling();
    } catch (e: unknown) {
      setError(extractError(e));
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="card p-6 space-y-3">
        <div>
          <p className="text-sm font-semibold text-charcoal">Run complete pipeline</p>
          <p className="text-xs mt-1" style={{ color: "#6b5a3a" }}>
            Scans the configured Google Drive folder for new files and runs the full pipeline
            (transcription → cleaning → knowledge base) on each. Files already imported are skipped.
          </p>
          {folderName && (
            <p className="text-xs mt-2 flex items-center gap-1.5" style={{ color: "#8a6d1f" }}>
              <span aria-hidden>📁</span>
              <span>
                Folder: <span className="font-semibold">{folderName}</span>
              </span>
            </p>
          )}
        </div>

        <button className="gold-btn" onClick={handleRun} disabled={running}>
          {running ? "Starting…" : "Run complete pipeline"}
        </button>

        {message && (
          <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-2">
            ✓ {message}
          </div>
        )}
        {error && (
          <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            ✗ {error}
          </div>
        )}
      </div>

      <DriveScheduleCard />

      <div className="card p-6 space-y-3">
        <div className="flex items-center gap-2">
          <p className="text-sm font-semibold text-charcoal">Live progress</p>
          {(active.length > 0 || importRunning) && (
            <svg className="animate-spin" width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden>
              <circle cx="12" cy="12" r="9" stroke="rgba(197,160,89,0.25)" strokeWidth="3" />
              <path d="M21 12a9 9 0 0 0-9-9" stroke="#C5A059" strokeWidth="3" strokeLinecap="round" />
            </svg>
          )}
          {importRunning && (
            <span
              className="flex items-center gap-1.5 text-[11px] px-2 py-0.5 rounded-full"
              style={{ background: "rgba(197,160,89,0.12)", color: "#8a6d1f", border: "1px solid rgba(197,160,89,0.35)" }}
            >
              <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "#C5A059" }} />
              Importing
            </span>
          )}
        </div>
        {active.length === 0 ? (
          importRunning ? (
            <p className="text-xs flex items-center gap-2" style={{ color: "#8a6d1f" }}>
              <span className="w-1.5 h-1.5 rounded-full animate-pulse flex-shrink-0" style={{ background: "#C5A059" }} />
              Import running — checking the folder for new files…
            </p>
          ) : (
            <p className="text-xs text-gray-400">No transcripts are currently processing.</p>
          )
        ) : (
          <ul className="divide-y divide-gray-100 border border-gray-100 rounded-lg">
            {active.map((t) => (
              <li
                key={t.id}
                className="flex items-center justify-between px-3 py-2 text-sm gap-3"
              >
                <span className="flex items-center gap-2 min-w-0 mr-3">
                  <span
                    className="w-1.5 h-1.5 rounded-full animate-pulse flex-shrink-0"
                    style={{ background: "#C5A059" }}
                  />
                  <span className="text-charcoal truncate">{displayName(t.naziv)}</span>
                </span>
                <StageStepper status={t.status} stage={t.pipeline_stage} />
              </li>
            ))}
          </ul>
        )}

        {sched?.last_run_at && (
          <p className="text-[11px] pt-1" style={{ color: "#9a8a6a", borderTop: "1px solid rgba(197,160,89,0.12)" }}>
            <span className="inline-block mt-1">
              Last scheduled run:{" "}
              <span className="text-charcoal font-medium">{fmtSchedTime(sched.last_run_at)}</span>
              {sched.last_result ? ` · ${sched.last_result}` : ""}
            </span>
          </p>
        )}
      </div>
    </div>
  );
}
