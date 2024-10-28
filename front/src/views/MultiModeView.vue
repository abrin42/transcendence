<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount } from 'vue';
    import { inject } from 'vue';


    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 

    onBeforeMount(async () => {
        await getUser();
        if (is_connected.value === false)
            __goTo('/')
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    //////////ROUTER AND GAME SELECTION////////////
    const router = useRouter();
    const gameSelection = inject('gameSelection');
    const varySpeed = inject('varySpeed');
    const game = inject('game');
    const mode1 = inject('mode1');
    const mode2 = inject('mode2');
    mode2.value = ''; 
    ////////////////////////////////////////////////
    varySpeed(1.9);

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }
    console.log('mode1valewerewrwerwerwewerewuehere!!!!!!');
    console.log(game.value);
    console.log(mode1.value);

    function goToMatchMakingLocal() {
        mode2.value = 'local';
        gameSelection(game.value, mode1.value, mode2.value);
        console.log('mode1valewerewrwerwerwewerewuehere!!!!!!');
        console.log(game.value);
        console.log(mode1.value);
        router.push('/matchmaking');
    }

    function goToTourney() {
        mode2.value = 'tourney';
        gameSelection(game.value, mode1.value, mode2.value);
        if(game.value == 'legacy')
            router.push('/legacy-tourney');
        else if(game.value == 'cyberpong')
            router.push('/cyberpong-tourney');
        else
            router.push('/legacy-tourney');
    }

    function goToMatchmakingRemote() {
        mode2.value = 'remote';
        gameSelection(game.value, mode1.value, mode2.value);
        router.push('/matchmakingremote');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-credits" @click="goToMatchMakingLocal()">
                    <span class="buttonText">{{ $t('local') }}</span>
                </button>
                <button class="button button-credits" @click="goToMatchmakingRemote()">
                    <span class="buttonText">{{ $t('remote') }}</span>
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