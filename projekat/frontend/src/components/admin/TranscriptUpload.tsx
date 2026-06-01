import { useRef, useState } from "react";
import { uploadTranscript } from "../../api/transcripts";
import { readableError } from "../../api/errors";
import type { TranscriptUploadResponse } from "../../types";

export default function TranscriptUpload() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [status, setStatus] = useState<
    "idle" | "uploading" | "success" | "error"
  >("idle");
  const [result, setResult] = useState<TranscriptUploadResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState("");

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setStatus("uploading");
    setErrorMsg("");
    try {
      const res = await uploadTranscript(file);
      setResult(res);
      setStatus("success");
    } catch (err: unknown) {
      setErrorMsg(readableError(err, "Couldn't upload the file. Please try again."));
      setStatus("error");
    } finally {
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
      <h2 className="font-semibold text-gray-800 mb-3">
        Upload transcript or audio recording
      </h2>
      <p className="text-xs text-gray-500 mb-4">
        Supported formats: <code>.txt</code> (transcript) or{" "}
        <code>.mp3 / .wav / .m4a</code> (audio).
      </p>

      <label className="block">
        <span className="sr-only">Choose file</span>
        <input
          ref={inputRef}
          type="file"
          accept=".txt,.mp3,.wav,.m4a,audio/*,text/plain"
          onChange={handleUpload}
          disabled={status === "uploading"}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-lg file:border-0
            file:text-sm file:font-medium
            file:bg-primary-50 file:text-primary-700
            hover:file:bg-primary-100 cursor-pointer"
        />
      </label>

      {status === "uploading" && (
        <p className="mt-3 text-sm text-primary-600 animate-pulse">
          Uploading...
        </p>
      )}

      {status === "success" && result && (
        <div className="mt-3 text-sm text-green-700 bg-green-50 border border-green-200 rounded-lg px-3 py-2">
          ✓ {result.message} <br />
          <span className="text-xs text-green-600">
            Task ID: {result.task_id}
          </span>
        </div>
      )}

      {status === "error" && (
        <p className="mt-3 text-sm text-red-600">{errorMsg}</p>
      )}
    </div>
  );
}
