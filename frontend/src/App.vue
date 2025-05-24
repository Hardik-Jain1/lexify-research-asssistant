<template>
  <div id="app-container" class="min-h-screen flex flex-col bg-slate-50"> 
    <Navbar />
    <main class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-24"> 
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/layout/Navbar.vue';
import Footer from '@/components/layout/Footer.vue';
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease-in-out; /* Slightly faster transition */
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Ensure main content is scrollable if it overflows, not the whole app-container if navbar is fixed */
main {
  overflow-y: auto; 
}
</style>