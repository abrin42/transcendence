<script setup> 
// Imports
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateSettingsButton from '../components/CreateSettingsButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount } from 'vue';

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

    const router = useRouter();
    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1;

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }

    function goToModeSelect() {
        router.push('/modeselect');
    }

    function goToCredits() {
        router.push('/credits');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="goToModeSelect">
                    <i class="fas fa-play" style="margin-right: 8px;"></i>
                    <span class="buttonText buttonTextSize">Play</span>
                </button>

                <button class="button button-credits" @click="goToCredits">
                    <span class="buttonText">Credits</span>
                </button>

                <button class="button button-log" @click="clickButton">
                    <span class="buttonText">Login</span>
                </button>
                <div>
                    <CreateSoundButton />
                </div>
                <div>
                    <CreateSettingsButton />
                </div>
                <div>
                    <CreateDropupButton />
                </div>
            </div>
        </div>
    </main>
</template>

<style>
    @import './../assets/main.scss';
</style>