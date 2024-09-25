<template>
    <button id="unmuteButton" class="button button-sound" @click="togglePlay">
        <i v-if="isPlaying" class="fa-solid fa-volume-high"></i>
        <i v-else class="fa-solid fa-volume-xmark"></i>
    </button>
</template>

<script setup>
import { ref } from 'vue';

const isPlaying = ref(false);

var myAudio = document.getElementById('background_audio');
function togglePlay() {
    isPlaying.value = !isPlaying.value;
    unmuteButton.addEventListener('click', function () {
        myAudio.muted = !myAudio.muted;
        unmuteButton.addEventListener('click', function () {
            var context = new AudioContext();
        })
    });
};
</script>

<style></style>