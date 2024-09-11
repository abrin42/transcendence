<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 2;
</script>

<template>
    <main>
        <div id="wrapper">
            <div>
                <CreateDropupButton />
            </div>
        </div>
    </main>
</template>

<style lang="scss">
@import './../assets/main.scss';

</style>