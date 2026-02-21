/**
 * Chat API Client for interacting with the /chat endpoint
 * Handles all chat requests to the backend with automatic JWT token inclusion
 */

import { getAuthToken } from './auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatResponse {
  message: string;
  status: number;
  error?: string;
}

export const chatApi = {
  async sendMessage(message: string): Promise<ChatResponse> {
    try {
      const token = getAuthToken();
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          message: data.detail || `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
          error: data.detail || `HTTP ${response.status}: ${response.statusText}`,
        };
      }

      return {
        message: data.response || data.message || 'No response received',
        status: response.status,
      };
    } catch (error) {
      return {
        message: error instanceof Error ? error.message : 'Network error',
        status: 500,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  },

  // Helper function to create chat message objects
  createMessage(role: 'user' | 'assistant', content: string): ChatMessage {
    return {
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date(),
    };
  },
};