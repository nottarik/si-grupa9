import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { updateMe, deleteMyHistory, deleteMyAccount } from "../../api/auth";
import type { User } from "../../types";

interface Props {
  user: User;
  onLogout: () => void;
  onRefreshUser: () => Promise<void>;
  onHistoryDeleted: () => void;
}

type View = "main" | "rename" | "confirmHistory" | "confirmAccount";

function initials(name: string | null): string {
  if (!name) return "?";
  const parts = name.trim().split(" ");
  return parts.length >= 2
    ? (parts[0][0] + parts[1][0]).toUpperCase()
    : parts[0].slice(0, 2).toUpperCase();
}

export default function UserMenu({ user, onLogout, onRefreshUser, onHistoryDeleted }: Props) {
  const [open, setOpen] = useState(false);
  const [view, setView] = useState<View>("main");
  const [renameValue, setRenameValue] = useState(user.full_name ?? "");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [menuPos, setMenuPos] = useState({ top: 0, right: 0 });
  const btnRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    function close(e: MouseEvent) {
      if (
        menuRef.current && !menuRef.current.contains(e.target as Node) &&
        btnRef.current && !btnRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
        setView("main");
        setError(null);
      }
    }
    window.addEventListener("mousedown", close);
    return () => window.removeEventListener("mousedown", close);
  }, [open]);

  function toggle() {
    if (!open && btnRef.current) {
      const rect = btnRef.current.getBoundingClientRect();
      setMenuPos({ top: rect.bottom + 8, right: window.innerWidth - rect.right });
    }
    setOpen((v) => !v);
    setView("main");
    setRenameValue(user.full_name ?? "");
    setError(null);
  }

  async function handleRename() {
    const trimmed = renameValue.trim();
    if (!trimmed) return;
    setBusy(true);
    setError(null);
    try {
      await updateMe(trimmed);
      await onRefreshUser();
      setView("main");
      setOpen(false);
    } catch {
      setError("Failed to update name.");
    } finally {
      setBusy(false);
    }
  }

  async function handleDeleteHistory() {
    setBusy(true);
    setError(null);
    try {
      await deleteMyHistory();
      onHistoryDeleted();
      setView("main");
      setOpen(false);
    } catch {
      setError("Failed to delete history.");
    } finally {
      setBusy(false);
    }
  }

  async function handleDeleteAccount() {
    setBusy(true);
    setError(null);
    try {
      await deleteMyAccount();
      onLogout();
    } catch {
      setError("Failed to delete account.");
      setBusy(false);
    }
  }

  const itemStyle: React.CSSProperties = {
    width: "100%",
    textAlign: "left",
    background: "none",
    border: "none",
    cursor: "pointer",
    padding: "10px 16px",
    fontSize: 13,
    fontFamily: "Inter, sans-serif",
    color: "#3a3028",
    display: "block",
  };

  const dangerStyle: React.CSSProperties = { ...itemStyle, color: "#dc2626" };

  return (
    <>
      {/* Avatar button */}
      <button
        ref={btnRef}
        onClick={toggle}
        title="User settings"
        className="coin-avatar flex items-center justify-center rounded-full font-cinzel font-bold transition-opacity hover:opacity-80"
        style={{ width: 32, height: 32, fontSize: 11, color: "#fff", border: "none", cursor: "pointer", flexShrink: 0 }}
      >
        {initials(user.full_name)}
      </button>

      {/* Dropdown — rendered via portal into document.body to escape backdrop-filter stacking context */}
      {open && createPortal(
        <div
          ref={menuRef}
          style={{
            position: "fixed",
            top: menuPos.top,
            right: menuPos.right,
            width: 230,
            background: "rgba(255,255,255,0.97)",
            backdropFilter: "blur(16px)",
            border: "1px solid rgba(197,160,89,0.25)",
            borderRadius: 10,
            boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
            zIndex: 9999,
            overflow: "hidden",
          }}
        >
          {/* ── Main view ── */}
          {view === "main" && (
            <>
              <div style={{ padding: "12px 16px 10px", borderBottom: "1px solid rgba(197,160,89,0.15)" }}>
                <p style={{ fontFamily: "Inter, sans-serif", fontSize: 13, fontWeight: 600, color: "#1C1C2E", margin: 0 }}>
                  {user.full_name || "—"}
                </p>
                <p style={{ fontFamily: "Inter, sans-serif", fontSize: 11, color: "#9a8a6a", margin: "2px 0 0" }}>
                  {user.email}
                </p>
              </div>

              <button
                style={itemStyle}
                onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(197,160,89,0.07)")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "none")}
                onClick={() => { setView("rename"); setRenameValue(user.full_name ?? ""); }}
              >
                Change name
              </button>

              <button
                style={itemStyle}
                onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(197,160,89,0.07)")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "none")}
                onClick={() => setView("confirmHistory")}
              >
                Delete all history
              </button>

              <button
                style={dangerStyle}
                onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(220,38,38,0.05)")}
                onMouseLeave={(e) => (e.currentTarget.style.background = "none")}
                onClick={() => setView("confirmAccount")}
              >
                Delete account
              </button>

              <div style={{ borderTop: "1px solid rgba(197,160,89,0.15)", margin: "4px 0 0" }}>
                <button
                  style={{ ...itemStyle, color: "rgba(197,160,89,0.8)" }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(197,160,89,0.07)")}
                  onMouseLeave={(e) => (e.currentTarget.style.background = "none")}
                  onClick={onLogout}
                >
                  Logout
                </button>
              </div>
            </>
          )}

          {/* ── Rename view ── */}
          {view === "rename" && (
            <div style={{ padding: "14px 16px" }}>
              <p style={{ fontFamily: "Inter, sans-serif", fontSize: 12, color: "#6b6050", margin: "0 0 10px", fontWeight: 500 }}>
                Change display name
              </p>
              <input
                autoFocus
                value={renameValue}
                onChange={(e) => setRenameValue(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter") handleRename(); if (e.key === "Escape") setView("main"); }}
                style={{
                  width: "100%",
                  boxSizing: "border-box",
                  padding: "7px 10px",
                  border: "1px solid rgba(197,160,89,0.35)",
                  borderRadius: 6,
                  fontFamily: "Inter, sans-serif",
                  fontSize: 13,
                  outline: "none",
                  color: "#1C1C2E",
                  marginBottom: 10,
                }}
              />
              {error && <p style={{ color: "#dc2626", fontSize: 11, margin: "0 0 8px", fontFamily: "Inter, sans-serif" }}>{error}</p>}
              <div style={{ display: "flex", gap: 8 }}>
                <button
                  onClick={handleRename}
                  disabled={busy || !renameValue.trim()}
                  style={{ flex: 1, padding: "7px 0", background: "rgba(197,160,89,0.9)", color: "#fff", border: "none", borderRadius: 6, cursor: busy ? "default" : "pointer", fontFamily: "Inter, sans-serif", fontSize: 12, opacity: busy ? 0.6 : 1 }}
                >
                  {busy ? "Saving…" : "Save"}
                </button>
                <button
                  onClick={() => { setView("main"); setError(null); }}
                  disabled={busy}
                  style={{ flex: 1, padding: "7px 0", background: "none", color: "#9a8a6a", border: "1px solid rgba(197,160,89,0.25)", borderRadius: 6, cursor: "pointer", fontFamily: "Inter, sans-serif", fontSize: 12 }}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* ── Confirm delete history ── */}
          {view === "confirmHistory" && (
            <div style={{ padding: "14px 16px" }}>
              <p style={{ fontFamily: "Inter, sans-serif", fontSize: 13, color: "#1C1C2E", margin: "0 0 6px", fontWeight: 600 }}>
                Delete all history?
              </p>
              <p style={{ fontFamily: "Inter, sans-serif", fontSize: 12, color: "#6b6050", margin: "0 0 14px" }}>
                All your conversations will be permanently removed.
              </p>
              {error && <p style={{ color: "#dc2626", fontSize: 11, margin: "0 0 8px", fontFamily: "Inter, sans-serif" }}>{error}</p>}
              <div style={{ display: "flex", gap: 8 }}>
                <button
                  onClick={handleDeleteHistory}
                  disabled={busy}
                  style={{ flex: 1, padding: "7px 0", background: "#dc2626", color: "#fff", border: "none", borderRadius: 6, cursor: busy ? "default" : "pointer", fontFamily: "Inter, sans-serif", fontSize: 12, opacity: busy ? 0.6 : 1 }}
                >
                  {busy ? "Deleting…" : "Delete all"}
                </button>
                <button
                  onClick={() => { setView("main"); setError(null); }}
                  disabled={busy}
                  style={{ flex: 1, padding: "7px 0", background: "none", color: "#9a8a6a", border: "1px solid rgba(197,160,89,0.25)", borderRadius: 6, cursor: "pointer", fontFamily: "Inter, sans-serif", fontSize: 12 }}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          {/* ── Confirm delete account ── */}
          {view === "confirmAccount" && (
            <div style={{ padding: "14px 16px" }}>
              <p style={{ fontFamily: "Inter, sans-serif", fontSize: 13, color: "#1C1C2E", margin: "0 0 6px", fontWeight: 600 }}>
                Delete account?
              </p>
              <p style={{ fontFamily: "Inter, sans-serif", fontSize: 12, color: "#6b6050", margin: "0 0 14px" }}>
                Your account and all data will be permanently deleted.
              </p>
              {error && <p style={{ color: "#dc2626", fontSize: 11, margin: "0 0 8px", fontFamily: "Inter, sans-serif" }}>{error}</p>}
              <div style={{ display: "flex", gap: 8 }}>
                <button
                  onClick={handleDeleteAccount}
                  disabled={busy}
                  style={{ flex: 1, padding: "7px 0", background: "#dc2626", color: "#fff", border: "none", borderRadius: 6, cursor: busy ? "default" : "pointer", fontFamily: "Inter, sans-serif", fontSize: 12, opacity: busy ? 0.6 : 1 }}
                >
                  {busy ? "Deleting…" : "Delete"}
                </button>
                <button
                  onClick={() => { setView("main"); setError(null); }}
                  disabled={busy}
                  style={{ flex: 1, padding: "7px 0", background: "none", color: "#9a8a6a", border: "1px solid rgba(197,160,89,0.25)", borderRadius: 6, cursor: "pointer", fontFamily: "Inter, sans-serif", fontSize: 12 }}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>,
        document.body
      )}
    </>
  );
}
