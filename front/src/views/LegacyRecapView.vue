<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;



    function goToHome() {
        router.push('/');
    }

    function goToGameSelect() {
        router.push('/gameselect');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="goToHome">
                    <i class="fas fa-play" style="margin-right: 8px;"></i>
                    <span class="buttonText buttonTextSize">Home</span>
                </button>

                <button class="button button-cyber" @click="goToGameSelect">
                    <span class="buttonText"> Play Again </span>
                </button>

                <div>
                    <CreateSoundButton />
                </div>

                <div>
                    <CreateDropupButton />
                </div>

                <div>
                    <CreateBackButton />
                </div>
            </div>
        </div>
    </main>
</template>

<style>
</style>