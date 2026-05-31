import { useEffect, useState } from "react";
import {
  DriveFileProgress,
  DriveFileStatus,
  DriveSchedule,
  Frequency,
  cancelDriveImport,
  getDriveSchedule,
  updateDriveSchedule,
} from "../../../api/schedule";

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

const FILE_STATUS: Record<DriveFileStatus, { label: string; color: string }> = {
  pending: { label: "Waiting…", color: "#9ca3af" },
  importing: { label: "Importing…", color: "#8a6d1f" },
  imported: { label: "✓ Imported", color: "#15803d" },
  skipped: { label: "Already imported", color: "#9ca3af" },
  failed: { label: "✗ Failed", color: "#dc2626" },
};

interface FormState {
  enabled: boolean;
  frequency: Frequency;
  hour: number;
  minute: number;
  day_of_week: number;
}

interface LiveState {
  running: boolean;
  cancelling: boolean;
  last_result: string | null;
  last_run_at: string | null;
  next_run_at: string | null;
  files: DriveFileProgress[];
}

function pad(n: number): string {
  return n.toString().padStart(2, "0");
}

function fmt(iso: string | null): string {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("en-GB", {
    timeZone: "Europe/Sarajevo",
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function DriveScheduleCard() {
  const [form, setForm] = useState<FormState | null>(null);
  const [live, setLive] = useState<LiveState | null>(null);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  function applyLive(s: DriveSchedule) {
    setLive({
      running: s.running,
      cancelling: s.cancelling,
      last_result: s.last_result,
      last_run_at: s.last_run_at,
      next_run_at: s.next_run_at,
      files: s.files ?? [],
    });
  }

  async function handleCancel() {
    // Reflect the cancel immediately; the fast poll below picks up running=false soon after.
    setLive((l) => (l ? { ...l, cancelling: true } : l));
    try {
      applyLive(await cancelDriveImport());
    } catch {
      setMessage("Could not cancel the import. Please try again.");
    }
  }

  // Load once for the form; then poll live status so a scheduled run shows up here.
  useEffect(() => {
    let active = true;
    getDriveSchedule()
      .then((s) => {
        if (!active) return;
        setForm({
          enabled: s.enabled,
          frequency: s.frequency,
          hour: s.hour,
          minute: s.minute,
          day_of_week: s.day_of_week,
        });
        applyLive(s);
      })
      .catch(() => {});
    const id = window.setInterval(() => {
      getDriveSchedule().then((s) => active && applyLive(s)).catch(() => {});
    }, 1_500);
    return () => {
      active = false;
      clearInterval(id);
    };
  }, []);

  function patch(p: Partial<FormState>) {
    setForm((f) => (f ? { ...f, ...p } : f));
    setMessage("");
  }

  async function handleSave() {
    if (!form) return;
    setSaving(true);
    setMessage("");
    try {
      const saved = await updateDriveSchedule(form);
      applyLive(saved);
      setMessage(saved.enabled ? "Schedule saved." : "Automatic import turned off.");
    } catch {
      setMessage("Could not save the schedule. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  if (!form) return null;

  return (
    <div className="card p-5 sm:p-6 space-y-4">
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <p className="text-sm font-semibold text-charcoal">Automatic schedule</p>
          <p className="text-xs mt-1" style={{ color: "#6b5a3a" }}>
            Run the Drive import automatically on a recurring schedule. Times are in
            Bosnian time (Europe/Sarajevo).
          </p>
        </div>
        {live?.running && (
          <div className="flex items-center gap-2 flex-shrink-0">
            <span
              className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full"
              style={{ background: "rgba(197,160,89,0.12)", color: "#8a6d1f", border: "1px solid rgba(197,160,89,0.35)" }}
            >
              <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "#C5A059" }} />
              {live.cancelling ? "Cancelling…" : "Checking & importing files…"}
            </span>
            <button
              className="outline-btn text-xs py-1"
              onClick={handleCancel}
              disabled={live.cancelling}
            >
              Cancel
            </button>
          </div>
        )}
      </div>

      {/* Live per-file progress — titles appear as soon as the run lists the folder. */}
      {live?.running && live.files.length > 0 && (
        <div
          className="rounded-lg border"
          style={{ borderColor: "rgba(197,160,89,0.2)", background: "rgba(249,245,239,0.5)" }}
        >
          <div
            className="px-3 py-2 text-xs font-semibold tracking-widest text-gold uppercase"
            style={{ borderBottom: "1px solid rgba(197,160,89,0.15)" }}
          >
            Importing {live.files.length} file{live.files.length > 1 ? "s" : ""}
          </div>
          <ul className="divide-y divide-gray-100" style={{ maxHeight: 200, overflowY: "auto" }}>
            {live.files.map((f) => {
              const s = FILE_STATUS[f.status] ?? FILE_STATUS.pending;
              return (
                <li
                  key={f.name}
                  className="flex items-center justify-between gap-3 px-3 py-1.5 text-sm"
                >
                  <span className="text-charcoal truncate">{f.name}</span>
                  <span className="text-xs shrink-0" style={{ color: s.color }}>
                    {s.label}
                  </span>
                </li>
              );
            })}
          </ul>
        </div>
      )}

      <label className="flex items-center gap-2 text-sm text-charcoal cursor-pointer">
        <input
          type="checkbox"
          checked={form.enabled}
          onChange={(e) => patch({ enabled: e.target.checked })}
          className="accent-gold"
        />
        Enable automatic import
      </label>

      <div className="flex flex-wrap items-end gap-4" style={{ opacity: form.enabled ? 1 : 0.5 }}>
        <div className="space-y-1">
          <label className="text-xs font-semibold tracking-widest text-gold uppercase block">
            Frequency
          </label>
          <select
            className="input-field"
            style={{ width: 140 }}
            disabled={!form.enabled}
            value={form.frequency}
            onChange={(e) => patch({ frequency: e.target.value as Frequency })}
          >
            <option value="hourly">Hourly</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
        </div>

        {form.frequency === "weekly" && (
          <div className="space-y-1">
            <label className="text-xs font-semibold tracking-widest text-gold uppercase block">
              Day
            </label>
            <select
              className="input-field"
              style={{ width: 140 }}
              disabled={!form.enabled}
              value={form.day_of_week}
              onChange={(e) => patch({ day_of_week: Number(e.target.value) })}
            >
              {DAYS.map((d, i) => (
                <option key={d} value={i}>
                  {d}
                </option>
              ))}
            </select>
          </div>
        )}

        {form.frequency !== "hourly" && (
          <div className="space-y-1">
            <label className="text-xs font-semibold tracking-widest text-gold uppercase block">
              Hour
            </label>
            <select
              className="input-field"
              style={{ width: 90 }}
              disabled={!form.enabled}
              value={form.hour}
              onChange={(e) => patch({ hour: Number(e.target.value) })}
            >
              {Array.from({ length: 24 }, (_, h) => (
                <option key={h} value={h}>
                  {pad(h)}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="space-y-1">
          <label className="text-xs font-semibold tracking-widest text-gold uppercase block">
            Minute
          </label>
          <select
            className="input-field"
            style={{ width: 90 }}
            disabled={!form.enabled}
            value={form.minute}
            onChange={(e) => patch({ minute: Number(e.target.value) })}
          >
            {Array.from({ length: 60 }, (_, m) => (
              <option key={m} value={m}>
                {pad(m)}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex items-center gap-4 flex-wrap">
        <button className="gold-btn" onClick={handleSave} disabled={saving}>
          {saving ? "Saving…" : "Save schedule"}
        </button>
        {message && (
          <span className="text-xs" style={{ color: "#8a6d1f" }}>
            {message}
          </span>
        )}
      </div>

      <div className="text-xs text-gray-400 pt-2" style={{ borderTop: "1px solid rgba(197,160,89,0.15)" }}>
        <div className="flex flex-wrap gap-x-6 gap-y-1 mt-1">
          <span>
            Next run:{" "}
            <span className="text-charcoal">{form.enabled ? fmt(live?.next_run_at ?? null) : "—"}</span>
          </span>
          <span>
            Last run: <span className="text-charcoal">{fmt(live?.last_run_at ?? null)}</span>
          </span>
          {live?.last_result && (
            <span>
              Result: <span className="text-charcoal">{live.last_result}</span>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
