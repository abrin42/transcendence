<script setup>
import CreateSoundButton from '../components/CreateSoundButton.vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateSettingsButton from '../components/CreateSettingsButton.vue';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();
var myVideo = document.getElementById('videoBG');
myVideo.playbackRate = 1;

function goToModeSelect() {
    router.push('/modeselect');
}

function goToCredits() {
    router.push('/credits');
}

function goToSettings() {
    router.push('/settings');
}

function goToLog() {
    router.push('/log');
}
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="goToModeSelect">
                    <i class="fas fa-play" style="margin-right: 1vw;"></i>
                    <span class="buttonText buttonTextSize">{{ $t('play') }}</span>
                </button>

                <button class="button button-credits" @click="goToCredits">
                    <span class="buttonText">{{ $t('credits') }}</span>
                </button>

                <button class="button button-log" @click="goToLog">
                    <span class="buttonText">{{ $t('login') }}</span>
                </button>
                <CreateSoundButton />
                <CreateSettingsButton @click="goToSettings" />
                <CreateDropupButton />
            </div>
        </div>
    </main>
</template>

<style>
@import './../assets/main.scss';

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.wrapper {
    z-index: 0;
}

.icon-rotate {
    display: inline-block;
    animation: rotate 1s ease-out;
}

.buttonContainer {
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 140vh;
    /* position: relative; */
}

.button {
    background-color: rgba(0, 0, 0, 0.25);
    padding: 2vh 2vw;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: border-color 0.5s;
    margin-top: 1vh;
    width: auto;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}

.buttonText {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
    opacity: 1;
    white-space: nowrap;
}

.button i {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.5vw;
    cursor: pointer;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}

.button-log {
    /* position: absolute; */
    width: 15vw;
    height: 7vh;
    top: 2vh;
    left: 45vw;
}

.button-settings {
    /* position: absolute; */
    width: 5vw;
    height: 7vh;
    top: 2vh;
    left: 40vw;
}

.button-sound {
    position: relative;
    width: 3vw;
    height: 6vh;
    bottom: 78vh;
    right: 47vw;
}

.button-credits {
    /* position: absolute; */
    top: 75vh;
    width: auto;
    min-width: 1vw;
    height: auto;
    padding: 2vh 2vw;
    display: flex;
    justify-content: center;
    align-items: center;
    white-space: nowrap;
}
</style>
