import { useState } from "react";

interface Props {
  onSubmit: (rating: number, comment?: string) => void;
  onSkip: () => void;
}

const LABELS = ["", "Poor", "Fair", "Good", "Very good", "Excellent"];

export default function RatingModal({ onSubmit, onSkip }: Props) {
  const [selected, setSelected] = useState(0);
  const [hovered, setHovered] = useState(0);
  const [comment, setComment] = useState("");

  const active = hovered || selected;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-50"
        style={{ background: "rgba(28,28,46,0.45)", backdropFilter: "blur(4px)" }}
      />

      {/* Card */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className="w-full max-w-sm rounded-2xl px-8 py-8 flex flex-col items-center gap-5"
          style={{
            background: "rgba(255,255,255,0.97)",
            boxShadow: "0 16px 56px rgba(0,0,0,0.14)",
            border: "1px solid rgba(197,160,89,0.25)",
          }}
        >
          {/* Coin icon */}
          <div
            className="flex items-center justify-center rounded-full font-cinzel font-bold"
            style={{
              width: 52,
              height: 52,
              fontSize: 22,
              color: "#fff",
              background: "radial-gradient(circle at 38% 35%, #d4aa55, #C5A059, #8a6d1f)",
              boxShadow: "0 4px 16px rgba(197,160,89,0.35)",
            }}
          >
            A
          </div>

          {/* Title */}
          <div className="text-center">
            <h2
              className="font-cinzel font-bold tracking-widest text-charcoal"
              style={{ fontSize: 15, letterSpacing: "0.18em" }}
            >
              RATE YOUR EXPERIENCE
            </h2>
            <p className="text-xs mt-1.5 font-sans" style={{ color: "#9a8a6a" }}>
              How was your conversation with Ambassador?
            </p>
          </div>

          {/* Stars */}
          <div className="flex gap-1">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                onMouseEnter={() => setHovered(star)}
                onMouseLeave={() => setHovered(0)}
                onClick={() => setSelected(star)}
                style={{
                  fontSize: 36,
                  lineHeight: 1,
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  color: star <= active ? "#C5A059" : "#e0d8c8",
                  transition: "color 0.12s, transform 0.1s",
                  transform: star <= active ? "scale(1.12)" : "scale(1)",
                  padding: "0 2px",
                }}
                aria-label={`${star} star${star !== 1 ? "s" : ""}`}
              >
                ★
              </button>
            ))}
          </div>

          {/* Star label */}
          <p
            className="text-xs font-sans -mt-2"
            style={{ color: "#C5A059", minHeight: 16, transition: "opacity 0.15s", opacity: active ? 1 : 0 }}
          >
            {LABELS[active]}
          </p>

          {/* Optional comment */}
          <textarea
            placeholder="Leave a comment (optional)…"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={2}
            style={{
              width: "100%",
              borderRadius: 10,
              border: "1px solid rgba(197,160,89,0.3)",
              padding: "8px 12px",
              fontSize: 13,
              fontFamily: "Inter, sans-serif",
              resize: "none",
              outline: "none",
              color: "#1C1C2E",
              background: "rgba(255,252,245,0.8)",
            }}
          />

          {/* Submit */}
          <button
            onClick={() => selected > 0 && onSubmit(selected, comment.trim() || undefined)}
            disabled={selected === 0}
            className="w-full rounded-full font-cinzel tracking-widest text-xs py-3"
            style={{
              background: selected > 0
                ? "radial-gradient(circle at 38% 35%, #d4aa55, #C5A059, #8a6d1f)"
                : "rgba(197,160,89,0.2)",
              color: selected > 0 ? "#fff" : "rgba(197,160,89,0.5)",
              border: "none",
              cursor: selected > 0 ? "pointer" : "default",
              letterSpacing: "0.15em",
              transition: "all 0.2s",
              boxShadow: selected > 0 ? "0 4px 14px rgba(197,160,89,0.3)" : "none",
            }}
          >
            SUBMIT RATING
          </button>

          {/* Skip */}
          <button
            onClick={onSkip}
            style={{
              background: "none",
              border: "none",
              cursor: "pointer",
              fontSize: 12,
              fontFamily: "Inter, sans-serif",
              color: "rgba(197,160,89,0.6)",
              marginTop: -8,
            }}
          >
            Skip
          </button>
        </div>
      </div>
    </>
  );
}
