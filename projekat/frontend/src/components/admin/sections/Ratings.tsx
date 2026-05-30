import { useEffect, useState } from "react";
import { getRatingsStats, adminGetSessionMessages, type RatingsStats } from "../../../api/chat";
import { Stars } from "../shared";

interface SessionMessage {
  role: string;
  content: string;
  timestamp: string | null;
}

export default function Ratings() {
  const [sessionModal, setSessionModal] = useState<{ sesija_id: number; messages: SessionMessage[] } | null>(null);
  const [sessionLoading, setSessionLoading] = useState(false);
  const [data, setData] = useState<RatingsStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function openSessionModal(sesija_id: number) {
    setSessionLoading(true);
    setSessionModal({ sesija_id, messages: [] });
    try {
      const result = await adminGetSessionMessages(sesija_id);
      setSessionModal({ sesija_id, messages: result.messages });
    } catch {
      setSessionModal(null);
    } finally {
      setSessionLoading(false);
    }
  }

  useEffect(() => {
    getRatingsStats()
      .then(setData)
      .catch((err) => {
        const status = err?.response?.status;
        const detail = err?.response?.data?.detail || err?.message || "";
        console.error("Ratings fetch failed:", err);
        setError(`Error (HTTP ${status ?? "network"})${detail ? `: ${detail}` : ""}`);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-5">
        <h2 className="section-title">Ratings Overview</h2>
        <div className="card p-8 text-center text-sm text-gray-400">Loading…</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="space-y-5">
        <h2 className="section-title">Ratings Overview</h2>
        <div
          className="card p-5 text-sm"
          style={{ color: "#ef4444" }}
        >
          {error || "No data available."}
        </div>
      </div>
    );
  }

  const maxAvg = data.trend.length > 0 ? Math.max(...data.trend.map((t) => t.avg)) : 5;
  const minAvg = data.trend.length > 0 ? Math.min(...data.trend.map((t) => t.avg)) : 1;
  const range = maxAvg - minAvg || 1;

  return (
    <div className="space-y-5">
      <h2 className="section-title">Ratings Overview</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Average Score", val: `${data.average_score} ★`, color: "#C5A059" },
          { label: "5-Star Responses", val: `${data.five_star_pct}%`, color: "#2e7d32" },
          { label: "Below 3 Stars", val: `${data.below_three_pct}%`, color: "#c62828" },
          { label: "Total Rated", val: data.total_rated.toLocaleString(), color: "#1565c0" },
        ].map((m) => (
          <div key={m.label} className="stat-card text-center">
            <div
              className="text-2xl font-bold font-cinzel mt-1"
              style={{ color: m.color }}
            >
              {m.val}
            </div>
            <div className="text-xs text-gray-400 mt-1">{m.label}</div>
          </div>
        ))}
      </div>

      {/* Score trend */}
      <div className="card p-5">
        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
          Score Trend — Last 14 Days
        </div>
        {data.trend.length === 0 ? (
          <div className="text-sm text-gray-400 text-center py-6">No data for this period.</div>
        ) : (
          <div className="flex items-end gap-2 h-28">
            {data.trend.map((t, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full rounded-t"
                  style={{
                    height: `${((t.avg - minAvg) / range) * 80 + 20}%`,
                    background: "linear-gradient(180deg,#e0c070,#C5A059)",
                    minHeight: 8,
                  }}
                  title={`${t.date}: ${t.avg}`}
                />
                <span className="text-gray-300" style={{ fontSize: 10 }}>
                  {new Date(t.date).toLocaleDateString("bs-BA", { day: "numeric", month: "numeric" })}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Top rated */}
      <div className="card p-5">
        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
          Top Rated Responses
        </div>
        {data.top_rated.length === 0 ? (
          <div className="text-sm text-gray-400 text-center py-6">No rated responses.</div>
        ) : (
          <div className="space-y-3">
            {data.top_rated.map((l, i) => (
              <div
                key={i}
                className="rounded-lg p-4"
                style={{ background: "rgba(249,245,239,0.7)", border: "1px solid rgba(197,160,89,0.15)" }}
              >
                <div className="flex items-center justify-between mb-2">
                  <Stars n={l.rating} />
                  <div className="flex items-center gap-3">
                    {l.confidence !== null && (
                      <span
                        className="text-xs px-2 py-0.5 rounded-full"
                        style={{ background: "rgba(197,160,89,0.12)", color: "#8a6d1f" }}
                      >
                        {Math.round(l.confidence * 100)}% confidence
                      </span>
                    )}
                    <span className="text-xs text-gray-400">{l.date}</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mb-1 font-semibold uppercase tracking-wide">Question</p>
                <p className="text-sm text-charcoal mb-2 leading-snug">{l.question}</p>
                <p className="text-xs text-gray-500 mb-1 font-semibold uppercase tracking-wide">Response</p>
                <p className="text-sm text-gray-600 leading-snug line-clamp-3">{l.answer}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent comments */}
      <div className="card p-5">
        <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
          Recent User Comments
        </div>
        {data.recent_comments.length === 0 ? (
          <div className="text-sm text-gray-400 text-center py-6">No comments yet.</div>
        ) : (
          <div className="space-y-3">
            {data.recent_comments.map((c, i) => (
              <div
                key={i}
                className="rounded-lg px-4 py-3"
                style={{ background: "rgba(249,245,239,0.7)", border: "1px solid rgba(197,160,89,0.15)" }}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    {c.rating !== null && <Stars n={c.rating} />}
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-gray-400">{c.date ?? ""}</span>
                    {c.sesija_id && (
                      <button
                        onClick={() => openSessionModal(c.sesija_id!)}
                        className="text-xs transition-colors"
                        style={{ color: "#C5A059", background: "none", border: "none", cursor: "pointer", padding: 0, textDecoration: "underline" }}
                      >
                        View Chat
                      </button>
                    )}
                  </div>
                </div>
                <p className="text-sm text-charcoal leading-snug">"{c.comment}"</p>
                {c.question && (
                  <p className="text-xs text-gray-400 mt-1.5 truncate">
                    re: {c.question}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Session conversation modal */}
      {sessionModal && (
        <div
          style={{
            position: "fixed", inset: 0, zIndex: 9999,
            background: "rgba(0,0,0,0.45)",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}
          onClick={() => setSessionModal(null)}
        >
          <div
            style={{
              background: "#fff", borderRadius: 12, width: "min(640px, 90vw)",
              maxHeight: "80vh", display: "flex", flexDirection: "column",
              boxShadow: "0 8px 40px rgba(0,0,0,0.18)",
              border: "1px solid rgba(197,160,89,0.2)",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div
              style={{ padding: "16px 20px", borderBottom: "1px solid rgba(197,160,89,0.15)", display: "flex", alignItems: "center", justifyContent: "space-between" }}
            >
              <span className="text-xs font-semibold tracking-widest text-gold uppercase">
                Session #{sessionModal.sesija_id}
              </span>
              <button
                onClick={() => setSessionModal(null)}
                style={{ color: "#9ca3af", background: "none", border: "none", cursor: "pointer", fontSize: 18, lineHeight: 1 }}
              >
                ×
              </button>
            </div>
            <div style={{ overflowY: "auto", padding: "16px 20px", flex: 1 }}>
              {sessionLoading ? (
                <div className="text-sm text-gray-400 text-center py-8">Loading…</div>
              ) : sessionModal.messages.length === 0 ? (
                <div className="text-sm text-gray-400 text-center py-8">No messages found.</div>
              ) : (
                <div className="space-y-2">
                  {sessionModal.messages.map((m, i) => (
                    <div
                      key={i}
                      className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                      <div
                        className="px-3 py-2 rounded-xl max-w-[80%] text-xs leading-relaxed"
                        style={{
                          background: m.role === "user" ? "rgba(197,160,89,0.15)" : "rgba(249,245,239,0.9)",
                          border: "1px solid rgba(197,160,89,0.2)",
                          color: "#1C1C2E",
                        }}
                      >
                        <span
                          className="font-semibold block mb-0.5"
                          style={{ color: m.role === "user" ? "#C5A059" : "#6b7280" }}
                        >
                          {m.role === "user" ? "User" : "Ambassador"}
                        </span>
                        {m.content}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
