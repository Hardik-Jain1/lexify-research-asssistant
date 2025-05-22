import apiClient from './api';
import type { 
  ChatRequestBody, 
  ChatResponse, 
  ChatSession, 
  ChatSessionMessagesResponse 
} from '@/types';

/**
 * Sends a query to the RAG chat system.
 * @param query The user's question.
 * @param selectedPaperDbIds Array of database IDs for the selected papers.
 * @param chatSessionId Optional ID of an existing chat session to continue.
 * @returns The chat response from the backend.
 */
export const getChatResponse = async (
  query: string,
  selectedPaperDbIds: number[],
  chatSessionId?: number | null
): Promise<ChatResponse> => {
  const payload: ChatRequestBody = {
    query,
    selected_paper_ids: selectedPaperDbIds,
  };
  if (chatSessionId) {
    payload.chat_session_id = chatSessionId;
  }
  const response = await apiClient.post<ChatResponse>('/rag/chat', payload);
  return response.data;
};

/**
 * Fetches a list of all past chat sessions for the current user.
 * @returns A promise that resolves to an array of chat sessions.
 */
export const listChatSessions = async (): Promise<ChatSession[]> => {
  const response = await apiClient.get<ChatSession[]>('/rag/sessions');
  return response.data;
};

/**
 * Fetches all messages for a specific past chat session.
 * @param sessionId The ID of the chat session.
 * @returns A promise that resolves to the details and messages of the chat session.
 */
export const getChatSessionMessages = async (sessionId: number): Promise<ChatSessionMessagesResponse> => {
  const response = await apiClient.get<ChatSessionMessagesResponse>(`/rag/sessions/${sessionId}/messages`);
  return response.data;
};