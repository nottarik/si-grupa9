import React, { useEffect, useRef, useState } from "react";
import { useSubViewBack } from "../../../hooks/useSubViewBack";
import { Ic, icons } from "../shared";
import apiClient from "../../../api/client";
import { adminGetSessionMessages, bulkDeleteChatLogs } from "../../../api/chat";

interface LogEntry {
  id: number;
  session_id: number | null;
  question: string;
  answer: string;
  time: string | null;
  date: string | null;
  confidence: number;
  method: string;
  rating: number | null;
}

interface SessionMessage {
  role: string;
  content: string;
  timestamp: string | null;
}

function Stars({ n }: { n: number | null }) {
  if (n === null) return <span className="text-xs text-gray-300">—</span>;
  const full = Math.round(n);
  return (
    <span className="text-xs" style={{ color: "#C5A059" }}>
      {"★".repeat(full)}{"☆".repeat(5 - full)}
    </span>
  );
}

interface Props {
  initialSearch?: string;
  initialDate?: string;
}

export default function ChatLogs({ initialSearch = "", initialDate = "" }: Props) {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState<number | null>(null);
  const [convo, setConvo] = useState<SessionMessage[] | null>(null);
  const [convoLoading, setConvoLoading] = useState(false);
  const [search, setSearch] = useState(initialSearch);
  const [date, setDate] = useState(initialDate);
  const [minRating, setMinRating] = useState("");
  const [checked, setChecked] = useState<Set<number>>(new Set());
  const [bulkDeleting, setBulkDeleting] = useState(false);
  const [error, setError] = useState("");

  useSubViewBack(open !== null, () => { setOpen(null); setConvo(null); });

  async function toggleDetails(l: LogEntry) {
    if (open === l.id) {
      setOpen(null);
      setConvo(null);
      return;
    }
    setOpen(l.id);
    setConvo(null);
    if (l.session_id == null) return;
    setConvoLoading(true);
    try {
      const res = await adminGetSessionMessages(l.session_id);
      setConvo(res.messages);
    } catch {
      setConvo(null);
    } finally {
      setConvoLoading(false);
    }
  }

  const searchRef = useRef(search);
  const dateRef = useRef(date);
  const minRatingRef = useRef(minRating);
  searchRef.current = search;
  dateRef.current = date;
  minRatingRef.current = minRating;

  async function fetchLogs() {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (searchRef.current) params.search = searchRef.current;
      if (dateRef.current) params.date = dateRef.current;
      if (minRatingRef.current) params.min_rating = minRatingRef.current;
      const { data } = await apiClient.get<LogEntry[]>("/api/v1/chat/logs", { params });
      setLogs(data);
      setChecked(new Set());
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchLogs();
  }, []);

  // Deletion unit is the conversation (session); entries without a session_id can't be selected.
  const selectable = logs.filter((l) => l.session_id != null);
  const allSelected = selectable.length > 0 && selectable.every((l) => checked.has(l.id));

  function toggleOne(id: number) {
    setChecked((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function toggleAll() {
    setChecked((prev) => {
      if (selectable.every((l) => prev.has(l.id))) {
        const next = new Set(prev);
        selectable.forEach((l) => next.delete(l.id));
        return next;
      }
      const next = new Set(prev);
      selectable.forEach((l) => next.add(l.id));
      return next;
    });
  }

  async function handleDeleteSelected() {
    const sessionIds = logs
      .filter((l) => checked.has(l.id) && l.session_id != null)
      .map((l) => l.session_id as number);
    if (sessionIds.length === 0) return;
    setBulkDeleting(true);
    try {
      await bulkDeleteChatLogs(sessionIds);
      setLogs((prev) => prev.filter((l) => !checked.has(l.id)));
      setChecked(new Set());
    } catch {
      setError("Error deleting selected chat logs.");
    } finally {
      setBulkDeleting(false);
    }
  }

  return (
    <div className="space-y-5">
      <h2 className="section-title">Chat Logs</h2>

      {error && (
        <div
          className="text-sm px-4 py-3 rounded-lg flex items-center justify-between"
          style={{
            background: "rgba(239,68,68,0.08)",
            color: "#ef4444",
            border: "1px solid rgba(239,68,68,0.2)",
          }}
        >
          <span>{error}</span>
          <button className="text-xs underline ml-3" onClick={() => setError("")}>
            Close
          </button>
        </div>
      )}

      <div className="card overflow-hidden">
        <div
          className="p-4 flex gap-3 flex-wrap"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          <div className="relative flex-1 min-w-40">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <Ic d={icons.search} />
            </span>
            <input
              className="input-field"
              style={{ paddingLeft: "2.25rem" }}
              placeholder="Search questions or answers…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") fetchLogs(); }}
            />
          </div>
          <input
            className="input-field"
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            style={{ width: "auto" }}
          />
          <select
            className="input-field"
            style={{ width: "auto" }}
            value={minRating}
            onChange={(e) => setMinRating(e.target.value)}
          >
            <option value="">All Ratings</option>
            <option value="5">5 ★</option>
            <option value="4">4+ ★</option>
            <option value="3">3+ ★</option>
          </select>
          <button className="gold-btn text-xs" onClick={fetchLogs}>
            Filter
          </button>
          {checked.size > 0 && (
            <button
              className="px-3 py-1 rounded text-xs flex items-center gap-1.5"
              onClick={handleDeleteSelected}
              disabled={bulkDeleting}
              style={{
                border: "1px solid rgba(220,38,38,0.3)",
                background: "rgba(220,38,38,0.05)",
                color: "#dc2626",
                cursor: bulkDeleting ? "default" : "pointer",
              }}
            >
              <Ic d={icons.trash} size={13} />
              {bulkDeleting ? "Deleting…" : `Delete selected (${checked.size})`}
            </button>
          )}
        </div>

        {loading ? (
          <div className="text-center py-8 text-sm text-gray-400">Loading…</div>
        ) : logs.length === 0 ? (
          <div className="text-center py-8 text-sm text-gray-400">No chat logs found.</div>
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
                <th>Question</th>
                <th>Time</th>
                <th>Date</th>
                <th>Method</th>
                <th>Rating</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {logs.map((l) => (
                <React.Fragment key={l.id}>
                  <tr>
                    <td>
                      <input
                        type="checkbox"
                        checked={checked.has(l.id)}
                        disabled={l.session_id == null}
                        onChange={() => toggleOne(l.id)}
                        aria-label={`Select conversation ${l.question}`}
                      />
                    </td>
                    <td className="font-medium text-charcoal max-w-xs truncate">
                      {l.question}
                    </td>
                    <td className="text-gray-400">{l.time ?? "—"}</td>
                    <td className="text-gray-400">{l.date ?? "—"}</td>
                    <td>
                      <span
                        className="text-xs px-2 py-0.5 rounded-full"
                        style={{
                          background: l.method === "Retrieval" ? "rgba(197,160,89,0.12)" : "rgba(107,90,58,0.08)",
                          color: l.method === "Retrieval" ? "#8a6d1f" : "#6b5a3a",
                        }}
                      >
                        {l.method}
                      </span>
                    </td>
                    <td><Stars n={l.rating} /></td>
                    <td>
                      <button
                        className="outline-btn py-1 text-xs"
                        onClick={() => toggleDetails(l)}
                      >
                        {open === l.id ? "Close" : "Details"}
                      </button>
                    </td>
                  </tr>
                  {open === l.id && (
                    <tr>
                      <td
                        colSpan={7}
                        style={{ background: "rgba(249,243,232,0.4)" }}
                        className="px-5 py-4"
                      >
                        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
                          Full Conversation
                        </div>
                        <div className="space-y-2">
                          {convoLoading ? (
                            <div className="text-sm text-gray-400 py-2">Loading…</div>
                          ) : convo && convo.length > 0 ? (
                            convo.map((m, i) => (
                              <div
                                key={i}
                                className="rounded-lg p-3 text-sm"
                                style={
                                  m.role === "user"
                                    ? { background: "#fff", border: "1px solid rgba(197,160,89,0.2)" }
                                    : { background: "#fff", borderLeft: "2px solid #C5A059" }
                                }
                              >
                                <strong>
                                  {m.role === "user" ? "User" : m.role === "agent" ? "Agent" : "Ambassador"}:
                                </strong>{" "}
                                {m.content}
                              </div>
                            ))
                          ) : (
                            <>
                              <div
                                className="rounded-lg p-3 text-sm border"
                                style={{ background: "#fff", borderColor: "rgba(197,160,89,0.2)" }}
                              >
                                <strong>User:</strong> {l.question}
                              </div>
                              <div
                                className="rounded-lg p-3 text-sm border-l-2"
                                style={{ background: "#fff", borderLeftColor: "#C5A059" }}
                              >
                                <strong>Ambassador:</strong> {l.answer}
                              </div>
                            </>
                          )}
                          <div className="flex gap-4 text-xs text-gray-400 mt-2">
                            <span>Confidence: {(l.confidence * 100).toFixed(0)}%</span>
                            <span>Method: {l.method}</span>
                            {l.rating && <span>Rating: {l.rating} ★</span>}
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
