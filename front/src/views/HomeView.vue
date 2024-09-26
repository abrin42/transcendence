<script setup>
import CreateSoundButton from '../components/CreateSoundButton.vue';
import CreateLogButton from '../components/CreateLogButton.vue';
import CreateSettingsButton from '../components/CreateSettingsButton.vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();
var myVideo = document.getElementById('videoBG');
myVideo.playbackRate = 1;

function __gotTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}

</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="__gotTo('/modeselect')">
                    <i class="fas fa-play" style="margin-right: 1vw;"></i>
                    <span class="buttonText buttonTextSize">{{ $t('play') }}</span>
                </button>
                <button class="button button-credits" @click="__gotTo('/credits')">
                    <span class="buttonText">{{ $t('credits') }}</span>
                </button>

                <!-- * BUTTONS OTHERS * -->
                <CreateSoundButton />
                <CreateLogButton @click="__gotTo('/log')" />
                <CreateSettingsButton @click="__gotTo('/settings')" />
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

.button-credits {
    top: 75vh;
    width: auto;
    min-width: 1vw;
    height: auto;
    padding: 1vh 1vw;
    display: flex;
    justify-content: center;
    align-items: center;
    white-space: nowrap;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
