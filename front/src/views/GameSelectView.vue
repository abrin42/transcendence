<script setup>
    //imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount } from 'vue';
    import { inject } from 'vue';

    //////////ROUTER AND GAME SELECTION////////////
    const router = useRouter();
    const gameSelection = inject('gameSelection');
    const varySpeed = inject('varySpeed');
    const game = inject('game');
    const mode1 = inject('mode1');
    const mode2 = inject('mode2');
    mode1.value = '';
    mode2.value = '';
    ////////////////////////////////////////////////
    varySpeed(1.3);

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js';
    const { getUser, is_connected } = useUser();

    onBeforeMount(async () => {
        await getUser();
        if (is_connected.value === false)
            __goTo('/')
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
        game.value = 'legacy';
            router.push('/modeselect');
    }

    function goToCyber() {
        game.value = 'cyberpong';
            router.push('/modeselect');
    }
</script>
<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">

                <button class="button" @click="goToLegacy">
                    <span class="buttonText buttonTextSize">Legacy</span>
                </button>

                <button class="button button-cyber" @click="goToCyber">
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