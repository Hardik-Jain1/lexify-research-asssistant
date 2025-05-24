<!-- RegisterView.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50 to-indigo-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
    <!-- Background Elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-300/20 to-indigo-300/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -right-40 w-80 h-80 bg-gradient-to-tr from-indigo-300/20 to-pink-300/20 rounded-full blur-3xl"></div>
      <div class="absolute top-1/4 right-1/4 w-64 h-64 bg-gradient-to-r from-purple-200/10 to-indigo-200/10 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-md w-full">
      <!-- Main Card -->
      <div class="bg-white/80 backdrop-blur-xl p-8 rounded-2xl shadow-2xl shadow-purple-500/10 border border-white/20">
        <!-- Header Section -->
        <div class="text-center mb-8">
          <div class="flex justify-center mb-4">
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl blur-lg opacity-30"></div>
              <div class="relative bg-gradient-to-r from-purple-600 to-indigo-600 p-3 rounded-xl">
                <svg class="h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zM3 19.235v-.11a6.375 6.375 0 0112.75 0v.109A12.318 12.318 0 0112 19.5c-2.357 0-4.541-.526-6.5-1.265z" />
                </svg>
              </div>
            </div>
          </div>
          <h2 class="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
            Join Lexify
          </h2>
          <p class="mt-2 text-slate-600">Start your AI-powered research journey today</p>
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
              <h3 class="text-sm font-medium text-red-800">Registration Error</h3>
              <p class="mt-1 text-sm text-red-700">{{ authStore.error }}</p>
            </div>
          </div>
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="handleRegister" class="space-y-5">
          <!-- Username Input -->
          <div class="group">
            <label for="username" class="block text-sm font-medium text-slate-700 mb-2">
              Username
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-slate-400 group-focus-within:text-purple-600 transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 8a3 3 0 100-6 3 3 0 000 6zM3.465 14.493a1.23 1.23 0 00.41 1.412A9.957 9.957 0 0010 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 00-13.074.003z" />
                </svg>
              </div>
              <input
                id="username"
                name="username"
                type="text"
                v-model="username"
                required
                class="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-200 bg-white/50 backdrop-blur-sm"
                placeholder="Choose a unique username"
              />
            </div>
          </div>

          <!-- Email Input -->
          <div class="group">
            <label for="email-address" class="block text-sm font-medium text-slate-700 mb-2">
              Email Address
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-slate-400 group-focus-within:text-purple-600 transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M3 4a2 2 0 012-2h10a2 2 0 012 2v1.586l-8 5.707L1 5.586V4z" />
                  <path d="M10 7.414L18 2.586V15a2 2 0 01-2 2H4a2 2 0 01-2-2V2.586l8 4.828z" />
                </svg>
              </div>
              <input
                id="email-address"
                name="email"
                type="email"
                v-model="email"
                required
                class="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-200 bg-white/50 backdrop-blur-sm"
                placeholder="Enter your email address"
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
                <svg class="h-5 w-5 text-slate-400 group-focus-within:text-purple-600 transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
                </svg>
              </div>
              <input
                id="password"
                name="password"
                type="password"
                v-model="password"
                required
                class="block w-full pl-10 pr-3 py-3 border border-slate-300 rounded-xl text-slate-900 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-200 bg-white/50 backdrop-blur-sm"
                placeholder="Create a secure password"
              />
            </div>
          </div>

          <!-- Password Requirements -->
          <div class="bg-slate-50 rounded-lg p-3 border border-slate-200">
            <p class="text-xs text-slate-600 font-medium mb-2">Password Requirements:</p>
            <ul class="text-xs text-slate-500 space-y-1">
              <li class="flex items-center space-x-2">
                <div class="w-1 h-1 bg-slate-400 rounded-full"></div>
                <span>At least 8 characters long</span>
              </li>
              <li class="flex items-center space-x-2">
                <div class="w-1 h-1 bg-slate-400 rounded-full"></div>
                <span>Include numbers and special characters</span>
              </li>
            </ul>
          </div>

          <!-- Register Button -->
          <div>
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="group relative w-full flex justify-center items-center py-3 px-4 border border-transparent text-sm font-semibold rounded-xl text-white bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-purple-500/25"
            >
              <div v-if="authStore.isLoading" class="absolute left-4">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <span :class="{ 'ml-6': authStore.isLoading }">
                {{ authStore.isLoading ? 'Creating Account...' : 'Create Account' }}
              </span>
              <svg v-if="!authStore.isLoading" class="ml-2 -mr-1 h-4 w-4 group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </div>

          <!-- Login Link -->
          <div class="text-center">
            <p class="text-sm text-slate-600">
              Already have an account?
              <router-link 
                to="/login" 
                class="font-semibold text-purple-600 hover:text-purple-500 transition-colors duration-200 ml-1"
              >
                Sign in here
              </router-link>
            </p>
          </div>
        </form>

        <!-- Terms Notice -->
        <div class="mt-6 pt-6 border-t border-slate-200">
          <p class="text-xs text-slate-500 text-center leading-relaxed">
            By creating an account, you agree to our 
            <a href="#" class="text-purple-600 hover:text-purple-500 font-medium">Terms of Service</a> 
            and 
            <a href="#" class="text-purple-600 hover:text-purple-500 font-medium">Privacy Policy</a>
          </p>
        </div>
      </div>

      <!-- Features Preview -->
      <div class="mt-8 grid grid-cols-2 gap-4">
        <div class="bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-white/20 text-center">
          <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-indigo-500 rounded-lg flex items-center justify-center mx-auto mb-2">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <p class="text-xs font-medium text-slate-700">AI-Powered</p>
          <p class="text-xs text-slate-500">Smart Research</p>
        </div>
        <div class="bg-white/60 backdrop-blur-sm rounded-xl p-4 border border-white/20 text-center">
          <div class="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center mx-auto mb-2">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-xs font-medium text-slate-700">Secure</p>
          <p class="text-xs text-slate-500">Data Protection</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/store/authStore';

const username = ref('');
const email = ref('');
const password = ref('');
const authStore = useAuthStore();

const handleRegister = async () => {
  authStore.error = null;
  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value,
    });
  } catch (error) {
    // Error is handled by the store
  }
};
</script>