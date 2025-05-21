// src/store/authStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
// We will create authService later
// import * as authService from '@/services/authService';
import type { UserCredentials, UserRegistrationData, User } from '@/types'; // We'll define these types
import router from '@/router';

// Placeholder for API service functions - will be replaced by actual service calls
const mockAuthService = {
  login: async (credentials: UserCredentials) => {
    console.log('Mock login with:', credentials);
    if (credentials.username_or_email === 'user' && credentials.password === 'pass') {
      return { access_token: 'mock_jwt_token', user_id: 1, username: 'Test User' };
    }
    throw new Error('Invalid mock credentials');
  },
  register: async (data: UserRegistrationData) => {
    console.log('Mock register with:', data);
    return { msg: 'Mock user created', user_id: 2 };
  },
  logout: async () => {
    console.log('Mock logout');
    return { msg: 'Mock logout successful' };
  }
};

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('authToken'));
  const currentUser = ref<User | null>(JSON.parse(localStorage.getItem('authUser') || 'null'));
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!token.value && !!currentUser.value);

  function setAuthData(newToken: string, userData: User) {
    token.value = newToken;
    currentUser.value = userData;
    localStorage.setItem('authToken', newToken);
    localStorage.setItem('authUser', JSON.stringify(userData));
    error.value = null;
  }

  function clearAuthData() {
    token.value = null;
    currentUser.value = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUser');
    // Also clear Axios default auth header if set by an interceptor
  }

  async function login(credentials: UserCredentials) {
    isLoading.value = true;
    error.value = null;
    try {
      // Replace with actual service call: const response = await authService.login(credentials);
      const response = await mockAuthService.login(credentials);
      setAuthData(response.access_token, { id: response.user_id, username: response.username, email: credentials.username_or_email }); // Assuming email is part of user, adjust as needed
      // Setup Axios default header here or in an interceptor
      // axios.defaults.headers.common['Authorization'] = `Bearer ${response.access_token}`;
      router.push( (router.currentRoute.value.query.redirect as string) || '/');
    } catch (e: any) {
      clearAuthData();
      error.value = e.message || 'Failed to login.';
      throw e; // Re-throw to be caught by component if needed
    } finally {
      isLoading.value = false;
    }
  }

  async function register(data: UserRegistrationData) {
    isLoading.value = true;
    error.value = null;
    try {
      // Replace with actual service call: await authService.register(data);
      await mockAuthService.register(data);
      // Optionally auto-login or redirect to login page
      router.push('/login');
    } catch (e: any) {
      error.value = e.message || 'Failed to register.';
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  async function logout() {
    isLoading.value = true;
    error.value = null;
    try {
      // Replace with actual service call: await authService.logout();
      await mockAuthService.logout(); // Call backend even if it's simple
    } catch (e: any) {
      // Log error, but proceed with client-side logout
      console.error('Logout API call failed:', e);
    } finally {
      clearAuthData();
      // Remove Axios default header
      // delete axios.defaults.headers.common['Authorization'];
      isLoading.value = false;
      router.push('/login');
    }
  }

  function initializeAuth() {
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('authUser');
    if (storedToken && storedUser) {
      token.value = storedToken;
      currentUser.value = JSON.parse(storedUser);
      // Setup Axios default header here too if token exists on load
      // axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    } else {
      clearAuthData(); // Ensure clean state if partial data exists
    }
  }

  // Call initializeAuth when the store is created to load persisted state
  initializeAuth();


  return {
    token,
    currentUser,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    initializeAuth, // expose if needed externally, but called internally too
    setAuthData, // for direct setting if needed (e.g. social login)
    clearAuthData,
  };
});