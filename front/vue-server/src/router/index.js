import { createRouter, createWebHistory } from 'vue-router'
import LoadingView from '../views/LoadingView.vue'
import StartView from '../views/StartView.vue'
import RecommendView from '../views/RecommendView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'loading',
      component: LoadingView
    },
    {
      path: '/start',
      name: 'start',
      component: StartView
    },
    {
      path: '/recommend',
      name: 'recommend',
      component: RecommendView
    }
  ]
})

export default router