<template>
	<div class="dropup" @mouseleave="hideMenu" @mouseenter="showMenu">
		<button id="p0" class="dropbtn">{{ userAccount.flag }}</button>
		<div class="dropup-content locale-changer" v-show="menuVisible">
			<a v-if="userAccount.language !== 'ES'" @click="switchLang('ES')">🇪🇸</a>
			<a v-if="userAccount.language !== 'FR'" @click="switchLang('FR')">🇫🇷</a>
			<a v-if="userAccount.language !== 'EN'" @click="switchLang('EN')">🇬🇧</a>
			<a v-if="userAccount.language !== 'DE'" @click="switchLang('DE')">🇩🇪</a>
			<a v-if="userAccount.language !== 'IT'" @click="switchLang('IT')">🇮🇹</a>
			<a v-if="userAccount.language !== 'MA'" @click="switchLang('MA')">⚔️</a>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { reactive, onMounted } from 'vue';

const { locale } = useI18n();


const userAccount = reactive({
	language:"",
	flag:"🇬🇧",
});

async function getLanguage() {
  try {
    //const response = await fetch(`http://localhost:8080/api/test-api/${state.id}`, {
    const response = await fetch(`http://localhost:8080/api/player/connected_user`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const user = await response.json();
    userAccount.language = user[0].fields.language;
  } catch (error) {
    console.error('Error retrieving user data:', error);
  }
}

async function setLanguage(new_language) {
    try {
        await fetch('/api/player/update_language/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Add your CSRF token retrieval here
            },
            body: JSON.stringify({
                language: new_language,
            })
        });
		userAccount.language = new_language;
    } catch (error) {
        console.error('Erreur lors du changement de langues:', error);
    }
}

function getCsrfToken() {
    // Helper function to get the CSRF token from cookies
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

onMounted(async () => {
  await getLanguage();
  switchLang(userAccount.language);
});

const menuVisible = ref(false);
let timeoutId;

function switchLang(lang) {
	locale.value = lang;
	if (lang === 'EN')
		userAccount.flag = '🇬🇧';
	else if (lang === 'FR')
		userAccount.flag = '🇫🇷';
	else if (lang === 'ES')
		userAccount.flag = '🇪🇸';
	else if (lang === 'DE')
		userAccount.flag = '🇩🇪';
	else if (lang === 'IT')
		userAccount.flag = '🇮🇹';
	else if (lang === 'MA')
		userAccount.flag = '⚔️';
	setLanguage(lang);
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
