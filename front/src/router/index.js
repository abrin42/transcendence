import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GameView from '../views/GameView.vue'
import CreditsView from '../views/CreditsView.vue'
import LegacyPongView from '../views/LegacyPongView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/game',
      name: 'game',
      component: GameView
    },
    {
      path: '/credits',
      name: 'credits',
      component: CreditsView
    },
    {
      path: '/legacy',
      name: 'legacy',
      component: LegacyPongView
    }
  ]
})

export default router