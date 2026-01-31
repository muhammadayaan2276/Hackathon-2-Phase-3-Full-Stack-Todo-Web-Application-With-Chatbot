/**
 * JWT Token Handling Utility
 * Handles JWT token storage and retrieval using localStorage for client-side
 */

const TOKEN_KEY = 'auth_token';
const USER_ID_KEY = 'user_id';

export const getAuthToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (error) {
    console.error('Error getting auth token:', error);
    return null;
  }
};

export const setAuthToken = (token: string, userId?: string): void => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(TOKEN_KEY, token);
    if (userId) {
      localStorage.setItem(USER_ID_KEY, userId);
    }
  } catch (error) {
    console.error('Error setting auth token:', error);
  }
};

// Alias for compatibility with login/signup pages
export const setJWTToken = setAuthToken;

export const removeAuthToken = (): void => {
  if (typeof window === 'undefined') return;
  try {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_ID_KEY);
  } catch (error) {
    console.error('Error removing auth token:', error);
  }
};

export const getUserId = (): string | null => {
  if (typeof window === 'undefined') return null;
  try {
    return localStorage.getItem(USER_ID_KEY);
  } catch (error) {
    console.error('Error getting user ID:', error);
    return null;
  }
};

// Helper for checking if user is authenticated
export const isAuthenticated = (): boolean => {
  return getAuthToken() !== null;
};