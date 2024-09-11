<template>
    <button class="button button-sound" @click="togglePlay">
        <i v-if="isPlaying" class="fa-solid fa-volume-high"></i>
        <i v-else class="fa-solid fa-volume-xmark"></i>
    </button>
</template>
  
<script setup>
    import { ref } from 'vue';

    const isPlaying = ref(true);
        
    function togglePlay() {
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