<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;



    function goToCreateLobby() {
    router.push('/matchmaking');
    }

    function goToJoinLobby() {
    router.push('/tourney');
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="goToCreateLobby">
                    <span class="buttonText">Create Lobby</span>
                </button>
                <button class="button" @click="goToJoinLobby">
                    <span class="buttonText">Join Lobby</span>
                </button>
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

<style lang="scss">
@import './../assets/main.scss';


</style>