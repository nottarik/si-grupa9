import { useState } from "react";
import { getNotifPrefs, setNotifPrefs } from "../escalation/notifPrefs";

export default function NotificationPrefs() {
  const [open, setOpen] = useState(false);
  const [prefs, setPrefs] = useState(getNotifPrefs);

  function toggle(key: "sound" | "browser") {
    const next = { ...prefs, [key]: !prefs[key] };
    if (key === "browser" && next.browser && Notification.permission === "default") {
      Notification.requestPermission().then((p) => {
        if (p !== "granted") next.browser = false;
        setPrefs(next);
        setNotifPrefs(next);
      });
      return;
    }
    setPrefs(next);
    setNotifPrefs(next);
  }

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        title="Notification preferences"
        className="flex items-center justify-center transition-colors"
        style={{
          width: 30,
          height: 30,
          borderRadius: 6,
          background: open ? "rgba(197,160,89,0.15)" : "transparent",
          border: "1px solid rgba(197,160,89,0.25)",
          color: "rgba(197,160,89,0.75)",
          cursor: "pointer",
        }}
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
      </button>

      {open && (
        <div
          className="card absolute right-0 top-9 z-50 p-4 space-y-3"
          style={{ minWidth: 220 }}
        >
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-1">
            Notifications
          </div>
          <label className="flex items-center justify-between gap-3 cursor-pointer text-sm text-charcoal">
            <span>Sound on new escalation</span>
            <input
              type="checkbox"
              checked={prefs.sound}
              onChange={() => toggle("sound")}
              className="accent-gold"
            />
          </label>
          <label className="flex items-center justify-between gap-3 cursor-pointer text-sm text-charcoal">
            <span>Browser notifications</span>
            <input
              type="checkbox"
              checked={prefs.browser}
              onChange={() => toggle("browser")}
              className="accent-gold"
            />
          </label>
          {prefs.browser && Notification.permission === "denied" && (
            <p className="text-xs" style={{ color: "#dc2626" }}>
              Notifications blocked in browser settings.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
