import { api } from './api';

export const modeAPI = {
  getCurrentMode: () => api.get('/admin/mode'),
  
  setMode: (mode) => api.put('/admin/mode', { mode }),
};
