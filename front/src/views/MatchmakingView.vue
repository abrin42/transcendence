<script setup type="text/javascript">
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { reactive, onMounted } from 'vue';
    import { useRouter } from 'vue-router';

    var myVideo = document.getElementById('videoBG');
    
    myVideo.playbackRate = 2;
    let player1;
    let player2;
    let gamemode = "Legacy Pong";
    let playerName1 = "Chachou";
    let playerName2 = "Chachou2";
    let playerRank1 = "noob";
    let playerRank2 = "beginner";
    const router = useRouter();

    const userAccount = reactive({
        nickname:"", 
        // profilePicture: profilePicture,
        rank:0,
    });

    function goToLegacy(id) {
    router.push(`/legacy/${id}`);
}

    onMounted(async () => {
        // await postUser();
    });


    //dynamic "loading" dots 
    if(document.getElementById("loading") != null)
    {
        //console.log(document.getElementById("loading"));
        if (document.getElementById("loading") != false)
        {
            var dots = window.setInterval( function() {
            var wait = document.getElementById("loading");
            console.log(document.getElementById("loading"));
            if ( wait.innerHTML.length >= 3 ) 
                wait.innerHTML = ".";
            else 
                wait.innerHTML += ".";
            }, 1000);
        }
    }

    // if(document.getElementById("right-side") != null &&
    // document.getElementById("loading") != null )
    // {
    // //when 2nd player is found, we hide "waiting for player" and show opponent
    //     let playerfound = true;
    //     if(playerfound == true)
    //     {
    //         document.getElementById("right-side").style.display = block;
    //         document.getElementById("loading").style.display = 'none';
    //     }
    //     else
    //     {
    //         document.getElementById("right-side").style.display = none;
    //         document.getElementById("loading").style.display = block;
    //     }
    // }
    
</script>

<template>
    <main>
        <div>
            <div id="wrapper-matchmaking">
                <CreateSoundButton />
                <CreateDropupButton />
                <CreateHomeButton />
                <CreateBackButton />
                <h2 id="matchmaking-title">Matchmaking</h2>
                <p id="game-type">{{gamemode}}</p>
                <p id="game-advice">Advice: dont read your phone in the stairs</p>
                <div class="buttonContainer">
                    <div class="stuff-to-move">
                        <img class="profile-picture-matchmaking-left" src="../assets/Chachou.png">
                        <p class="profile-text-left">{{playerName1}}</p>
                        <p class="rank-text-left">{{playerRank1}}</p>
                    </div>
                    <div id="stuff-to-hide">
                        <span id="loading" class="waiting-text">.</span>
                        <p class="opponent-text">Looking for an opponent</p>
                    </div>
                    <div id="stuff-to-show">
                        <p class="rank-text-right">{{playerRank2}}</p>
                        <p class="profile-text-right">{{playerName2}}</p>
                        <img class="profile-picture-matchmaking-right" src="../assets/Chachou.png">
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
@import './../assets/main.scss';

.wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

#wrapper-matchmaking {
    box-shadow: inset 0 0 0 1000px rgba(0, 0, 0, 0.398);
}

#matchmaking-title {
    position: flex;
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

#loading {
    position: fixed;
    z-index: 5;
    font-size: 80px;
    top: 38vw;
    left: 45vw;
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
.opponent-text {
    position: fixed;
    z-index: 5;
    font-size: 30px;
    top: 36vw;
    left: 38vw;
    color: white;
}
</style>