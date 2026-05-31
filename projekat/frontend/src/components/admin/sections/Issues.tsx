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
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [deleting, setDeleting] = useState(false);

  useSubViewBack(detail !== null, () => setDetail(null));

  async function fetchIssues(f?: string) {
    setLoading(true);
    try {
      const activeFilter = f ?? filter;
      const params: Record<string, string> = {};
      if (activeFilter !== "All") params.status_filter = activeFilter;
      const { data } = await apiClient.get<Issue[]>("/api/v1/chat/issues", { params });
      setIssues(data);
      setSelected(new Set());
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

  async function handleDelete(id: number) {
    setDeleting(true);
    try {
      await apiClient.delete(`/api/v1/chat/issues/${id}`);
      setIssues((prev) => prev.filter((i) => i.id !== id));
      setSelected((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    } catch {
      // ignore
    } finally {
      setDeleting(false);
    }
  }

  async function handleDeleteSelected() {
    const ids = [...selected];
    if (ids.length === 0) return;
    if (
      !window.confirm(
        `Delete ${ids.length} selected issue${ids.length > 1 ? "s" : ""}?\nThis action cannot be undone.`
      )
    )
      return;
    setDeleting(true);
    try {
      await apiClient.post("/api/v1/chat/issues/bulk-delete", { ids });
      setIssues((prev) => prev.filter((i) => !selected.has(i.id)));
      setSelected(new Set());
    } catch {
      // ignore
    } finally {
      setDeleting(false);
    }
  }

  if (detail) {
    return <IssueDetail issue={detail} onBack={() => setDetail(null)} onUpdate={fetchIssues} />;
  }

  const filtered = issues.filter((i) => {
    if (!search) return true;
    return i.title.toLowerCase().includes(search.toLowerCase());
  });

  function toggleOne(id: number) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  const allSelected = filtered.length > 0 && filtered.every((i) => selected.has(i.id));

  function toggleAll() {
    setSelected((prev) => {
      if (filtered.every((i) => prev.has(i.id))) {
        const next = new Set(prev);
        filtered.forEach((i) => next.delete(i.id));
        return next;
      }
      const next = new Set(prev);
      filtered.forEach((i) => next.add(i.id));
      return next;
    });
  }

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
          {selected.size > 0 && (
            <button
              className="px-3 py-1 rounded text-xs flex items-center gap-1.5"
              onClick={handleDeleteSelected}
              disabled={deleting}
              style={{
                border: "1px solid rgba(220,38,38,0.3)",
                background: "rgba(220,38,38,0.05)",
                color: "#dc2626",
                cursor: deleting ? "default" : "pointer",
              }}
            >
              <Ic d={icons.trash} size={13} />
              Delete selected ({selected.size})
            </button>
          )}
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
                <th>
                  <input
                    type="checkbox"
                    checked={allSelected}
                    onChange={toggleAll}
                    aria-label="Select all"
                  />
                </th>
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
                  <td colSpan={8} className="text-center text-gray-400 py-8 text-sm">
                    No issues found.
                  </td>
                </tr>
              )}
              {filtered.map((i) => (
                <tr key={i.id}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selected.has(i.id)}
                      onChange={() => toggleOne(i.id)}
                      aria-label={`Select issue ${i.id}`}
                    />
                  </td>
                  <td className="text-gray-400 font-mono text-xs">{i.id}</td>
                  <td className="font-medium text-charcoal max-w-xs truncate">{i.title}</td>
                  <td className="text-xs text-gray-400">{i.type ?? "—"}</td>
                  <td><StatusBadge s={i.severity} /></td>
                  <td><StatusBadge s={i.status} /></td>
                  <td className="text-gray-400">{i.date}</td>
                  <td>
                    <div className="flex items-center gap-2">
                      <button
                        className="outline-btn py-1 text-xs"
                        onClick={() => setDetail(i)}
                      >
                        View
                      </button>
                      <button
                        className="p-1.5 rounded"
                        onClick={() => handleDelete(i.id)}
                        disabled={deleting}
                        title="Delete issue"
                        style={{ color: "#ef4444", cursor: deleting ? "default" : "pointer" }}
                      >
                        <Ic d={icons.trash} size={13} />
                      </button>
                    </div>
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
