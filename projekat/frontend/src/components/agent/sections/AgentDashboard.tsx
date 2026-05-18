import { useEffect, useState } from "react";
import { escalationApi, EscalationItem } from "../../../api/escalation";
import { useAuth } from "../../../hooks/useAuth";
import { AgentStats } from "../../../types";
import { StatusBadge } from "../../admin/shared";
import { timeAgo, PRIORITY_LABELS } from "../../escalation/EscalationCard";

function fmtSeconds(s: number | null): string {
  if (s === null) return "—";
  const m = Math.floor(s / 60);
  const sec = Math.round(s % 60);
  return m > 0 ? `${m}m ${sec}s` : `${sec}s`;
}

interface StatCardProps {
  label: string;
  value: string | number;
  sub?: string;
}

function StatCard({ label, value, sub }: StatCardProps) {
  return (
    <div className="stat-card">
      <div className="font-cinzel font-bold text-2xl text-charcoal mb-1">{value}</div>
      <div className="text-xs font-semibold tracking-widest text-gold uppercase">{label}</div>
      {sub && <div className="text-xs text-gray-400 mt-0.5">{sub}</div>}
    </div>
  );
}

interface Props {
  onGoToQueue: () => void;
  queue: EscalationItem[];
}

export default function AgentDashboard({ onGoToQueue, queue }: Props) {
  const { user } = useAuth();
  const [stats, setStats] = useState<AgentStats | null>(null);
  const [history, setHistory] = useState<EscalationItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [sRes, hRes] = await Promise.all([
          escalationApi.myStats(),
          escalationApi.myHistory(5, 0),
        ]);
        if (!cancelled) {
          setStats(sRes.data);
          setHistory(hRes.data);
        }
      } catch {
        /* ignore */
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, []);

  const pendingCount = queue.filter((e) => e.status === "Cekanje").length;
  // Only show the active-chat panel for escalations assigned to this agent
  const activeChat = queue.find(
    (e) => e.status === "UToku" && e.dodjeljeni_agent_id === user?.id
  );

  if (loading) {
    return <div className="text-center py-12 text-sm text-gray-400">Loading…</div>;
  }

  return (
    <div className="space-y-5">
      <h2 className="section-title">Dashboard</h2>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard
          label="Handled Today"
          value={stats?.handled_today ?? 0}
          sub="resolved escalations"
        />
        <StatCard
          label="This Week"
          value={stats?.handled_week ?? 0}
          sub="last 7 days"
        />
        <StatCard
          label="Avg Response"
          value={fmtSeconds(stats?.avg_response_seconds ?? null)}
          sub="last 30 days"
        />
        <StatCard
          label="Queue Now"
          value={pendingCount}
          sub="waiting for an agent"
        />
      </div>

      <div className="meander" />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Currently handling */}
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
            Currently Handling
          </div>
          {activeChat ? (
            <div className="space-y-2">
              <p className="text-sm text-charcoal">
                You have an active escalation{" "}
                <span className="font-mono font-semibold">#{activeChat.id}</span>.
              </p>
              <p className="text-xs text-gray-400">
                {activeChat.tema ?? "No topic"} · Started {timeAgo(activeChat.datum_kreiranja)}
              </p>
              <button className="gold-btn text-xs mt-2" onClick={onGoToQueue}>
                Go to Live Queue →
              </button>
            </div>
          ) : (
            <div className="text-center py-6">
              <p className="text-sm text-gray-400 mb-3">No active chat right now.</p>
              <button className="outline-btn text-xs" onClick={onGoToQueue}>
                View Queue
              </button>
            </div>
          )}
        </div>

        {/* Recent activity */}
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-4">
            Recent Activity
          </div>
          {history.length === 0 ? (
            <p className="text-sm text-gray-400">No resolved escalations yet.</p>
          ) : (
            <ul className="space-y-2">
              {history.map((e) => (
                <li
                  key={e.id}
                  className="flex items-center justify-between text-sm py-1.5"
                  style={{ borderBottom: "1px solid rgba(197,160,89,0.1)" }}
                >
                  <div>
                    <span className="font-mono text-gray-400 text-xs mr-2">#{e.id}</span>
                    <span className="text-charcoal">{e.tema ?? "—"}</span>
                    <span className="ml-2 text-xs text-gray-400">
                      {PRIORITY_LABELS[e.prioritet] ?? e.prioritet}
                    </span>
                  </div>
                  <StatusBadge s={e.status} />
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
