import apiClient from "./client";

export type Frequency = "hourly" | "daily" | "weekly";

export type DriveFileStatus = "pending" | "importing" | "imported" | "skipped" | "failed";

export interface DriveFileProgress {
  name: string;
  status: DriveFileStatus;
}

export interface DriveSchedule {
  enabled: boolean;
  frequency: Frequency;
  hour: number;
  minute: number;
  day_of_week: number; // Mon=0 … Sun=6
  last_run_at: string | null;
  next_run_at: string | null;
  running: boolean;
  cancelling: boolean;
  last_result: string | null;
  files: DriveFileProgress[];
}

export type DriveScheduleUpdate = Pick<
  DriveSchedule,
  "enabled" | "frequency" | "hour" | "minute" | "day_of_week"
>;

export async function getDriveSchedule(): Promise<DriveSchedule> {
  const { data } = await apiClient.get<DriveSchedule>("/api/v1/schedule/drive");
  return data;
}

export async function updateDriveSchedule(
  body: DriveScheduleUpdate
): Promise<DriveSchedule> {
  const { data } = await apiClient.put<DriveSchedule>("/api/v1/schedule/drive", body);
  return data;
}

export async function cancelDriveImport(): Promise<DriveSchedule> {
  const { data } = await apiClient.post<DriveSchedule>("/api/v1/schedule/drive/cancel");
  return data;
}
