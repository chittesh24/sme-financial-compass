/**
 * API Service - Backend Integration
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://sme-financial-compass-api.onrender.com';

// Helper function to get auth token
const getAuthToken = (): string | null => {
  return localStorage.getItem('access_token');
};

// Helper function to make authenticated requests
const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const token = getAuthToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Token expired, redirect to login
    localStorage.removeItem('access_token');
    window.location.href = '/auth';
  }

  return response;
};

// Auth APIs
export const authAPI = {
  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  async signup(email: string, password: string, full_name: string) {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name }),
    });
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  async logout() {
    await fetchWithAuth('/api/auth/logout', { method: 'POST' });
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

// Business APIs
export const businessAPI = {
  async create(businessData: any) {
    const response = await fetchWithAuth('/api/business/', {
      method: 'POST',
      body: JSON.stringify(businessData),
    });
    return response.json();
  },

  async getAll() {
    const response = await fetchWithAuth('/api/business/');
    return response.json();
  },

  async getById(id: string) {
    const response = await fetchWithAuth(`/api/business/${id}`);
    return response.json();
  },

  async update(id: string, data: any) {
    const response = await fetchWithAuth(`/api/business/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
    return response.json();
  },
};

// Upload APIs
export const uploadAPI = {
  async uploadDocument(file: File, businessId?: string) {
    const formData = new FormData();
    formData.append('file', file);
    if (businessId) {
      formData.append('business_id', businessId);
    }

    const token = getAuthToken();
    const response = await fetch(`${API_BASE_URL}/api/upload/document`, {
      method: 'POST',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      body: formData,
    });
    return response.json();
  },

  async getDocuments(businessId?: string) {
    const url = businessId 
      ? `/api/upload/documents?business_id=${businessId}`
      : '/api/upload/documents';
    const response = await fetchWithAuth(url);
    return response.json();
  },

  async deleteDocument(documentId: string) {
    const response = await fetchWithAuth(`/api/upload/documents/${documentId}`, {
      method: 'DELETE',
    });
    return response.json();
  },
};

// Analysis APIs
export const analysisAPI = {
  async analyzeFinancialHealth(businessId: string, periodStart?: string, periodEnd?: string) {
    const response = await fetchWithAuth('/api/analysis/financial-health', {
      method: 'POST',
      body: JSON.stringify({ business_id: businessId, period_start: periodStart, period_end: periodEnd }),
    });
    return response.json();
  },

  async getHistory(businessId: string, limit: number = 10) {
    const response = await fetchWithAuth(`/api/analysis/history/${businessId}?limit=${limit}`);
    return response.json();
  },

  async getRatios(businessId: string) {
    const response = await fetchWithAuth(`/api/analysis/ratios/${businessId}`);
    return response.json();
  },
};

// Forecast APIs
export const forecastAPI = {
  async generate(businessId: string, forecastPeriod: string, forecastType: string = 'revenue') {
    const response = await fetchWithAuth('/api/forecast/generate', {
      method: 'POST',
      body: JSON.stringify({ business_id: businessId, forecast_period: forecastPeriod, forecast_type: forecastType }),
    });
    return response.json();
  },

  async getHistory(businessId: string, limit: number = 10) {
    const response = await fetchWithAuth(`/api/forecast/history/${businessId}?limit=${limit}`);
    return response.json();
  },
};

// Insights APIs
export const insightsAPI = {
  async chat(message: string, businessId?: string) {
    const response = await fetchWithAuth('/api/insights/chat', {
      method: 'POST',
      body: JSON.stringify({ message, business_id: businessId }),
    });
    return response.json();
  },

  async getRecommendations(businessId: string) {
    const response = await fetchWithAuth('/api/insights/recommendations', {
      method: 'POST',
      body: JSON.stringify({ business_id: businessId }),
    });
    return response.json();
  },
};

// Reports APIs
export const reportsAPI = {
  async generate(businessId: string, reportType: string, language: string = 'en', includeCharts: boolean = true) {
    const response = await fetchWithAuth('/api/reports/generate', {
      method: 'POST',
      body: JSON.stringify({ business_id: businessId, report_type: reportType, language, include_charts: includeCharts }),
    });
    return response.json();
  },

  async getReports(businessId: string) {
    const response = await fetchWithAuth(`/api/reports/${businessId}`);
    return response.json();
  },
};

// Banking APIs
export const bankingAPI = {
  async createPlaidLinkToken(businessId: string) {
    const response = await fetchWithAuth('/api/banking/plaid/link-token', {
      method: 'POST',
      body: JSON.stringify({ business_id: businessId }),
    });
    return response.json();
  },

  async exchangePlaidToken(publicToken: string, businessId: string) {
    const response = await fetchWithAuth('/api/banking/plaid/exchange-token', {
      method: 'POST',
      body: JSON.stringify({ public_token: publicToken, business_id: businessId }),
    });
    return response.json();
  },

  async getTransactions(businessId: string, days: number = 30) {
    const response = await fetchWithAuth(`/api/banking/transactions/${businessId}?days=${days}`);
    return response.json();
  },
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.json();
  } catch (error) {
    return { status: 'offline', error };
  }
};

export default {
  auth: authAPI,
  business: businessAPI,
  upload: uploadAPI,
  analysis: analysisAPI,
  forecast: forecastAPI,
  insights: insightsAPI,
  reports: reportsAPI,
  banking: bankingAPI,
  healthCheck,
};
