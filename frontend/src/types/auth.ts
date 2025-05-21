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
  email?: string; // Make email optional or ensure it's always available
}