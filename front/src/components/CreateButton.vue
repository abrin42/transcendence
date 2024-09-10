<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isPlaying = ref(false);
const isRotating = ref(false);

function goToNewPage() {
    router.push('/game');
}

function toggleIcon() {
    isPlaying.value = !isPlaying.value;
}

function clickButton() {
    console.log('Button clicked');
}

function rotateIcon() {
    isRotating.value = true;
    setTimeout(() => {
        isRotating.value = false;
    }, 1000);
}
</script>

<template>
    <div id="app">
        <div class="buttonContainer">
            <button class="button" @click="goToNewPage">
                <i class="fas fa-play" style="margin-right: 8px;"></i>
                <span class="buttonText buttonTextSize">Play</span>
            </button>

            <button class="button button-credits" @click="clickButton">
                <span class="buttonText">Credits</span>
            </button>

            <button class="button button-log" @click="clickButton">
                <span class="buttonText">Login</span>
            </button>

            <button class="button button-settings" @click="rotateIcon">
                <!-- Ajoutez ou enlevez la classe icon-rotate selon l'état -->
                <i :class="['fas fa-gear', { 'icon-rotate': isRotating }]"></i>
            </button>

            <button class="button button-sound" @click="toggleIcon">
                <i v-if="isPlaying" class="fa-solid fa-volume-high"></i>
                <i v-else class="fa-solid fa-volume-xmark"></i>
            </button>
        </div>
    </div>
</template>

<style>
@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.icon-rotate {
    display: inline-block;
    animation: rotate 1s ease-out;
}

/* Autres styles existants */
.buttonContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 140vh;
    position: relative;
}

.button {
    background-color: rgba(255, 255, 255, 0.0);
    padding: 1rem 1rem;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    border-width: 0.15vw;
    transition: border-color 0.5s;
    margin-top: 10px;
    width: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.buttonText {
    color: rgb(255, 255, 255);
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
    opacity: 1;
}

.button i {
    color: rgb(255, 255, 255);
    font-size: 1.5rem;
    cursor: pointer;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}

.button-log {
    position: absolute;
    width: 120px;
    height: 50px;
    top: 10px;
    right: 10px;
}

.button-settings {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 10px;
    right: 140px;
}

.button-sound {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 10px;
    left: 10px;
}

.button-credits {
    width: 120px;
    height: 50px;
}
</style>
