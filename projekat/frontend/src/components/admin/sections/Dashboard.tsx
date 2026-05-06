import { useEffect, useMemo, useState } from "react";
import { getRatingsStats, type RatingsStats } from "../../../api/chat";
import { listTranscripts } from "../../../api/transcripts";
import { listUsers } from "../../../api/users";
import type { Transcript } from "../../../types";

function relativeTime(dateStr: string): string {
  const ms = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(ms / 60_000);
  const hours = Math.floor(ms / 3_600_000);
  const days = Math.floor(ms / 86_400_000);
  if (mins < 1) return "Just now";
  if (mins < 60) return `${mins}min`;
  if (hours < 24) return `${hours}h`;
  if (days === 1) return "Yesterday";
  return `${days}d`;
}

export default function Dashboard() {
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [userCount, setUserCount] = useState<number | null>(null);
  const [ratings, setRatings] = useState<RatingsStats | null>(null);

  useEffect(() => {
    listTranscripts()
      .then(setTranscripts)
      .catch(() => {});

    listUsers()
      .then((u) => setUserCount(u.length))
      .catch(() => {});

    getRatingsStats()
      .then(setRatings)
      .catch(() => {});
  }, []);

  const transcriptTotal = transcripts.length;
  const transcriptProcessed = transcripts.filter((t) => t.status === "Obradjeno").length;
  const fmt = (n: number | null) => (n === null ? "…" : String(n));

  const stats = [
    {
      label: "Avg. Rating",
      val: ratings ? `${ratings.average_score} ★` : "…",
      sub: `${ratings?.total_rated ?? "…"} ratings`,
      icon: "★",
    },
    {
      label: "Transcripts",
      val: fmt(transcriptTotal),
      sub: `${fmt(transcriptProcessed)} processed`,
      icon: "📄",
    },
    {
      label: "Users",
      val: fmt(userCount),
      sub: "Registered",
      icon: "👤",
    },
    {
      label: "Open Issues",
      val: "6",
      sub: "Requires attention",
      icon: "⚠",
    },
  ];

  const ratingPcts = ratings?.distribution ?? { "5": 0, "4": 0, "3": 0, "2": 0, "1": 0 };

  const activityItems = useMemo(() => {
    const sorted = [...transcripts]
      .filter((t) => t.datum_uploada)
      .sort(
        (a, b) =>
          new Date(b.datum_uploada!).getTime() - new Date(a.datum_uploada!).getTime()
      )
      .slice(0, 5);

    if (sorted.length === 0) return [];

    return sorted.map((t) => ({
      txt:
        t.status === "Obradjeno"
          ? `Transcript "${t.naziv || "Untitled"}" processed`
          : `Transcript "${t.naziv || "Untitled"}" uploaded`,
      time: relativeTime(t.datum_uploada!),
    }));
  }, [transcripts]);

  return (
    <div className="space-y-6">
      <h2 className="section-title">Dashboard</h2>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="stat-card">
            <div className="text-2xl mb-1">{s.icon}</div>
            <div className="text-2xl font-bold text-charcoal font-cinzel">{s.val}</div>
            <div className="text-xs font-semibold text-gold mt-1">{s.label}</div>
            <div className="text-xs text-gray-400 mt-0.5">{s.sub}</div>
          </div>
        ))}
      </div>

      <div className="meander" />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Rating distribution */}
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
            Rating Distribution
          </div>
          {ratings === null ? (
            <div className="text-sm text-gray-400 text-center py-4">Loading…</div>
          ) : ratings.total_rated === 0 ? (
            <div className="text-sm text-gray-400 text-center py-4">No ratings yet.</div>
          ) : (
            [5, 4, 3, 2, 1].map((n) => {
              const pct = ratingPcts[String(n)] ?? 0;
              return (
                <div key={n} className="flex items-center gap-3 mb-2">
                  <span className="text-xs w-4 text-gray-500">{n}★</span>
                  <div className="flex-1 bg-gray-100 rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${pct}%`,
                        background: "linear-gradient(90deg,#e0c070,#C5A059)",
                      }}
                    />
                  </div>
                  <span className="text-xs text-gray-400 w-8">{pct}%</span>
                </div>
              );
            })
          )}
        </div>

        {/* Recent activity */}
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
            Recent Activity
          </div>
          {transcripts.length === 0 ? (
            <div className="text-sm text-gray-400 text-center py-4">No recent activity.</div>
          ) : (
            activityItems.map((a, i) => (
              <div
                key={i}
                className="flex justify-between items-center py-2 border-b last:border-0"
                style={{ borderColor: "rgba(197,160,89,0.1)" }}
              >
                <span className="text-sm text-charcoal truncate mr-3">{a.txt}</span>
                <span className="text-xs text-gray-400 flex-shrink-0">{a.time}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
