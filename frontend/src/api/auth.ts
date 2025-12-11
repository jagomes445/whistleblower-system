import apiClient from './client';
import { LoginCredentials, RegisterData, AuthTokens, User } from '../types';

export const authAPI = {
  // Register a new user
  register: async (data: RegisterData): Promise<User> => {
    const response = await apiClient.post('/auth/register/', data);
    return response.data;
  },

  // Login
  login: async (credentials: LoginCredentials): Promise<AuthTokens> => {
    const response = await apiClient.post('/auth/login/', credentials);
    return response.data;
  },

  // Logout
  logout: async (refreshToken: string): Promise<void> => {
    await apiClient.post('/auth/logout/', { refresh_token: refreshToken });
  },

  // Get current user profile
  getProfile: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me/');
    return response.data;
  },

  // Update user profile
  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await apiClient.put('/auth/me/', data);
    return response.data;
  },
};
