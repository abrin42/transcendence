<script setup> 
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';

</script>

<template>
    <main>
        <div id="wrapper">

            <video id="CreditsScene" autoplay muted loop class="flex">
                <source src="./../assets/CreditsSceneNoEffects.mp4" type="video/mp4">
                    Your browser does not support the video element.
            </video>

            <div class="buttonContainer">
                <div>
                    <CreateBackButton />
                </div>
                <div>
                    <CreateSoundButton />
                </div>
            </div>
        </div>
    </main>
</template>

<style>
    .buttonContainer {
    z-index: 1;

}

</style>