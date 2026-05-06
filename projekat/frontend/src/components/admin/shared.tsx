import React from "react";

// ── Generic SVG icon ─────────────────────────────────────────────────
interface IcProps {
  d: React.ReactNode;
  size?: number;
}
export const Ic = ({ d, size = 16 }: IcProps) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {typeof d === "string" ? <path d={d} /> : d}
  </svg>
);

// ── Icon path registry ───────────────────────────────────────────────
export const icons = {
  dashboard: (
    <>
      <rect x="3" y="3" width="7" height="7" rx="1" />
      <rect x="14" y="3" width="7" height="7" rx="1" />
      <rect x="3" y="14" width="7" height="7" rx="1" />
      <rect x="14" y="14" width="7" height="7" rx="1" />
    </>
  ),
  transcripts: (
    <>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
      <polyline points="10 9 9 9 8 9" />
    </>
  ),
  chat: (
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  ),
  ratings: (
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
  ),
  issues: (
    <>
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </>
  ),
  training: (
    <>
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
    </>
  ),
  upload: (
    <>
      <polyline points="16 16 12 12 8 16" />
      <line x1="12" y1="12" x2="12" y2="21" />
      <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
    </>
  ),
  users: (
    <>
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </>
  ),
  edit: (
    <>
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
    </>
  ),
  trash: (
    <>
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
      <path d="M10 11v6M14 11v6" />
      <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
    </>
  ),
  check: "M20 6L9 17l-5-5",
  x: "M18 6L6 18M6 6l12 12",
};

// ── Star rating display ──────────────────────────────────────────────
export const Stars = ({ n }: { n: number }) => (
  <span className="text-sm" style={{ color: "#C5A059" }}>
    {"★".repeat(Math.round(n))}
    {"☆".repeat(5 - Math.round(n))}
  </span>
);

// ── Coloured status badge ────────────────────────────────────────────
const BADGE_MAP: Record<string, string> = {
  Processed: "badge-green",
  Pending: "badge-yellow",
  Flagged: "badge-red",
  Open: "badge-red",
  "In Progress": "badge-yellow",
  Resolved: "badge-green",
  High: "badge-red",
  Medium: "badge-yellow",
  Low: "badge-blue",
  processed: "badge-green",
  pending: "badge-yellow",
  processing: "badge-yellow",
  failed: "badge-red",
  approved: "badge-green",
  rejected: "badge-red",
  pending_approval: "badge-yellow",
  // Bosnian transcript statuses (DB values)
  Sirovi: "badge-yellow",
  Obradjeno: "badge-green",
  Odbacen: "badge-red",
};

const LABEL_MAP: Record<string, string> = {
  Sirovi: "Raw",
  Obradjeno: "Processed",
  Odbacen: "Rejected",
};

export const StatusBadge = ({ s }: { s: string }) => (
  <span className={`badge ${BADGE_MAP[s] ?? "badge-gray"}`}>{LABEL_MAP[s] ?? s}</span>
);
