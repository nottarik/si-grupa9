import { useState } from "react";
import { useAuth } from "../../../hooks/useAuth";
import { useSubViewBack } from "../../../hooks/useSubViewBack";
import { Ic, StatusBadge, icons } from "../shared";

interface Issue {
  id: number;
  title: string;
  severity: string;
  status: string;
  date: string;
  reporter: string;
  description?: string;
}

const INITIAL_ISSUES: Issue[] = [
  { id: 1, title: "AI answered incorrectly about refund deadline", severity: "High", status: "Open", date: "2024-04-26", reporter: "Marko P." },
  { id: 2, title: "Response time exceeded 10 seconds", severity: "Medium", status: "In Progress", date: "2024-04-25", reporter: "Ana K." },
  { id: 3, title: "Transcription failed for audio file", severity: "High", status: "Resolved", date: "2024-04-24", reporter: "Ivana B." },
  { id: 4, title: "Wrong escalation path suggested", severity: "Low", status: "Open", date: "2024-04-23", reporter: "Tomislav R." },
  { id: 5, title: "Chat log not saving after session end", severity: "Medium", status: "In Progress", date: "2024-04-22", reporter: "Ana K." },
];

const EMPTY_FORM = { title: "", severity: "Medium", reporter: "", description: "" };

function IssueDetail({ issue, onBack }: { issue: Issue; onBack: () => void }) {
  const [status, setStatus] = useState(issue.status);

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Issue #{issue.id}</h2>
        <button className="outline-btn text-xs" onClick={onBack}>
          ← Back to List
        </button>
      </div>
      <div className="card p-6 space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="text-base font-semibold text-charcoal">{issue.title}</div>
            <div className="text-xs text-gray-400 mt-1">
              Reported by {issue.reporter} · {issue.date}
            </div>
          </div>
          <div className="flex gap-2 flex-shrink-0">
            <StatusBadge s={issue.severity} />
            <StatusBadge s={status} />
          </div>
        </div>

        <div className="meander" />

        {issue.description && (
          <div className="space-y-3">
            <div className="text-xs font-semibold tracking-widest text-gold uppercase">
              Description
            </div>
            <p className="text-sm text-charcoal leading-relaxed">{issue.description}</p>
          </div>
        )}

        <div className="space-y-2">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase">
            Update Status
          </div>
          <div className="flex gap-2">
            {["Open", "In Progress", "Resolved"].map((s) => (
              <button
                key={s}
                className={status === s ? "gold-btn" : "outline-btn"}
                style={{ fontSize: 12, padding: "6px 14px" }}
                onClick={() => setStatus(s)}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-2">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase">
            Add Note
          </div>
          <textarea
            className="input-field"
            rows={3}
            placeholder="Add a note or resolution detail…"
          />
          <button className="gold-btn" style={{ fontSize: 12 }}>
            Save Note
          </button>
        </div>
      </div>
    </div>
  );
}

function ReportModal({
  onClose,
  onSubmit,
  defaultReporter,
}: {
  onClose: () => void;
  onSubmit: (issue: Omit<Issue, "id" | "status" | "date">) => void;
  defaultReporter: string;
}) {
  const [form, setForm] = useState({ ...EMPTY_FORM, reporter: defaultReporter });
  const [error, setError] = useState("");

  function handleSubmit() {
    if (!form.title.trim()) { setError("Title is required."); return; }
    onSubmit({ title: form.title.trim(), severity: form.severity, reporter: defaultReporter, description: form.description.trim() });
    onClose();
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ background: "rgba(0,0,0,0.35)", backdropFilter: "blur(4px)" }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="card p-6 space-y-4 w-full max-w-md mx-4">
        <div className="flex items-center justify-between">
          <div className="font-cinzel font-bold text-charcoal tracking-widest text-sm">
            Report Issue
          </div>
          <button className="text-gray-400 hover:text-gold transition-colors text-lg leading-none" onClick={onClose}>×</button>
        </div>

        <div className="meander" />

        {error && (
          <div className="text-xs px-3 py-2 rounded" style={{ background: "rgba(239,68,68,0.08)", color: "#ef4444", border: "1px solid rgba(239,68,68,0.2)" }}>
            {error}
          </div>
        )}

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Title</label>
            <input
              className="input-field"
              placeholder="Describe the issue briefly…"
              value={form.title}
              onChange={(e) => { setForm((f) => ({ ...f, title: e.target.value })); setError(""); }}
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Severity</label>
              <select
                className="input-field"
                value={form.severity}
                onChange={(e) => setForm((f) => ({ ...f, severity: e.target.value }))}
              >
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Reporter</label>
              <div
                className="input-field"
                style={{ color: "#6b7280", background: "rgba(249,245,239,0.8)", cursor: "default" }}
              >
                {defaultReporter}
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "rgba(197,160,89,0.9)" }}>Description</label>
            <textarea
              className="input-field"
              rows={3}
              placeholder="Provide additional details…"
              value={form.description}
              onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
            />
          </div>
        </div>

        <div className="flex gap-2 justify-end pt-1">
          <button className="outline-btn text-xs py-1.5" onClick={onClose}>Cancel</button>
          <button className="gold-btn text-xs py-1.5" onClick={handleSubmit}>Submit Report</button>
        </div>
      </div>
    </div>
  );
}

export default function Issues() {
  const { user } = useAuth();
  const [issues, setIssues] = useState<Issue[]>(INITIAL_ISSUES);
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [detail, setDetail] = useState<Issue | null>(null);
  const [reporting, setReporting] = useState(false);
  const reporterName = user?.full_name || "Admin";

  useSubViewBack(detail !== null, () => setDetail(null));

  function handleReport(data: Omit<Issue, "id" | "status" | "date">) {
    const today = new Date().toISOString().slice(0, 10);
    setIssues((prev) => [
      { id: prev.length + 1, status: "Open", date: today, ...data },
      ...prev,
    ]);
  }

  if (detail) {
    return <IssueDetail issue={detail} onBack={() => setDetail(null)} />;
  }

  const filtered = issues.filter((i) => {
    const matchesFilter = filter === "All" || i.status === filter;
    const matchesSearch = !search || i.title.toLowerCase().includes(search.toLowerCase()) || i.reporter.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="space-y-5">
      {reporting && <ReportModal onClose={() => setReporting(false)} onSubmit={handleReport} defaultReporter={reporterName} />}

      <div className="flex items-center justify-between">
        <h2 className="section-title">Issues</h2>
        <button className="gold-btn flex items-center gap-2" onClick={() => setReporting(true)}>
          <span>+</span> Report Issue
        </button>
      </div>

      <div className="card overflow-hidden">
        <div
          className="p-4 flex gap-2 flex-wrap"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          {["All", "Open", "In Progress", "Resolved"].map((s) => (
            <button
              key={s}
              className={`tab-btn ${filter === s ? "active" : ""}`}
              onClick={() => setFilter(s)}
            >
              {s}
            </button>
          ))}
          <div className="ml-auto relative">
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
              <Ic d={icons.search} />
            </span>
            <input
              className="input-field"
              placeholder="Search issues…"
              style={{ width: 200, paddingRight: "2.25rem" }}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        <table className="tbl">
          <thead>
            <tr>
              <th>#</th>
              <th>Title</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Reporter</th>
              <th>Date</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 && (
              <tr>
                <td colSpan={7} className="text-center text-gray-400 py-8 text-sm">
                  No issues match your search.
                </td>
              </tr>
            )}
            {filtered.map((i) => (
              <tr key={i.id}>
                <td className="text-gray-400 font-mono text-xs">{i.id}</td>
                <td className="font-medium text-charcoal">{i.title}</td>
                <td><StatusBadge s={i.severity} /></td>
                <td><StatusBadge s={i.status} /></td>
                <td>{i.reporter}</td>
                <td className="text-gray-400">{i.date}</td>
                <td>
                  <button
                    className="outline-btn py-1 text-xs"
                    onClick={() => setDetail(i)}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
