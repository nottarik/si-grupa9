import { useState } from "react";
import { Ic, StatusBadge, icons } from "../shared";

interface Issue {
  id: number;
  title: string;
  severity: string;
  status: string;
  date: string;
  reporter: string;
}

const ISSUES: Issue[] = [
  { id: 1, title: "AI answered incorrectly about refund deadline", severity: "High", status: "Open", date: "2024-04-26", reporter: "Marko P." },
  { id: 2, title: "Response time exceeded 10 seconds", severity: "Medium", status: "In Progress", date: "2024-04-25", reporter: "Ana K." },
  { id: 3, title: "Transcription failed for audio file", severity: "High", status: "Resolved", date: "2024-04-24", reporter: "Ivana B." },
  { id: 4, title: "Wrong escalation path suggested", severity: "Low", status: "Open", date: "2024-04-23", reporter: "Tomislav R." },
  { id: 5, title: "Chat log not saving after session end", severity: "Medium", status: "In Progress", date: "2024-04-22", reporter: "Ana K." },
];

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

        <div className="space-y-3">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase">
            Description
          </div>
          <p className="text-sm text-charcoal leading-relaxed">
            This issue was flagged during routine quality review. The AI response did
            not align with the current policy documentation. The affected interaction
            has been logged for retraining consideration.
          </p>
        </div>

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

export default function Issues() {
  const [filter, setFilter] = useState("All");
  const [detail, setDetail] = useState<Issue | null>(null);

  if (detail) {
    return <IssueDetail issue={detail} onBack={() => setDetail(null)} />;
  }

  const filtered =
    filter === "All" ? ISSUES : ISSUES.filter((i) => i.status === filter);

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Issues</h2>
        <button className="gold-btn flex items-center gap-2">
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
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <Ic d={icons.search} />
            </span>
            <input
              className="input-field pl-9"
              placeholder="Search issues…"
              style={{ width: 200 }}
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
            {filtered.map((i) => (
              <tr key={i.id}>
                <td className="text-gray-400 font-mono text-xs">{i.id}</td>
                <td className="font-medium text-charcoal">{i.title}</td>
                <td>
                  <StatusBadge s={i.severity} />
                </td>
                <td>
                  <StatusBadge s={i.status} />
                </td>
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
