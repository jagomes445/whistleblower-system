// User types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  company: string;
  company_name: string;
  role: 'admin' | 'manager';
  is_active: boolean;
  created_at: string;
}

// Company types
export interface Company {
  id: string;
  name: string;
  created_by: string;
  created_by_name: string;
  users_count: number;
  created_at: string;
  updated_at: string;
}

// Magic Link types
export interface MagicLink {
  id: string;
  token: string;
  company: string;
  company_name: string;
  created_by: string;
  created_by_name: string;
  name: string;
  is_active: boolean;
  expires_at: string | null;
  created_at: string;
  is_valid: boolean;
  url: string;
}

export interface CreateMagicLinkData {
  name: string;
  is_active: boolean;
  expires_at: string | null;
}

// Report types
export type ReportCategory = 'harassment' | 'fraud' | 'safety' | 'discrimination' | 'other';
export type ReportStatus = 'new' | 'in_review' | 'investigating' | 'resolved' | 'closed';

export interface Report {
  id: string;
  magic_link: string;
  magic_link_name: string;
  category: ReportCategory;
  category_display: string;
  description: string;
  is_anonymous: boolean;
  reporter_name: string | null;
  reporter_email: string | null;
  status: ReportStatus;
  status_display: string;
  internal_notes: string;
  created_at: string;
  updated_at: string;
}

export interface SubmitReportData {
  category: ReportCategory;
  description: string;
  is_anonymous: boolean;
  reporter_name?: string;
  reporter_email?: string;
}

export interface UpdateReportData {
  status?: ReportStatus;
  internal_notes?: string;
}

// Auth types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  company_name: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

// API response types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  detail?: string;
  [key: string]: any;
}
