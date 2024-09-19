<script setup>
// Imports
import CreateSoundButton from '../components/CreateSoundButton.vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateSettingsButton from '../components/CreateSettingsButton.vue';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

// Routing functions
const router = useRouter();
var myVideo = document.getElementById('videoBG');
myVideo.playbackRate = 1;

function goToModeSelect() {
    router.push('/modeselect');

}

function goToCredits() {
    router.push('/credits');
}

</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="goToModeSelect">
                    <i class="fas fa-play" style="margin-right: 8px;"></i>
                    <span class="buttonText buttonTextSize">{{ $t('play') }}</span>
                </button>

                <button class="button button-credits" @click="goToCredits">
                    <span class="buttonText">{{ $t('credits') }}</span>
                </button>

                <button class="button button-log" @click="clickButton">
                    <span class="buttonText">{{ $t('login') }}</span>
                </button>
                <div>
                    <CreateSoundButton />
                </div>
                <div>
                    <CreateSettingsButton />
                </div>
                <div>
                    <CreateDropupButton />
                </div>
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

#dropup {
    z-index: 1;
    position: relative;
    top: 690px;
    left: -770px;
}

.buttonContainer {
    z-index: 1;
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
    left: 48vW;
}
.button-settings {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 10px;
    left: 43vW;
}

.button-sound {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 10px;
    right: 95vh;
}

.button-credits {
    position: absolute;
    top: 75vh;
    width: 120px;
    height: 50px;
}
</style>