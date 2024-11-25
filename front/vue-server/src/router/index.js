import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'loading-view',
    component: () => import('../views/LoadingView.vue'),
    meta: { transition: 'fade' }
  },
  {
    path: '/start',
    name: 'start-view',
    component: () => import('../views/StartView.vue'),
    meta: { transition: 'fade' }
  },
  {
    path: '/animation',
    name: 'animation-view',
    component: () => import('../views/AnimationView.vue'),
    meta: { transition: 'fade' }
  },
  {
    path: '/recommend',
    name: 'recommend-view',
    component: () => import('../views/RecommendView.vue'),
    meta: { transition: 'fade' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router