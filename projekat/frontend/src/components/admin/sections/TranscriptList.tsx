import { useEffect, useState } from "react";
import { getTranscript, listTranscripts } from "../../../api/transcripts";
import type { Transcript, TranscriptDetail } from "../../../types";
import { Ic, StatusBadge, icons } from "../shared";

// ── Transcript detail view ───────────────────────────────────────────

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
    getTranscript(summary.id)
      .then(setDetail)
      .catch(() => setError("Failed to load transcript content."))
      .finally(() => setLoading(false));
  }, [summary.id]);

  const date = summary.datum_uploada
  ? new Date(summary.datum_uploada).toLocaleDateString()
  : "—";

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="section-title">
            {summary.naziv || "Bez naziva"}
          </h2>
          <div className="text-xs text-gray-400 mt-1">
            {date} · {summary.transcript_type}
          </div>
        </div>
        <div className="flex gap-2 items-center">
          <StatusBadge s={summary.status} />
          <button className="outline-btn text-xs py-1" onClick={onBack}>
            ← Back
          </button>
        </div>
      </div>

      <div className="meander" />

      {loading && (
        <div className="card p-8 text-center text-sm text-gray-400">
          Loading…
        </div>
      )}
      {error && (
        <div className="card p-5 text-sm text-red-600">{error}</div>
      )}
      {!loading && !error && detail && (
        <div className="card p-5">
          <div className="text-xs font-semibold tracking-widest text-gold uppercase mb-3">
            {detail.processed_text ? "Processed Transcript" : "Raw Content"}
          </div>
          <div
            className="rounded-lg p-4 text-sm leading-relaxed text-charcoal border whitespace-pre-wrap"
            style={{
              minHeight: 200,
              background: "#f8f5f0",
              borderColor: "rgba(197,160,89,0.15)",
            }}
          >
            {detail.processed_text ?? "(Content not yet available — processing in progress)"}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Transcript list view ─────────────────────────────────────────────

export default function TranscriptList() {
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [selected, setSelected] = useState<Transcript | null>(null);

  useEffect(() => {
    listTranscripts()
      .then(setTranscripts)
      .catch(() => setError("Failed to load transcripts."))
      .finally(() => setLoading(false));
  }, []);
  
  const getTranscriptName = (t: Transcript) => t.naziv || "Bez naziva";

  if (selected) {
    return <DetailView summary={selected} onBack={() => setSelected(null)} />;
  }

  const filtered = transcripts.filter((t) => {
    const matchSearch =
      !search ||
      getTranscriptName(t).toLowerCase().includes(search.toLowerCase());
    const matchStatus =
      statusFilter === "All" || t.status === statusFilter.toLowerCase();
    return matchSearch && matchStatus;
  });

  return (
    <div className="space-y-5">
      <h2 className="section-title">Transcripts</h2>

      <div className="card overflow-hidden">
        <div
          className="p-4 flex gap-3 flex-wrap"
          style={{ borderBottom: "1px solid rgba(197,160,89,0.2)" }}
        >
          <div className="relative flex-1 min-w-40">
             <input
              className="input-field pr-9"
              placeholder="Search by filename…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
              <Ic d={icons.search} />
            </span>
          </div>
          <select
            className="input-field"
            style={{ width: "auto" }}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option>All</option>
            <option>pending</option>
            <option>processing</option>
            <option>processed</option>
            <option>failed</option>
          </select>
        </div>

        {loading && (
          <div className="p-8 text-center text-sm text-gray-400">Loading…</div>
        )}
        {error && (
          <div className="p-5 text-sm text-red-600">{error}</div>
        )}
        {!loading && !error && (
          <table className="tbl">
            <thead>
              <tr>
                <th>File</th>
                <th>Date</th>
                <th>Type</th>
                <th>Status</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-center text-gray-400 py-8">
                    No transcripts found.
                  </td>
                </tr>
              )}
              {filtered.map((t) => (
                <tr key={t.id}>
                  <td className="font-medium text-charcoal">
                    {getTranscriptName(t)}
                  </td>
                  <td className="text-gray-400">
                    {t.datum_uploada
                      ? new Date(t.datum_uploada).toLocaleDateString()
                      : "—"}
                  </td>
                  <td className="text-gray-400">{t.transcript_type}</td>
                  <td>
                    <StatusBadge s={t.status} />
                  </td>
                  <td>
                    <button
                      className="outline-btn py-1 text-xs"
                      onClick={() => setSelected(t)}
                    >
                      View
                    </button>
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
