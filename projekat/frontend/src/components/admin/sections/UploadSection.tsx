import { useEffect, useRef, useState } from "react";
import {
  confirmAudioTranscript,
  createManualTranscript,
  importDriveTranscripts,
  listTranscripts,
  transcribeAudioPreview,
  uploadTranscript,
} from "../../../api/transcripts";
import { StageStepper } from "../PipelineStage";
import { cancelDriveImport } from "../../../api/schedule";

// Extract a human-readable message from an Axios/fetch error response
function extractError(e: unknown): string {
  if (e && typeof e === "object" && "response" in e) {
    const resp = (e as { response?: { data?: { detail?: unknown } } }).response;
    const detail = resp?.data?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg as string;
  }
  if (e instanceof Error) return e.message;
  return "An unexpected error occurred. Please try again.";
}

type UploadType = "text" | "audio" | "drive";
type TextTab = "file" | "manual";
type AudioStage = "upload" | "transcribing" | "review" | "saving" | "done";

// ── Validation helpers ───────────────────────────────────────────────

const ALLOWED_TEXT_EXTS = ["txt", "pdf"];
const ALLOWED_AUDIO_EXTS = ["mp3", "wav", "m4a", "ogg"];
const MAX_SIZE = 10 * 1024 * 1024;

function getExt(name: string) {
  return name.split(".").pop()?.toLowerCase() ?? "";
}

function validateTextFile(file: File): string | null {
  const ext = getExt(file.name);
  if (!ALLOWED_TEXT_EXTS.includes(ext)) {
    return "Only .txt and .pdf files are supported";
  }
  if (file.size > MAX_SIZE) return "File exceeds the 10 MB limit";
  return null;
}

function validateAudioFile(file: File): string | null {
  const ext = getExt(file.name);
  if (!ALLOWED_AUDIO_EXTS.includes(ext)) {
    return "Only .mp3, .wav, .m4a and .ogg files are supported";
  }
  if (file.size > MAX_SIZE) return "File exceeds the 10 MB limit";
  return null;
}

interface ManualErrors {
  agent_name?: string;
  date?: string;
  content?: string;
}

function validateTranscriptFormat(content: string): string | null {
  const lines = content.split("\n");
  const hasAgent = lines.some(
    (line) => /^\s*AGENT\s*:/i.test(line) && line.split(":").slice(1).join(":").trim() !== ""
  );
  const hasUser = lines.some(
    (line) => /^\s*(USER|KORISNIK)\s*:/i.test(line) && line.split(":").slice(1).join(":").trim() !== ""
  );
  if (!hasAgent && !hasUser) {
    return "Content must be in format 'AGENT: text' and 'USER: text'";
  }
  if (!hasAgent) {
    return "Content must contain at least one line in format 'AGENT: text'";
  }
  if (!hasUser) {
    return "Content must contain at least one line in format 'USER: text'";
  }
  return null;
}

function validateManual(
  agentName: string,
  date: string,
  content: string
): ManualErrors {
  const errors: ManualErrors = {};
  if (!agentName.trim()) errors.agent_name = "Agent name is required";
  if (!date) errors.date = "Date is required";
  if (!content.trim()) {
    errors.content = "Content is required";
  } else if (content.trim().length < 20) {
    errors.content = "Content must have at least 20 characters";
  } else {
    const formatError = validateTranscriptFormat(content);
    if (formatError) errors.content = formatError;
  }
  return errors;
}

// ── Text file upload sub-panel ───────────────────────────────────────

function TextFileUpload() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState("");
  const [agentName, setAgentName] = useState("");
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">(
    "idle"
  );
  const [message, setMessage] = useState("");

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0] ?? null;
    setFile(f);
    setFileError(f ? validateTextFile(f) ?? "" : "");
    setStatus("idle");
    setMessage("");
  }

  async function handleUpload() {
    if (!file) return;
    const err = validateTextFile(file);
    if (err) { setFileError(err); return; }

    setStatus("loading");
    setMessage("");
    try {
      const res = await uploadTranscript(file);
      setMessage(res.message);
      setStatus("success");
      setFile(null);
      if (inputRef.current) inputRef.current.value = "";
    } catch (e: unknown) {
      setMessage(extractError(e));
      setStatus("error");
    }
  }

  function handleClear() {
    setFile(null);
    setFileError("");
    setAgentName("");
    setDate(new Date().toISOString().split("T")[0]);
    setStatus("idle");
    setMessage("");
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <div className="card p-6 space-y-4">
      <div
        className="upload-zone"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          const f = e.dataTransfer.files[0];
          if (f) {
            setFile(f);
            setFileError(validateTextFile(f) ?? "");
          }
        }}
      >
        <p className="text-sm font-semibold text-charcoal">
          {file ? file.name : "Drag & drop transcript file here"}
        </p>
        <p className="text-xs mt-1" style={{ color: "#6b5a3a" }}>
          Supported: .txt, .pdf — max 10 MB
        </p>
        <button className="gold-btn mt-4" type="button">
          Browse Files
        </button>
        <input
          ref={inputRef}
          type="file"
          accept=".txt,.pdf,text/plain,application/pdf"
          className="hidden"
          onChange={handleFileChange}
        />
      </div>

      {fileError && (
        <p className="text-xs text-red-600">{fileError}</p>
      )}

      <div className="grid grid-cols-2 gap-3">
        <input
          className="input-field"
          placeholder="Agent name (optional)"
          value={agentName}
          onChange={(e) => setAgentName(e.target.value)}
        />
        <input
          className="input-field"
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      <div className="flex gap-2">
        <button
          className="gold-btn"
          onClick={handleUpload}
          disabled={!file || !!fileError || status === "loading"}
        >
          {status === "loading" ? "Uploading…" : "Upload & Process"}
        </button>
        <button className="outline-btn" onClick={handleClear}>
          Clear
        </button>
      </div>

      {status === "success" && (
        <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-2">
          ✓ {message}
        </div>
      )}
      {status === "error" && (
        <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          ✗ {message}
        </div>
      )}
    </div>
  );
}

// ── Manual entry sub-panel ───────────────────────────────────────────

function ManualEntry() {
  const [agentName, setAgentName] = useState("");
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [content, setContent] = useState("");
  const [errors, setErrors] = useState<ManualErrors>({});
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">(
    "idle"
  );
  const [message, setMessage] = useState("");

  async function handleSubmit() {
    const errs = validateManual(agentName, date, content);
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    setStatus("loading");
    setMessage("");
    try {
      const res = await createManualTranscript({
        agent_name: agentName,
        date,
        content,
      });
      setMessage(res.message);
      setStatus("success");
      setAgentName("");
      setContent("");
      setDate(new Date().toISOString().split("T")[0]);
    } catch (e: unknown) {
      setMessage(extractError(e));
      setStatus("error");
    }
  }

  function handleClear() {
    setAgentName("");
    setDate(new Date().toISOString().split("T")[0]);
    setContent("");
    setErrors({});
    setStatus("idle");
    setMessage("");
  }

  return (
    <div className="card p-6 space-y-4">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <input
            className={`input-field ${errors.agent_name ? "error" : ""}`}
            placeholder="Agent name"
            value={agentName}
            onChange={(e) => {
              setAgentName(e.target.value);
              if (errors.agent_name) setErrors({ ...errors, agent_name: undefined });
            }}
          />
          {errors.agent_name && (
            <p className="text-xs text-red-600 mt-1">{errors.agent_name}</p>
          )}
        </div>
        <div>
          <input
            className={`input-field ${errors.date ? "error" : ""}`}
            type="date"
            value={date}
            onChange={(e) => {
              setDate(e.target.value);
              if (errors.date) setErrors({ ...errors, date: undefined });
            }}
          />
          {errors.date && (
            <p className="text-xs text-red-600 mt-1">{errors.date}</p>
          )}
        </div>
      </div>

      <div>
        <textarea
          className={`input-field ${errors.content ? "error" : ""}`}
          rows={10}
          placeholder={"AGENT: Good day, how can I help you?\nUSER: I have an issue with my invoice.\nAGENT: I understand, could you provide your account number?"}
          style={{ resize: "vertical", fontFamily: "monospace", fontSize: 13 }}
          value={content}
          onChange={(e) => {
            setContent(e.target.value);
            if (errors.content) setErrors({ ...errors, content: undefined });
          }}
        />
        {errors.content && (
          <p className="text-xs text-red-600 mt-1">{errors.content}</p>
        )}
        <p className="text-xs text-gray-400 mt-1">
          Format: <code className="bg-gray-100 px-1 rounded">AGENT: text</code> and <code className="bg-gray-100 px-1 rounded">USER: text</code> · {content.trim().length} characters (min. 20)
        </p>
      </div>

      <div className="flex gap-2">
        <button
          className="gold-btn"
          onClick={handleSubmit}
          disabled={status === "loading"}
        >
          {status === "loading" ? "Saving…" : "Save Transcript"}
        </button>
        <button className="outline-btn" onClick={handleClear}>
          Clear
        </button>
      </div>

      {status === "success" && (
        <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-2">
          ✓ {message}
        </div>
      )}
      {status === "error" && (
        <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          ✗ {message}
        </div>
      )}
    </div>
  );
}

// ── Audio upload sub-panel ───────────────────────────────────────────

function AudioUpload() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [stage, setStage] = useState<AudioStage>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState("");
  const [language, setLanguage] = useState("bs");
  const [transcriptText, setTranscriptText] = useState("");
  const [textError, setTextError] = useState("");
  const [qualityWarning, setQualityWarning] = useState<string | null>(null);
  const [filename, setFilename] = useState("");
  const [agentName, setAgentName] = useState("");
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0] ?? null;
    setFile(f);
    setFileError(f ? validateAudioFile(f) ?? "" : "");
    setError("");
  }

  async function handleStartTranscription() {
    if (!file) return;
    const err = validateAudioFile(file);
    if (err) { setFileError(err); return; }

    setStage("transcribing");
    setError("");
    try {
      const res = await transcribeAudioPreview(file, language);
      setTranscriptText(res.text);
      setQualityWarning(res.quality_warning);
      setFilename(res.filename);
      setStage("review");
    } catch (e: unknown) {
      setError(extractError(e));
      setStage("upload");
    }
  }

  async function handleConfirm() {
    if (transcriptText.trim().length < 20) {
      setTextError("Transcript must have at least 20 characters");
      return;
    }
    setStage("saving");
    setError("");
    try {
      const res = await confirmAudioTranscript({
        text: transcriptText,
        agent_name: agentName,
        date,
        filename,
        language,
      });
      setSuccessMessage(res.message);
      setStage("done");
    } catch (e: unknown) {
      setError(extractError(e));
      setStage("review");
    }
  }

  function handleReset() {
    setStage("upload");
    setFile(null);
    setFileError("");
    setTranscriptText("");
    setTextError("");
    setQualityWarning(null);
    setFilename("");
    setAgentName("");
    setDate(new Date().toISOString().split("T")[0]);
    setError("");
    setSuccessMessage("");
    if (inputRef.current) inputRef.current.value = "";
  }

  if (stage === "upload") {
    return (
      <div className="card p-6 space-y-4">
        <div
          className="upload-zone"
          onClick={() => inputRef.current?.click()}
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            const f = e.dataTransfer.files[0];
            if (f) {
              setFile(f);
              setFileError(validateAudioFile(f) ?? "");
              setError("");
            }
          }}
        >
          <p className="text-sm font-semibold text-charcoal">
            {file ? file.name : "Drop audio file here"}
          </p>
          <p className="text-xs mt-1" style={{ color: "#6b5a3a" }}>
            Supported: .mp3, .wav, .m4a, .ogg — max 10 MB
          </p>
          <button className="gold-btn mt-4" type="button">
            Browse Audio Files
          </button>
          <input
            ref={inputRef}
            type="file"
            accept=".mp3,.wav,.m4a,.ogg,audio/*"
            className="hidden"
            onChange={handleFileChange}
          />
        </div>

        {fileError && <p className="text-xs text-red-600">{fileError}</p>}

        <select
          className="input-field"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="bs">Language: Bosnian (BS)</option>
          <option value="en">English (EN)</option>
          <option value="de">German (DE)</option>
        </select>

        <button
          className="gold-btn"
          onClick={handleStartTranscription}
          disabled={!file || !!fileError}
        >
          Start Transcription
        </button>

        {error && (
          <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            ✗ {error}
          </div>
        )}
      </div>
    );
  }

  if (stage === "transcribing") {
    return (
      <div className="card p-6 flex flex-col items-center gap-4 py-12">
        <div
          className="w-10 h-10 rounded-full border-4 border-t-transparent animate-spin"
          style={{ borderColor: "#C5A059", borderTopColor: "transparent" }}
        />
        <p className="text-sm font-semibold text-charcoal">Transcribing audio…</p>
        <p className="text-xs text-gray-400 text-center max-w-xs">
          This may take up to a minute depending on the length of the recording. Please wait.
        </p>
      </div>
    );
  }

  if (stage === "review" || stage === "saving") {
    const isSaving = stage === "saving";
    return (
      <div className="card p-6 space-y-4">
        <div className="flex items-center justify-between">
          <p className="text-sm font-semibold text-charcoal">{filename}</p>
          <span className="badge badge-yellow">Review</span>
        </div>

        {qualityWarning && (
          <div className="text-sm bg-amber-50 border border-amber-200 rounded-lg px-3 py-2" style={{ color: "#92400e" }}>
            ⚠ {qualityWarning}
          </div>
        )}

        <div>
          <p className="text-xs text-gray-400 mb-1">
            Review and correct the transcription before saving. Optionally add{" "}
            <code className="bg-gray-100 px-1 rounded">AGENT:</code> and{" "}
            <code className="bg-gray-100 px-1 rounded">USER:</code> prefixes for speaker labelling.
          </p>
          <textarea
            className={`input-field ${textError ? "error" : ""}`}
            rows={12}
            style={{ resize: "vertical", fontFamily: "monospace", fontSize: 13 }}
            value={transcriptText}
            disabled={isSaving}
            onChange={(e) => {
              setTranscriptText(e.target.value);
              if (textError) setTextError("");
            }}
          />
          {textError && <p className="text-xs text-red-600 mt-1">{textError}</p>}
          <p className="text-xs text-gray-400 mt-1">{transcriptText.trim().length} characters (min. 20)</p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <input
            className="input-field"
            placeholder="Agent name (optional)"
            value={agentName}
            disabled={isSaving}
            onChange={(e) => setAgentName(e.target.value)}
          />
          <input
            className="input-field"
            type="date"
            value={date}
            disabled={isSaving}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="flex gap-2">
          <button
            className="gold-btn"
            onClick={handleConfirm}
            disabled={isSaving}
          >
            {isSaving ? "Saving…" : "Confirm & Save"}
          </button>
          <button
            className="outline-btn"
            onClick={() => setStage("upload")}
            disabled={isSaving}
          >
            ← Back
          </button>
        </div>

        {error && (
          <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            ✗ {error}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="card p-6 space-y-4">
      <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-2">
        ✓ {successMessage}
      </div>
      <button className="outline-btn text-xs" onClick={handleReset}>
        ← Upload Another
      </button>
    </div>
  );
}

// ── Google Drive import sub-panel ────────────────────────────────────

type DriveFile = {
  name: string;
  status: "queued" | "skipped" | "imported" | "failed" | "cancelled";
  stage?: string | null; // live pipeline_stage while status === "queued"
};

// Accept either a bare folder ID or a pasted Drive URL and return the ID.
function extractDriveId(input: string): string {
  const s = input.trim();
  const patterns = [/\/folders\/([a-zA-Z0-9_-]+)/, /\/d\/([a-zA-Z0-9_-]+)/, /[?&]id=([a-zA-Z0-9_-]+)/];
  for (const re of patterns) {
    const m = s.match(re);
    if (m) return m[1];
  }
  return s;
}

const RECENT_DRIVE_KEY = "recent_drive_folder";

function DriveImport() {
  const [folderId, setFolderId] = useState("");
  const [recent, setRecent] = useState<string>(() => {
    try { return localStorage.getItem(RECENT_DRIVE_KEY) ?? ""; } catch { return ""; }
  });
  const [language, setLanguage] = useState("bs");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">(
    "idle"
  );
  const [message, setMessage] = useState("");
  const [files, setFiles] = useState<DriveFile[]>([]);
  // True for the whole active import (Start clicked → all files settled / cancelled),
  // so the Cancel button stays visible the entire time, not just between poll ticks.
  const [importing, setImporting] = useState(false);

  // Keep a live mirror of files so the polling interval reads current state.
  const filesRef = useRef<DriveFile[]>(files);
  useEffect(() => {
    filesRef.current = files;
  }, [files]);

  const pollRef = useRef<number | null>(null);
  const attemptsRef = useRef(0);

  function stopPolling() {
    if (pollRef.current !== null) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }

  // Clear the interval if the component unmounts mid-import.
  useEffect(() => () => stopPolling(), []);

  function startPolling(fid: string) {
    stopPolling();
    attemptsRef.current = 0;
    // Transcripts move Sirovi → Obradjeno (or Odbacen) as the pipeline runs.
    // Match each queued file by name against this folder's transcripts.
    pollRef.current = window.setInterval(async () => {
      attemptsRef.current += 1;
      const current = filesRef.current;
      if (!current.some((f) => f.status === "queued")) {
        stopPolling();
        setImporting(false);
        return;
      }
      try {
        const list = await listTranscripts({ q: fid });
        const byName = new Map(list.map((t) => [t.naziv, t]));
        const next = current.map<DriveFile>((f) => {
          if (f.status !== "queued") return f;
          const t = byName.get(f.name);
          // Wait for the stage to clear (post-embedding) before marking imported, so the
          // final Embedding tick is visible rather than jumping straight to ✓.
          if (t?.status === "Obradjeno" && !t.pipeline_stage) return { ...f, status: "imported" };
          if (t?.status === "Odbacen") return { ...f, status: "failed" };
          return { ...f, stage: t?.pipeline_stage ?? null };
        });
        setFiles(next);
        if (!next.some((f) => f.status === "queued")) {
          stopPolling();
          setImporting(false);
        }
      } catch {
        // transient error — keep trying
      }
      // Give up after ~3 minutes so the interval doesn't run forever.
      if (attemptsRef.current >= 72) {
        stopPolling();
        setImporting(false);
      }
    }, 2500);
  }

  async function handleCancel() {
    // Update the UI immediately so the button reacts instantly; the cancel request
    // is fired afterwards (and not awaited for the UI to settle). Files still in flight
    // on the server may finish — the Transcripts list reflects the true final state.
    stopPolling();
    setImporting(false);
    setFiles((prev) =>
      prev.map((f) => (f.status === "queued" ? { ...f, status: "cancelled" } : f))
    );
    setMessage("Import cancelled. Files that had already started may still finish processing.");
    cancelDriveImport().catch(() => {
      // best-effort: the UI is already cancelled regardless
    });
  }

  async function handleImport() {
    const id = extractDriveId(folderId);
    if (!id) return;
    stopPolling();
    setImporting(true);
    setStatus("loading");
    setMessage("");
    setFiles([]);
    try {
      const res = await importDriveTranscripts(id, language);
      setMessage(res.message);
      setFiles(res.files);
      setStatus("success");
      const used = folderId.trim();
      try { localStorage.setItem(RECENT_DRIVE_KEY, used); } catch { /* ignore */ }
      setRecent(used);
      if (res.files.some((f) => f.status === "queued")) startPolling(id);
      else setImporting(false); // nothing queued (all skipped) — nothing to cancel
    } catch (e: unknown) {
      setMessage(extractError(e));
      setStatus("error");
      setImporting(false);
    }
  }

  return (
    <div className="card p-6 space-y-4">
      <div>
        <p className="text-sm font-semibold text-charcoal">Import from Google Drive</p>
        <p className="text-xs mt-1" style={{ color: "#6b5a3a" }}>
          Share the folder with the service account, then paste its folder URL or ID below.
          Supported files (.mp3, .wav, .m4a, .ogg, .txt, .pdf) are imported and processed.
          Files already imported from this folder are skipped.
        </p>
      </div>

      <input
        className="input-field"
        placeholder="Google Drive folder URL or ID"
        value={folderId}
        onChange={(e) => {
          setFolderId(e.target.value);
          if (status !== "idle") {
            stopPolling();
            setStatus("idle");
            setMessage("");
            setFiles([]);
            setImporting(false);
          }
        }}
      />

      {recent && recent !== folderId.trim() && (
        <div className="flex items-center gap-2 text-xs" style={{ color: "#6b5a3a" }}>
          <span>Recently used:</span>
          <button
            type="button"
            className="truncate text-left"
            style={{
              maxWidth: 320,
              color: "#8a6d1f",
              background: "rgba(197,160,89,0.1)",
              border: "1px solid rgba(197,160,89,0.3)",
              borderRadius: 999,
              padding: "2px 10px",
              cursor: "pointer",
            }}
            title={recent}
            onClick={() => setFolderId(recent)}
          >
            {recent}
          </button>
        </div>
      )}

      <select
        className="input-field"
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
      >
        <option value="bs">Language: Bosnian (BS)</option>
        <option value="en">English (EN)</option>
        <option value="de">German (DE)</option>
        <option value="auto">Auto / Mixed (detect per file)</option>
      </select>

      <div className="flex gap-2">
        <button
          className="gold-btn"
          onClick={handleImport}
          disabled={!folderId.trim() || status === "loading"}
        >
          {status === "loading" ? "Starting…" : "Start Import"}
        </button>
        {importing && (
          <button
            className="outline-btn"
            onClick={handleCancel}
            disabled={status === "loading"}
          >
            Cancel Import
          </button>
        )}
      </div>

      {status === "success" && (
        <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-2">
          ✓ {message}
        </div>
      )}
      {status === "error" && (
        <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          ✗ {message}
        </div>
      )}

      {status === "success" && files.length > 0 && (
        <ul className="divide-y divide-gray-100 border border-gray-100 rounded-lg">
          {files.map((f) => (
            <li
              key={f.name}
              className="flex items-center justify-between px-3 py-2 text-sm"
            >
              <span className="text-charcoal truncate mr-3">{f.name}</span>
              {f.status === "queued" && (
                <StageStepper status="Sirovi" stage={f.stage ?? null} />
              )}
              {f.status === "imported" && (
                <span className="text-xs text-green-700 shrink-0">✓ Imported</span>
              )}
              {f.status === "failed" && (
                <span className="text-xs text-red-600 shrink-0">✗ Failed</span>
              )}
              {f.status === "skipped" && (
                <span className="text-xs text-gray-400 shrink-0">Already imported</span>
              )}
              {f.status === "cancelled" && (
                <span className="text-xs text-gray-400 shrink-0">Cancelled</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// ── Main Upload section ──────────────────────────────────────────────

export default function UploadSection() {
  const [type, setType] = useState<UploadType>("text");
  const [textTab, setTextTab] = useState<TextTab>("file");

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="section-title">Upload</h2>
        <div className="type-toggle">
          <button
            className={type === "text" ? "on" : ""}
            onClick={() => setType("text")}
          >
            📄 Textual
          </button>
          <button
            className={type === "audio" ? "on" : ""}
            onClick={() => setType("audio")}
          >
            🎙️ Audio
          </button>
          <button
            className={type === "drive" ? "on" : ""}
            onClick={() => setType("drive")}
          >
            ☁️ Drive
          </button>
        </div>
      </div>

      <div className="meander" />

      {type === "text" && (
        <div className="space-y-4">
          <div className="flex gap-1 bg-gray-100/80 p-1 rounded-lg w-fit">
            {(
              [
                { id: "file", label: "Upload File" },
                { id: "manual", label: "Manual Entry" },
              ] as const
            ).map((t) => (
              <button
                key={t.id}
                className={`tab-btn ${textTab === t.id ? "active" : ""}`}
                onClick={() => setTextTab(t.id)}
              >
                {t.label}
              </button>
            ))}
          </div>

          {textTab === "file" && <TextFileUpload />}
          {textTab === "manual" && <ManualEntry />}
        </div>
      )}

      {type === "audio" && <AudioUpload />}

      {type === "drive" && <DriveImport />}
    </div>
  );
}
