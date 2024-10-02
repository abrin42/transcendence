<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;

    function goToSolo() {
    router.push('/gameselect');
    }

    function goToMulti() {
    router.push('/gameselect');
    }

    function goToTournoi() {
    router.push('/gameselect');
    }
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