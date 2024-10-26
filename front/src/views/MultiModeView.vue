<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onMounted } from 'vue';
    import { inject } from 'vue';


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

    const gameSelection = inject('gameSelection');
    const varySpeed = inject('varySpeed');
    const game = inject('game');
    const mode = inject('mode');

    varySpeed(1.6);
    mode.value = ''; //resets mode in case user uses back"back"

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }

    function goToMatchMakingLocal() {
        mode.value = 'local';
        gameSelection(game.value, mode.value);
        router.push('/gameselect');
    }

    function goToTourney() {
        mode.value = 'tourney';
        gameSelection(game.value, mode.value);
        router.push('/gameselect');
    }

    function goToRemote() {
        mode.value = 'remote';
        gameSelection(game.value, mode.value);
        router.push('/gameselect');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-credits" @click="goToMatchMakingLocal()">
                    <span class="buttonText">{{ $t('local') }}</span>
                </button>
                <button class="button button-credits" @click="goToTourney()">
                    <span class="buttonText">{{ $t('tourney') }}</span>
                </button>
                <button class="button button-credits" @click="goToRemote()">
                    <span class="buttonText">{{ $t('remote') }}</span>
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