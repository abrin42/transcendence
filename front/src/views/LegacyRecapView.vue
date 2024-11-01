<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { useRouter } from 'vue-router';
    import { onMounted, ref } from 'vue';

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 
    const currentUrl = window.location.href; 
    const lastSegment = currentUrl.split('/').filter(Boolean).pop();
    
    let scoreplayer1 = ref(0);
    let scoreplayer2 = ref(0);

    onMounted(async () => {
        await getUser();
        await getGameInfo();
        // if (is_connected.value === false)
        //     __goTo('/')
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    const router = useRouter();

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
            console.log('Game updated successfully!', responseData);
        }
        else if (response.status === 404) {
            goToHome();
        }
        else
        {
            const errorData = await response.json();
            console.error('Error:', errorData.error);
        }
    } catch (error) {
        console.error('Error updating game:', error);
    }
  }

    let result = "GAME IN PROGRESS";
    if (scoreplayer1.value == 5)
        result = "PLAYER 1 WINS!";
    if (scoreplayer2.value == 5)
        result = "PLAYER 2 WINS!";

</script>

<template>
    <main>
        <div id="wrapper">
            <div id="dark-background">
            <div class="buttonContainer">
                <button v-if="currentValue >= 10" class="button button-cyber" @click="goToHome">
                    <span class="buttonText">{{ $t('home') }}</span>
                </button>
                <button v-if="currentValue >= 10" class="button button-cyber" @click="goToGameSelect">
                    <span class="buttonText">{{ $t('play_again') }}</span>
                </button>
                <div class="player-one">
                    <img id="player1-picture" class="profile-picture-matchmaking-left" :src="profilePicture"/>
                    <p id="player1-name" class="profile-text-left">{{playerName1}}</p>
                    <p id="player1-rank" class="rank-text-left">{{playerRank1}}</p>
                </div>
                <div id="player-two">
                    <img id="player2-picture" class="profile-picture-matchmaking-right" :src="profilePicture"/>
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