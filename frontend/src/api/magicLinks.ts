import apiClient from './client';
import { MagicLink, CreateMagicLinkData } from '../types';

export const magicLinksAPI = {
  // List all magic links for the user's company
  list: async (): Promise<MagicLink[]> => {
    const response = await apiClient.get('/magic-links/');
    return response.data;
  },

  // Create a new magic link
  create: async (data: CreateMagicLinkData): Promise<MagicLink> => {
    const response = await apiClient.post('/magic-links/', data);
    return response.data;
  },

  // Get a specific magic link
  get: async (id: string): Promise<MagicLink> => {
    const response = await apiClient.get(`/magic-links/${id}/`);
    return response.data;
  },

  // Update a magic link
  update: async (id: string, data: Partial<CreateMagicLinkData>): Promise<MagicLink> => {
    const response = await apiClient.put(`/magic-links/${id}/`, data);
    return response.data;
  },

  // Delete a magic link
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/magic-links/${id}/`);
  },
};
