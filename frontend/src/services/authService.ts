// src/services/authService.ts
import apiClient from './api';
import type { UserCredentials, UserRegistrationData, User } from '@/types';

interface LoginResponse {
  access_token: string;
  user_id: number;
  username: string;
}

interface RegisterResponse {
  msg: string;
  user_id: number;
}

interface LogoutResponse {
  msg: string;
}

export const login = async (credentials: UserCredentials): Promise<LoginResponse> => {
  const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
  return response.data;
};

export const register = async (userData: UserRegistrationData): Promise<RegisterResponse> => {
  const response = await apiClient.post<RegisterResponse>('/auth/register', userData);
  return response.data;
};

export const logout = async (): Promise<LogoutResponse> => {
  // The backend logout endpoint might not return a body,
  // but we expect a success message.
  // If using token blocklisting, this call is important.
  const response = await apiClient.post<LogoutResponse>('/auth/logout');
  return response.data;
};

// Optional: A function to verify token or fetch current user details
// if you create a /api/auth/me endpoint on the backend
export const fetchCurrentUser = async (): Promise<User> => {
  // Assuming you have an endpoint like /api/auth/me or /api/auth/protected
  // that returns user details based on the token.
  // For this example, let's assume /api/auth/protected returns { user_id, username }
  const response = await apiClient.get<{ user_id: number; username: string }>('/auth/protected');
  return { id: response.data.user_id, username: response.data.username };
};