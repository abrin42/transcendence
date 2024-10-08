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

    function goToMulti() {
    router.push('/multimode');
    }

    function goToTournoi() {
    router.push('/tourney');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-credits" @click="__goToGameSelect()">
                    <span class="buttonText">{{ $t('solo') }}</span>
                </button>
                <button class="button button-credits" @click="__goToMulti()">
                    <span class="buttonText">{{ $t('multiplayer') }}</span>
                </button>
                <button class="button button-credits" @click="__goToTournoi()">
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