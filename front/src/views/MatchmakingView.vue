<template>
    <main>                        
        <p id="loading" class="waiting-text">.</p>
        <div id="wrapper-matchmaking">
            <CreateSoundButton />
            <CreateDropupButton />
            <CreateHomeButton />
            <CreateBackButton />
            <h2 id="matchmaking-title">Matchmaking</h2>
            <p id="game-type">game-mode: {{gamemode}}</p>
            <p id="game-advice">{{tipdisplayed}}</p>
            <div class="button-container-mm">
                <div class="stuff-to-move">
                    <img id="player1-picture" class="profile-picture-matchmaking-left" src="../assets/Chachou.png"/>
                    <p class="profile-text-left">{{playerName1}}</p>
                    <p class="rank-text-left">{{playerRank1}}</p>
                </div>
                <div id="stuff-to-hide" v-if="loadingmodule">
                        <p class="opponent-text">Looking for an opponent...</p>
                    </div>
                    <div id="stuff-to-show" v-if="rightplayervisible">
                        <p class="rank-text-right">{{playerRank2}}</p>
                        <p class="profile-text-right">{{playerName2}}</p>
                        <img class="profile-picture-matchmaking-right" src="../assets/Chachou.png"/>
                    </div>
                </div>
            </div>
    </main>
</template>


<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { ref, reactive, onMounted, watch } from 'vue';
    import $ from 'jquery';
    import { useRouter } from 'vue-router';


    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 

    onMounted(async () => {
        await getUser();
        if (is_connected.value === false)
            __goTo('/')
        await insertPlayer();
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }
    
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    var myVideo = document.getElementById('videoBG');
    
    myVideo.playbackRate = 2;
    let player1;
    let player2;
    let gamemode = "legacy"; //fetch game mode selected?
    let playerName1 = "Chachou";
    let playerName2 = "Chachou2";
    let playerRank1 = "Noob";
    let playerRank2 = "Beginner";
    const router = useRouter();

    let waitingPlayer = 1;

    function goToLegacy(id) {
    router.push(`/legacy_remote/${id}`);
}



async function insertPlayer() {
        
    try {
        const response = await fetch('api/game/insertplayer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Assuming you have CSRF protection enabled
            },
            body: JSON.stringify({
                username: userAccount.username,
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            if (data.player2 == null)
            {
                waitingPlayer = 1;
                await new Promise(resolve => setTimeout(resolve, 1000));
                insertPlayer();
            }
            else
            {
                waitingPlayer = 0;
                console.log("lancement dans 3");
                await new Promise(resolve => setTimeout(resolve, 1000));
                console.log("lancement dans 2");
                await new Promise(resolve => setTimeout(resolve, 1000));
                console.log("lancement dans 1");
                await new Promise(resolve => setTimeout(resolve, 1000));
                goToLegacy(data.id);
            }

            }
        } catch (error) {
            console.error('Erreur lors de la connexion:', error);
            alert('An error occurred during login2222');
        }
    }



    ///////////////////////////////////////////////
    let rightplayervisible = ref(false);
    let loadingmodulevisible = ref(true);

    //dynamic "loading" dots 
    if (document.getElementById("loading") != false)
    {
        var dots = window.setInterval( function() {
        var wait = document.getElementById('loading');
        if ( wait.innerHTML.length >= 3 ) 
            wait.innerHTML = ".";
        else 
            wait.innerHTML += ".";
        }, 1000);
    }

    var tips = ['Tip: Reading your phone in the stairs might lead to severe injury.', 'Tip: Try pressing \'C\' while playing ;)', 
    'Tip: Wash your cereal bowl right after eating', 'Don\'t forget to put your paddle back in the center!', 
    'Recipe for a lribette : one tchoukball ball (?), 50 kilos of pasta, and many many many many many Star Wars anecdotes.', 
    'Tu es triste? Arrête.', '"Jeu de pain, jeu de vilain" - Miro', 'Bois de l\'eau. Dans 20, 30 ans y\'en aura plus.'];
    var tipdisplayed = tips[Math.floor(Math.random()*tips.length)];

    //when 2nd player is found, we hide "waiting for player" and show opponent
    let playerfound = true;
    if(playerfound == true)
    {
        //onTriggerMovePlayer1ProfilePicture();
        rightplayervisible = !rightplayervisible;
        loadingmodulevisible = !loadingmodulevisible;
    }


    function onTriggerMovePlayer1ProfilePicture() {
        const player1_pic = document.getElementById('player1-picture');
        player1_pic.classList.add(...[to-anim]);
    }
</script>


<style scoped>
@import './../assets/main.scss';
.button-container-mm {
    position: relative; 
    display: inline-block; 
}

.wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.to-anim {
    position: relative;

    animation-duration: .4s;
    animation-name: my_anim;
}

@keyframes my_anim {
    0% {
        left: 0;
    }

    .5% {
        left: 100px;
    }

    100% {
        left: 0px;
    }
}

#wrapper-matchmaking {
    box-shadow: inset 0 0 0 1000px rgba(0, 0, 0, 0.398);
    height: 100vh;
}

#matchmaking-title {
    position: fixed;
    display: none;
    top: 15%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 55px;
    font-weight: bold;
    color: white;   
    filter: drop-shadow(5px 5px 4px #0000003b);
}

#game-type{
    position: fixed;
    top: 1%;
    right: 1%;
    font-size: 20px;
    font-weight: bold;
    color: rgb(208, 208, 208);
}

#game-advice{
    position: fixed;
    top: 92%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 20px;
    font-weight: bold;
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.profile-picture-matchmaking-left {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    position: fixed;
    top: 47.5%;
    transform: translate(-50%, -50%);
    left: 50%;
    text-align: center;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.profile-picture-matchmaking-left.slide-left {
	animation: slide-left 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}

@keyframes slide-left {
  0% {
            transform: translateX(0);
  }
  100% {
            transform: translateX(-100px);
  }
}

.profile-text-left {
    position: fixed;
    top: 65%;
    text-align: left;
    font-size: 30px;
    font-weight: bold;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
}
.profile-text-right {
    position: fixed;
    font-weight: bold;
    top: 35vw;
    right: 22vw;
    color: white;
}

.rank-text-left {
    position: fixed;
    font-size: 25px;
    font-weight: bold;
    top: 68%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
}

.rank-text-right {
    position: fixed;
    font-size: 25px;
    font-weight: bold;
    top: 38vw;
    left:75vw;
    color: white;
}

#loading {
    position: fixed;
    z-index: 5;
    font-size: 80px;
    font-weight: bold;
    text-align: center;
    top: 72%;
    left: 48%;
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);
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
    font-weight: bold;
    top: 24%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);

}
</style>