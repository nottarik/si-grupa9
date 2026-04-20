import { useState, useRef, useEffect } from "react";
import { useChat } from "../../hooks/useChat";
import MessageBubble from "./MessageBubble";

export default function ChatWindow() {
  const [input, setInput] = useState("");
  const { messages, isLoading, error, ask, sendFeedback } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const q = input.trim();
    if (!q || isLoading) return;
    setInput("");
    await ask(q);
  }

  async function handleFeedback(interactionId: string, isPositive: boolean) {
    await sendFeedback({ interaction_id: interactionId, is_positive: isPositive });
  }

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto w-full px-4 py-6 gap-4">
      {/* Message list */}
      <div className="flex-1 overflow-y-auto pr-1">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 gap-2">
            <span className="text-4xl">💬</span>
            <p className="text-sm">Postavite pitanje za početak razgovora.</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble
            key={i}
            message={msg}
            onFeedback={handleFeedback}
          />
        ))}

        {isLoading && (
          <div className="flex justify-start mb-3">
            <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 shadow-sm">
              <span className="text-gray-400 text-sm animate-pulse">
                Asistent tipka...
              </span>
            </div>
          </div>
        )}

        {error && (
          <p className="text-center text-red-500 text-sm py-2">{error}</p>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input form */}
      <form
        onSubmit={handleSubmit}
        className="flex gap-2 bg-white border border-gray-200 rounded-2xl shadow-sm px-4 py-2"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Unesite pitanje..."
          disabled={isLoading}
          className="flex-1 text-sm outline-none bg-transparent placeholder-gray-400"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="bg-primary-600 hover:bg-primary-700 disabled:opacity-40 text-white text-sm font-medium rounded-xl px-4 py-1.5 transition-colors"
        >
          Pošalji
        </button>
      </form>
    </div>
  );
}
