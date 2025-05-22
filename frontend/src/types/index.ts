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