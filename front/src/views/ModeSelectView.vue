<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount, onMounted } from 'vue';
    import { inject } from 'vue';

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 

    onBeforeMount(async () => {
        await getUser();
        //if (is_connected.value === false)
          //  __goTo('/')
    });

    onMounted(async () => {
        await getUser();
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    
    const router = useRouter();

    const gameSelection = inject('gameSelection');
    const varySpeed = inject('varySpeed');
    const game = inject('game');
    const mode = inject('mode');
    let playerName2 = "@AI.Bot";

    varySpeed(1.3);
    game.value = ''; //resets game in case user uses "back"
    mode.value = ''; //resets mode in case user uses back"back"
    
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

    function goToIA() {
        console.log("-------------- CREATING THE IA PLAYER --------------");
        createAIPlayer();
        console.log("-------------- WE ARE GOING TO IA --------------");
        game.value = 'solo';
        gameSelection(game.value, mode.value);
        createGameLocal();
    }

    function goToMulti() {
        router.push('/multimode');
        game.value = 'multi';
        gameSelection(game.value, mode.value);
    }

    async function createAIPlayer() {
        try {
            const response = await fetch('/api/game/createOneFalsePlayer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    username1: "@AI.Bot"
                })
            });
            if (response.ok) {
                const user = await response.json();
                if (user) {
                    // console.log('Response data:', data);
                    console.log("hereee");
                    console.log(user);
                    console.log(user.username);
                }
            }  
        } catch (error) {
            console.error('Erreur lors de la creation du bot AI:', error);
            alert('An error occurred while creation du bot AI');
        }
    }

    async function createGameLocal()
    {
        try {
            const response = await fetch('/api/game/create_game_local/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() // Assuming you have CSRF protection enabled
                },
                body: JSON.stringify({
                    username1: userAccount.username,
                    username2: "#@AI.Bot", //change to seconde player
                })
            });
            if (response.ok) {
                const data = await response.json();
                console.log('Game Data:', data);

                console.log('data:', data);
                console.log("game id", data.id);
                console.log("p1 =",data.player1);
                console.log("p2 =",data.player2);
                
                router.push(`/legacy-ia/${data.id}/`);
            }
        }
        catch (error) {
            console.error('Erreur lors de la creation du jeu local:', error);
            alert('An error occurred while creating local game');
        }
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-solo" @click="goToIA()">
                    <i class="fa-solid fa-user"></i>
                    <span class="buttonText" style="margin-left: 0.5vw;">{{ $t('solo') }}</span>
                </button>
                <button class="button button-credits" @click="goToMulti()">
                    <i class="fa-solid fa-users"></i>
                    <span class="buttonText" style="margin-left: 0.5vw;">{{ $t('multiplayer') }}</span>
                </button>
                <CreateHomeButton />
                <CreateSoundButton />
                <CreateDropupButton />
                <CreateBackButton />
            </div>
        </div>
    </main>
</template>

<style scoped>

</style>