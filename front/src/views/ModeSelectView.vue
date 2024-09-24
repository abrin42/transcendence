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
                <button class="button" @click="goToSolo">
                    <i class="fas fa-play" style="margin-right: 8px;"></i>
                    <span class="buttonText buttonTextSize">Solo</span>
                </button>

                <button class="button button-credits" @click="goToMulti">
                    <span class="buttonText">Multi</span>
                </button>

                <button class="button button-tournoi" @click="goToTournoi">
                    <span class="buttonText">Tournoi</span>
                </button>

                <button class="button button-log" @click="clickButton">
                    <span class="buttonText">Login</span>
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