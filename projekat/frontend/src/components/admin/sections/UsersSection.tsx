import { useEffect, useState } from "react";
import { listUsers, updateUserRole } from "../../../api/users";
import type { User, UserRole } from "../../../types";

const ROLES: { value: UserRole; label: string }[] = [
  { value: "admin", label: "Admin" },
  { value: "manager", label: "Manager" },
  { value: "agent", label: "Agent" },
  { value: "user", label: "User" },
];

const ROLE_BADGE: Record<UserRole, string> = {
  admin: "badge-red",
  manager: "badge-yellow",
  agent: "badge-blue",
  user: "badge-gray",
};

export default function UsersSection() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState<string | null>(null);
  const [saved, setSaved] = useState<string | null>(null);

  useEffect(() => {
    listUsers()
      .then(setUsers)
      .catch(() => setError("Failed to load users."))
      .finally(() => setLoading(false));
  }, []);

  async function handleRoleChange(user: User, newRole: UserRole) {
    if (newRole === user.role) return;
    setSaving(user.id);
    setSaved(null);
    try {
      const updated = await updateUserRole(user.id, newRole);
      setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
      setSaved(user.id);
      setTimeout(() => setSaved(null), 2000);
    } catch {
      setError(`Failed to update role for ${user.email}.`);
    } finally {
      setSaving(null);
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <h2 className="section-title">Upravljanje korisnicima</h2>
        <div className="card p-8 text-center text-gray-400 text-sm">Učitavanje...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="section-title">Upravljanje korisnicima</h2>

      {error && (
        <div
          className="text-sm px-4 py-3 rounded-lg"
          style={{ background: "rgba(239,68,68,0.08)", color: "#ef4444", border: "1px solid rgba(239,68,68,0.2)" }}
        >
          {error}
          <button
            className="ml-3 underline text-xs"
            onClick={() => setError(null)}
          >
            Zatvori
          </button>
        </div>
      )}

      <div className="card overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr style={{ borderBottom: "1px solid rgba(197,160,89,0.15)" }}>
              {["Ime i prezime", "Email", "Uloga", "Status", ""].map((h) => (
                <th
                  key={h}
                  className="text-left px-4 py-3 text-xs font-semibold tracking-widest uppercase"
                  style={{ color: "rgba(197,160,89,0.8)" }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr
                key={u.id}
                style={{ borderBottom: "1px solid rgba(197,160,89,0.08)" }}
                className="hover:bg-amber-50/30 transition-colors"
              >
                <td className="px-4 py-3 text-charcoal font-medium">
                  {u.full_name || "—"}
                </td>
                <td className="px-4 py-3 text-gray-500">{u.email}</td>
                <td className="px-4 py-3">
                  <span className={`badge ${ROLE_BADGE[u.role]}`}>{u.role}</span>
                </td>
                <td className="px-4 py-3">
                  <span className={`badge ${u.is_active ? "badge-green" : "badge-gray"}`}>
                    {u.is_active ? "Aktivan" : "Neaktivan"}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <select
                      value={u.role}
                      disabled={saving === u.id}
                      onChange={(e) => handleRoleChange(u, e.target.value as UserRole)}
                      className="text-xs rounded-md px-2 py-1.5 border transition-colors"
                      style={{
                        border: "1px solid rgba(197,160,89,0.4)",
                        background: "rgba(255,255,255,0.8)",
                        color: "#3d3d3d",
                        minWidth: 110,
                      }}
                    >
                      {ROLES.map((r) => (
                        <option key={r.value} value={r.value}>
                          {r.label}
                        </option>
                      ))}
                    </select>
                    {saving === u.id && (
                      <span className="text-xs text-gray-400">Čuvanje...</span>
                    )}
                    {saved === u.id && (
                      <span className="text-xs" style={{ color: "#22c55e" }}>
                        ✓ Sačuvano
                      </span>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {users.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-gray-400 text-sm">
                  Nema korisnika.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
