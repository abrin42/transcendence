<script setup>
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';

var myVideo = document.getElementById('videoBG');
myVideo.playbackRate = 1.3;
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <CreateBackButton />
                <CreateDropupButton />
            </div>
        </div>
    </main>
</template>

<style lang="scss">
@import './../assets/main.scss';

.buttonContainer {
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 140vh;
    position: relative;
}
</style>