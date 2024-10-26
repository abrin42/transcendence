<script setup>
    //imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount } from 'vue';
    import { inject } from 'vue';


    const router = useRouter();
    const gameSelection = inject('gameSelection');
    const varySpeed = inject('varySpeed');
    const game = inject('game');
    const mode = inject('mode');

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js';
    const { getUser, is_connected } = useUser();

    onBeforeMount(async () => {
        await getUser();
        if (is_connected.value === false)
            __goTo('/');
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }

    function goToLegacy() {
        // go to Legacy IA
        if(game.value == 'solo')
            router.push('/legacy-ia');
        // go to Legacy multi local
        else if(game.value == 'multi' && mode.value == 'local')
            router.push('/legacy-local/:id');
        // go to legacy multi remote
        else if(game.value == 'multi' && mode.value == 'tourney')
            router.push('/legacy-tourney');
        // go to legacy tourney 
        else if(game.value == 'multi' && mode.value == 'remote')
            router.push('/legacy-remote/:id');
        else
            console.error("Error with game selection");
    }

    function goToCyber() {
        // go to Cyber IA
        if(game.value == 'solo')
            router.push('/cyberpong-ia');
        // go to Cyber multi local
        else if(game.value == 'multi' && mode.value == 'local')
            router.push('/cyberpong-local/:id');
        // go to Cyber multi remote
        else if(game.value == 'multi' && mode.value == 'tourney')
            router.push('/cyber-tourney');
        // go to legacy tourney 
        else if(game.value == 'multi' && mode.value == 'remote')
            router.push('/cyber-remote/:id');
        else
            console.error("Error with game selection");
    }

    function goToThree() {
        // go to Three IA
        if(game.value == 'solo')
            router.push('/threepong-ia');
        else
            console.error("Error with game selection");
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">

                <button class="button" @click="goToLegacy">
                    <i class="fa-solid fa-poo" style="margin-right: 1vw;"></i>
                    <span class="buttonText buttonTextSize">Legacy</span>
                </button>

                <button class="button button-cyber" @click="goToCyber">
                    <i class="fa-solid fa-hippo" style="margin-right: 1vw;"></i>
                    <span class="buttonText">CyberPong</span>
                </button>

                <button  v-if="game.value == 'solo'" class="button button-cyber" @click="goToThree">
                    <i class="fa-solid fa-hippo" style="margin-right: 1vw;"></i>
                    <span class="buttonText">CyberPong</span>
                </button>

                <CreateHomeButton />
                <CreateSoundButton />
                <CreateDropupButton />
                <CreateBackButton />
            </div>
        </div>
    </main>
</template>

<style></style>