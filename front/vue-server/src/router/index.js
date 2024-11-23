import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'loading-view',
    component: () => import('../views/LoadingView.vue'), // 동적 임포트
    meta: { transition: 'fade' }
  },
  {
    path: '/start',
    name: 'start-view',
    component: () => import('../views/StartView.vue'),
    meta: { transition: 'slide' }
  },
  {
    path: '/recommend',
    name: 'recommend-view',
    component: () => import('../views/RecommendView.vue'),
    meta: { transition: 'zoom' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router