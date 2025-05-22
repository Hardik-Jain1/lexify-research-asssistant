// src/services/api.ts
import axios, { type InternalAxiosRequestConfig, type AxiosResponse } from 'axios';
import { useAuthStore } from '@/store/authStore'; // To get token and handle logout on 401
import router from '@/router'; // To redirect on certain errors

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api', // Your backend API URL
//   timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: To add JWT token to requests
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const authStore = useAuthStore();
    const token = authStore.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: To handle global errors like 401 Unauthorized
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Any status code that lie within the range of 2xx cause this function to trigger
    return response;
  },
  (error) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    const authStore = useAuthStore(); // Access store here, inside the function

    if (error.response) {
      const { status } = error.response;

      if (status === 401) {
        // If 401 Unauthorized (e.g., token expired or invalid)
        // except for login and register pages to avoid redirect loop if token is bad from start
        if (router.currentRoute.value.name !== 'Login' && router.currentRoute.value.name !== 'Register') {
          authStore.logout(); // Perform logout action (clears token, redirects to login)
          // The authStore.logout() already handles redirection to /login
        }
      } else if (status === 403) {
        // Forbidden - user is authenticated but not authorized for the resource
        // You might want to redirect to a 'Forbidden' page or show a notification
        console.error('403 Forbidden:', error.response.data);
        // Example: router.push('/forbidden');
      } else if (status >= 500) {
        // Server error
        console.error('Server Error:', error.response.data);
        // Show a generic server error message to the user
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('Network Error or No Response:', error.request);
      // Show a network error message
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default apiClient;