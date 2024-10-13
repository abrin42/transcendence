<template>
    <button class="button button-sound" @click="togglePlayAndSound">
        <i v-if="isPlaying" class="fa-solid fa-volume-high"></i>
        <i v-else class="fa-solid fa-volume-xmark"></i>
    </button>
</template>
  
<script setup>
    import { inject } from 'vue';
    const isPlaying = inject('isPlaying');
    const togglePlay = inject('togglePlay');

    function togglePlayAndSound() {
        togglePlay(); // appelle fonction dans App.vue
    const audioElement = document.getElementById('background_audio');

    if (isPlaying.value) {
        audioElement.play();
        audioElement.muted = false;
    } else {
        audioElement.muted = true;
    }
}
</script>
  
<style>
.button-sound {
    position: fixed;
    width: 3vw;
    height: 6vh;
    top: 92vh;
    left: 95vw;
}
</style>