<!-- LoginView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50 to-purple-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
    <!-- Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-indigo-300/20 to-purple-300/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-purple-300/20 to-pink-300/20 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-indigo-200/10 to-purple-200/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-md w-full">
      <!-- Main Card -->
      <div class="bg-white/80 backdrop-blur-xl p-8 rounded-2xl shadow-2xl shadow-indigo-500/10 border border-white/20">
        <!-- Header Section -->
        <div class="text-center mb-8">
          <div class="flex justify-center mb-4">
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl blur-lg opacity-30"></div>
              <div class="relative bg-gradient-to-r from-indigo-600 to-purple-600 p-3 rounded-xl">
                <svg class="h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
                </svg>
              </div>
            </div>
          </div>
          <h2 class="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
            Welcome Back
          </h2>
          <p class="mt-2 text-slate-600">Sign in to continue your research journey</p>
        </div>

        <!-- Error Alert -->
        <div v-if="authStore.error" class="mb-6">
          <div class="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start space-x-3">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 10-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd" />
              </svg>
            </div>
            <div>
              <h3 class="text-sm font-medium text-red-800">Authentication Error</h3>
              <p class="mt-1 text-sm text-red-700">{{ authStore.error }}</p>
            </div>
          </div>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email/Username Input -->
          <div class="group">
            <label for="email-address" class="block text-sm font-medium text-slate-700 mb-2">
              Email or Username
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M3 4a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 0h4.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 2H19a2 2 0 012 2v11a2 2 0 01-2 2H5a2 2 0 01-2-2V4z" />
                  <path d="M15 8a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <input
                id="email-address"
                name="email"
                type="text"
                v-model="usernameOrEmail"
                required
                class="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all duration-200 bg-white/50 backdrop-blur-sm"
                placeholder="Enter your email or username"
              />
            </div>
          </div>

          <!-- Password Input -->
          <div class="group">
            <label for="password" class="block text-sm font-medium text-slate-700 mb-2">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
                </svg>
              </div>
              <input
                id="password"
                name="password"
                type="password"
                v-model="password"
                required
                class="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all duration-200 bg-white/50 backdrop-blur-sm"
                placeholder="Enter your password"
              />
            </div>
          </div>

          <!-- Sign In Button -->
          <div>
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="group relative w-full flex justify-center items-center py-3 px-4 border border-transparent text-sm font-semibold rounded-xl text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-indigo-500/25"
            >
              <div v-if="authStore.isLoading" class="absolute left-4">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <span :class="{ 'ml-6': authStore.isLoading }">
                {{ authStore.isLoading ? 'Signing in...' : 'Sign In' }}
              </span>
              <svg v-if="!authStore.isLoading" class="ml-2 -mr-1 h-4 w-4 group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </div>

          <!-- Register Link -->
          <div class="text-center">
            <p class="text-sm text-slate-600">
              Don't have an account?
              <router-link 
                to="/register" 
                class="font-semibold text-indigo-600 hover:text-indigo-500 transition-colors duration-200 ml-1"
              >
                Create one now
              </router-link>
            </p>
          </div>
        </form>

        <!-- Divider -->
        <div class="mt-8 pt-6 border-t border-slate-200">
          <div class="text-center">
            <p class="text-xs text-slate-500">
              Secure authentication powered by advanced encryption
            </p>
          </div>
        </div>
      </div>

      <!-- Footer Badge -->
      <div class="text-center mt-6">
        <div class="inline-flex items-center space-x-2 px-4 py-2 bg-white/60 backdrop-blur-sm rounded-full border border-white/20">
          <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span class="text-xs font-medium text-slate-600">Lexify Research Platform</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'vue-router';

const usernameOrEmail = ref('');
const password = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  try {
    await authStore.login({
      username_or_email: usernameOrEmail.value,
      password: password.value,
    });
  } catch (error) {
    // Error is handled by the store
  }
};
</script>