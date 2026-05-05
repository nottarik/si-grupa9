import { useEffect, useState } from "react";
import {
  deleteTranscript,
  getTranscript,
  listTranscripts,
  updateTranscript,
} from "../../../api/transcripts";

import { useAuth } from "../../../hooks/useAuth";
import type { Transcript, TranscriptDetail, TranscriptUpdate } from "../../../types";
import { Ic, StatusBadge, icons } from "../shared";

function validateTranscriptFormat(content: string): string | null {
  const lines = content.split("\n");
  const hasAgent = lines.some(
    (line) => /^\s*AGENT\s*:/i.test(line) && line.split(":").slice(1).join(":").trim() !== ""
  );
  const hasKorisnik = lines.some(
    (line) => /^\s*KORISNIK\s*:/i.test(line) && line.split(":").slice(1).join(":").trim() !== ""
  );
  if (!hasAgent && !hasKorisnik) return "Sadržaj mora biti u formatu 'AGENT: tekst' i 'KORISNIK: tekst'";
  if (!hasAgent) return "Sadržaj mora sadržavati najmanje jednu liniju u formatu 'AGENT: tekst'";
  if (!hasKorisnik) return "Sadržaj mora sadržavati najmanje jednu liniju u formatu 'KORISNIK: tekst'";
  return null;
}

// ── Detail view ──────────────────────────────────────────────────────────────

function DetailView({
  summary,
  onBack,
}: {
  summary: Transcript;
  onBack: () => void;
}) {
  const [detail, setDetail] = useState<TranscriptDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getTranscript(String(summary.id))
      .then(setDetail)
      .catch(() => setError("Greška pri učitavanju sadržaja transkripta."))
      .finally(() => setLoading(false));
  }, [summary.id]);

  const date = summary.datum_uploada
    ? new Date(summary.datum_uploada).toLocaleDateString("bs-BA")
    : "—";

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="section-title">{summary.naziv || "Bez naziva"}</h2>
          <div className="text-xs text-gray-400 mt-1">
            {date} · {summary.format}
          </div>
        </div>
        <div className="flex gap-2 items-center">
          <StatusBadge s={summary.status} />
          <button className="outline-btn text-xs py-1" onClick={onBack}>
            ← Nazad
          </button>
        </div>
      </div>

      <div className="meander" />

      {loading && (
        <div className="card p-8 text-center text-sm text-gray-400">Učitavanje…</div>
      )}
      {error && (
        <div className="card p-5 text-sm" style={{ color: "#ef4444" }}>{error}</div>
      )}
      {!loading && !error && detail && (
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest uppercase mb-3" style={{ color: "rgba(197,160,89,0.9)" }}>
            {detail.processed_text ? "Obrađeni transkript" : "Sirovi sadržaj"}
          </div>
          <div
            className="rounded-lg p-4 text-sm leading-relaxed text-charcoal border whitespace-pre-wrap"
            style={{ minHeight: 200, background: "#f8f5f0", borderColor: "rgba(197,160,89,0.15)" }}
          >
            {detail.processed_text ?? "(Sadržaj još nije dostupan — obrada u toku)"}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Edit view ────────────────────────────────────────────────────────────────

function EditView({
  summary,
  onBack,
  onSaved,
}: {
  summary: Transcript;
  onBack: () => void;
  onSaved: (updated: TranscriptDetail) => void;
}) {
  const [originalDetail, setOriginalDetail] = useState<TranscriptDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(true);
  const [naziv, setNaziv] = useState(summary.naziv || "");
  const [processedText, setProcessedText] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [contentError, setContentError] = useState("");

  useEffect(() => {
    getTranscript(String(summary.id))
      .then((d) => {
        setOriginalDetail(d);
        setNaziv(d.naziv || "");
        setProcessedText(d.processed_text || "");
      })
      .catch(() => setError("Greška pri učitavanju transkripta."))
      .finally(() => setLoadingDetail(false));
  }, [summary.id]);

  const date = summary.datum_uploada
    ? new Date(summary.datum_uploada).toLocaleDateString("bs-BA")
    : "—";
  const isAudio = summary.format === "audio";

  async function handleSave() {
    if (!naziv.trim()) {
      setError("Naziv ne smije biti prazan.");
      return;
    }
    if (!isAudio && processedText.trim()) {
      const formatError = validateTranscriptFormat(processedText);
      if (formatError) {
        setContentError(formatError);
        return;
      }
    }
    setContentError("");
    setSaving(true);
    setError("");
    const payload: TranscriptUpdate = {};
    if (naziv.trim() !== originalDetail?.naziv) payload.naziv = naziv.trim();
    if (processedText !== (originalDetail?.processed_text || ""))
      payload.processed_text = processedText;
    try {
      const updated = await updateTranscript(String(summary.id), payload);
      onSaved(updated);
    } catch {
      setError("Greška pri čuvanju izmjena. Pokušajte ponovo.");
      setSaving(false);
    }
  }

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="section-title">Uredi transkript</h2>
          <div className="text-xs text-gray-400 mt-1">{date} · {summary.format}</div>
        </div>
        <div className="flex gap-2">
          <button className="outline-btn text-xs py-1" onClick={onBack} disabled={saving}>
            ← Odustani
          </button>
          <button
            className="gold-btn text-xs py-1"
            onClick={handleSave}
            disabled={saving || loadingDetail}
          >
            {saving ? "Čuvanje..." : "Sačuvaj izmjene"}
          </button>
        </div>
      </div>

      <div className="meander" />

      {error && (
        <div
          className="text-sm px-4 py-3 rounded-lg"
          style={{
            background: "rgba(239,68,68,0.08)",
            color: "#ef4444",
            border: "1px solid rgba(239,68,68,0.2)",
          }}
        >
          {error}
        </div>
      )}

      {loadingDetail ? (
        <div className="card p-8 text-center text-sm text-gray-400">Učitavanje…</div>
      ) : (
        <div className="card p-5 space-y-5">
          <div>
            <label
              className="block text-xs font-semibold tracking-widest uppercase mb-2"
              style={{ color: "rgba(197,160,89,0.9)" }}
            >
              Naziv
            </label>
            <input
              className="input-field"
              value={naziv}
              onChange={(e) => setNaziv(e.target.value)}
              placeholder="Naziv transkripta"
            />
          </div>

          {isAudio ? (
            <div
              className="rounded-lg px-4 py-3 text-sm"
              style={{
                background: "rgba(197,160,89,0.06)",
                border: "1px solid rgba(197,160,89,0.2)",
                color: "#8a6d1f",
              }}
            >
              Audio transkripti — sadržaj se ne može direktno uređivati.
            </div>
          ) : (
            <div>
              <label
                className="block text-xs font-semibold tracking-widest uppercase mb-2"
                style={{ color: "rgba(197,160,89,0.9)" }}
              >
                Sadržaj
              </label>
              <textarea
                className={`input-field ${contentError ? "error" : ""}`}
                style={{
                  minHeight: 320,
                  resize: "vertical",
                  fontFamily: "monospace",
                  fontSize: 12.5,
                  lineHeight: 1.6,
                }}
                value={processedText}
                onChange={(e) => {
                  setProcessedText(e.target.value);
                  if (contentError) setContentError("");
                }}
                placeholder="Sadržaj transkripta…"
              />
              {contentError && (
                <p className="text-xs text-red-600 mt-1">{contentError}</p>
              )}
              <div className="text-xs text-gray-400 mt-1">
                Format: <code style={{ background: "#f3f4f6", padding: "0 3px", borderRadius: 3 }}>AGENT: tekst</code> i <code style={{ background: "#f3f4f6", padding: "0 3px", borderRadius: 3 }}>KORISNIK: tekst</code> · Izmjene ne pokreću ponovnu obradu.
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Transcript list ──────────────────────────────────────────────────────────

type ViewMode = "list" | "detail" | "edit";

export default function TranscriptList() {
  const { user } = useAuth();
  const isAdmin = user?.role === "admin";

  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [viewMode, setViewMode] = useState<ViewMode>("list");
  const [selected, setSelected] = useState<Transcript | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);

  // Debounce keyword search so we don't fire on every keystroke
  useEffect(() => {
    const t = setTimeout(() => setDebouncedSearch(search), 400);
    return () => clearTimeout(t);
  }, [search]);

  // Re-fetch when any server-side filter changes
  useEffect(() => {
    setLoading(true);
    listTranscripts({
      q: debouncedSearch || undefined,
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined,
    })
      .then(setTranscripts)
      .catch(() => setError("Greška pri učitavanju transkripata."))
      .finally(() => setLoading(false));
  }, [debouncedSearch, dateFrom, dateTo]);

  async function handleDelete(t: Transcript) {
    if (
      !window.confirm(
        `Obrisati transkript "${t.naziv}"?\nOva akcija se ne može poništiti.`
      )
    )
      return;
    setDeleting(String(t.id));
    try {
      await deleteTranscript(String(t.id));
      setTranscripts((prev) => prev.filter((x) => String(x.id) !== String(t.id)));
    } catch {
      setError(`Greška pri brisanju transkripta "${t.naziv}".`);
    } finally {
      setDeleting(null);
    }
  }

  function handleSaved(updated: TranscriptDetail) {
    setTranscripts((prev) =>
      prev.map((t) => (String(t.id) === String(updated.id) ? { ...t, ...updated } : t))
    );
    setViewMode("list");
  }

  // Status is client-side (server already filtered by keyword/date)
  const filtered = transcripts.filter((t) => !statusFilter || t.status === statusFilter);

  if (viewMode === "detail" && selected) {
    return <DetailView summary={selected} onBack={() => setViewMode("list")} />;
  }
  if (viewMode === "edit" && selected) {
    return (
      <EditView
        summary={selected}
        onBack={() => setViewMode("list")}
        onSaved={handleSaved}
      />
    );
  }

  return (
    <div className="space-y-5">
      <h2 className="section-title">Transkripti</h2>

      {error && (
        <div
          className="text-sm px-4 py-3 rounded-lg flex items-center justify-between"
          style={{
            background: "rgba(239,68,68,0.08)",
            color: "#ef4444",
            border: "1px solid rgba(239,68,68,0.2)",
          }}
        >
          <span>{error}</span>
          <button className="text-xs underline ml-3" onClick={() => setError("")}>
            Zatvori
          </button>
        </div>
      )}

      <div className="card overflow-hidden">
        {/* ── Filters ── */}
        <div
          className="p-4 space-y-3"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          {/* Keyword search + status */}
          <div className="flex gap-3 flex-wrap">
            <div className="relative flex-1 min-w-48">
              <input
                className="input-field pr-9"
                placeholder="Pretraži po nazivu, agentu ili ključnim riječima…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                <Ic d={icons.search} size={14} />
              </span>
            </div>
            <select
              className="input-field"
              style={{ width: "auto", minWidth: 150 }}
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">Sve statuse</option>
              <option value="Sirovi">Sirovi</option>
              <option value="Obradjeno">Obradjeno</option>
              <option value="Odbacen">Odbacen</option>
            </select>
          </div>

          {/* Date range */}
          <div className="flex gap-3 flex-wrap items-center">
            <span className="text-xs" style={{ color: "rgba(197,160,89,0.8)" }}>
              Datum od/do:
            </span>
            <input
              type="date"
              className="input-field"
              style={{ width: "auto" }}
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
            />
            <span className="text-xs text-gray-400">—</span>
            <input
              type="date"
              className="input-field"
              style={{ width: "auto" }}
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
            />
            {(dateFrom || dateTo) && (
              <button
                className="outline-btn text-xs py-1"
                onClick={() => { setDateFrom(""); setDateTo(""); }}
              >
                Obriši datume
              </button>
            )}
          </div>
        </div>

        {/* ── Table ── */}
        {loading && (
          <div className="p-8 text-center text-sm text-gray-400">Učitavanje…</div>
        )}
        {!loading && (
          <table className="tbl">
            <thead>
              <tr>
                <th>Naziv</th>
                <th>Datum</th>
                <th>Format</th>
                <th>Status</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center text-gray-400 py-8 text-sm">
                    Nema transkripata koji odgovaraju pretrazi.
                  </td>
                </tr>
              )}
              {filtered.map((t) => (
                <tr key={t.id}>
                  <td className="font-medium text-charcoal">{t.naziv || "—"}</td>
                  <td className="text-gray-400">
                    {t.datum_uploada
                      ? new Date(t.datum_uploada).toLocaleDateString("bs-BA")
                      : "—"}
                  </td>
                  <td className="text-gray-400">{t.format}</td>
                  <td>
                    <StatusBadge s={t.status} />
                  </td>
                  <td>
                    <div className="flex items-center gap-1.5">
                      <button
                        className="outline-btn py-1 text-xs"
                        onClick={() => { setSelected(t); setViewMode("detail"); }}
                      >
                        Pregled
                      </button>
                      <button
                        className="outline-btn py-1 px-2"
                        onClick={() => { setSelected(t); setViewMode("edit"); }}
                        title="Uredi transkript"
                      >
                        <Ic d={icons.edit} size={13} />
                      </button>
                      {isAdmin && (
                        <button
                          onClick={() => handleDelete(t)}
                          disabled={deleting === String(t.id)}
                          title="Obriši transkript"
                          className="p-1.5 rounded transition-colors"
                          style={{
                            color: deleting === String(t.id) ? "#d1d5db" : "#ef4444",
                          }}
                          onMouseEnter={(e) => {
                            if (deleting !== String(t.id))
                              (e.currentTarget as HTMLElement).style.background =
                                "rgba(239,68,68,0.08)";
                          }}
                          onMouseLeave={(e) => {
                            (e.currentTarget as HTMLElement).style.background = "transparent";
                          }}
                        >
                          <Ic d={icons.trash} size={13} />
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
