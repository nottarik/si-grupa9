import { useEffect, useState } from "react";
import { listSessions, getSessionMessages, type SessionSummary } from "../../api/chat";
import type { ChatMessage } from "../../types";

interface Props {
  isOpen: boolean;
  onToggle: () => void;
  onLoadSession: (messages: ChatMessage[], sessionId: number, isClosed: boolean) => void;
  currentSessionId: number | null;
}

function timeLabel(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffDays = Math.floor(diffMs / 86_400_000);
  if (diffDays === 0) return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 7) return d.toLocaleDateString([], { weekday: "short" });
  return d.toLocaleDateString([], { month: "short", day: "numeric" });
}

export default function ChatHistory({ isOpen, onToggle, onLoadSession, currentSessionId }: Props) {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingId, setLoadingId] = useState<number | null>(null);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      listSessions()
        .then(setSessions)
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  async function handleClick(session: SessionSummary) {
    if (session.id === currentSessionId) return;
    setLoadingId(session.id);
    try {
      const data = await getSessionMessages(session.id);
      const msgs: ChatMessage[] = data.messages.map((m) => ({
        role: m.role as "user" | "assistant",
        content: m.content,
      }));
      onLoadSession(msgs, session.id, session.status === "Zatvorena");
    } catch {
      // ignore
    } finally {
      setLoadingId(null);
    }
  }

  return (
    <>
      {/* Toggle button */}
      <button
        onClick={onToggle}
        className="fixed top-4 left-4 z-50 rounded-full flex items-center justify-center transition-all"
        style={{
          width: 36,
          height: 36,
          background: "rgba(255,255,255,0.85)",
          backdropFilter: "blur(8px)",
          border: "1px solid rgba(197,160,89,0.3)",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
          cursor: "pointer",
        }}
        title={isOpen ? "Close history" : "Chat history"}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#C5A059" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          {isOpen ? (
            <>
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </>
          ) : (
            <>
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </>
          )}
        </svg>
      </button>

      {/* Sidebar */}
      <aside
        className="fixed top-0 left-0 h-full z-40 flex flex-col transition-transform duration-200"
        style={{
          width: 280,
          transform: isOpen ? "translateX(0)" : "translateX(-100%)",
          background: "rgba(255,255,255,0.92)",
          backdropFilter: "blur(16px)",
          borderRight: "1px solid rgba(197,160,89,0.2)",
          boxShadow: isOpen ? "4px 0 20px rgba(0,0,0,0.06)" : "none",
        }}
      >
        {/* Header */}
        <div
          className="px-5 py-4 flex items-center gap-3 flex-shrink-0"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#C5A059" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          <span className="font-cinzel text-xs tracking-widest text-charcoal uppercase">
            Chat History
          </span>
        </div>

        {/* Session list */}
        <div className="flex-1 overflow-y-auto py-2">
          {loading && (
            <div className="text-center text-xs text-gray-400 py-8">Loading…</div>
          )}
          {!loading && sessions.length === 0 && (
            <div className="text-center text-xs text-gray-400 py-8">No previous chats</div>
          )}
          {sessions.map((s) => (
            <button
              key={s.id}
              onClick={() => handleClick(s)}
              disabled={loadingId === s.id}
              className="w-full text-left px-4 py-3 transition-colors"
              style={{
                background: s.id === currentSessionId ? "rgba(197,160,89,0.1)" : "transparent",
                borderBottom: "1px solid rgba(197,160,89,0.08)",
                cursor: s.id === currentSessionId ? "default" : "pointer",
                opacity: loadingId === s.id ? 0.5 : 1,
              }}
              onMouseEnter={(e) => {
                if (s.id !== currentSessionId) (e.currentTarget.style.background = "rgba(197,160,89,0.06)");
              }}
              onMouseLeave={(e) => {
                if (s.id !== currentSessionId) (e.currentTarget.style.background = "transparent");
              }}
            >
              <div className="flex items-center justify-between mb-0.5">
                <span className="text-[11px] text-gray-400">{timeLabel(s.started_at)}</span>
                <div className="flex items-center gap-1.5">
                  {s.status === "Zatvorena" && (
                    <span
                      className="text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded-full"
                      style={{ background: "rgba(197,160,89,0.12)", color: "#9a8a6a", border: "1px solid rgba(197,160,89,0.2)" }}
                    >
                      Closed
                    </span>
                  )}
                  <span className="text-[10px] text-gray-300">{s.message_count} msg</span>
                </div>
              </div>
              <p
                className="text-sm text-charcoal leading-snug"
                style={{
                  overflow: "hidden",
                  display: "-webkit-box",
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: "vertical",
                }}
              >
                {s.preview || "Empty conversation"}
              </p>
            </button>
          ))}
        </div>

        {/* Footer */}
        <div
          className="px-5 py-3 flex-shrink-0 text-center"
          style={{ borderTop: "1px solid rgba(197,160,89,0.15)" }}
        >
          <button
            onClick={onToggle}
            className="text-xs transition-colors"
            style={{ color: "rgba(197,160,89,0.7)", background: "none", border: "none", cursor: "pointer" }}
          >
            Close
          </button>
        </div>
      </aside>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-30"
          style={{ background: "rgba(0,0,0,0.1)" }}
          onClick={onToggle}
        />
      )}
    </>
  );
}
