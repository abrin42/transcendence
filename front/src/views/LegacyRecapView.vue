<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount, onMounted, ref } from 'vue';
    import profilePicture from '@/assets/img/default-profile.png';

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser } = useUser(); 
    const currentUrl = window.location.href; 
    const lastSegment = currentUrl.split('/').filter(Boolean).pop();
    
    let scoreplayer1 = ref(0);
    let scoreplayer2 = ref(0);
    let profilePicture1 = ref("");
    let profilePicture2 = ref("");
    let gamestatus;
    
    onBeforeMount(async () => {
        await getUser();
    });

    onMounted(async () => {
        await getUser();
        await getGameInfo();
    });
    
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    
    const router = useRouter();
    const result = ref("GAME IN PROGRESS");

    function goToHome() {
        router.push('/');
    }

    function goToGameSelect() {
        router.push('/gameselect');
    }
    
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    async function getGameInfo() {
    try {
        const response = await fetch('/api/game/getGameInfo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                id: lastSegment,
            }),
        });

        if (response.ok) {
            const responseData = await response.json();
            scoreplayer1.value = responseData.scorep1;
            scoreplayer2.value = responseData.scorep2;
            profilePicture1 = responseData.player1.profile_picture;
            profilePicture2 = responseData.player2.profile_picture;
            gamestatus = responseData.state;
            
            console.log("la game---");
            console.log(responseData);

        }
        else if (response.status === 404) {
            goToHome();
        }
        else
        {
            const errorData = await response.json();
            console.error('Error:', errorData.error);
        }
        console.log('HEEEEEEEERE');
        console.log(result.value);
        if (gamestatus == 'end' && scoreplayer1.value >= 5)
            result.value = "PLAYER 1 WINS!";
        else if (gamestatus == 'end' && scoreplayer2.value >= 5)
            result.value = "PLAYER 2 WINS!";
        console.log(result.value);
    } catch (error) {
        console.error('Error updating game:', error);
    }
  }
</script>

<template>
    <main>
        <div id="wrapper">
            <div id="dark-background">
            <div class="buttonContainer">
                <button id="home-button-recap" v-if="gamestatus = 'end'" class="button button-cyber" @click="goToHome">
                    <span class="buttonText">{{ $t('home') }}</span>
                </button>
                <button id="play-button-recap" v-if="gamestatus = 'end'" class="button button-cyber" @click="goToGameSelect">
                    <span class="buttonText">{{ $t('play_again') }}</span>
                </button>
                <div class="player-one">
                    <img id="player1-picture" class="profile-picture-matchmaking-left" :src="profilePicture1 || profilePicture"/>
                    <p id="player1-name" class="profile-text-left">{{playerName1}}</p>
                    <p id="player1-rank" class="rank-text-left">{{playerRank1}}</p>
                </div>
                <div id="player-two">
                    <img id="player2-picture" class="profile-picture-matchmaking-right" :src="profilePicture2 || profilePicture"/>
                    <p id="player2-name" class="profile-text-right">{{playerName2}}</p>
                    <p id="player2-rank" class="rank-text-right">{{playerRank2}}</p>
                </div>
                <p id="endgame-message">{{ result }}</p>
                <p id="score">{{ scoreplayer1 }} - {{ scoreplayer2 }}</p>
                <div>
                    <CreateSoundButton />
                </div>
                <div>
                    <CreateDropupButton />
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
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'CyberFont', sans-serif;
    font-size: 150px;
    font-weight: bold;
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

#endgame-message{
    position: fixed;
    top: 22%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'CyberFont', sans-serif;
    font-size: 75px;
    font-weight: bold;
    color: rgb(255, 91, 192);
    filter: drop-shadow(5px 5px 4px #ff42e068);
}

#home-button-recap
{
    position: fixed;
    top: 70%;
}

#play-button-recap
{
    position: fixed;
    top: 80%;
}

@font-face {
  font-family: 'CyberFont';
  src: url('../assets/Cyberway-Riders.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}

.profile-picture-matchmaking-right {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 36%;
    right: 15%;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.profile-picture-matchmaking-left {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 36%;
    left: 15%;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.profile-text-left {
    position: fixed;
    top: 62%;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    left: 45%;
    color: white;
}

.profile-text-right {
    position: fixed;
    opacity: 0;
    top: 62%;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    left: 75%;
    color: white;
}

.rank-text-left {
    position: fixed;
    font-size: 25px;
    font-weight: bold;
    top: 65%;
    left: 47%;
    color: white;
}

.rank-text-right {
    position: fixed;
    opacity: 0;
    font-size: 25px;
    font-weight: bold;
    top: 65%;
    left: 77%;
    color: white;
}

</style>