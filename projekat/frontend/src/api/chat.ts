import apiClient from "./client";
import type { ChatResponse, FeedbackRequest } from "../types";

export interface RatingsStats {
  average_score: number;
  total_rated: number;
  five_star_pct: number;
  below_three_pct: number;
  distribution: Record<string, number>;
  trend: Array<{ date: string; avg: number }>;
  top_rated: Array<{ question: string; rating: number; date: string }>;
}

export async function sendMessage(question: string): Promise<ChatResponse> {
  const { data } = await apiClient.post<ChatResponse>("/api/v1/chat/", {
    question,
  });
  return data;
}

export async function submitFeedback(payload: FeedbackRequest): Promise<void> {
  await apiClient.post("/api/v1/chat/feedback", payload);
}

export async function getRatingsStats(): Promise<RatingsStats> {
  const { data } = await apiClient.get<RatingsStats>("/api/v1/chat/ratings");
  return data;
}
