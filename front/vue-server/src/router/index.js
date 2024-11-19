import { createRouter, createWebHistory } from 'vue-router'
import StartView from '@/views/StartView.vue'
import RecommendView from '@/views/RecommendView.vue'

const routes = [
  {
    path: '/',
    name: 'Start',
    component: StartView
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: RecommendView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
