import apiClient from "./client";

export interface Announcement {
  id: number;
  naslov: string | null;
  tekst: string;
  aktivna: boolean;
  datum_kreiranja: string;
  datum_azuriranja: string | null;
  id_administratora: string;
}

export const announcementsApi = {
  listActive: () =>
    apiClient.get<Announcement[]>("/api/v1/announcements/active"),

  listAll: () =>
    apiClient.get<Announcement[]>("/api/v1/announcements"),

  create: (data: { naslov?: string; tekst: string }) =>
    apiClient.post<Announcement>("/api/v1/announcements", data),

  update: (id: number, data: { naslov?: string; tekst?: string; aktivna?: boolean }) =>
    apiClient.patch<Announcement>(`/api/v1/announcements/${id}`, data),

  remove: (id: number) =>
    apiClient.delete(`/api/v1/announcements/${id}`),
};
