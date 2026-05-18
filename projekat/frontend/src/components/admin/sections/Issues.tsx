import { useEffect, useState } from "react";
import { useSubViewBack } from "../../../hooks/useSubViewBack";
import { Ic, StatusBadge, icons } from "../shared";
import apiClient from "../../../api/client";

interface Issue {
  id: number;
  title: string;
  severity: string;
  status: string;
  date: string | null;
  type: string | null;
  description: string | null;
}

function IssueDetail({ issue, onBack, onUpdate }: { issue: Issue; onBack: () => void; onUpdate: () => void }) {
  const [status, setStatus] = useState(issue.status);
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSave() {
    setSaving(true);
    try {
      const params: Record<string, string> = {};
      if (status !== issue.status) params.status = status;
      if (note.trim()) params.note = note.trim();
      if (Object.keys(params).length > 0) {
        await apiClient.patch(`/api/v1/chat/issues/${issue.id}`, null, { params });
        onUpdate();
      }
    } catch {
      // ignore
    } finally {
      setSaving(false);
      setNote("");
    }
  }

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
              {issue.type ?? "Unknown type"} · {issue.date}
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
            <p className="text-sm text-charcoal leading-relaxed whitespace-pre-wrap">{issue.description}</p>
          </div>
        )}

        <div className="space-y-2">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase">
            Update Status
          </div>
          <div className="flex gap-2">
            {["Open", "Resolved", "Dismissed"].map((s) => (
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
            value={note}
            onChange={(e) => setNote(e.target.value)}
          />
          <button
            className="gold-btn"
            style={{ fontSize: 12 }}
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? "Saving…" : "Save"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function Issues() {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("All");
  const [search, setSearch] = useState("");
  const [detail, setDetail] = useState<Issue | null>(null);

  useSubViewBack(detail !== null, () => setDetail(null));

  async function fetchIssues(f?: string) {
    setLoading(true);
    try {
      const activeFilter = f ?? filter;
      const params: Record<string, string> = {};
      if (activeFilter !== "All") params.status_filter = activeFilter;
      const { data } = await apiClient.get<Issue[]>("/api/v1/chat/issues", { params });
      setIssues(data);
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchIssues(filter);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  if (detail) {
    return <IssueDetail issue={detail} onBack={() => setDetail(null)} onUpdate={fetchIssues} />;
  }

  const filtered = issues.filter((i) => {
    if (!search) return true;
    return i.title.toLowerCase().includes(search.toLowerCase());
  });

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Issues</h2>
        <span className="text-xs text-gray-400">{issues.length} total</span>
      </div>

      <div className="card overflow-hidden">
        <div
          className="p-4 flex gap-2 flex-wrap"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          {["All", "Open", "Resolved", "Dismissed"].map((s) => (
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

        {loading ? (
          <div className="text-center py-8 text-sm text-gray-400">Loading…</div>
        ) : (
          <table className="tbl">
            <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Type</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Date</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="text-center text-gray-400 py-8 text-sm">
                    No issues found.
                  </td>
                </tr>
              )}
              {filtered.map((i) => (
                <tr key={i.id}>
                  <td className="text-gray-400 font-mono text-xs">{i.id}</td>
                  <td className="font-medium text-charcoal max-w-xs truncate">{i.title}</td>
                  <td className="text-xs text-gray-400">{i.type ?? "—"}</td>
                  <td><StatusBadge s={i.severity} /></td>
                  <td><StatusBadge s={i.status} /></td>
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
        )}
      </div>
    </div>
  );
}
