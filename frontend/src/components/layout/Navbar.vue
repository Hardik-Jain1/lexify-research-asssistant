<template>
  <nav class="bg-gray-800 text-white shadow-lg">
    <div class="container mx-auto px-6 py-3">
      <div class="flex items-center justify-between">
        <router-link to="/" class="text-xl font-semibold hover:text-gray-300">
          Lexify: AI Research Assistant
        </router-link>

        <div class="flex items-center space-x-4">
          <router-link v-if="authStore.isAuthenticated" to="/" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
            Research
          </router-link>
           <router-link v-if="authStore.isAuthenticated" to="/chat-history" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
            Chat History
          </router-link>
          <router-link v-if="!authStore.isAuthenticated" to="/login" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
            Login
          </router-link>
          <router-link v-if="!authStore.isAuthenticated" to="/register" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
            Register
          </router-link>
          <span v-if="authStore.isAuthenticated && authStore.currentUser" class="text-sm hidden md:block">Welcome, {{ authStore.currentUser.username }}!</span>
          <button v-if="authStore.isAuthenticated" @click="handleLogout" class="px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-700">
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
// No longer need 'computed' from vue here for these as store provides them
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/authStore';

const router = useRouter();
const authStore = useAuthStore();

const handleLogout = async () => {
  await authStore.logout();
  // Router push is now handled within authStore.logout()
};
</script>