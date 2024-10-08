<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;

    function goToGameSelect() {
    router.push('/gameselect');
    }

    function goToMatchmaking() {
    router.push('/matchmaking');
    }

    function goToTourney() {
    router.push('/tourney');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-credits" @click="goToGameSelect()">
                    <span class="buttonText">{{ $t('local') }}</span>
                </button>
                <button class="button button-credits" @click="goToMatchmaking()">
                    <span class="buttonText">{{ $t('online') }}</span>
                </button>
                <button class="button button-credits" @click="goToTourney()">
                    <span class="buttonText">{{ $t('tourney') }}</span>
                </button>
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