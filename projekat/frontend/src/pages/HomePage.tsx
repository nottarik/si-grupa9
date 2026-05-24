import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import UserMenu from "../components/chat/UserMenu";
import { listSessions, getSessionMessages, type SessionSummary } from "../api/chat";
import type { ChatMessage } from "../types";

/* ── Laurel (reused from ChatWindow visual identity) ── */
const Laurel = ({ flip = false, size = 44 }: { flip?: boolean; size?: number }) => (
  <svg
    width={size}
    height={Math.round(size * 0.55)}
    viewBox="0 0 90 50"
    fill="none"
    style={{ color: "#C5A059", transform: flip ? "scaleX(-1)" : "none", display: "block" }}
  >
    <path d="M44 42 Q38 36 30 30 Q20 22 12 18" stroke="currentColor" strokeWidth="1.2" fill="none" opacity="0.5" />
    {[
      "M12 18 Q8 12 14 8 Q20 6 21 14 Q17 15 12 18",
      "M22 14 Q20 7 27 5 Q34 3 34 12 Q29 13 22 14",
      "M34 11 Q34 4 41 3 Q48 2 47 11 Q42 12 34 11",
      "M10 18 Q4 16 3 22 Q2 28 9 27 Q10 22 10 18",
      "M20 26 Q14 25 13 31 Q12 37 19 35 Q20 31 20 26",
      "M30 31 Q25 31 24 37 Q23 43 30 41 Q31 36 30 31",
    ].map((d, i) => (
      <path key={i} d={d} fill="currentColor" opacity={0.65 + i * 0.04} />
    ))}
  </svg>
);

function timeLabel(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - d.getTime()) / 86_400_000);
  if (diffDays === 0) return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 7) return d.toLocaleDateString([], { weekday: "short" });
  return d.toLocaleDateString([], { month: "short", day: "numeric" });
}

export default function HomePage() {
  const { user, logout, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [helpOpen, setHelpOpen] = useState(false);
  const [loadingSession, setLoadingSession] = useState<number | null>(null);
  const didLoad = useRef(false);

  const firstName = user?.full_name?.split(" ")[0] ?? user?.email ?? "there";

  useEffect(() => {
    if (didLoad.current) return;
    didLoad.current = true;
    listSessions()
      .then(setSessions)
      .catch(() => {})
      .finally(() => setLoadingHistory(false));
  }, []);

  const activeSession = sessions.find((s) => s.status === "Aktivna");

  async function openSession(session: SessionSummary) {
    setLoadingSession(session.id);
    try {
      const data = await getSessionMessages(session.id);
      const messages: ChatMessage[] = data.messages.map((m) => ({
        role: m.role as "user" | "assistant",
        content: m.content,
      }));
      navigate("/chat", { state: { sessionId: session.id, messages } });
    } catch {
      /* on error, just open chat normally */
      navigate("/chat", { state: { sessionId: session.id } });
    }
  }

  function startFresh() {
    navigate("/chat", { state: { fresh: true } });
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="chat-bg flex flex-col" style={{ minHeight: "100vh" }}>
      {/* ── Header ── */}
      <header className="glass-header flex-shrink-0 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 flex-1 justify-center">
            <Laurel size={44} />
            <div className="text-center">
              <h1
                className="font-cinzel font-bold tracking-[0.2em] text-charcoal"
                style={{ fontSize: 18 }}
              >
                AMBASSADOR
              </h1>
              <p
                className="font-sans text-[11px] tracking-[0.22em] uppercase mt-0.5"
                style={{ color: "#C5A059", opacity: 0.85 }}
              >
                CALL CENTER  CHATBOT
              </p>
            </div>
            <Laurel size={44} flip />
          </div>

          {/* Right: avatar + logout */}
          <div className="flex-shrink-0 flex items-center gap-3 ml-4">
            {user?.role === "admin" && (
              <>
                <a
                  href="/admin"
                  className="text-xs transition-colors"
                  style={{ color: "rgba(197,160,89,0.7)", textDecoration: "none" }}
                >
                  Admin
                </a>
                <a
                  href="/agent"
                  className="text-xs transition-colors"
                  style={{ color: "rgba(197,160,89,0.7)", textDecoration: "none" }}
                >
                  Agent
                </a>
              </>
            )}
            {user && (
              <UserMenu
                user={user}
                onLogout={handleLogout}
                onRefreshUser={refreshUser}
                onHistoryDeleted={() => setSessions([])}
              />
            )}
          </div>
        </div>
      </header>

      {/* ── Main content ── */}
      <main className="flex-1 overflow-y-auto px-6 sm:px-12 md:px-20 lg:px-32 xl:px-48 py-10">
        <div className="max-w-2xl mx-auto space-y-7">

          {/* Welcome block */}
          <div className="text-center space-y-2">
            <div
              className="text-xs font-semibold tracking-widest uppercase mb-1"
              style={{ color: "#C5A059" }}
            >
              Welcome back
            </div>
            <h2
              className="font-cinzel font-bold tracking-[0.1em] text-charcoal"
              style={{ fontSize: 26 }}
            >
              {firstName}.
            </h2>
            <p className="text-sm" style={{ color: "#6b5a3a" }}>
              Your Ambassador assistant is ready.
            </p>
            <div className="flex justify-center mt-2">
              <span className="badge badge-green" style={{ fontSize: 11 }}>
                ● Assistant Online
              </span>
            </div>
          </div>

          {/* Resume banner */}
          {activeSession && (
            <div
              className="card p-5 flex items-center justify-between gap-4"
              style={{ borderLeft: "3px solid #C5A059" }}
            >
              <div>
                <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-1">
                  Continue where you left off
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
                  {activeSession.preview || "Active conversation"}
                </p>
                <p className="text-xs text-gray-400 mt-0.5">
                  {activeSession.message_count} messages · {timeLabel(activeSession.started_at)}
                </p>
              </div>
              <button
                className="gold-btn flex-shrink-0"
                disabled={loadingSession === activeSession.id}
                onClick={() => openSession(activeSession)}
              >
                {loadingSession === activeSession.id ? "…" : "Resume"}
              </button>
            </div>
          )}

          {/* Primary CTA */}
          <div className="card p-8 text-center space-y-4">
            <div className="text-xs font-semibold tracking-widest text-gold uppercase">
              Start a conversation
            </div>
            <p className="text-sm" style={{ color: "#6b5a3a" }}>
              Ask Ambassador anything about call center procedures, policies, or escalations.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <button className="gold-btn" onClick={startFresh}>
                Start New Chat
              </button>
              <button
                className="outline-btn flex items-center gap-2"
                onClick={() => navigate("/chat", { state: { fresh: true, autoMic: true } })}
              >
                <svg
                  width={14}
                  height={14}
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <rect x="9" y="2" width="6" height="12" rx="3" />
                  <path d="M5 10a7 7 0 0 0 14 0" />
                  <line x1="12" y1="19" x2="12" y2="22" />
                  <line x1="8" y1="22" x2="16" y2="22" />
                </svg>
                Open with Voice
              </button>
            </div>
          </div>

          {/* Help panel */}
          <div className="card overflow-hidden">
            <button
              className="w-full px-5 py-4 flex items-center justify-between"
              onClick={() => setHelpOpen((v) => !v)}
            >
              <div className="text-xs font-semibold tracking-widest text-gold uppercase">
                How to use Ambassador
              </div>
              <svg
                width={14}
                height={14}
                viewBox="0 0 24 24"
                fill="none"
                stroke="#C5A059"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                style={{
                  transform: helpOpen ? "rotate(180deg)" : "none",
                  transition: "transform 0.15s",
                }}
              >
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>
            {helpOpen && (
              <div
                className="px-5 pb-5 space-y-3 text-sm"
                style={{ borderTop: "1px solid rgba(197,160,89,0.15)", color: "#5a4a30" }}
              >
                <div className="flex gap-3 pt-4">
                  <span
                    className="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white font-cinzel"
                    style={{ background: "radial-gradient(circle at 38% 35%,#e8cc80,#c5a059,#8a6d1f)" }}
                  >
                    1
                  </span>
                  <p>
                    <strong>Ask anything</strong> — Ambassador can answer questions about refund
                    policies, service tiers, escalation procedures, and more using the
                    call-center knowledge base.
                  </p>
                </div>
                <div className="flex gap-3">
                  <span
                    className="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white font-cinzel"
                    style={{ background: "radial-gradient(circle at 38% 35%,#e8cc80,#c5a059,#8a6d1f)" }}
                  >
                    2
                  </span>
                  <p>
                    <strong>Talk to a human</strong> — If the assistant can't help, click
                    "Talk to agent" on any response or use the mic button to speak your
                    request. A call-center agent will be connected to you.
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Chat history */}
          <div>
            <h3 className="section-title mb-4">Your Conversations</h3>

            {loadingHistory && (
              <div className="text-center py-8 text-sm text-gray-400">Loading history…</div>
            )}

            {!loadingHistory && sessions.length === 0 && (
              <div className="card p-8 text-center text-sm text-gray-400">
                No conversations yet. Start one above!
              </div>
            )}

            {sessions.length > 0 && (
              <div
                className="space-y-1 rounded-lg overflow-hidden"
                style={{ border: "1px solid rgba(197,160,89,0.2)" }}
              >
                {sessions.map((s, i) => (
                  <button
                    key={s.id}
                    onClick={() => openSession(s)}
                    disabled={loadingSession === s.id}
                    className="w-full text-left px-5 py-4 flex items-center justify-between gap-3 transition-colors"
                    style={{
                      background:
                        loadingSession === s.id
                          ? "rgba(197,160,89,0.06)"
                          : "rgba(255,255,255,0.7)",
                      borderBottom:
                        i < sessions.length - 1
                          ? "1px solid rgba(197,160,89,0.12)"
                          : "none",
                      cursor: loadingSession === s.id ? "default" : "pointer",
                    }}
                    onMouseEnter={(e) => {
                      (e.currentTarget.style.background = "rgba(197,160,89,0.06)");
                    }}
                    onMouseLeave={(e) => {
                      if (loadingSession !== s.id)
                        (e.currentTarget.style.background = "rgba(255,255,255,0.7)");
                    }}
                  >
                    <div className="flex-1 min-w-0">
                      <p
                        className="text-sm text-charcoal leading-snug"
                        style={{
                          overflow: "hidden",
                          display: "-webkit-box",
                          WebkitLineClamp: 1,
                          WebkitBoxOrient: "vertical",
                        }}
                      >
                        {s.preview || "Empty conversation"}
                      </p>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-xs text-gray-400">{timeLabel(s.started_at)}</span>
                        <span className="text-xs text-gray-300">·</span>
                        <span className="text-xs text-gray-400">{s.message_count} messages</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className={`badge ${s.status === "Aktivna" ? "badge-green" : "badge-gray"} text-[10px]`}>
                        {s.status === "Aktivna" ? "Active" : "Closed"}
                      </span>
                      {loadingSession === s.id ? (
                        <span className="text-xs text-gray-400">…</span>
                      ) : (
                        <svg
                          width={12}
                          height={12}
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="rgba(197,160,89,0.5)"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <polyline points="9 18 15 12 9 6" />
                        </svg>
                      )}
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
