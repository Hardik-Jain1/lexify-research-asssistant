// src/types/index.ts
export interface UserCredentials {
  username_or_email: string;
  password: string;
}

export interface UserRegistrationData {
  username: string;
  email: string;
  password: string;
}

export interface User {
  id: number;
  username: string;
  email?: string;
}

// New Types for Papers:
export interface Paper {
  db_id: number;
  paper_id: string; // This is the arXiv ID
  title: string;
  authors: string[];
  abstract?: string;
  published: string; // Keep as string for simplicity from API
  pdf_url: string;
  individual_summary?: string;
  source?: string;
  is_processed_for_chat: boolean;
  qdrant_collection_name?: string | null;
  
  // Frontend-specific state for UI and polling
  processing_status_message?: string;
  is_polling_status?: boolean;
  is_selected_for_chat?: boolean; // Used for checkbox state in UI
  pollingAttempts?: number;      // New: Tracks polling attempts
  retryInitiated?: boolean;      // New: Tracks if a retry has been triggered
}

export interface PaperSearchResponse {
  consolidated_summary: string;
  token_usage_consolidated?: { // Optional, based on backend response
    input: number | null;
    output: number | null;
  };
  papers: Paper[];
}

export interface PaperStatusResponse {
  paper_id: string;
  db_id: number;
  title: string;
  downloaded_at?: string | null;
  text_extracted_at?: string | null;
  cleaned_text_at?: string | null;
  indexed_at?: string | null;
  qdrant_collection_name?: string | null;
  is_ready_for_chat: boolean;
  processing_status_notes?: string | null; // e.g., "arXiv", "arXiv (Download Failed)"
}

// --- RAG Chat System Types ---

export interface ChatMessage {
  id?: number; // Optional if not always present on client-side creation
  session_id?: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string; // ISO date string
  sources?: Record<string, ChatMessageSource> | null; // Or Source[] if it's an array
  // any other fields your ChatMessage might have
}

export interface ChatSession {
  id: number;
  session_name: string; // Or a generated name like "Chat about Paper A..."
  user_id: number;
  created_at: string;
  updated_at: string;
  // Potentially include associated paper IDs or titles if the API provides them directly
  associated_paper_titles?: string[]; 
}

export interface ChatRequestBody {
  query: string;
  selected_paper_ids: number[]; // db_ids of processed papers
  chat_session_id?: number | null;
}

export interface ChatResponse {
  chat_session_id: number;
  response: string; // The LLM's answer
  sources: Record<string, { title: string; text: string; _chunks?: any[] }>; // Context from papers
  token_usage?: { // Optional, if your backend provides it
    input_tokens?: number;
    output_tokens?: number;
    total_tokens?: number;
  };
  // Any other relevant data from the backend chat response
}

export interface ChatSessionMessagesResponse {
  session_id: number;
  session_name: string;
  associated_paper_titles: string[];
  messages: ChatMessage[];
}

export interface ChatSessionInfo {
  id: number;
  session_name: string | null;
  created_at: string; 
  updated_at: string; 
  paper_ids_in_session: number[]; 
  paper_titles_in_session: string[]; // Added based on updated API
  // Optional summaries if you decide to add them to the API later
  first_user_message_summary?: string | null; 
  last_message_summary?: string | null; 
}

export interface ChatMessageSource { // If not already defined
  title?: string;
  text: string;
  // any other relevant fields for a source
}

export interface FullChatSession { // For /sessions/<id>/messages
  session_id: number;
  session_name: string | null;
  associated_paper_titles: string[]; // From API
  messages: ChatMessage[];
}