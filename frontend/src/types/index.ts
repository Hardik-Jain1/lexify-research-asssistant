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
  paper_id: string; // ArXiv ID
  title: string;
  authors: string[];
  published: string; // Date string
  pdf_url: string;
  abstract: string | null;
  individual_summary: string | null;
  source: string;
  is_processed_for_chat: boolean;
  qdrant_collection_name: string | null;
  // For frontend state management, we might add more fields like:
  processing_status_message?: string; // e.g., "Downloading...", "Indexing..."
  is_polling_status?: boolean;
  is_selected_for_chat?: boolean;
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
  downloaded_at: string | null;
  text_extracted_at: string | null;
  cleaned_text_at: string | null;
  indexed_at: string | null;
  qdrant_collection_name: string | null;
  is_ready_for_chat: boolean;
  processing_status_notes: string | null;
}