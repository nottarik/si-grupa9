import { useEffect, useRef } from "react";
import type { EscalationItem } from "../api/escalation";
import { getNotifPrefs } from "../components/escalation/notifPrefs";

function playNotificationTone() {
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.frequency.setValueAtTime(880, ctx.currentTime);
    osc.frequency.setValueAtTime(1100, ctx.currentTime + 0.1);
    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.3);
  } catch {
    /* audio not available */
  }
}

/**
 * Fire a sound + browser notification when a new escalation enters the queue,
 * regardless of which dashboard section is currently open. Only active once the
 * agent/admin has gone Online (`enabled`). Mount this once at the shell level.
 */
export function useNewEscalationAlert(queue: EscalationItem[], enabled: boolean) {
  const prevPendingRef = useRef<number | null>(null);

  useEffect(() => {
    const pending = queue.filter((e) => e.status === "Cekanje").length;
    const prev = prevPendingRef.current;
    prevPendingRef.current = pending;
    if (!enabled) return;
    // First observation after going online sets the baseline — don't alert for backlog.
    if (prev === null) return;
    if (pending > prev) {
      const prefs = getNotifPrefs();
      if (prefs.sound) playNotificationTone();
      if (
        prefs.browser &&
        typeof Notification !== "undefined" &&
        Notification.permission === "granted"
      ) {
        new Notification("New agent call", { body: "A user is waiting in the queue." });
      }
    }
  }, [queue, enabled]);

  // Going offline clears the baseline so re-going-online won't alert for the backlog.
  useEffect(() => {
    if (!enabled) prevPendingRef.current = null;
  }, [enabled]);
}
