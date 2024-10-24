import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ModeSelectView from '../views/ModeSelectView.vue'
import CreditsView from '../views/CreditsView.vue'
import GameSelectView from '../views/GameSelectView.vue'
import LegacyPongView from '../views/LegacyPongView.vue'
import legacy_remote from '../views/LegacyPongRemoteView.vue'
import LegacyRecapView from '../views/LegacyRecapView.vue'
import CyberPongView from '../views/CyberPongView.vue'
import CyberRecapView from '../views/CyberRecapView.vue'

import ThreePongView from '../views/ThreePongView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import LoginView from '../views/LoginView.vue'
import MatchmakingView from '../views/MatchmakingView.vue'
import MyAccountView from '../views/MyAccountView.vue'
import TourneyView from '../views/TourneyView.vue'
import MultiModeView from '../views/MultiModeView.vue'

import SettingsView from '../views/SettingsView.vue'
import CreateLobbyView from '../views/CreateLobbyView.vue'
import JoinLobbyView from '../views/JoinLobbyView.vue'
import LogView from '../views/LogView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import IAPongView from '../views/IAPongView.vue'
import TwoFaView from '../views/2faView.vue'
import TermsView from '../views/TermsView.vue'
import LeaderboardView2 from '../views/LeaderboardView2.vue'
import NotFound from '../views/NotFound.vue'

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
      path: '/multimode',
      name: 'multimode',
      component: MultiModeView
    },
    {
      path: '/tourney',
      name: 'tourney',
      component: TourneyView
    },
    {
      path: '/createlobby',
      name: 'createlobby',
      component: CreateLobbyView
    },
    {
      path: '/joinlobby',
      name: 'joinlobby',
      component: JoinLobbyView
    },
    {
      path: '/matchmaking',
      name: 'matchmaking',
      component: MatchmakingView
    },
    {
      path: '/cyberpong-ia',
      name: 'cyberpong-ia',
      component: CyberPongView
    },
    {
      path: '/cyberrecap',
      name: 'cyberrecap',
      component: CyberRecapView
    },
    {
      path: '/legacy/:id',
      name: 'legacy',
      component: LegacyPongView
    },
    {
      path: '/legacy_remote/:id',
      name: 'legacy_remote',
      component: legacy_remote
    },
    {
      path: '/legacyrecap/:id',
      name: 'legacyrecap',
      component: LegacyRecapView
    },
    {
      path: '/ia',
      name: 'ia',
      component: IAPongView
    },
    {
      path: '/2fa',
      name: '2fa',
      component: TwoFaView
    },
    {
      // path: '/leaderboard', // for testing front end
      path: '/leaderboard/:username',
      name: 'leaderboard',
      component: LeaderboardView
    },
    {
      path: '/terms',
      name: 'terms',
      component: TermsView
    },
    {
      path: '/leaderboard2',
      name: 'leaderboard2',
      component: LeaderboardView2
    },
    {
      path: '/:pathMatch(.*)*', // Cela correspond à toute route non définie
      component: NotFound
    },
    {
      path: '/api/:pathMatch(.*)*', // Cela correspond à toute route non définie
      component: NotFound
    },

  ]
})

export default router