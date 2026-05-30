import React, { useEffect, useRef, useState } from "react";
import { useSubViewBack } from "../../../hooks/useSubViewBack";
import { Ic, icons } from "../shared";
import apiClient from "../../../api/client";

interface LogEntry {
  id: number;
  question: string;
  answer: string;
  time: string | null;
  date: string | null;
  confidence: number;
  method: string;
  rating: number | null;
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
  const [search, setSearch] = useState(initialSearch);
  const [date, setDate] = useState(initialDate);
  const [minRating, setMinRating] = useState("");

  useSubViewBack(open !== null, () => setOpen(null));

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
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div className="space-y-5">
      <h2 className="section-title">Chat Logs</h2>
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
        </div>

        {loading ? (
          <div className="text-center py-8 text-sm text-gray-400">Loading…</div>
        ) : logs.length === 0 ? (
          <div className="text-center py-8 text-sm text-gray-400">No chat logs found.</div>
        ) : (
          <table className="tbl">
            <thead>
              <tr>
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
                        onClick={() => setOpen(open === l.id ? null : l.id)}
                      >
                        {open === l.id ? "Close" : "Details"}
                      </button>
                    </td>
                  </tr>
                  {open === l.id && (
                    <tr>
                      <td
                        colSpan={6}
                        style={{ background: "rgba(249,243,232,0.4)" }}
                        className="px-5 py-4"
                      >
                        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
                          Full Exchange
                        </div>
                        <div className="space-y-2">
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
