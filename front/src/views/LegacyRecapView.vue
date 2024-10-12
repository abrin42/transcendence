<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;



    function goToHome() {
        router.push('/');
    }

    function goToGameSelect() {
        router.push('/gameselect');
    }

    let scoreplayer1 = 10; //remplacer par fetch score p1
    let scoreplayer2 = 1; //remplacer par fetch score p2

    let result = "win"; //fetch 'win' ou 'lose'
    let endgamemessage;
    if (result = "win")
    {
        endgamemessage = "Congratulations!";
    }
    else
    {
        endgamemessage = "WASTED";
    }

</script>

<template>
    <main>
        <div id="wrapper">
            <div id="dark-background">
            <div class="buttonContainer">
                <button class="button button-cyber" @click="goToHome">
                    <span class="buttonText"> Home </span>
                </button>

                <button class="button button-cyber" @click="goToGameSelect">
                    <span class="buttonText"> Play Again </span>
                </button>
                <p id="score">You {{result}} {{ scoreplayer1 }} - {{ scoreplayer2 }}</p>
                <p id="endgame-message">{{ endgamemessage }}</p>
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
        </div>
        
    </main>
</template>

<style>
#dark-background{
    box-shadow: inset 0 0 0 1000px rgba(0, 0, 0, 0.398);
    width: 100vw;
    height: 100vh;
}

#score{
    position: fixed;
    top: 33%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 60px;
    font-weight: bold;
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

#endgame-message{
    position: fixed;
    top: 22%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 100px;
    font-weight: bold;
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}
</style>