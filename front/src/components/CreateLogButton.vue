<template>
    <div class="button-container" @mouseenter="showDropdown" @mouseleave="hideDropdown">
        <button ref="button" class="button button-log" @click="__goTo(isConnect ? '/' : '/log')">
            <span class="buttonText">{{ isConnect ? username : $t('login') }}</span>
        </button>

        <!-- Afficher le dropdown seulement si la popup d'amis n'est pas visible -->
        <div v-if="dropdownVisible && !friendsPopupVisible" class="dropdown">
            <button ref="dropdownButtons" class="button buttondropdown" @click="__goTo('/dashboard')">
                <i class="fa-solid fa-user" style="margin-right: 0.25vw;"></i>
                <span class="buttonText buttonTextSize">My account</span>
            </button>

            <button ref="dropdownButtons" class="button buttondropdown" @click="toggleFriendsPopup">
                <i class="fa-solid fa-user-group" style="margin-right: 0.25vw;"></i>
                <span class="buttonText buttonTextSize">Friends</span>
            </button>

            <button ref="dropdownButtons" class="button buttondropdown" @click="__logout">
                <i class="fa-solid fa-right-from-bracket" style="margin-right: 0.25vw;"></i>
                <span class="buttonText buttonTextSize">Logout</span>
            </button>
        </div>

        <!-- Composant FriendsPopup, écoute l'événement 'close' pour masquer la popup -->
        <FriendsPopup v-if="friendsPopupVisible" @close="toggleFriendsPopup" />
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import FriendsPopup from './FriendsPopup.vue';

const router = useRouter();

function __goTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}

const isConnect = ref(true); // Changer quand le player est connecté
var username = 'username'; // Nom d'utilisateur pour tester

const button = ref(null);
const dropdownVisible = ref(false);
const friendsPopupVisible = ref(false);
const dropdownButtons = ref([]);
let hoverTimeout = null;

function adjustButtonPosition() {
    const buttonWidth = (button.value.offsetWidth / window.innerWidth) * 100; // Convertir en vw
    button.value.style.left = `calc(100vw - ${buttonWidth + 5}vw)`; // Ajuster la position à droite
}

function adjustDropdownButtonsWidth() {
    const buttonWidthVW = (button.value.offsetWidth / window.innerWidth) * 100;  // Convertir la largeur en vw
    const buttonFontSize = window.getComputedStyle(button.value).fontSize;  // Récupérer la taille de la police

    dropdownButtons.value.forEach((dropdownButton) => {
        dropdownButton.style.width = `${buttonWidthVW}vw`;  // Appliquer la largeur en vw
        dropdownButton.style.fontSize = buttonFontSize;  // Appliquer la taille du texte du bouton principal
    });
}

onMounted(() => {
    adjustButtonPosition();
    dropdownButtons.value = Array.from(document.querySelectorAll('.buttondropdown'));
    adjustDropdownButtonsWidth();  // Ajuster la largeur et la taille du texte des boutons du dropdown après le montage
});

watch([() => username, () => dropdownVisible.value], adjustDropdownButtonsWidth);

function showDropdown() {
    hoverTimeout = setTimeout(() => {
        dropdownVisible.value = true;
    }, 5);
}

function hideDropdown() {
    clearTimeout(hoverTimeout);
    dropdownVisible.value = false;
}

function __logout() {
    console.log('Logging out...');
    __goTo('/log');
}

function toggleFriendsPopup() {
    friendsPopupVisible.value = !friendsPopupVisible.value;
    dropdownVisible.value = false; // Masquer le dropdown lorsque la popup est ouverte
}
</script>

<style>
.button-log {
    position: fixed;
    bottom: 93vh;
    height: 6vh;
    width: 7vw;
    min-width: fit-content;
    white-space: nowrap;
    transition: width 0.3s ease, left 0.3s ease;
}

.dropdown {
    position: fixed;
    bottom: 87%;
    left: 83.2%;
    height: 6%;
    width: 11vw;
    min-width: fit-content;
    white-space: nowrap;
    border-radius: 2vw;
    z-index: 1000;
    display: flex;
    flex-direction: column;
}

.dropdown button {
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.25);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: border-color 0.5s;
    margin-top: 0.1vh;
    display: flex;
    align-items: left;
    justify-content: flex-start;
    gap: 0.5vw;
    width: 100%;
    box-sizing: border-box;
}

.buttondropdown {
    height: 6vh;
    display: flex;
    align-items: center;
    justify-content: flex-start;
}

.buttondropdown i {
    margin-right: 0.5vw;
}

.buttonTextSize {
    left: 0.5vw;
    white-space: nowrap;
    font-size: 0.1rem;
}

.dropdown button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
