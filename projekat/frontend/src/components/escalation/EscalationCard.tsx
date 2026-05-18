import { useState } from "react";
import { escalationApi, EscalationItem } from "../../api/escalation";
import { StatusBadge } from "../admin/shared";

export const TRIGGER_LABELS: Record<string, string> = {
  NiskaPouz: "Low Confidence",
  EksplicitanZahtjev: "User Requested",
  PonovljeniNeuspjeh: "Repeated Failure",
  OsjetljivaTema: "Sensitive Topic",
};

export const PRIORITY_LABELS: Record<string, string> = {
  Nizak: "Low",
  Normalan: "Normal",
  Visok: "High",
  Hitan: "Urgent",
};

export const PRIORITY_COLOR: Record<string, string> = {
  Hitan: "#ef4444",
  Visok: "#f59e0b",
  Normalan: "#6b7280",
  Nizak: "#9ca3af",
};

export function timeAgo(iso: string): string {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  return `${Math.floor(diff / 3600)}h ago`;
}

interface Props {
  item: EscalationItem;
  currentAgentId: string;
  onAccepted: (item: EscalationItem) => void;
}

export default function EscalationCard({ item, currentAgentId, onAccepted }: Props) {
  const [expanded, setExpanded] = useState(false);
  const [accepting, setAccepting] = useState(false);

  const isAssignedToOther =
    item.status === "UToku" &&
    item.dodjeljeni_agent_id != null &&
    item.dodjeljeni_agent_id !== currentAgentId;

  const isAssignedToMe =
    item.status === "UToku" && item.dodjeljeni_agent_id === currentAgentId;

  async function handleAccept() {
    setAccepting(true);
    try {
      await escalationApi.accept(item.id);
      onAccepted(item);
    } catch {
      setAccepting(false);
    }
  }

  const lastUserMsg =
    [...(item.razgovor ?? [])].reverse().find((m) => m.role === "user")?.content ?? "—";
  const color = PRIORITY_COLOR[item.prioritet] ?? "#9ca3af";

  return (
    <div
      className="card p-4 space-y-3 cursor-pointer"
      onClick={() => setExpanded((v) => !v)}
      style={{ borderLeft: `3px solid ${color}` }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs font-mono text-gray-400">#{item.id}</span>
            <span
              className="text-xs font-semibold px-2 py-0.5 rounded-full"
              style={{ background: `${color}20`, color }}
            >
              {PRIORITY_LABELS[item.prioritet] ?? item.prioritet}
            </span>
            <span className="badge badge-yellow">
              {TRIGGER_LABELS[item.trigger_tip ?? ""] ?? item.trigger_tip}
            </span>
            <StatusBadge s={item.status === "Cekanje" ? "Pending" : "In Progress"} />
            {isAssignedToOther && (
              <span
                className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full"
                style={{
                  background: "rgba(107,90,58,0.08)",
                  color: "#6b5a3a",
                  border: "1px solid rgba(107,90,58,0.2)",
                }}
              >
                <svg
                  width={10}
                  height={10}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
                {item.agent_name || "Agent"}
              </span>
            )}
            {isAssignedToMe && (
              <span
                className="text-xs px-2 py-0.5 rounded-full"
                style={{
                  background: "rgba(197,160,89,0.15)",
                  color: "#8a6d1f",
                  border: "1px solid rgba(197,160,89,0.3)",
                }}
              >
                You
              </span>
            )}
          </div>
          <p
            className="text-sm text-charcoal mt-1.5 leading-snug"
            style={{
              overflow: "hidden",
              display: "-webkit-box",
              WebkitLineClamp: expanded ? undefined : 2,
              WebkitBoxOrient: "vertical",
            }}
          >
            {lastUserMsg}
          </p>
        </div>

        <div className="flex-shrink-0 text-right space-y-2">
          <div className="text-xs text-gray-400">{timeAgo(item.datum_kreiranja)}</div>
          {item.status === "Cekanje" && (
            <button
              className="gold-btn text-xs"
              style={{ padding: "5px 14px" }}
              onClick={(e) => {
                e.stopPropagation();
                handleAccept();
              }}
              disabled={accepting}
            >
              {accepting ? "…" : "Accept"}
            </button>
          )}
        </div>
      </div>

      {expanded && item.razgovor && item.razgovor.length > 0 && (
        <div
          className="mt-2 space-y-1.5 pt-3"
          style={{ borderTop: "1px solid rgba(197,160,89,0.15)" }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-2">
            Conversation History
          </div>
          {item.razgovor.slice(-6).map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className="px-3 py-1.5 rounded-lg text-xs max-w-[80%]"
                style={{
                  background:
                    m.role === "user" ? "rgba(197,160,89,0.12)" : "rgba(255,255,255,0.8)",
                  border: "1px solid rgba(197,160,89,0.2)",
                  color: "#1C1C2E",
                }}
              >
                <span
                  className="font-semibold"
                  style={{ color: m.role === "user" ? "#C5A059" : m.role === "agent" ? "#8a6d1f" : "#6b7280" }}
                >
                  {m.role === "user" ? "User" : m.role === "agent" ? "Agent" : "Bot"}:{" "}
                </span>
                {m.content}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
