const KEY = "agent_notif_prefs";

export interface NotifPrefs {
  sound: boolean;
  browser: boolean;
}

const DEFAULTS: NotifPrefs = { sound: true, browser: false };

export function getNotifPrefs(): NotifPrefs {
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch { /* ignore */ }
  return DEFAULTS;
}

export function setNotifPrefs(prefs: Partial<NotifPrefs>): void {
  localStorage.setItem(KEY, JSON.stringify({ ...getNotifPrefs(), ...prefs }));
}
