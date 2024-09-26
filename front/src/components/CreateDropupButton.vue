<template>
	<div class="dropup" @mouseleave="hideMenu" @mouseenter="showMenu">
		<button id="p0" class="dropbtn">{{ currentFlag }}</button>
		<div class="dropup-content locale-changer" v-show="menuVisible">
			<a v-if="currentLang !== 'ES'" @click="switchLang('ES')">🇪🇸</a>
			<a v-if="currentLang !== 'FR'" @click="switchLang('FR')">🇫🇷</a>
			<a v-if="currentLang !== 'EN'" @click="switchLang('EN')">🇬🇧</a>
			<a v-if="currentLang !== 'DE'" @click="switchLang('DE')">🇩🇪</a>
			<a v-if="currentLang !== 'IT'" @click="switchLang('IT')">🇮🇹</a>
			<a v-if="currentLang !== 'MA'" @click="switchLang('MA')">⚔️</a>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();

const currentLang = ref('EN');
const currentFlag = ref('🇬🇧');
const menuVisible = ref(false);
let timeoutId;

function switchLang(lang) {
	currentLang.value = lang;
	locale.value = lang;
	if (lang === 'EN')
		currentFlag.value = '🇬🇧';
	else if (lang === 'FR')
		currentFlag.value = '🇫🇷';
	else if (lang === 'ES')
		currentFlag.value = '🇪🇸';
	else if (lang === 'DE')
		currentFlag.value = '🇩🇪';
	else if (lang === 'IT')
		currentFlag.value = '🇮🇹';
	else if (lang === 'MA')
		currentFlag.value = '⚔️';
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

<style>
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
