<template>
    <div class="button-container" @mouseenter="showDropdown" @mouseleave="hideDropdown">
        <button ref="button" class="button button-log" @click="goToLeaderboardLog">
            <span class="buttonText">{{ is_connected ? userAccount.nickname : $t('login') }}</span>
        </button>

        <div id="dropdown-content" v-if="dropdownVisible" class="dropdown">
            <button class="button buttonText buttondropdown" @click="__goTo('/dashboard')">{{ $t('my_account') }}</button>
            <!-- Appel à la méthode toggleFriendsPopup pour afficher la popup -->
            <button class="button buttonText buttondropdown" @click="toggleFriendsPopup">{{ $t('friends') }}</button>
            <button class="button buttonText buttondropdown" @click="__goTo('/leaderboard2')">{{ $t('leaderboard') }}</button>
            <button class="button buttonText buttondropdown" @click="handleLogout">{{ $t('logout') }}</button>
        </div>

        <!-- Composant FriendsPopup, écoute l'événement 'close' pour masquer la popup -->
    </div>
    <FriendsPopup v-if="friendsPopupVisible" @close="toggleFriendsPopup" />
</template>

<script setup>
    import { ref, onMounted, onBeforeMount, watch } from 'vue';
    import { useRouter } from 'vue-router';
    import FriendsPopup from './FriendsPopup.vue'; 

////////////////////////////////////////////////
/////// GET USER ///////////////////////////////
////////////////////////////////////////////////

import { useUser } from '../useUser.js';
const { getUser, userAccount, is_connected } = useUser();

    onMounted(async () => {
        await getUser();
    });

////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////

const router = useRouter();

    function __goTo(page) {
        if (page == null) {
            return;
        }
        router.push(page);
    }

    const goToLeaderboardLog = () => {
        const path = is_connected.value ? `/leaderboard/${userAccount.username}` : '/log/';
        router.push(path);
    };

    const button = ref(null);
    const dropdownVisible = ref(false);
    const friendsPopupVisible = ref(false);
    let hoverTimeout = null;
    
    const handleLogout = async () => {
        try {
            await fetch("/api/player/logout/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
            });
            router.push('/log');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    onMounted(async() => {
        await getUser();
        adjustButtonPosition();
    });

    watch(() => userAccount.nickname, adjustButtonPosition);

    function adjustButtonPosition() {
        const buttonWidth = button.value.offsetWidth;
        button.value.style.right = `calc(${buttonWidth -40}px)`;
    }

    function showDropdown() {
        hoverTimeout = setTimeout(() => {
            if (is_connected.value)
                dropdownVisible.value = true;
        }, 5);
    }

function hideDropdown() {
    clearTimeout(hoverTimeout);
    dropdownVisible.value = false;
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
    right: 3vw;
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