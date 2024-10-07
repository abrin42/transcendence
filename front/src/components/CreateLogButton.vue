<template>
    <button ref="button" class="button button-log" @click="__goTo(isConnect ? '/dashboard' : '/log')">
        <span class="buttonText">{{ isConnect ? username : $t('login') }}</span>
    </button>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
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
function adjustButtonPosition() {
    const buttonWidth = button.value.offsetWidth;
    button.value.style.left = `calc(100vw - ${buttonWidth + 100}px)`; 
}

onMounted(() => {
    adjustButtonPosition();
});

watch(() => username, adjustButtonPosition);
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
</style>
