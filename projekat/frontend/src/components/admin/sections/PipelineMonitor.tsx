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

export default function PipelineMonitor() {
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [active, setActive] = useState<Transcript[]>([]);
  const [folderName, setFolderName] = useState<string | null>(null);
  const [schedRunning, setSchedRunning] = useState(false);

  useEffect(() => {
    getDriveFolder().then((f) => setFolderName(f.name)).catch(() => {});
  }, []);

  const pollRef = useRef<number | null>(null);
  const attemptsRef = useRef(0);
  const emptyStreakRef = useRef(0);

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
      if (emptyStreakRef.current >= 6) stopPolling(); // ~15s idle → stop
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
        setSchedRunning(s.running);
        if (s.running && pollRef.current === null) startPolling();
      } catch {
        /* ignore */
      }
    }
    checkSchedule();
    const id = window.setInterval(checkSchedule, 10_000);
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

      {schedRunning && (
        <div
          className="card p-4 flex items-center gap-3"
          style={{ borderLeft: "3px solid #C5A059", background: "rgba(197,160,89,0.06)" }}
        >
          <span className="w-2 h-2 rounded-full animate-pulse flex-shrink-0" style={{ background: "#C5A059" }} />
          <p className="text-sm" style={{ color: "#6b5a3a" }}>
            Scheduled import is running — checking the Drive folder and processing new files.
            Progress appears below.
          </p>
        </div>
      )}

      <div className="card p-6 space-y-3">
        <p className="text-sm font-semibold text-charcoal">Live progress</p>
        {active.length === 0 ? (
          <p className="text-xs text-gray-400">No transcripts are currently processing.</p>
        ) : (
          <ul className="divide-y divide-gray-100 border border-gray-100 rounded-lg">
            {active.map((t) => (
              <li
                key={t.id}
                className="flex items-center justify-between px-3 py-2 text-sm gap-3"
              >
                <span className="text-charcoal truncate mr-3">{t.naziv}</span>
                <StageStepper status={t.status} stage={t.pipeline_stage} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
