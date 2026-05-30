import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { useEscalation } from "../../hooks/useEscalation";
import { escalationApi } from "../../api/escalation";
import NotificationPrefs from "./NotificationPrefs";
import AgentDashboard from "./sections/AgentDashboard";
import AgentQueue from "./sections/AgentQueue";
import KbLookup from "./sections/KbLookup";
import MyHistory from "./sections/MyHistory";

const ESCALATION_ICON = (
  <>
    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.91a16 16 0 0 0 6.13 6.13l.91-.91a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z" />
    <line x1="18" y1="2" x2="22" y2="6" />
    <polyline points="15 2 18 2 18 5" />
  </>
);

const KB_ICON = (
  <>
    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
  </>
);

const HISTORY_ICON = (
  <>
    <circle cx="12" cy="12" r="10" />
    <polyline points="12 6 12 12 16 14" />
  </>
);

const DASHBOARD_ICON = (
  <>
    <rect x="3" y="3" width="7" height="7" rx="1" />
    <rect x="14" y="3" width="7" height="7" rx="1" />
    <rect x="3" y="14" width="7" height="7" rx="1" />
    <rect x="14" y="14" width="7" height="7" rx="1" />
  </>
);

type NavId = "dashboard" | "queue" | "kb" | "history";

const NAV: { id: NavId; label: string; icon: React.ReactNode }[] = [
  { id: "dashboard", label: "Dashboard",      icon: DASHBOARD_ICON },
  { id: "queue",     label: "Live Queue",     icon: ESCALATION_ICON },
  { id: "kb",        label: "Knowledge Base", icon: KB_ICON },
  { id: "history",   label: "My History",    icon: HISTORY_ICON },
];

const TODAY = new Date().toLocaleDateString("en-US", {
  month: "long",
  day: "numeric",
  year: "numeric",
});

export default function AgentShell() {
  const [active, setActive] = useState<NavId>("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [agentOnline, setAgentOnline] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // Single hook instance — owns the WebSocket for the entire agent session
  const eskal = useEscalation();

  // Connect agent WS on mount so it's open before any chat is accepted
  useEffect(() => {
    eskal.connectAgentWs();
    return () => eskal.disconnectWs();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Poll queue every 10 s as a fallback for missed WS broadcasts
  useEffect(() => {
    eskal.fetchQueue();
    const id = setInterval(eskal.fetchQueue, 10_000);
    return () => clearInterval(id);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const initial = (user?.full_name || user?.email || "A").charAt(0).toUpperCase();

  async function toggleOnline() {
    const next = !agentOnline;
    try {
      await escalationApi.updateAgentStatus(next ? "Online" : "Offline");
      // WS stays connected regardless of Online/Offline toggle (mount keeps it alive)
      // Re-connect proactively in case it dropped while the agent was Offline
      if (next) eskal.connectAgentWs();
      setAgentOnline(next);
    } catch {
      /* ignore */
    }
  }

  function handleLogout() {
    escalationApi.updateAgentStatus("Offline").catch(() => {});
    eskal.disconnectWs();
    logout();
    navigate("/login");
  }

  const currentLabel = NAV.find((n) => n.id === active)?.label ?? "";

  function renderSection() {
    switch (active) {
      case "dashboard":
        return (
          <AgentDashboard
            onGoToQueue={() => setActive("queue")}
            queue={eskal.queue}
          />
        );
      case "queue":
        return (
          <AgentQueue
            currentAgentId={user?.id ?? ""}
            agentOnline={agentOnline}
            onToggleOnline={toggleOnline}
            queue={eskal.queue}
            loading={eskal.loading}
            fetchQueue={eskal.fetchQueue}
            sendAgentMessage={eskal.sendAgentMessage}
            sendTypingSignal={eskal.sendTypingSignal}
            resolveEscalation={eskal.resolveEscalation}
            releaseEscalation={eskal.releaseEscalation}
            registerUserMsgHandler={eskal.registerUserMsgHandler}
          />
        );
      case "kb":
        return <KbLookup />;
      case "history":
        return <MyHistory />;
    }
  }

  return (
    <div className="admin-bg" style={{ height: "100vh", display: "flex", overflow: "hidden" }}>
      {/* ── Sidebar ── */}
      <aside
        className="flex-shrink-0 flex flex-col transition-all duration-200"
        style={{
          width: sidebarOpen ? 224 : 0,
          overflow: "hidden",
          background: "rgba(255,255,255,0.7)",
          backdropFilter: "blur(16px)",
          borderRight: "1px solid rgba(197,160,89,0.2)",
        }}
      >
        <div className="px-5 py-5" style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}>
          <div className="font-cinzel font-bold text-charcoal tracking-widest text-sm">
            AMBASSADOR
          </div>
          <div className="text-xs tracking-widest mt-0.5" style={{ color: "rgba(197,160,89,0.7)" }}>
            Agent Console
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
          {NAV.map((n) => (
            <button
              key={n.id}
              className={`sidebar-item ${active === n.id ? "active" : ""}`}
              onClick={() => setActive(n.id)}
            >
              <svg
                width={15}
                height={15}
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                {n.icon}
              </svg>
              {n.label}
            </button>
          ))}
        </nav>

        <div className="px-5 py-4" style={{ borderTop: "1px solid rgba(197,160,89,0.15)" }}>
          <a
            href="/chat"
            className="text-xs flex items-center gap-1.5 transition-colors"
            style={{ color: "rgba(197,160,89,0.7)" }}
            onMouseEnter={(e) => ((e.target as HTMLElement).style.color = "#C5A059")}
            onMouseLeave={(e) => ((e.target as HTMLElement).style.color = "rgba(197,160,89,0.7)")}
          >
            <svg
              width={12}
              height={12}
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            Open Chatbot
          </a>
        </div>
      </aside>

      {/* ── Main area ── */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header
          className="glass flex-shrink-0 flex items-center gap-4 px-6 py-3"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          <button
            onClick={() => setSidebarOpen((v) => !v)}
            className="text-gray-400 hover:text-gold transition-colors"
          >
            <svg
              width={18}
              height={18}
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>

          <div
            className="font-cinzel text-xs tracking-widest uppercase"
            style={{ color: "rgba(197,160,89,0.7)" }}
          >
            {currentLabel}
          </div>

          <div className="ml-auto flex items-center gap-3">
            <div className="text-xs text-gray-400">{TODAY}</div>

            <a
              href="/chat"
              className="text-xs transition-colors"
              style={{ color: "rgba(197,160,89,0.7)", textDecoration: "none" }}
              onMouseEnter={(e) => ((e.target as HTMLElement).style.color = "#C5A059")}
              onMouseLeave={(e) => ((e.target as HTMLElement).style.color = "rgba(197,160,89,0.7)")}
            >
              Chat
            </a>

            {/* Agent status pill — always visible, controls the WS */}
            <button
              onClick={toggleOnline}
              className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full transition-all"
              style={{
                background: agentOnline
                  ? "linear-gradient(135deg,#e8cc80,#c5a059)"
                  : "rgba(156,163,175,0.15)",
                color: agentOnline ? "#fff" : "#9ca3af",
                border: agentOnline ? "none" : "1px solid rgba(156,163,175,0.3)",
                fontWeight: 500,
              }}
            >
              <span
                className="w-1.5 h-1.5 rounded-full"
                style={{ background: agentOnline ? "#fff" : "#9ca3af" }}
              />
              {agentOnline ? "Online" : "Offline"}
            </button>

            <NotificationPrefs />

            <button
              onClick={handleLogout}
              className="text-xs text-gray-400 hover:text-gold transition-colors"
            >
              Logout
            </button>

            <div
              className="w-7 h-7 rounded-full flex items-center justify-center text-white font-cinzel font-bold text-xs"
              style={{
                background: "radial-gradient(circle at 38% 35%,#e8cc80,#c5a059,#8a6d1f)",
                boxShadow: "0 2px 6px rgba(197,160,89,0.3)",
              }}
            >
              {initial}
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">{renderSection()}</main>
      </div>
    </div>
  );
}
