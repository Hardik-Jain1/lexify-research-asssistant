import { createRouter, createWebHistory } from 'vue-router';
// 👇 Only import RouteRecordRaw as a type
import type { RouteRecordRaw } from 'vue-router';// We will create these view components shortly
// import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ResearchView from '../views/ResearchView.vue';
import ChatHistoryView from '../views/ChatHistoryView.vue';
import { useAuthStore } from '@/store/authStore'; // For route guards

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Research',
    component: ResearchView, // We'll create this
    // component: () => import('../views/ResearchView.vue'), // Lazy load
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    // component: () => import('../views/LoginView.vue'), // Lazy load
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    // component: () => import('../views/RegisterView.vue'), // Lazy load
    meta: { guestOnly: true },
  },
  {
    path: '/chat-history',
    name: 'ChatHistory',
    component: ChatHistoryView,
    // component: () => import('../views/ChatHistoryView.vue'), // Lazy load
    meta: { requiresAuth: true },
  },
  // Example of a simple home/landing page if needed, otherwise Research can be home
  // {
  //   path: '/home', // Or keep '/' as Research and add a separate landing if needed
  //   name: 'Home',
  //   component: HomeView,
  // },
  // Fallback route for 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// Navigation Guard (will be implemented properly with Pinia store)
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore(); // Get store instance

  // Ensure store is initialized, especially if using SSR or complex async setup
  // For CSR, initializeAuth() in store should have run.
  // If not directly available: await authStore.initializeAuth(); // if initializeAuth becomes async and public

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'Research' }); // Or your main authenticated route
  } else {
    next();
  }
});

export default router;