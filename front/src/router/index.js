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
import RegisterView from '../views/RegisterView.vue'
import SettingsView from '../views/SettingsView.vue'
import TourneyModeView from '../views/TourneyModeView.vue'


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
      path: '/legacy',
      name: 'legacy',
      component: LegacyPongView
    }
    // {
    //   path: '/cyberpong',
    //   name: 'cyberpong',
    //   component: CyberPongView
    // },
    // {
    //   path: '/threepong',
    //   name: 'threepong',
    //   component: ThreePongView
    // },
    // {
    //   path: '/leaderboard',
    //   name: 'leaderboard',
    //   component: LeaderboardView
    // },
    // {
    //    path: '/login',
    //    name: 'login',
    //    component: LoginView
    // },
    // {
    //   path: '/matchmaking',
    //   name: 'matchmaking',
    //   component: MatchmakingView
    // },
    // {
    //   path: '/account',
    //   name: 'account',
    //   component: MyAccountView
    // },
    // {
    //   path: '/register',
    //   name: 'register',
    //   component: RegisterView
    // },
    // {
    //   path: '/settings',
    //   name: 'settings',
    //   component: SettingsView
    // },
    // {
    //   path: '/tourney',
    //   name: 'tourney',
    //   component: TourneyModeView
    // }
  ]
})

export default router