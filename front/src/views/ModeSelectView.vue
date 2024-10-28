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

    varySpeed(1.3);
    game.value = ''; //resets game in case user uses "back"
    mode.value = ''; //resets mode in case user uses back"back"

    
    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }

    function goToIA() {
        router.push('/IA');
        game.value = 'solo';
        gameSelection(game.value, mode.value);
    }

    function goToMulti() {
        router.push('/multimode');
        game.value = 'multi';
        gameSelection(game.value, mode.value);
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-solo" @click="goToIA()">
                    <i class="fa-solid fa-user"></i>
                    <span class="buttonText" style="margin-left: 0.5vw;">{{ $t('solo') }}</span>
                </button>
                <button class="button button-credits" @click="goToMulti()">
                    <i class="fa-solid fa-users"></i>
                    <span class="buttonText" style="margin-left: 0.5vw;">{{ $t('multiplayer') }}</span>
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

</style>