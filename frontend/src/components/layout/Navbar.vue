<template>
  <nav class="fixed top-0 left-0 right-0 z-40 bg-white shadow-md border-b border-slate-200 h-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
      <div class="flex items-center justify-between h-full">
        <div class="flex items-center">
          <RouterLink to="/" class="flex-shrink-0 flex items-center space-x-2">
            <svg class="h-8 w-auto text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
            </svg>
            <span class="font-bold text-xl text-slate-800 hover:text-indigo-600 transition-colors">Lexify RA</span>
          </RouterLink>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center space-x-1">
          <template v-if="authStore.isAuthenticated">
            <span v-if="authStore.currentUser" class="px-3 py-2 text-sm font-medium text-slate-700">Welcome, {{ authStore.currentUser.username }}!</span>
            <RouterLink 
              v-for="item in authenticatedNavigation" 
              :key="item.name" 
              :to="item.href"
              custom
              v-slot="{ href, navigate, isActive }"
            >
              <a 
                :href="href" 
                @click="navigate"
                class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="[
                  isActive 
                    ? 'bg-indigo-50 text-indigo-700 font-semibold' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                ]"
              >
                {{ item.name }}
              </a>
            </RouterLink>
            <button @click="handleLogout" class="px-3 py-2 rounded-md text-sm font-medium text-slate-600 hover:bg-red-50 hover:text-red-700 transition-colors">
              Logout
            </button>
          </template>
          <template v-else>
            <RouterLink 
              v-for="item in unauthenticatedNavigation" 
              :key="item.name" 
              :to="item.href"
              custom
              v-slot="{ href, navigate, isActive }"
            >
              <a 
                :href="href" 
                @click="navigate"
                class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
                :class="[
                  isActive 
                    ? 'bg-indigo-50 text-indigo-700 font-semibold' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                ]"
              >
                {{ item.name }}
              </a>
            </RouterLink>
          </template>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button @click="mobileMenuOpen = !mobileMenuOpen" type="button" class="inline-flex items-center justify-center p-2 rounded-md text-slate-500 hover:text-slate-700 hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500" aria-controls="mobile-menu" :aria-expanded="mobileMenuOpen.toString()">
            <span class="sr-only">Open main menu</span>
            <svg v-if="!mobileMenuOpen" class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
            <svg v-else class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu, show/hide based on menu state. -->
    <div v-if="mobileMenuOpen" class="md:hidden absolute top-16 inset-x-0 bg-white border-b border-slate-200 shadow-lg" id="mobile-menu">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        <template v-if="authStore.isAuthenticated">
          <div v-if="authStore.currentUser" class="block px-3 py-2 rounded-md text-base font-medium text-slate-700">Welcome, {{ authStore.currentUser.username }}!</div>
          <RouterLink 
            v-for="item in authenticatedNavigation" 
            :key="item.name" 
            :to="item.href"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a 
              :href="href" 
              @click="() => { navigate(); mobileMenuOpen = false; }"
              class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
              :class="[
                isActive 
                  ? 'bg-indigo-50 text-indigo-700 font-semibold' 
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              ]"
            >
              {{ item.name }}
            </a>
          </RouterLink>
          <button @click="() => { handleLogout(); mobileMenuOpen = false; }" class="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-slate-600 hover:bg-red-50 hover:text-red-700 transition-colors">
            Logout
          </button>
        </template>
        <template v-else>
          <RouterLink 
            v-for="item in unauthenticatedNavigation" 
            :key="item.name" 
            :to="item.href"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a 
              :href="href" 
              @click="() => { navigate(); mobileMenuOpen = false; }"
              class="block px-3 py-2 rounded-md text-base font-medium transition-colors"
              :class="[
                isActive 
                  ? 'bg-indigo-50 text-indigo-700 font-semibold' 
                  : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
              ]"
            >
              {{ item.name }}
            </a>
          </RouterLink>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router'; // Added useRouter
import { useAuthStore } from '@/store/authStore';

const router = useRouter(); // Initialize router
const authStore = useAuthStore();
const mobileMenuOpen = ref(false);

const authenticatedNavigation = [
  { name: 'Research', href: '/' }, // Corrected from '/'
  { name: 'Chat History', href: '/chat-history' }, // Corrected from '/chat-history'
];

const unauthenticatedNavigation = [
  { name: 'Login', href: '/login' },
  { name: 'Register', href: '/register' },
];

const handleLogout = async () => {
  await authStore.logout();
  mobileMenuOpen.value = false; // Close mobile menu on logout
  // Navigation is handled by the watcher in authStore or App.vue
};
</script>