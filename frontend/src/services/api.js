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
  changePassword: (data) => api.post('/auth/change-password', data),
};

export const dashboardAPI = {
  getSummary: (year = null) => {
    const params = year ? { year } : {};
    return api.get('/dashboard', { params });
  },
  getAvailableYears: () => api.get('/dashboard/available-years'),
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
  getUsers: () => api.get('/settings/users'),
  resetUserPassword: (userId, data) => api.post(`/settings/users/${userId}/reset-password`, data),
  getRoles: () => api.get('/settings/roles'),
  getRoleUsers: (roleId) => api.get(`/settings/roles/${roleId}/users`),
  resetRolePassword: (roleId, data) => api.post(`/settings/roles/${roleId}/reset-password-for-users`, data),
  getCINumberingConfig: () => api.get('/admin/ci-numbering'),
  updateCINumberingConfig: (data) => api.put('/admin/ci-numbering', data),
  getCurrentMode: () => api.get('/admin/mode'),
  setMode: (mode) => api.put('/admin/mode', { mode }),
};

export const auditAPI = {
  getLogs: () => api.get('/audit'),
};

export const reportsAPI = {
  getSummary: () => api.get('/reports/summary'),
};

export default api;
