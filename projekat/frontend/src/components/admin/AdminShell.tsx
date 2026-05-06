import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import { icons } from "./shared";
import Dashboard from "./sections/Dashboard";
import UploadSection from "./sections/UploadSection";
import TranscriptList from "./sections/TranscriptList";
import ChatLogs from "./sections/ChatLogs";
import Ratings from "./sections/Ratings";
import Issues from "./sections/Issues";
import Training from "./sections/Training";
import UsersSection from "./sections/UsersSection";

const NAV = [
  { id: "dashboard",   label: "Dashboard",        icon: icons.dashboard },
  { id: "upload",      label: "Upload",            icon: icons.upload },
  { id: "transcripts", label: "Transcripts",       icon: icons.transcripts },
  { id: "chat",        label: "Chat Logs",         icon: icons.chat },
  { id: "ratings",     label: "Ratings",           icon: icons.ratings },
  { id: "issues",      label: "Issues",            icon: icons.issues },
  { id: "training",    label: "Training Dataset",  icon: icons.training },
  { id: "users",       label: "Users",              icon: icons.users },
] as const;

type NavId = (typeof NAV)[number]["id"];

const TODAY = new Date().toLocaleDateString("en-US", {
  month: "long",
  day: "numeric",
  year: "numeric",
});

export default function AdminShell() {
  const [active, setActive] = useState<NavId>("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [transcriptKey, setTranscriptKey] = useState(0);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  function handleNavClick(id: NavId) {
    if (id === "transcripts") setTranscriptKey((k) => k + 1);
    setActive(id);
  }

  const sections: Record<NavId, JSX.Element> = {
    dashboard:   <Dashboard />,
    upload:      <UploadSection />,
    transcripts: <TranscriptList key={transcriptKey} />,
    chat:        <ChatLogs />,
    ratings:     <Ratings />,
    issues:      <Issues />,
    training:    <Training />,
    users:       <UsersSection />,
  };

  const currentLabel = NAV.find((n) => n.id === active)?.label ?? "";
  const initial = (user?.full_name || user?.email || "A").charAt(0).toUpperCase();

  return (
    <div
      className="admin-bg"
      style={{ height: "100vh", display: "flex", overflow: "hidden" }}
    >
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
        {/* Logo */}
        <div
          className="px-5 py-5"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          <div className="font-cinzel font-bold text-charcoal tracking-widest text-sm">
            AMBASSADOR
          </div>
          <div className="text-xs tracking-widest mt-0.5" style={{ color: "rgba(197,160,89,0.7)" }}>
            Admin Panel
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
          {NAV.map((n) => (
            <button
              key={n.id}
              className={`sidebar-item ${active === n.id ? "active" : ""}`}
              onClick={() => handleNavClick(n.id)}
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

        {/* Footer */}
        <div
          className="px-5 py-4"
          style={{ borderTop: "1px solid rgba(197,160,89,0.15)" }}
        >
          <a
            href="/"
            className="text-xs flex items-center gap-1.5 transition-colors"
            style={{ color: "rgba(197,160,89,0.7)" }}
            onMouseEnter={(e) =>
              ((e.target as HTMLElement).style.color = "#C5A059")
            }
            onMouseLeave={(e) =>
              ((e.target as HTMLElement).style.color = "rgba(197,160,89,0.7)")
            }
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
        {/* Top bar */}
        <header
          className="glass flex-shrink-0 flex items-center gap-4 px-6 py-3"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          {/* Hamburger */}
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

          {/* Section label */}
          <div
            className="font-cinzel text-xs tracking-widest uppercase"
            style={{ color: "rgba(197,160,89,0.7)" }}
          >
            {currentLabel}
          </div>

          {/* Right side */}
          <div className="ml-auto flex items-center gap-3">
            <div className="text-xs text-gray-400">{TODAY}</div>
            <button
              onClick={handleLogout}
              className="text-xs text-gray-400 hover:text-gold transition-colors"
            >
              Logout
            </button>
            {/* Avatar */}
            <div
              className="w-7 h-7 rounded-full flex items-center justify-center text-white font-cinzel font-bold text-xs"
              style={{
                background:
                  "radial-gradient(circle at 38% 35%,#e8cc80,#c5a059,#8a6d1f)",
                boxShadow: "0 2px 6px rgba(197,160,89,0.3)",
              }}
            >
              {initial}
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-6">{sections[active]}</main>
      </div>
    </div>
  );
}
