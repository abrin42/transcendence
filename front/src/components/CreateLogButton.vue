<template>
    <button class="button button-log" @click="__goTo(isConnect ? '/dashboard' : '/log')">
        <span class="buttonText">{{ isConnect ? username : $t('login') }}</span>
    </button>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

function __goTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}

const isConnect = ref(true); // Changer quand le player est connecter
var username = 'username ewjbjiffw'; // Nom d'utilisateur pour tester
</script>

<style scoped>
.button-log {
    position: fixed;
    bottom: 7vh; /* Position en bas de l'écran */
    left: 83vw; /* Aligner à gauche avec une marge de 2vw du bord de l'écran */
    height: 6vh; /* Hauteur du bouton */
    padding: 0.5rem 1rem; /* Espacement intérieur */
    min-width: 7vw; /* Largeur minimale pour le bouton */
    max-width: 50vw; /* Largeur maximale */
    white-space: nowrap; /* Empêche le texte de se retourner */
    transition: width 0.3s ease, left 0.3s ease;
}
.buttonText {
    display: inline-block;
}
</style>
