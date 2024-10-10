<script setup type="text/javascript">
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 2;
    let player1;
    let player2;
    let gamemode = "Legacy Pong";
    let playerName1 = "Chachou";
    let playerName2 = "Chachou2";
    let playerRank1 = "noob";
    let playerRank2 = "beginner";

    //dynamic loading dots 
    if (document.getElementById("loading") != null)
    {
        var dots = window.setInterval( function() {
        var wait = document.getElementById("loading");
            if ( Math.random() < .5 && wait.innerHTML.length <= 4)
                    wait.innerHTML += ".";
            else
                    wait.innerHTML = wait.innerHTML.substring(1, wait.innerHTML.length);
            }, 1000);
    }

    //when 2nd player is found, we hide "waiting for player" and show opponent
    let playerfound = 1;
    if(playerfound == 1)
    {
//document.getElementById('right-side').style.display = 'show';
    }
    else
    {
        document.getElementById('right-side').style.display = 'none';
        document.getElementById('waiting-text').style.display = show;
    }
    
</script>

<template>
    <main>
        <div id="wrapper-matchmaking">
            <CreateSoundButton />
            <!-- <CreateDropupButton /> -->
            <CreateBackButton />
            <h1 id="matchmaking">Matchmaking</h1>
            <h1 id="game-type">{{gamemode}}</h1>
            <img class="profile-picture-matchmaking-left" src="../assets/Chachou.png">
            <img class="profile-picture-matchmaking-right" src="../assets/Chachou.png">
            <div class="buttonContainer">
                <div class="left">
                    <h1 class="profile-text-left">{{playerName1}}</h1>
                    <h1 class="profile-text-right">{{playerName2}}</h1>
                    <h1 class="rank-text-left">{{playerRank1}}</h1>
                    <h1 class="rank-text-right">{{playerRank2}}</h1>
                </div>
            </div>
            <div id="left">
                <span id="loading" class="waiting-text">.</span>
            </div>
        </div>
    </main>
</template>

<style lang="scss">
@import './../assets/main.scss';

#wrapper-matchmaking {
    box-shadow: inset 0 0 0 1000px rgba(0, 0, 0, 0.398);
}

#matchmaking {
    position: fixed;
    text-align: center;
    left: 38vw;
    text-align: center;
    font-size: 55px;
    top: 5vh;
    color: white;   
}

#game-type{
    position: fixed;
    text-align: center;
    left: 42vw;
    text-align: center;
    font-size: 35px;
    top: 11vh;
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
    left:75vw;
    color: white;
}

.waiting-text {
    position: fixed;
    z-index: 5;
    font-size: 80px;
    top: 38vw;
    left: 70vw;
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