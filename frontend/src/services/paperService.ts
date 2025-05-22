// src/services/paperService.ts
import apiClient from './api';
import type { Paper, PaperSearchResponse, PaperStatusResponse } from '@/types'; // We'll define these types

export const searchPapers = async (query: string): Promise<PaperSearchResponse> => {
  const response = await apiClient.post<PaperSearchResponse>('/papers/search', { query });
  return response.data;
};

export const getPaperStatus = async (paperDbId: number): Promise<PaperStatusResponse> => {
  const response = await apiClient.get<PaperStatusResponse>(`/papers/${paperDbId}/status`);
  return response.data;
};