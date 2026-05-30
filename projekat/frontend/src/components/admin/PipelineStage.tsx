// Maps a transcript's backend status + pipeline_stage to a compact visual stepper
// showing where it is in the pipeline: Queued → Transcribing → Cleaning → Embedding → Done.

const STEPS = ["U redu", "Transkripcija", "Ciscenje", "Ugradnja"] as const;

const STEP_LABELS: Record<string, string> = {
  "U redu": "Queued",
  Transkripcija: "Transcribing",
  Ciscenje: "Cleaning",
  Ugradnja: "Embedding",
};

export type StageInfo = { index: number; label: string; done: boolean; failed: boolean };

export function deriveStage(status: string, stage: string | null): StageInfo {
  if (status === "Odbacen" || stage === "Greska")
    return { index: -1, label: "Failed", done: false, failed: true };
  // An in-progress sub-stage wins over Obradjeno: status flips to Obradjeno before the
  // final embedding (Ugradnja) runs, and we want that last tick to show.
  if (stage && (STEPS as readonly string[]).includes(stage))
    return { index: STEPS.indexOf(stage as (typeof STEPS)[number]), label: STEP_LABELS[stage], done: false, failed: false };
  if (status === "Obradjeno")
    return { index: STEPS.length, label: "Done", done: true, failed: false };
  return { index: 0, label: STEP_LABELS["U redu"], done: false, failed: false };
}

export function StageStepper({ status, stage }: { status: string; stage: string | null }) {
  const info = deriveStage(status, stage);
  if (info.failed) return <span className="text-xs text-red-600 shrink-0">✗ Failed</span>;
  if (info.done) return <span className="text-xs text-green-700 shrink-0">✓ Done</span>;
  return (
    <div className="flex items-center gap-2 shrink-0">
      <div className="flex gap-1">
        {STEPS.map((s, i) => (
          <span
            key={s}
            className="h-1.5 w-5 rounded-full transition-colors"
            style={{ background: i <= info.index ? "#C5A059" : "rgba(197,160,89,0.2)" }}
          />
        ))}
      </div>
      <span className="text-xs text-gray-500 w-20">{info.label}…</span>
    </div>
  );
}
