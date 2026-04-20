// ── Auth ──────────────────────────────────────────────────────────────
export type UserRole = "admin" | "agent" | "user" | "manager";

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  role: UserRole;
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// ── Chat ──────────────────────────────────────────────────────────────
export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  interactionId?: string;
  confidenceScore?: number;
  isLowConfidence?: boolean;
}

export interface ChatResponse {
  answer: string;
  confidence_score: number;
  is_low_confidence: boolean;
  source_id: string | null;
  interaction_id: string;
}

export interface FeedbackRequest {
  interaction_id: string;
  is_positive?: boolean;
  rating?: number;
  comment?: string;
  is_incorrect?: boolean;
}

// ── Transcripts ───────────────────────────────────────────────────────
export type TranscriptStatus = "pending" | "processing" | "processed" | "failed";
export type TranscriptType = "text" | "audio";

export interface Transcript {
  id: string;
  original_filename: string;
  transcript_type: TranscriptType;
  status: TranscriptStatus;
  celery_task_id: string | null;
}

export interface TranscriptUploadResponse {
  transcript_id: string;
  task_id: string;
  message: string;
}

// ── Knowledge ─────────────────────────────────────────────────────────
export type QAStatus = "pending_approval" | "active" | "rejected" | "archived";

export interface KnowledgeItem {
  id: string;
  question: string;
  answer: string;
  category: string | null;
  status: QAStatus;
}
