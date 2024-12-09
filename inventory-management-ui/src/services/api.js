import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.config.url, response.data);
    return response;
  },
  (error) => {
    console.error('API Error:', error.config?.url, error.response?.data || error.message);
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Set up token if it exists
const token = localStorage.getItem('token');
if (token) {
  api.defaults.headers.common['Authorization'] = `Token ${token}`;
}

export const inventoryApi = {
  // Authentication
  login: (credentials) => api.post('/api/auth/login/', credentials),

  // Item operations
  getItems: () => api.get('/api/items/'),
  getItem: (id) => api.get(`/api/items/${id}/`),
  createItem: (data) => api.post('/api/items/', data),
  updateItem: (id, data) => api.put(`/api/items/${id}/`, data),
  deleteItem: (id) => api.delete(`/api/items/${id}/`),

  // Warehouse operations
  getWarehouses: () => api.get('/api/warehouses/'),
  getWarehouse: (id) => api.get(`/api/warehouses/${id}/`),
  createWarehouse: (data) => api.post('/api/warehouses/', data),
  updateWarehouse: (id, data) => api.put(`/api/warehouses/${id}/`, data),
  deleteWarehouse: (id) => api.delete(`/api/warehouses/${id}/`),

  // SubWarehouse operations
  getSubWarehouses: () => api.get('/api/subwarehouses/'),
  getSubWarehouse: (id) => api.get(`/api/subwarehouses/${id}/`),
  createSubWarehouse: (data) => api.post('/api/subwarehouses/', data),
  updateSubWarehouse: (id, data) => api.put(`/api/subwarehouses/${id}/`, data),
  deleteSubWarehouse: (id) => api.delete(`/api/subwarehouses/${id}/`),

  // Dashboard operations
  getDashboardStats: () => api.get('/api/dashboard/stats/'),
};
