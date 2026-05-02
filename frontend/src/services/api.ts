import axios, { AxiosInstance, AxiosError } from 'axios';
import { toast } from 'react-hot-toast';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        const status = error.response?.status;
        if (status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
          toast.error('Session expired. Please login again.');
        } else if (status === 403) {
          toast.error('Access denied');
        } else if (status && status >= 500) {
          toast.error('Server error. Please try again later.');
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(phone: string, password: string) {
    const response = await this.client.post('/auth/login', { phone, password });
    return response.data;
  }

  async register(data: {
    email: string;
    phone: string;
    password: string;
    full_name: string;
    company_name?: string;
  }) {
    const response = await this.client.post('/auth/register', data);
    return response.data;
  }

  async getCurrentPlanner() {
    const response = await this.client.get('/planners/me');
    return response.data;
  }

  // Event endpoints
  async getEvents(params?: { page?: number; page_size?: number; status?: string }) {
    const response = await this.client.get('/events', { params });
    return response.data;
  }

  async getEvent(eventId: string) {
    const response = await this.client.get(`/events/${eventId}`);
    return response.data;
  }

  async createEvent(data: {
    name: string;
    event_type: string;
    description?: string;
    event_date: string;
    venue: string;
    expected_guests: number;
    budget?: number;
  }) {
    const response = await this.client.post('/events', data);
    return response.data;
  }

  async updateEvent(eventId: string, data: Partial<any>) {
    const response = await this.client.put(`/events/${eventId}`, data);
    return response.data;
  }

  async deleteEvent(eventId: string) {
    const response = await this.client.delete(`/events/${eventId}`);
    return response.data;
  }

  // Guest endpoints
  async getGuests(eventId: string, params?: { page?: number; page_size?: number }) {
    const response = await this.client.get(`/events/${eventId}/guests`, { params });
    return response.data;
  }

  async addGuest(eventId: string, data: any) {
    const response = await this.client.post(`/events/${eventId}/guests`, data);
    return response.data;
  }

  async bulkAddGuests(eventId: string, guests: any[]) {
    const response = await this.client.post(`/events/${eventId}/guests/bulk`, { guests });
    return response.data;
  }

  async updateGuest(guestId: string, data: Partial<any>) {
    const response = await this.client.put(`/guests/${guestId}`, data);
    return response.data;
  }

  async deleteGuest(guestId: string) {
    const response = await this.client.delete(`/guests/${guestId}`);
    return response.data;
  }

  // FAQ endpoints
  async getFAQs(eventId: string) {
    const response = await this.client.get(`/events/${eventId}/faqs`);
    return response.data;
  }

  async addFAQ(eventId: string, data: { question: string; answer: string; category: string }) {
    const response = await this.client.post(`/events/${eventId}/faqs`, data);
    return response.data;
  }

  async updateFAQ(faqId: string, data: Partial<any>) {
    const response = await this.client.put(`/faqs/${faqId}`, data);
    return response.data;
  }

  async deleteFAQ(faqId: string) {
    const response = await this.client.delete(`/faqs/${faqId}`);
    return response.data;
  }

  // Document upload
  async uploadDocument(eventId: string, file: File, type: string, onProgress?: (progress: number) => void) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    const response = await this.client.post(`/events/${eventId}/documents`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    });
    return response.data;
  }

  async getDocuments(eventId: string) {
    const response = await this.client.get(`/events/${eventId}/documents`);
    return response.data;
  }

  async deleteDocument(documentId: string) {
    const response = await this.client.delete(`/documents/${documentId}`);
    return response.data;
  }

  // Analytics
  async getEventStats() {
    const response = await this.client.get('/events/stats');
    return response.data;
  }

  async getEventAnalytics(eventId: string) {
    const response = await this.client.get(`/analytics/events/${eventId}`);
    return response.data;
  }
}

export const api = new ApiService();
export default api;

// Made with Bob
