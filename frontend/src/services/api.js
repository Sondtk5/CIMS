import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cims_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

export const authAPI = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  getMe: () => api.get('/auth/me'),
};

export const dashboardAPI = {
  getSummary: () => api.get('/dashboard'),
};

export const projectsAPI = {
  getAll: (params) => api.get('/projects', { params }),
  getById: (id) => api.get(`/projects/${id}`),
  create: (data) => api.post('/projects', data),
  update: (id, data) => api.put(`/projects/${id}`, data),
  delete: (id) => api.delete(`/projects/${id}`),
};

export const settingsAPI = {
  getKPITargets: () => api.get('/settings/kpi-targets'),
  updateKPITarget: (kpiKey, data) => api.put(`/settings/kpi-targets/${kpiKey}`, data),
};

export const auditAPI = {
  getLogs: () => api.get('/audit'),
};

export const reportsAPI = {
  getSummary: () => api.get('/reports/summary'),
};

export default api;
