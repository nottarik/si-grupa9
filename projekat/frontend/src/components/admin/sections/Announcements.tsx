import { useState, useEffect } from "react";
import { announcementsApi, type Announcement } from "../../../api/announcements";
import { Ic, icons, StatusBadge } from "../shared";

export default function Announcements() {
  const [items, setItems] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Create form state
  const [newNaslov, setNewNaslov] = useState("");
  const [newTekst, setNewTekst] = useState("");
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);

  // Edit state
  const [editId, setEditId] = useState<number | null>(null);
  const [editNaslov, setEditNaslov] = useState("");
  const [editTekst, setEditTekst] = useState("");
  const [saving, setSaving] = useState(false);

  // Delete confirmation
  const [deleteId, setDeleteId] = useState<number | null>(null);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const res = await announcementsApi.listAll();
      setItems(res.data);
    } catch {
      setError("Failed to load announcements.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!newTekst.trim()) return;
    setCreating(true);
    setCreateError(null);
    try {
      const res = await announcementsApi.create({
        naslov: newNaslov.trim() || undefined,
        tekst: newTekst.trim(),
      });
      setItems((prev) => [res.data, ...prev]);
      setNewNaslov("");
      setNewTekst("");
    } catch {
      setCreateError("Failed to create announcement.");
    } finally {
      setCreating(false);
    }
  }

  async function handleToggle(item: Announcement) {
    try {
      const res = await announcementsApi.update(item.id, { aktivna: !item.aktivna });
      setItems((prev) => prev.map((i) => (i.id === item.id ? res.data : i)));
    } catch {
      // silent
    }
  }

  function startEdit(item: Announcement) {
    setEditId(item.id);
    setEditNaslov(item.naslov ?? "");
    setEditTekst(item.tekst);
  }

  function cancelEdit() {
    setEditId(null);
    setEditNaslov("");
    setEditTekst("");
  }

  async function handleSave(id: number) {
    if (!editTekst.trim()) return;
    setSaving(true);
    try {
      const res = await announcementsApi.update(id, {
        naslov: editNaslov.trim() || undefined,
        tekst: editTekst.trim(),
      });
      setItems((prev) => prev.map((i) => (i.id === id ? res.data : i)));
      cancelEdit();
    } catch {
      // keep edit open on failure
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: number) {
    try {
      await announcementsApi.remove(id);
      setItems((prev) => prev.filter((i) => i.id !== id));
      setDeleteId(null);
    } catch {
      // silent
    }
  }

  function formatDate(iso: string) {
    return new Date(iso).toLocaleDateString("en-US", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  }

  return (
    <div className="space-y-5 max-w-3xl">
      {/* ── Header ── */}
      <div className="flex items-center justify-between">
        <h2 className="section-title">Announcements</h2>
        <span className="text-xs" style={{ color: "rgba(197,160,89,0.7)" }}>
          {items.length} total · {items.filter((i) => i.aktivna).length} active
        </span>
      </div>

      {/* ── Create form ── */}
      <div className="card p-5">
        <p className="text-xs font-semibold tracking-widest uppercase mb-4" style={{ color: "#8a6d1f" }}>
          New Announcement
        </p>
        <form onSubmit={handleCreate} className="space-y-3">
          <input
            className="input-field w-full"
            placeholder="Title (optional)"
            value={newNaslov}
            onChange={(e) => setNewNaslov(e.target.value)}
          />
          <textarea
            className="input-field w-full resize-none"
            rows={3}
            placeholder="Message text…"
            value={newTekst}
            onChange={(e) => setNewTekst(e.target.value)}
            required
          />
          {createError && (
            <p className="text-xs text-red-600">{createError}</p>
          )}
          <div className="flex justify-end">
            <button
              type="submit"
              className="gold-btn px-5 py-2 text-xs"
              disabled={creating || !newTekst.trim()}
            >
              {creating ? "Creating…" : "Create Announcement"}
            </button>
          </div>
        </form>
      </div>

      {/* ── List ── */}
      <div className="card p-5 space-y-3">
        <p className="text-xs font-semibold tracking-widest uppercase mb-2" style={{ color: "#8a6d1f" }}>
          All Announcements
        </p>

        {loading && (
          <p className="text-sm text-gray-400 py-4 text-center">Loading…</p>
        )}
        {error && (
          <p className="text-sm text-red-600 py-4 text-center">{error}</p>
        )}
        {!loading && !error && items.length === 0 && (
          <p className="text-sm text-gray-400 py-4 text-center">No announcements yet.</p>
        )}

        {items.map((item) => (
          <div
            key={item.id}
            className="rounded-lg p-4 space-y-2"
            style={{
              border: "1px solid rgba(197,160,89,0.2)",
              background: item.aktivna ? "rgba(197,160,89,0.04)" : "rgba(0,0,0,0.02)",
            }}
          >
            {editId === item.id ? (
              /* ── Edit mode ── */
              <div className="space-y-2">
                <input
                  className="input-field w-full"
                  placeholder="Title (optional)"
                  value={editNaslov}
                  onChange={(e) => setEditNaslov(e.target.value)}
                />
                <textarea
                  className="input-field w-full resize-none"
                  rows={3}
                  value={editTekst}
                  onChange={(e) => setEditTekst(e.target.value)}
                  required
                />
                <div className="flex gap-2 justify-end">
                  <button
                    className="outline-btn px-3 py-1.5 text-xs"
                    onClick={cancelEdit}
                    disabled={saving}
                  >
                    Cancel
                  </button>
                  <button
                    className="gold-btn px-4 py-1.5 text-xs"
                    onClick={() => handleSave(item.id)}
                    disabled={saving || !editTekst.trim()}
                  >
                    {saving ? "Saving…" : "Save"}
                  </button>
                </div>
              </div>
            ) : deleteId === item.id ? (
              /* ── Delete confirm ── */
              <div className="space-y-2">
                <p className="text-sm text-charcoal">
                  Delete announcement{item.naslov ? ` "${item.naslov}"` : ""}?
                </p>
                <div className="flex gap-2 justify-end">
                  <button
                    className="outline-btn px-3 py-1.5 text-xs"
                    onClick={() => setDeleteId(null)}
                  >
                    Cancel
                  </button>
                  <button
                    className="px-4 py-1.5 text-xs rounded font-semibold"
                    style={{ background: "#dc2626", color: "#fff", border: "none", cursor: "pointer" }}
                    onClick={() => handleDelete(item.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ) : (
              /* ── View mode ── */
              <>
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    {item.naslov && (
                      <p className="font-cinzel text-xs font-semibold tracking-widest uppercase mb-1" style={{ color: "#8a6d1f" }}>
                        {item.naslov}
                      </p>
                    )}
                    <p className="text-sm leading-relaxed text-charcoal">{item.tekst}</p>
                  </div>
                  <div className="flex-shrink-0 flex items-center gap-2">
                    <StatusBadge s={item.aktivna ? "Aktivna" : "Neaktivna"} />
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <span className="text-xs" style={{ color: "rgba(197,160,89,0.6)" }}>
                    {formatDate(item.datum_kreiranja)}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      className="outline-btn px-3 py-1 text-xs"
                      onClick={() => handleToggle(item)}
                      title={item.aktivna ? "Deactivate" : "Activate"}
                    >
                      {item.aktivna ? "Deactivate" : "Activate"}
                    </button>
                    <button
                      className="outline-btn px-2 py-1"
                      onClick={() => startEdit(item)}
                      title="Edit"
                      style={{ color: "#C5A059" }}
                    >
                      <Ic d={icons.edit} size={13} />
                    </button>
                    <button
                      className="px-2 py-1 rounded"
                      onClick={() => setDeleteId(item.id)}
                      title="Delete"
                      style={{
                        border: "1px solid rgba(220,38,38,0.3)",
                        background: "rgba(220,38,38,0.05)",
                        color: "#dc2626",
                        cursor: "pointer",
                      }}
                    >
                      <Ic d={icons.trash} size={13} />
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
