// src/store/authStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import * as authService from '@/services/authService'; // Import the actual authService
import type { UserCredentials, UserRegistrationData, User } from '@/types';
import router from '@/router';
import apiClient from '@/services/api'; // Import apiClient to set/clear auth headers

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
    // Set Axios default header
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
    error.value = null;
  }

  function clearAuthData() {
    token.value = null;
    currentUser.value = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUser');
    // Remove Axios default header
    delete apiClient.defaults.headers.common['Authorization'];
  }

  async function login(credentials: UserCredentials) {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await authService.login(credentials); // Use actual service
      // Assuming backend returns email if username was used for login, or we fetch it
      // For now, using what backend login endpoint returns
      const userData: User = { id: response.user_id, username: response.username };
      setAuthData(response.access_token, userData);
      
      // Redirect to the intended page or home
      const redirectPath = router.currentRoute.value.query.redirect as string || '/';
      router.push(redirectPath);

    } catch (e: any) {
      clearAuthData(); // Ensure auth data is cleared on login failure
      error.value = e.response?.data?.msg || e.message || 'Failed to login.';
      throw e; 
    } finally {
      isLoading.value = false;
    }
  }

  async function register(data: UserRegistrationData) {
    isLoading.value = true;
    error.value = null;
    try {
      await authService.register(data); // Use actual service
      // After successful registration, you might want to:
      // 1. Show a success message and redirect to login
      // 2. Or automatically log the user in (would require another API call or different backend response)
      router.push({ name: 'Login', query: { registered: 'true' } }); // Example redirect with a query param
    } catch (e: any) {
      error.value = e.response?.data?.msg || e.message || 'Failed to register.';
      throw e;
    } finally {
      isLoading.value = false;
    }
  }

  async function logout() {
    // No need to set isLoading for logout unless the API call is very slow
    // or you want to provide UI feedback during the API call.
    // isLoading.value = true;
    error.value = null;
    try {
      if (token.value) { // Only call backend logout if there's a token
        await authService.logout();
      }
    } catch (e: any) {
      console.error('Logout API call failed (token might already be invalid or server issue):', e);
      // Still proceed with client-side cleanup even if API call fails
    } finally {
      clearAuthData();
      // isLoading.value = false;
      router.push('/login');
    }
  }
  
  // Attempt to rehydrate auth state from localStorage and set Axios header
  function initializeAuth() {
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('authUser');

    if (storedToken && storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        // Basic validation of stored user data
        if (parsedUser && typeof parsedUser.id === 'number' && typeof parsedUser.username === 'string') {
          token.value = storedToken;
          currentUser.value = parsedUser;
          apiClient.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
        } else {
          // Stored user data is invalid, clear everything
          clearAuthData();
        }
      } catch (e) {
        // Error parsing stored user, clear everything
        console.error("Error parsing stored user data:", e);
        clearAuthData();
      }
    } else {
      // No token or user in localStorage, ensure clean state
      clearAuthData();
    }
  }
  
  initializeAuth(); // Initialize on store creation

  return {
    token,
    currentUser,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    initializeAuth,
    setAuthData,
    clearAuthData,
  };
});