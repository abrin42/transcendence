<script setup>
//imports
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import CreateSoundButton from '../components/CreateSoundButton.vue';
import CreateHomeButton from '../components/CreateHomeButton.vue';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const router = useRouter();

////////////////////////////////////////////////
/////// GET USER ///////////////////////////////
////////////////////////////////////////////////

import { useUser } from '../useUser.js';
const { getUser, is_connected } = useUser();

onMounted(async () => {
    await getUser();
    if (is_connected.value === false)
        __goTo('/')
});

////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////

function __goTo(page) {
    if (page == null)
        return;
    router.push(page);
}

var myVideo = document.getElementById('videoBG');
myVideo.playbackRate = 1.3;

function goToMatchmaking() {
    router.push('/matchmaking');
}

function goToLegacy() {
    router.push('/ia');
}

function goToCyber() {
    router.push('/cyberpong-ia');
}

function goToThree() {
    router.push('/legacy');
}
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">

                <button class="button" @click="goToLegacy">
                    <i class="fa-solid fa-poo" style="margin-right: 1vw;"></i>
                    <span class="buttonText buttonTextSize">Legacy</span>
                </button>

                <button class="button button-cyber" @click="goToCyber">
                    <i class="fa-solid fa-hippo" style="margin-right: 1vw;"></i>
                    <span class="buttonText">CyberPong</span>
                </button>

                <CreateHomeButton />
                <CreateSoundButton />
                <CreateDropupButton />
                <CreateBackButton />
            </div>
        </div>
    </main>
</template>

<style></style>