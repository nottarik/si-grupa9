import type { ChatMessage } from "../../types";

interface Props {
  message: ChatMessage;
  onFeedback?: (interactionId: string, isPositive: boolean) => void;
}

export default function MessageBubble({ message, onFeedback }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 shadow-sm ${
          isUser
            ? "bg-primary-600 text-white rounded-br-sm"
            : "bg-white text-gray-800 rounded-bl-sm border border-gray-100"
        }`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
        </p>

        {/* Low-confidence warning */}
        {!isUser && message.isLowConfidence && (
          <p className="mt-1 text-xs text-amber-600 font-medium">
            ⚠ Nisam siguran u ovaj odgovor. Preporučujem kontakt s agentom.
          </p>
        )}

        {/* Feedback buttons for assistant messages */}
        {!isUser && message.interactionId && onFeedback && (
          <div className="flex gap-2 mt-2">
            <button
              onClick={() => onFeedback(message.interactionId!, true)}
              className="text-xs text-gray-400 hover:text-green-600 transition-colors"
              title="Korisno"
            >
              👍
            </button>
            <button
              onClick={() => onFeedback(message.interactionId!, false)}
              className="text-xs text-gray-400 hover:text-red-500 transition-colors"
              title="Nije korisno"
            >
              👎
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
