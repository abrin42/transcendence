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

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }

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

    let result = "win"; //fetch 'win' ou 'lose'
    let endgamemessage;
    

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
    
    if (result == "win")
    {
        endgamemessage = "congratulations";
    }
    else
    {
        endgamemessage = "wasted";
    }

</script>

<template>
    <main>
        <div id="wrapper">
            <div id="dark-background">
            <div class="buttonContainer">
                <button class="button button-cyber" @click="goToHome">
                    <span class="buttonText">{{ $t('home') }}</span>
                </button>

                <button class="button button-cyber" @click="goToGameSelect">
                    <span class="buttonText">{{ $t('play_again') }}</span>
                </button>
                <p id="score">You {{result}} {{ scoreplayer1 }} - {{ scoreplayer2 }}</p>
                <p id="endgame-message">{{ $t(endgamemessage) }}</p>
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