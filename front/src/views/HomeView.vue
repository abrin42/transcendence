<script setup> 
    import CreateButton from '../components/CreateButton.vue';
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isPlaying = ref(true);
const isRotating = ref(false);
var myAudio = document.getElementById("myAudio");

function goToGame() {
    router.push('/game');
}

function goToCredits() {
    router.push('/credits');
}

function togglePlay() {
    isPlaying.value = !isPlaying.value;
    if(document.getElementById('background_audio').muted == false){
    document.getElementById('background_audio').muted = true;
    } 
    else {
    document.getElementById('background_audio').muted = false;
    }
};

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
    <main>
        <audio id="background_audio" autoplay="true" loop="loop">
        <source src="./../assets/test.mp3">
            Your browser does not support the audio element.
        </audio>

        <div id="wrapper">
            
            <div class="buttonContainer">
            <button class="button" @click="goToGame">
                <i class="fas fa-play" style="margin-right: 8px;"></i>
                <span class="buttonText buttonTextSize">Play</span>
            </button>

            <button class="button button-credits" @click="goToCredits">
                <span class="buttonText">Credits</span>
            </button>

            <button class="button button-log" @click="clickButton">
                <span class="buttonText">Login</span>
            </button>

            <button class="button button-settings" @click="rotateIcon">
                <!-- Ajoutez ou enlevez la classe icon-rotate selon l'état -->
                <i :class="['fas fa-gear', { 'icon-rotate': isRotating }]"></i>
            </button>

            <button class="button button-sound" @click="togglePlay()">
                <i v-if="isPlaying" class="fa-solid fa-volume-high"></i>
                <i v-else class="fa-solid fa-volume-xmark"></i>
            </button>
            </div>
            <div id="dropup">
                <CreateDropupButton />
            </div>
            <div id="video">
                <video id="videoBG" autoplay muted loop>
                    <source src="./../assets/Homeview.mp4" type="video/mp4">
                </video>
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

.icon-rotate {
    display: inline-block;
    animation: rotate 1s ease-out;
}
    
    #wrapper {
    position: absolute;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    }
    
    #dropup {
        z-index: 1;
        position: relative;
        top: 690px;
        left: -770px;
    } 

    #video {
        z-index: -1;
        position: absolute;
        width: auto;
        height: auto;
        min-width: 100%;
        max-height: 100%;
    }

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
    left: -65vh;
}

    .button-credits {
    position: absolute;
    top: 75vh;
    width: 120px;
    height: 50px;
}
</style>