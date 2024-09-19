<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';


    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;
</script>

<template>
    <main>
        <div id="wrapper">
            <div>
                <CreateDropupButton />
            </div>
            <div>
                <CreateBackButton />
            </div>
        </div>
    </main>
</template>

<style lang="scss">
@import './../assets/main.scss';

</style>