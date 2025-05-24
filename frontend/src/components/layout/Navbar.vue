<!-- Navbar.vue -->
<template>
  <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md shadow-sm border-b border-slate-200/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16">
      <div class="flex items-center justify-between h-full">
        <!-- Logo Section -->
        <div class="flex items-center">
          <RouterLink to="/" class="group flex-shrink-0 flex items-center space-x-3">
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg blur-sm opacity-20 group-hover:opacity-40 transition-opacity duration-300"></div>
              <div class="relative bg-gradient-to-r from-indigo-600 to-purple-600 p-2 rounded-lg">
                <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
                </svg>
              </div>
            </div>
            <div class="flex flex-col">
              <span class="font-bold text-xl bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent group-hover:from-indigo-600 group-hover:to-purple-600 transition-all duration-300">
                Lexify
              </span>
              <span class="text-xs text-slate-500 font-medium -mt-1">AI Research Assistant</span>
            </div>
          </RouterLink>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center space-x-2">
          <template v-if="authStore.isAuthenticated">
            <!-- User Welcome -->
            <div v-if="authStore.currentUser" class="flex items-center space-x-3 px-4 py-2 rounded-full bg-gradient-to-r from-slate-50 to-indigo-50 border border-slate-200">
              <div class="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center">
                <span class="text-white text-sm font-semibold">{{ authStore.currentUser.username.charAt(0).toUpperCase() }}</span>
              </div>
              <span class="text-sm font-medium text-slate-700">{{ authStore.currentUser.username }}</span>
            </div>
            
            <!-- Navigation Links -->
            <div class="flex items-center space-x-1 ml-4">
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
                  class="relative px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 group"
                  :class="[
                    isActive 
                      ? 'text-white bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg shadow-indigo-200' 
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  ]"
                >
                  <span class="relative z-10">{{ item.name }}</span>
                  <div v-if="!isActive" class="absolute inset-0 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 opacity-0 group-hover:opacity-10 transition-opacity duration-200"></div>
                </a>
              </RouterLink>
            </div>
            
            <!-- Logout Button -->
            <button 
              @click="handleLogout" 
              class="ml-4 px-4 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-red-600 hover:bg-red-50 transition-all duration-200 border border-slate-200 hover:border-red-200"
            >
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </template>
          
          <template v-else>
            <div class="flex items-center space-x-2">
              <RouterLink 
                v-for="(item, index) in unauthenticatedNavigation" 
                :key="item.name" 
                :to="item.href"
                custom
                v-slot="{ href, navigate, isActive }"
              >
                <a 
                  :href="href" 
                  @click="navigate"
                  class="px-6 py-2.5 rounded-lg text-sm font-medium transition-all duration-200"
                  :class="[
                    index === 1 
                      ? 'text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-200 hover:shadow-indigo-300' 
                      : 'text-slate-600 hover:text-slate-900 border border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  ]"
                >
                  {{ item.name }}
                </a>
              </RouterLink>
            </div>
          </template>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen" 
            type="button" 
            class="inline-flex items-center justify-center p-2 rounded-lg text-slate-500 hover:text-slate-700 hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all duration-200" 
            aria-controls="mobile-menu" 
            :aria-expanded="mobileMenuOpen.toString()"
          >
            <span class="sr-only">Open main menu</span>
            <div class="relative w-6 h-6">
              <svg 
                v-if="!mobileMenuOpen" 
                class="absolute inset-0 w-6 h-6 transition-all duration-200 transform" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="2" 
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
              <svg 
                v-else 
                class="absolute inset-0 w-6 h-6 transition-all duration-200 transform" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke-width="2" 
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu with smooth animation -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div v-if="mobileMenuOpen" class="md:hidden absolute top-16 inset-x-0 bg-white/95 backdrop-blur-md border-b border-slate-200/50 shadow-xl" id="mobile-menu">
        <div class="px-4 pt-4 pb-6 space-y-2">
          <template v-if="authStore.isAuthenticated">
            <!-- Mobile User Info -->
            <div v-if="authStore.currentUser" class="flex items-center space-x-3 p-4 rounded-xl bg-gradient-to-r from-slate-50 to-indigo-50 border border-slate-200 mb-4">
              <div class="w-10 h-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center">
                <span class="text-white font-semibold">{{ authStore.currentUser.username.charAt(0).toUpperCase() }}</span>
              </div>
              <div>
                <p class="text-sm font-medium text-slate-900">{{ authStore.currentUser.username }}</p>
                <p class="text-xs text-slate-500">Researcher</p>
              </div>
            </div>
            
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
                class="block px-4 py-3 rounded-xl text-base font-medium transition-all duration-200"
                :class="[
                  isActive 
                    ? 'text-white bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg' 
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                ]"
              >
                {{ item.name }}
              </a>
            </RouterLink>
            
            <button 
              @click="() => { handleLogout(); mobileMenuOpen = false; }" 
              class="w-full text-left block px-4 py-3 rounded-xl text-base font-medium text-slate-700 hover:bg-red-50 hover:text-red-700 transition-all duration-200 border border-slate-200 hover:border-red-200 mt-4"
            >
              <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </template>
          
          <template v-else>
            <RouterLink 
              v-for="(item, index) in unauthenticatedNavigation" 
              :key="item.name" 
              :to="item.href"
              custom
              v-slot="{ href, navigate, isActive }"
            >
              <a 
                :href="href" 
                @click="() => { navigate(); mobileMenuOpen = false; }"
                class="block px-4 py-3 rounded-xl text-base font-medium transition-all duration-200 text-center"
                :class="[
                  index === 1 
                    ? 'text-white bg-gradient-to-r from-indigo-600 to-purple-600 shadow-lg' 
                    : 'text-slate-700 hover:bg-slate-100 hover:text-slate-900 border border-slate-200'
                ]"
              >
                {{ item.name }}
              </a>
            </RouterLink>
          </template>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuthStore } from '@/store/authStore';

const router = useRouter();
const authStore = useAuthStore();
const mobileMenuOpen = ref(false);

const authenticatedNavigation = [
  { name: 'Research', href: '/' },
  { name: 'Chat History', href: '/chat-history' },
];

const unauthenticatedNavigation = [
  { name: 'Login', href: '/login' },
  { name: 'Register', href: '/register' },
];

const handleLogout = async () => {
  await authStore.logout();
  mobileMenuOpen.value = false;
};
</script>