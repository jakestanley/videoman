import { createRouter, createWebHistory } from 'vue-router'
import VideosView from '@/views/VideosView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: VideosView
    }
  ]
})

export default router
