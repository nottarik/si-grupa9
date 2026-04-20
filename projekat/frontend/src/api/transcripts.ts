import apiClient from "./client";
import type { Transcript, TranscriptUploadResponse } from "../types";

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

export async function listTranscripts(): Promise<Transcript[]> {
  const { data } = await apiClient.get<Transcript[]>("/api/v1/transcripts/");
  return data;
}

export async function getTranscript(id: string): Promise<Transcript> {
  const { data } = await apiClient.get<Transcript>(`/api/v1/transcripts/${id}`);
  return data;
}
