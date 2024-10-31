<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount, onMounted, ref } from 'vue';
    import { inject } from 'vue';
    import i18n from '../i18n.js';

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
    
    //////////ROUTER AND GAME SELECTION////////////
    const router = useRouter();
    const gameSelection = inject('gameSelection');
    const varySpeed = inject('varySpeed');
    const game = inject('game');
    // let playerName2 = "@AI.Bot";

    const mode1 = inject('mode1');
    const mode2 = inject('mode2');
    mode1.value = ''; 
    mode2.value = ''; 
    ////////////////////////////////////////////////
    varySpeed(1.6);
    
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

    // function goToIA() {
    //     console.log("-------------- CREATING THE IA PLAYER --------------");
    //     createAIPlayer();
    //     console.log("-------------- WE ARE GOING TO IA --------------");
    //     game.value = 'solo';
    //     gameSelection(game.value, mode.value);
    //     createGameLocal();
    
    let game_id = ref(0);

    async function goToSolo() {
        mode1.value = 'solo';
        if(game.value == 'legacy')
        {
   
            await createAIPlayer();
            await createGameLocal();
            console.log(game_id.value);
            router.push(`/legacy-ia/${game_id.value}/`);
        }
        else if(game.value == 'cyberpong')
        {
            await createAIPlayer();
            await createGameLocal();
            console.log(game_id.value);
            router.push(`/cyberpong-ia/${game_id.value}/`);
        }
        else if(game.value == 'threepong')
            router.push('/threepong-ia');
    }

    function goToMulti() {
        mode1.value = 'multi';
        router.push('/multimode');
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
                    console.log("hereee");
                    console.log(user);
                    console.log(user.username);
                }
            }  
        } catch (error) {
            console.error('Erreur lors de la creation du bot AI:', error);
            alert(i18n.global.t('error_creating_AI_bot'));
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
                game_id.value =  data.id;
                console.log('data:', data);
                console.log("game id", data.id);
                console.log("p1 =",data.player1);
                console.log("p2 =",data.player2);
                
            }
        }
        catch (error) {
            console.error('Erreur lors de la creation du jeu local:', error);
            alert(i18n.global.t('error_creating_local_game'));
        }
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button button-solo" @click="goToSolo()">
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