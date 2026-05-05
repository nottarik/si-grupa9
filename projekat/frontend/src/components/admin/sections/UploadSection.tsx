import { useRef, useState } from "react";
import {
  createManualTranscript,
  uploadTranscript,
} from "../../../api/transcripts";

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

type UploadType = "text" | "audio";
type TextTab = "file" | "manual";
type AudioStage = "upload" | "preview";

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
  const hasKorisnik = lines.some(
    (line) => /^\s*KORISNIK\s*:/i.test(line) && line.split(":").slice(1).join(":").trim() !== ""
  );
  if (!hasAgent && !hasKorisnik) {
    return "Sadržaj mora biti u formatu 'AGENT: tekst' i 'KORISNIK: tekst'";
  }
  if (!hasAgent) {
    return "Sadržaj mora sadržavati najmanje jednu liniju u formatu 'AGENT: tekst'";
  }
  if (!hasKorisnik) {
    return "Sadržaj mora sadržavati najmanje jednu liniju u formatu 'KORISNIK: tekst'";
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
    errors.content = "Sadržaj je obavezan";
  } else if (content.trim().length < 20) {
    errors.content = "Sadržaj mora imati najmanje 20 znakova";
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
          placeholder={"AGENT: Dobar dan, kako vam mogu pomoći?\nKORISNIK: Imam problem sa fakturom.\nAGENT: Razumijem, možete li mi reći broj računa?"}
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
          Format: <code className="bg-gray-100 px-1 rounded">AGENT: tekst</code> i <code className="bg-gray-100 px-1 rounded">KORISNIK: tekst</code> · {content.trim().length} znakova (min. 20)
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
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">(
    "idle"
  );
  const [message, setMessage] = useState("");

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0] ?? null;
    setFile(f);
    setFileError(f ? validateAudioFile(f) ?? "" : "");
    setStatus("idle");
    setMessage("");
  }

  async function handleTranscribe() {
    if (!file) return;
    const err = validateAudioFile(file);
    if (err) { setFileError(err); return; }

    setStatus("loading");
    try {
      const res = await uploadTranscript(file);
      setMessage(res.message);
      setStatus("success");
      setStage("preview");
    } catch (e: unknown) {
      setMessage(extractError(e));
      setStatus("error");
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-1 bg-gray-100/80 p-1 rounded-lg w-fit">
        {(["upload", "preview"] as const).map((t) => (
          <button
            key={t}
            className={`tab-btn ${stage === t ? "active" : ""}`}
            onClick={() => setStage(t)}
          >
            {t === "preview" ? "Preview & Edit" : "Upload Audio"}
          </button>
        ))}
      </div>

      {stage === "upload" && (
        <div className="card p-6 space-y-4">
          <div
            className="upload-zone"
            onClick={() => inputRef.current?.click()}
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

          <div className="grid grid-cols-2 gap-3">
            <select className="input-field">
              <option>Language: Bosnian (BS)</option>
              <option>English (EN)</option>
              <option>German (DE)</option>
            </select>
            <select className="input-field">
              <option>Model: Standard</option>
              <option>Model: Enhanced</option>
            </select>
          </div>

          <button
            className="gold-btn"
            onClick={handleTranscribe}
            disabled={!file || !!fileError || status === "loading"}
          >
            {status === "loading" ? "Uploading…" : "Start Transcription"}
          </button>

          {status === "error" && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              ✗ {message}
            </div>
          )}
        </div>
      )}

      {stage === "preview" && (
        <div className="card p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="text-sm font-semibold text-charcoal">
              {file?.name ?? "audio file"}
            </div>
            {status === "success" && (
              <span className="badge badge-yellow">Processing</span>
            )}
          </div>

          {status === "success" && (
            <div className="text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-2">
              ✓ {message} Transcription is running in the background.
            </div>
          )}

          <div className="meander" />
          <p className="text-xs text-gray-400">
            The audio is being transcribed asynchronously. Check the Transcripts
            section for the result once processing is complete.
          </p>
          <button
            className="outline-btn text-xs"
            onClick={() => {
              setStage("upload");
              setFile(null);
              setStatus("idle");
              setMessage("");
            }}
          >
            ← Upload Another
          </button>
        </div>
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
    </div>
  );
}
