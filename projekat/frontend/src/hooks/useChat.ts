import { useState, useCallback } from "react";
import { sendMessage, submitFeedback } from "../api/chat";
import type { ChatMessage, FeedbackRequest } from "../types";

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ask = useCallback(async (question: string) => {
    setError(null);
    // Snapshot history before appending the new user message
    const history = messages
      .slice(-6)
      .map(({ role, content }) => ({ role, content }));

    const userMessage: ChatMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(question, history);
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.answer,
        interactionId: response.interaction_id,
        confidenceScore: response.confidence_score,
        isLowConfidence: response.is_low_confidence,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch {
      setError("Error communicating with the server. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  const sendFeedback = useCallback(async (payload: FeedbackRequest) => {
    await submitFeedback(payload);
  }, []);

  const clearMessages = useCallback(() => setMessages([]), []);

  return { messages, isLoading, error, ask, sendFeedback, clearMessages };
}
