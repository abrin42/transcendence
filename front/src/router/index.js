import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GameView from '../views/GameView.vue'
import ModeSelectView from '../views/ModeSelectView.vue'
import CreditsView from '../views/CreditsView.vue'
import SettingsView from '../views/SettingsView.vue'
import LogView from '../views/LogView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import TwoFaView from '../views/2faView.vue'

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
			path: '/game',
			name: 'game',
			component: GameView
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
			path: '/2fa',
			name: '2fa',
			component: TwoFaView
		},
	]
})

export default router