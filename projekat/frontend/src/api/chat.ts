import apiClient from "./client";
import type { ChatResponse, FeedbackRequest } from "../types";

export async function sendMessage(question: string): Promise<ChatResponse> {
  const { data } = await apiClient.post<ChatResponse>("/api/v1/chat/", {
    question,
  });
  return data;
}

export async function submitFeedback(payload: FeedbackRequest): Promise<void> {
  await apiClient.post("/api/v1/chat/feedback", payload);
}
