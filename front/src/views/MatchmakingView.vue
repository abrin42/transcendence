<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 2;
</script>

<template>
    <main>
        <img class="profile-picture-matchmaking-left" src="../assets/Chachou.png">
        <img class="profile-picture-matchmaking-right" src="../assets/Chachou.png">
        <div id="wrapper-matchmaking">
            <section class="left">
                <h1 id="game-type">Legacy Pong</h1>
                <h1 class="profile-text-left">Chachou1</h1>
                <h1 class="profile-text-right">Chachou2</h1>
                <h1 class="rank-text-left">Newbie</h1>
                <h1 class="rank-text-right">Beginner</h1>
                <div class="buttonContainer">
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
            </section>
            <div class="separation"></div>
            <section class="right">
                <div>
                    <div class="left-player">
                    </div>
                </div>
            </section>
        </div>
    </main>
</template>

<style lang="scss">
@import './../assets/main.scss';

#wrapper-matchmaking {
    box-shadow: inset 0 0 0 1000px rgba(0,0,0,.2);
}

#game-type{
    position: fixed;
    text-align: center;
    left: 38vw;
    text-align: center;
    font-size: 55px;
    top: 5vh;
    color: white;
}

.profile-picture-matchmaking-left {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 30vh;
    left: 20vw;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.profile-text-left {
    position: fixed;
    top: 35vw;
    left: 22vw;
    color: white;
}
.profile-text-right {
    position: fixed;
    top: 35vw;
    right: 22vw;
    color: white;
}

.rank-text-left {
    position: fixed;
    font-size: 25px;
    top: 38vw;
    left: 22vw;
    color: white;
}

.rank-text-right {
    position: fixed;
    font-size: 25px;
    top: 38vw;
    right: 22vw;
    color: white;
}



.profile-picture-matchmaking-right {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 30vh;
    right: 20vw;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}
</style>