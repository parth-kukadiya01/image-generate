/**
 * Centralized Axios instance for all API calls.
 * Base URL is read from VITE_API_URL env var with a localhost fallback.
 */
import axios from 'axios';

export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 180_000, // 3 min — enough for Gemini generation
});

// Global response error logger (non-blocking)
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error(
      '[API Error]',
      err.config?.url,
      err.response?.status,
      err.response?.data?.detail ?? err.message,
    );
    return Promise.reject(err);
  },
);

export default apiClient;
