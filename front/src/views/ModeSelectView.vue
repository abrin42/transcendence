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
                <button class="button button-solo" @click="goToGameSelect()">
                    <i class="fa-solid fa-user"></i>
                    <span class="buttonText" style="margin-left: 0.5vw;">{{ $t('Solo') }}</span>
                </button>
                <button class="button button-credits" @click="goToMulti()">
                    <i class="fa-solid fa-users"></i>
                    <span class="buttonText" style="margin-left: 0.5vw;">{{ $t('Multiplayer') }}</span>
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