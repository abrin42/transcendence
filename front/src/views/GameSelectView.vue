<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';

    import { useRouter } from 'vue-router';

    const router = useRouter();

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;

    function goToMatchmaking() {
        router.push('/matchmaking');
    }

    function goToLegacy() {
        router.push('/legacy');
    }

    function goToCyber() {
        router.push('/cyberpong');
    }

    function goToThree() {
        router.push('/legacy');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="goToMatchmaking">
                    <i class="fas fa-play" style="margin-right: 8px;"></i>
                    <span class="buttonText buttonTextSize">Legacy</span>
                </button>

                <button class="button button-cyber" @click="goToCyber">
                    <span class="buttonText">CyberPong</span>
                </button>

                <button class="button button-three" @click="goToThree">
                    <span class="buttonText">ThreePong</span>
                </button>
                <div>
                    <CreateHomeButton />
                </div>

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