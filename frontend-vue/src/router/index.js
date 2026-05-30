import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { guest: true },
    },
    {
      path: '/',
      component: () => import('@/layouts/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'galerias',
          name: 'galerias',
          component: () => import('@/views/GaleriasView.vue'),
        },
        {
          path: 'galerias/:id',
          name: 'galeria-detail',
          component: () => import('@/views/GaleriaDetailView.vue'),
          props: true,
        },
        {
          path: 'obras',
          name: 'obras',
          component: () => import('@/views/ObrasView.vue'),
        },
        {
          path: 'obras/:id',
          name: 'obra-detail',
          component: () => import('@/views/ObraDetailView.vue'),
          props: true,
        },
        {
          path: 'exposicoes',
          name: 'exposicoes',
          component: () => import('@/views/ExposicoesView.vue'),
        },
        {
          path: 'exposicoes/:id',
          name: 'exposicao-detail',
          component: () => import('@/views/ExposicaoDetailView.vue'),
          props: true,
        },
        {
          path: 'perfil',
          name: 'perfil',
          component: () => import('@/views/PerfilView.vue'),
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: () => {
        const auth = useAuthStore()
        return auth.isLoggedIn ? { name: 'home' } : { name: 'login' }
      },
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const guestOnly = to.matched.some((record) => record.meta.guest)

  if (requiresAuth && !auth.isLoggedIn) {
    return {
      name: 'login',
      query: to.fullPath !== '/' ? { redirect: to.fullPath } : undefined,
    }
  }

  if (guestOnly && auth.isLoggedIn) {
    return { name: 'home' }
  }
})

export default router
