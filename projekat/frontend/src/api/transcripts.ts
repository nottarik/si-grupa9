import apiClient from "./client";
import type {
  AudioTranscriptConfirm,
  Transcript,
  TranscribePreviewResponse,
  TranscriptDetail,
  TranscriptManualCreate,
  TranscriptManualResponse,
  TranscriptUpdate,
  TranscriptUploadResponse,
} from "../types";

export async function uploadTranscript(
  file: File
): Promise<TranscriptUploadResponse> {
  const form = new FormData();
  form.append("file", file);
  const { data } = await apiClient.post<TranscriptUploadResponse>(
    "/api/v1/transcripts/upload",
    form
  );
  return data;
}

export async function createManualTranscript(
  body: TranscriptManualCreate
): Promise<TranscriptManualResponse> {
  const { data } = await apiClient.post<TranscriptManualResponse>(
    "/api/v1/transcripts/manual",
    body
  );
  return data;
}

export async function listTranscripts(params?: {
  q?: string;
  date_from?: string;
  date_to?: string;
}): Promise<Transcript[]> {
  const { data } = await apiClient.get<Transcript[]>("/api/v1/transcripts/", { params });
  return data;
}

export async function getTranscript(id: string): Promise<TranscriptDetail> {
  const { data } = await apiClient.get<TranscriptDetail>(
    `/api/v1/transcripts/${id}`
  );
  return data;
}

export async function updateTranscript(
  id: string,
  payload: TranscriptUpdate
): Promise<TranscriptDetail> {
  const { data } = await apiClient.patch<TranscriptDetail>(
    `/api/v1/transcripts/${id}`,
    payload
  );
  return data;
}

export async function deleteTranscript(id: string): Promise<void> {
  await apiClient.delete(`/api/v1/transcripts/${id}`);
}

export async function transcribeAudioPreview(
  file: File,
  language: string
): Promise<TranscribePreviewResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("language", language);
  const { data } = await apiClient.post<TranscribePreviewResponse>(
    "/api/v1/transcripts/transcribe-preview",
    form
  );
  return data;
}

export async function confirmAudioTranscript(
  body: AudioTranscriptConfirm
): Promise<TranscriptManualResponse> {
  const { data } = await apiClient.post<TranscriptManualResponse>(
    "/api/v1/transcripts/confirm-audio",
    body
  );
  return data;
}
