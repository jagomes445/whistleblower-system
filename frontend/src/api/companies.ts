import apiClient from './client';
import { Company } from '../types';

export const companiesAPI = {
  // Get current user's company
  getMyCompany: async (): Promise<Company> => {
    const response = await apiClient.get('/companies/me/');
    return response.data;
  },

  // Update company
  updateCompany: async (data: Partial<Company>): Promise<Company> => {
    const response = await apiClient.put('/companies/me/', data);
    return response.data;
  },
};
