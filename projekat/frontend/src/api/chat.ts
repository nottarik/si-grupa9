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

export interface SessionSummary {
  id: number;
  started_at: string | null;
  status: string;
  message_count: number;
  preview: string | null;
}

export interface SessionMessages {
  session_id: number;
  messages: Array<{
    role: string;
    content: string;
    timestamp: string | null;
    confidence_score?: number;
  }>;
}

export async function sendMessage(
  question: string,
  history: Array<{ role: string; content: string }> = [],
  session_id?: number | null,
): Promise<ChatResponse> {
  const { data } = await apiClient.post<ChatResponse>("/api/v1/chat/ask", {
    question,
    history,
    session_id: session_id ?? null,
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

export async function listSessions(): Promise<SessionSummary[]> {
  const { data } = await apiClient.get<SessionSummary[]>("/api/v1/chat/sessions");
  return data;
}

export async function getSessionMessages(sessionId: number): Promise<SessionMessages> {
  const { data } = await apiClient.get<SessionMessages>(`/api/v1/chat/sessions/${sessionId}/messages`);
  return data;
}
