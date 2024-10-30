<template>
	<div class="dropup" @mouseleave="hideMenu" @mouseenter="showMenu">
		<button id="p0" class="dropbtn">{{ current_flag }}</button>
		<div class="dropup-content locale-changer" v-show="menuVisible">
			<a v-if="current_lang !== 'ES'" @click="switchLang('ES')">🇪🇸</a>
			<a v-if="current_lang !== 'FR'" @click="switchLang('FR')">🇫🇷</a>
			<a v-if="current_lang !== 'EN'" @click="switchLang('EN')">🇬🇧</a>
			<a v-if="current_lang !== 'DE'" @click="switchLang('DE')">🇩🇪</a>
			<a v-if="current_lang !== 'IT'" @click="switchLang('IT')">🇮🇹</a>
			<a v-if="current_lang !== 'MA'" @click="switchLang('MA')">⚔️</a>
		</div>
	</div>
</template>

<script setup>
	import { ref } from 'vue';
	import { useI18n } from 'vue-i18n';
	import { inject, onBeforeMount } from 'vue';
    const current_flag = inject('current_flag');
    const toggle_flag = inject('toggle_flag');

	const current_lang = inject('current_lang');
    const toggle_lang = inject('toggle_lang');
	
	const { locale } = useI18n();
	
	function injectToggleFlag(lang) {
		toggle_flag(lang); 
	}
	
	function injectToggleLang(lang) {
		toggle_lang(lang); 
	}
	
	const menuVisible = ref(false);
	let timeoutId;
	
	////////////////////////////////////////////////
	/////// GET USER ///////////////////////////////
	////////////////////////////////////////////////
	
	import { useUser } from '../useUser.js'; 
	const { getUser, userAccount, is_connected } = useUser(); 
	
	onBeforeMount(async () => {
		await getUser();
		if (is_connected.value == true)
			switchLang(userAccount.language);
		else
			switchLang(current_lang.value);
	});

	////////////////////////////////////////////////
	////////////////////////////////////////////////
	////////////////////////////////////////////////


	async function setLanguage(new_language) {
		try {
			await fetch('/api/player/update_language/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': getCsrfToken()
				},
				body: JSON.stringify({
					language: new_language,
				})
			});
			current_lang.value = new_language;
		} catch (error) {
			console.error('Erreur lors du changement de langues:', error);
		}
	}

	function getCsrfToken() {
		const cookieValue = document.cookie
			.split('; ')
			.find(row => row.startsWith('csrftoken='))
			?.split('=')[1];
		return cookieValue || '';
	}

	function switchLang(lang) {
		locale.value = lang;
		current_lang.value = lang;
		const langs = ["EN", "FR", "ES", "DE", "IT", "MA"];
		const flags = ["🇬🇧", "🇫🇷", "🇪🇸", "🇩🇪", "🇮🇹", "⚔️"];
		for (let i = 0; i < 6; ++i)
			if (lang == langs[i])
				current_flag.value = flags[i];
		if (is_connected.value == true) {
			setLanguage(lang);
		} else {
			injectToggleFlag(current_flag.value);
			injectToggleLang(current_lang.value)
		}
	}

	function showMenu() {
		clearTimeout(timeoutId);
		menuVisible.value = true;
	}

	function hideMenu() {
		timeoutId = setTimeout(() => {
			menuVisible.value = false;
		}, 300);
	}
</script>

<style scoped>
@import './../assets/main.scss';

.dropbtn {
	/* Handler Position and Size */
	position: fixed;
	top: 92vh;
	right: 95vw;
	width: 3vw;
	height: 6vh;

	/* Background style button HomeView */
	background-color: rgba(0, 0, 0, 0.25);
	padding: 2vh 2vw;
	border: 0.15vw solid rgba(0, 0, 0, 0.25);
	border-radius: 0.4vw;
	transition: border-color 0.5s;
	margin-top: 1vh;

	/* Handler emoji */
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 1.5vw;
}

.dropup-content {
	position: fixed;
	bottom: 8vh;
	right: 95vw;
	display: flex;
	flex-direction: column-reverse;
}

.dropup-content a {
	/* Handler Position */
	width: 3vw;
	height: 6vh;

	/* Background style button HomeView */
	background-color: rgba(0, 0, 0, 0.25);
	padding: 2vh 2vw;
	border: 0.15vw solid rgba(0, 0, 0, 0.25);
	border-radius: 0.4vw;
	transition: border-color 0.5s;
	margin-top: 1vh;

	/* Handler emoji */
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 1.5vw;
}

.dropup-content a:hover {
	border-color: rgba(255, 255, 255, 1);
	background-color: rgba(255, 255, 255, 0.4);
}
</style>
