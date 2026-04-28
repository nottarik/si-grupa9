import apiClient from "./client";
import type {
  Transcript,
  TranscriptDetail,
  TranscriptManualCreate,
  TranscriptManualResponse,
  TranscriptUploadResponse,
} from "../types";

export async function uploadTranscript(
  file: File
): Promise<TranscriptUploadResponse> {
  const form = new FormData();
  form.append("file", file);
  const { data } = await apiClient.post<TranscriptUploadResponse>(
    "/api/v1/transcripts/upload",
    form,
    { headers: { "Content-Type": "multipart/form-data" } }
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

export async function listTranscripts(): Promise<Transcript[]> {
  const { data } = await apiClient.get<Transcript[]>("/api/v1/transcripts/");
  return data;
}

export async function getTranscript(id: string): Promise<TranscriptDetail> {
  const { data } = await apiClient.get<TranscriptDetail>(
    `/api/v1/transcripts/${id}`
  );
  return data;
}
