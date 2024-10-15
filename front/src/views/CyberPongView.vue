<script setup>
//imports
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import CreateSoundButton from '../components/CreateSoundButton.vue';

var myVideo = document.getElementById('videoBG');
</script>

<template>
    <main>
        <div id="wrapper">
            <video autoplay muted loop class="flex">
                <source src="./../assets/GameScene.mp4" type="video/mp4">
                Your browser does not support the video element.
            </video>

            <div class="buttonContainer">
                <CreateBackButton />
                <CreateSoundButton />
            </div>
        </div>
    </main>
</template>

<style scoped>


</style>