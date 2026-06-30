import axios from 'axios';

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const extractFromFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/extract', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const extractFromText = async (text) => {
  const formData = new FormData();
  formData.append('text', text);

  const response = await api.post('/extract-text', formData);
  return response.data;
};

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const getRecords = async (limit = 100, offset = 0) => {
  const response = await api.get('/records', {
    params: { limit, offset },
  });
  return response.data;
};

export const getRecord = async (recordId) => {
  const response = await api.get(`/records/${recordId}`);
  return response.data;
};

export const searchRecords = async (query) => {
  const response = await api.get('/search', {
    params: { query },
  });
  return response.data;
};

export const deleteRecord = async (recordId) => {
  const response = await api.delete(`/records/${recordId}`);
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;