import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'opening-view',
    component: () => import('../views/OpeningView.vue'),
    meta: { transition: 'fade' }
  },
  {
    path: '/measure',
    name: 'measure-view',
    component: () => import('../views/MeasureView.vue'),
    meta: { transition: 'fade' }
  },
  {
    path: '/animation',
    name: 'animation-view',
    component: () => import('../views/AnimationView.vue'),
  },
  {
    path: '/recommend',
    name: 'recommend-view',
    component: () => import('../views/RecommendView.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router