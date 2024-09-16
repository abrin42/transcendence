<template>
    <button id="unmuteButton" class="button button-sound" @click="togglePlay">
        <i v-if="isPlaying" class="fa-solid fa-volume-high"></i>
        <i v-else class="fa-solid fa-volume-xmark"></i>
    </button>
</template>
  
<script setup>
    import { ref } from 'vue';

    const isPlaying = ref(false);
    document.getElementById('background_audio').muted = true;

    var myAudio = document.getElementById('background_audio');
    function togglePlay() {
        document.getElementById('background_audio').play();
        isPlaying.value = !isPlaying.value;
        if(document.getElementById('background_audio').muted == false){
        document.getElementById('background_audio').muted = true;
        } 
        else {
        document.getElementById('background_audio').muted = false;
        }
    };
</script>
  
<style>

</style>