import { useEffect, useRef, useState } from "react";
import { importDriveTranscripts, listActiveTranscripts } from "../../../api/transcripts";
import type { Transcript } from "../../../types";
import { StageStepper } from "../PipelineStage";

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

  async function handleRun() {
    setRunning(true);
    setError("");
    setMessage("");
    try {
      const res = await importDriveTranscripts(null, "bs");
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
