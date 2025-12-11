import apiClient from './client';
import axios from 'axios';
import { Report, SubmitReportData, UpdateReportData, PaginatedResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const reportsAPI = {
  // List reports with optional filters
  list: async (params?: {
    status?: string;
    category?: string;
    page?: number;
  }): Promise<PaginatedResponse<Report>> => {
    const response = await apiClient.get('/reports/', { params });
    return response.data;
  },

  // Get a specific report
  get: async (id: string): Promise<Report> => {
    const response = await apiClient.get(`/reports/${id}/`);
    return response.data;
  },

  // Update a report (status and notes)
  update: async (id: string, data: UpdateReportData): Promise<Report> => {
    const response = await apiClient.put(`/reports/${id}/`, data);
    return response.data;
  },

  // Validate a magic link (public endpoint)
  validateMagicLink: async (token: string): Promise<{
    is_valid: boolean;
    company_name: string;
    message: string;
  }> => {
    const response = await axios.get(`${API_URL}/reports/public/${token}/`);
    return response.data;
  },

  // Submit a report via magic link (public endpoint)
  submitReport: async (token: string, data: SubmitReportData): Promise<{
    message: string;
    report_id: string;
  }> => {
    const response = await axios.post(`${API_URL}/reports/public/${token}/submit/`, data);
    return response.data;
  },
};
