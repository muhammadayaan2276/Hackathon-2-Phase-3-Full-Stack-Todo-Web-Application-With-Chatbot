/**
 * API Client with Automatic JWT Attachment
 * Handles all API requests to the backend with automatic JWT token inclusion
 */

import { getAuthToken } from './auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  status: number;
}

export const apiClient = {
  async get<T>(url: string): Promise<ApiResponse<T>> {
    try {
      const token = getAuthToken();
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_URL}${url}`, {
        method: 'GET',
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          data: null,
          error: data.detail || `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
        };
      }

      return {
        data,
        error: null,
        status: response.status,
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Network error',
        status: 500,
      };
    }
  },

  async post<T>(url: string, body: unknown): Promise<ApiResponse<T>> {
    try {
      const token = getAuthToken();
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_URL}${url}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          data: null,
          error: data.detail || `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
        };
      }

      return {
        data,
        error: null,
        status: response.status,
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Network error',
        status: 500,
      };
    }
  },

  async put<T>(url: string, body: unknown): Promise<ApiResponse<T>> {
    try {
      const token = getAuthToken();
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_URL}${url}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          data: null,
          error: data.detail || `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
        };
      }

      return {
        data,
        error: null,
        status: response.status,
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Network error',
        status: 500,
      };
    }
  },

  async delete<T>(url: string): Promise<ApiResponse<T>> {
    try {
      const token = getAuthToken();
      const headers: HeadersInit = {};

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_URL}${url}`, {
        method: 'DELETE',
        headers,
      });

      // Check if response has content
      const contentType = response.headers.get('content-type');
      let data = null;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      }

      if (!response.ok) {
        return {
          data: null,
          error: data?.detail || `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
        };
      }

      return {
        data: data as T,
        error: null,
        status: response.status,
      };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Network error',
        status: 500,
      };
    }
  },
};

interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

// Convenience functions for todo operations
export const todosApi = {
  async getAll() {
    return apiClient.get<Todo[]>('/api/todos');
  },

  async create(title: string, description?: string) {
    return apiClient.post<Todo>(
      '/api/todos',
      { title, description, completed: false }
    );
  },

  async update(id: string, updates: { title?: string; description?: string; completed?: boolean }) {
    return apiClient.put<Todo>(
      `/api/todos/${id}`,
      updates
    );
  },

  async delete(id: string) {
    return apiClient.delete(`/api/todos/${id}`);
  },

  async toggleCompletion(id: string) {
    return apiClient.put<Todo>(
      `/api/todos/${id}/toggle`,
      {}
    );
  },
};