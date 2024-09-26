<script setup>
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import CreateSoundButton from '../components/CreateSoundButton.vue';

var myVideo = document.getElementById('videoBG');
myVideo.playbackRate = 1.3;
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <CreateSoundButton />
                <CreateDropupButton />
                <CreateBackButton />
            </div>
        </div>
    </main>
</template>

<style scoped>
@import './../assets/main.scss';
</style>