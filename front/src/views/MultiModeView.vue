<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onMounted } from 'vue';

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 

    onMounted(async () => {
        await getUser();
        if (is_connected.value === false)
            __goTo('/')
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    const router = useRouter();

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }

    function goToGameSelect() {
        router.push('/legacy');
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
                <CreateHomeButton />
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