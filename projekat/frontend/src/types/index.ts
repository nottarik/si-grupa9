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
  role: "user" | "assistant" | "agent";
  content: string;
  interactionId?: string;
  confidenceScore?: number;
  isLowConfidence?: boolean;
  sourceTopic?: string;
  agentName?: string;
}

export interface EscalationInfo {
  escalation_id: number;
  status: string;
  queue_position: number;
  trigger_tip: string;
}

export interface ChatResponse {
  answer?: string | null;
  confidence_score: number;
  is_low_confidence: boolean;
  source_id: string | null;
  source_topic?: string | null;
  interaction_id?: number | null;
  session_id: number;
  escalation?: EscalationInfo | null;
  is_agent_chat?: boolean;
  needs_escalation?: boolean;
}

export interface FeedbackRequest {
  interaction_id: number;
  is_positive?: boolean;
  rating?: number;
  comment?: string;
  is_incorrect?: boolean;
}

// ── Transcripts ───────────────────────────────────────────────────────
export type TranscriptStatus = "pending" | "processing" | "processed" | "failed";
export type TranscriptType = "text" | "audio";

export interface Transcript {
  /*id: string;
  original_filename: string;
  transcript_type: TranscriptType;
  status: TranscriptStatus;
  celery_task_id: string | null;
  created_at: string | null;*/
  id: string;
  naziv: string;
  format: string;
  status: string;
  celery_task_id: string | null;
  datum_uploada: string | null;
  transcript_type: TranscriptType;
}

export interface TranscriptDetail extends Transcript {
  processed_text: string | null;
}

export interface TranscriptUploadResponse {
  transcript_id: string;
  task_id: string | null;
  message: string;
}

export interface TranscriptManualCreate {
  date: string;
  content: string;
  agent_name: string;
}

export interface TranscriptManualResponse {
  transcript_id: string;
  message: string;
}

export interface TranscriptUpdate {
  naziv?: string;
  processed_text?: string | null;
}

export interface TranscribePreviewResponse {
  text: string;
  quality_warning: string | null;
  filename: string;
}

export interface AudioTranscriptConfirm {
  text: string;
  agent_name: string;
  date: string;
  filename: string;
  language: string;
}

// ── Agent ─────────────────────────────────────────────────────────────
export interface AgentStats {
  handled_today: number;
  handled_week: number;
  avg_response_seconds: number | null;
}

export interface KbSearchItem {
  id: number;
  pitanje: string;
  odgovor: string;
  id_kategorije: number | null;
  datum_azuriranja: string | null;
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

export interface KnowledgeApprovedItem {
  id: number;
  question: string;
  answer: string;
  category: number | null;
  source_type: "manual" | "transcript";
  datum_kreiranja: string | null;
}

export interface KnowledgeCategory {
  id: number;
  naziv: string;
}

export interface ManualQACreate {
  pitanje: string;
  odgovor: string;
  id_kategorije?: number | null;
}

export interface ManualQAUpdate {
  pitanje: string;
  odgovor: string;
  id_kategorije?: number | null;
}
