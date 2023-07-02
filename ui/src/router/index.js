import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import { useUserStore } from '@/stores/user.store';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

// Navigation guard to protect routes
/* router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isLoggedIn = userStore.access !== '';

  if (to.name !== 'Login' && !isLoggedIn) {
    // Redirect to login if not logged in
    next({ name: 'Login' });
  } else {
    // Allow access to the route
    next();
  }
}); */

export default router
