import { useEffect, useState } from "react";
import { getRatingsStats, type RatingsStats } from "../../../api/chat";
import { Stars } from "../shared";

export default function Ratings() {
  const [data, setData] = useState<RatingsStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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
          <table className="tbl">
            <thead>
              <tr>
                <th>Question</th>
                <th>Rating</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {data.top_rated.map((l, i) => (
                <tr key={i}>
                  <td className="text-charcoal">{l.question}</td>
                  <td>
                    <Stars n={l.rating} />
                  </td>
                  <td className="text-gray-400">{l.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
