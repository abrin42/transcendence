<template>
    <div class="button-container" @mouseenter="showDropdown" @mouseleave="hideDropdown">
        <button ref="button" class="button button-log" @click="__goTo(isConnect ? '/dashboard' : '/log')">
            <span class="buttonText">{{ isConnect ? username : $t('login') }}</span>
        </button>

        <div v-if="dropdownVisible" class="dropdown">
            <button class="button buttonText buttondropdown" @click="__goTo('/dashboard')">My Account</button>
            <!-- Appel à la méthode toggleFriendsPopup pour afficher la popup -->
            <button class="button buttonText buttondropdown" @click="toggleFriendsPopup">Friends</button>
            <button class="button buttonText buttondropdown" @click="__logout">Logout</button>
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
const friendsPopupVisible = ref(true);
let hoverTimeout = null;

function adjustButtonPosition() {
    const buttonWidth = button.value.offsetWidth;
    button.value.style.left = `calc(100vw - ${buttonWidth + 85}px)`;
}

onMounted(() => {
    adjustButtonPosition();
});

watch(() => username, adjustButtonPosition);

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
}
</script>

<style>
.button-container {
    /* position: relative; */
    /* display: inline-block; */
}

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
    padding: 2vh 2vw;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: border-color 0.5s;
    margin-top: 0.1vh;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}

.buttondropdown {
    width: 11vw;
    height: 6vh;
}

.dropdown button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
