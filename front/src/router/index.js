  import { createRouter, createWebHistory } from 'vue-router'
  /**************MENU************/
  import HomeView from '../views/HomeView.vue'
  import ModeSelectView from '../views/ModeSelectView.vue'
  import CreditsView from '../views/CreditsView.vue'
  import GameSelectView from '../views/GameSelectView.vue'
  import SettingsView from '../views/SettingsView.vue'
  import LogView from '../views/LogView.vue'
  import RegisterView from '../views/RegisterView.vue'
  import DashboardView from '../views/DashboardView.vue'
  import MultiModeView from '../views/MultiModeView.vue'
  import CreateLobbyView from '../views/CreateLobbyView.vue'
  import JoinLobbyView from '../views/JoinLobbyView.vue'
  import MatchmakingView from '../views/MatchmakingView.vue'
  import MatchmakingRemoteView from '../views/MatchmakingRemoteView.vue'
  import TwoFaView from '../views/2faView.vue'
  import LeaderboardView from '../views/LeaderboardView.vue'
  import LeaderboardView2 from '../views/LeaderboardView2.vue'
  import TermsView from '../views/TermsView.vue'
  import NotFound from '../views/NotFound.vue'
  /**************GAMES*************/
  /*************LEGACY*************/
  import LegacyIAView from '../views/LegacyIAView.vue'
  import LegacyLocalView from '../views/LegacyLocalView.vue'
  import LegacyRemoteView from '../views/LegacyRemoteView.vue'
  import LegacyTourneyView from '../views/LegacyTourneyView.vue'
  import LegacyRecapView from '../views/LegacyRecapView.vue'
  /************CYBERPONG***********/
  import CyberPongIAView from '../views/CyberPongIAView.vue'
  import CyberPongLocalView from '../views/CyberPongLocalView.vue'
  import CyberPongRemoteView from '../views/CyberPongRemoteView.vue'
  import CyberPongTourneyView from '../views/CyberPongTourneyView.vue'
  import CyberRecapView from '../views/CyberRecapView.vue'
  /**************3PONG*************/
  import ThreePongIAView from '../views/ThreePongIAView.vue'
  /********************************/

  const router = createRouter({
  history: createWebHistory(),
  routes: [
    /**************MENU************/
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
      path: '/matchmakingremote',
      name: 'matchmakingremote',
      component: MatchmakingRemoteView
    },
    {
      path: '/2fa',
      name: '2fa',
      component: TwoFaView
    },
    {
      path: '/leaderboard/:username',
      name: 'leaderboard',
      component: LeaderboardView
    },
    {
      path: '/leaderboard2',
      name: 'leaderboard2',
      component: LeaderboardView2
    },
    {
      path: '/terms',
      name: 'terms',
      component: TermsView
    },
    {
      path: '/:pathMatch(.*)*', // Cela correspond à toute route non définie
      component: NotFound
    },
    /*******************************/
    /*************GAMES*************/
    /************LEGACY*************/
    {
      path: '/legacy-ia/:id',
      name: 'legacy-ia',
      component: LegacyIAView
    },
    {
      path: '/legacy-local/:id',
      name: 'legacy-local',
      component: LegacyLocalView
    },
    {
      path: '/legacy-remote/:id',
      name: 'legacy-remote',
      component: LegacyRemoteView
    },
    {
      path: '/legacy-tourney',
      name: 'legacy-tourney',
      component: LegacyTourneyView
    },
    {
      path: '/legacyrecap/:id',
      name: 'legacyrecap',
      component: LegacyRecapView
    },
    /***********CYBERPONG**********/
    {
      path: '/cyberpong-ia/:id',
      name: 'cyberpong-ia',
      component: CyberPongIAView
    },
    {
      path: '/cyberpong-local/:id',
      name: 'cyberpong-local',
      component: CyberPongLocalView
    },
    {
      path: '/cyberpong-remote/:id',
      name: 'cyberpong-remote',
      component: CyberPongRemoteView
    },
    {
      path: '/cyberpong-tourney',
      name: 'cyberpong-tourney',
      component: CyberPongTourneyView
    },
    {
      path: '/cyberrecap/:id',
      name: 'cyberrecap',
      component: CyberRecapView
    },
    /************3PONG************/
    {
      path: '/threepong-ia',
      name: 'threepong-ia',
      component: ThreePongIAView
    }]
  })
export default router