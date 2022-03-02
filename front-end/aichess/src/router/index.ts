import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import ChessPage from '../views/ChessView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: ChessPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
