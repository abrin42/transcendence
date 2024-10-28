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
    varySpeed(1.6);
    console.log(game.value);

    let isMultiButtonVisible = false;
    if (game.value == 'legacy' || game.value == 'cyberpong')
        isMultiButtonVisible = true;
    
    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }

    function goToSolo() {
        mode1.value = 'solo';
        if(game.value == 'legacy')
            router.push('/legacy-ia');
        else if(game.value == 'cyberpong')
            router.push('/cyberpong-ia');
        else if(game.value == 'threepong')
            router.push('/threepong-ia');
    }

    function goToMulti() {
        mode1.value = 'multi';
        router.push('/multimode');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-solo" @click="goToSolo()">
                    <i class="fa-solid fa-user"></i>
                    <span class="buttonText" style="margin-left: 0.5vw;">{{ $t('solo') }}</span>
                </button>
                <button v-if="isMultiButtonVisible" class="button button-credits" @click="goToMulti()">
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