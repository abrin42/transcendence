import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ModeSelectView from '../views/ModeSelectView.vue'
import CreditsView from '../views/CreditsView.vue'
import GameSelectView from '../views/GameSelectView.vue'
import LegacyPongView from '../views/LegacyPongView.vue'
import CyberPongView from '../views/CyberPongView.vue'
import ThreePongView from '../views/ThreePongView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import LoginView from '../views/LoginView.vue'
import MatchmakingView from '../views/MatchmakingView.vue'
import MyAccountView from '../views/MyAccountView.vue'
import TourneyModeView from '../views/TourneyModeView.vue'
import SettingsView from '../views/SettingsView.vue'
import LogView from '../views/LogView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import IAPongView from '../views/IAPongView.vue'


const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/modeselect',
      name: 'modeselect',
      component: ModeSelectView
    },
    {
      path: '/credits',
      name: 'credits',
      component: CreditsView
    },
    {
      path: '/gameselect',
      name: 'gameselect',
      component: GameSelectView
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView
    },
    {
      path: '/log',
      name: 'log',
      component: LogView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/tourneymode',
      name: 'tourneymode',
      component: TourneyModeView
    },
    {
      path: '/cyberpong',
      name: 'cyberpong',
      component: CyberPongView
    },
    {
      path: '/legacy',
      name: 'legacy',
      component: LegacyPongView
    },
    {
      path: '/IA',
      name: 'IA',
      component: IAPongView
    }
  ]
})

export default router