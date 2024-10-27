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
                <img id="versus-image" src="../assets/vs_text.png"/>
                <div class="stuff-to-move">
                    <img id="player1-picture" class="profile-picture-matchmaking-left" :src="profilePicture"/>
                    <p id="player1-name" class="profile-text-left">{{playerName1}}</p>
                    <p id="player1-rank" class="rank-text-left">{{playerRank1}}</p>
                </div>
                <div id="stuff-to-hide">
                    <p id="opponent-text" class="opponent-text">Looking for an opponent...</p>
                </div>
                <div id="stuff-to-show">
                    <img id="player2-picture" class="profile-picture-matchmaking-right" :src="profilePicture"/>

                    <div v-if="validateGame">
                        <p id="player2-name" class="profile-text-right">{{playerName2}}</p>
                        <p id="player2-rank" class="rank-text-right">{{playerRank2}}</p>
                    </div>
                    <div v-else>
                        <Input id="player2-name" class="input-right" placeholder-text="Entrez le pseudo du joueur." v-model="playerName2"></Input>
                        <button class="button button-valid" @click="validGame">
                            <span class="buttonText">Valider</span>
                        </button>
                    </div>
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
    import Input from '../components/Input.vue';
    import { ref, onBeforeMount, onMounted, onUnmounted, watch, defineEmits } from 'vue';
    import $ from 'jquery';
    import { useRouter } from 'vue-router';
    import i18n from '../i18n.js'
    import profilePicture from '@/assets/img/default-profile.png';

    let validateGame = false;
    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 

    onUnmounted(() => {
        stopLoading();
    });

    onBeforeMount(async () => {
        await getUser();
        if (is_connected.value === false)
            __goTo('/')
    });

    onMounted(async () => {
        createPlyInput();
        // await createGameLocal();
        // await insertPlayer();
        await createGameLocal();

    });


    function stopLoading() {
        clearInterval(dots);  // Stop the interval
        console.log("Loading stopped.");
}
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
        console.log("id hereee");
        console.log(id);
        router.push(`/legacy-local/${id}`);
        // router.push(`/matchmaking`);
    }

let loadingmodule = true;
let game_id;

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
                username2: playerName2, //change to seconde player
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Game Data:', data);

            console.log('data:', data);
            console.log("game id", data.id);
            console.log("p1 =",data.player1);
            console.log("p2 =",data.player2);
            

            // const player1 = data.player1;
            // const player1_pic = document.getElementById('player1-picture');
            // const player1_name = document.getElementById('player1-name');
            // const player1_rank = document.getElementById('player1-rank');
            // const player2 = data.player2;
            // const player2_pic = document.getElementById('player2-picture');
            // const player2_name = document.getElementById('player2-name');
            // const player2_rank = document.getElementById('player2-rank');

            // player1_pic.src = player1.profile_picture;
            // player1_name.textContent = player1.username;
            // player1_rank.textContent = `Rank: ${player1.rank}`; 
            // player2_pic.src = player2.profile_picture;
            // player2_name.textContent = player2.username;
            // player2_rank.textContent = `Rank: ${player2.rank}`; 

            // player1_pic.classList.add(...['slide-left']);
            // player1_name.classList.add(...['slide-left']);
            // player1_rank.classList.add(...['slide-left']);
            // player2_pic.classList.add(...['fade-in']);
            // player2_name.classList.add(...['fade-in']);
            // player2_rank.classList.add(...['fade-in']);


            console.log("lancement dans 3");
            await new Promise(resolve => setTimeout(resolve, 1000));
            console.log("lancement dans 2");
            await new Promise(resolve => setTimeout(resolve, 1000));
            console.log("lancement dans 1");
            await new Promise(resolve => setTimeout(resolve, 1000));
            goToLegacy(data.id);
        }
    }
    catch (error) {
        console.error('Erreur lors de la connexion:', error);
        alert('An error occurred while logging in');
    }
}

async function insertPlayer() {
    try {
        const response = await fetch('/api/game/insertplayer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Assuming you have CSRF protection enabled
            },
            body: JSON.stringify({
                username1: userAccount.username,
                username2: player2.username, //change to seconde player
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Game Data:', data);

            if (data.serializer_data) {
                const gameData = JSON.parse(data.serializer_data);  
                console.log('Player Data:', gameData);
          
                if (gameData.length > 0) {
                    const game = gameData[0].fields;  
                    console.log('game:', game);
                    if (game.player2 == null) {
                        waitingPlayer = 1;
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        insertPlayer();
                    } 
                    else 
                    {
                        waitingPlayer = 0;
        
                        //slide first player
                        const player1_pic = document.getElementById('player1-picture');
                        player1_pic.classList.add(...['slide-left']);
                        const player1_name = document.getElementById('player1-name');
                        player1_name.classList.add(...['slide-left']);
                        const player1_rank = document.getElementById('player1-rank');
                        player1_rank.classList.add(...['slide-left']);
        
                        //fadein second player
                        const player2_pic = document.getElementById('player2-picture');
                        player2_pic.classList.add(...['fade-in']);
                        const player2_name = document.getElementById('player2-name');
                        player2_name.classList.add(...['fade-in']);
                        const player2_rank = document.getElementById('player2-rank');
                        player2_rank.classList.add(...['fade-in']);
                        const versus_text = document.getElementById('versus-text');
                        versus_text.classList.add(...['fade-in']);
                        
                        //fadeout loading assets
                        loadingmodule = false;
                        const dotdotdot = document.getElementById('loading');
                        dotdotdot.classList.add(...['fade-out']);
                        const waiting_text = document.getElementById('opponent-text');
                        waiting_text.classList.add(...['fade-out']);
        
                        console.log("lancement dans 3");
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        console.log("lancement dans 2");
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        console.log("lancement dans 1");
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        //goToLegacy(data.id);
                    }
                }
            }
            else
            {
                waitingPlayer = 0;

                // const player1 = data.player1;
                // const player1_pic = document.getElementById('player1-picture');
                // const player1_name = document.getElementById('player1-name');
                // const player1_rank = document.getElementById('player1-rank');
                // const player2 = data.player2;
                // const player2_pic = document.getElementById('player2-picture');
                // const player2_name = document.getElementById('player2-name');
                // const player2_rank = document.getElementById('player2-rank');

                // player1_pic.src = player1.profile_picture;
                // player1_name.textContent = player1.username;
                // player1_rank.textContent = `Rank: ${player1.rank}`; 
                // player2_pic.src = player2.profile_picture;
                // player2_name.textContent = player2.username;
                // player2_rank.textContent = `Rank: ${player2.rank}`; 

                // player1_pic.classList.add(...['slide-left']);
                // player1_name.classList.add(...['slide-left']);
                // player1_rank.classList.add(...['slide-left']);
                // player2_pic.classList.add(...['fade-in']);
                // player2_name.classList.add(...['fade-in']);
                // player2_rank.classList.add(...['fade-in']);

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
        alert(i18n.global.t('error_login'));
    }
}

// async function insertPlayer() {
//     try {
//         const response = await fetch('/api/game/insertplayer/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCsrfToken() // Assuming you have CSRF protection enabled
//             },
//             body: JSON.stringify({
//                 username: userAccount.username,
//             })
//         });
//         if (response.ok) {
//             const data = await response.json();
//
//             if (data.serializer_data) {
//                 const gameData = JSON.parse(data.serializer_data);
//                 console.log('Player Data:', gameData);
//
//                 if (gameData.length > 0) {
//                     const game = gameData[0].fields;
//                     console.log('game:', game);
//                     game.player2 = "test 2"
//                     if (game.player2 == null) {
//                         waitingPlayer = 1;
//                         await new Promise(resolve => setTimeout(resolve, 1000));
//                         insertPlayer();
//                     }
//                     else
//                     {
//                         waitingPlayer = 0;
//
//                         //slide first player
//                         const player1_pic = document.getElementById('player1-picture');
//                         player1_pic.classList.add(...['slide-left']);
//                         const player1_name = document.getElementById('player1-name');
//                         player1_name.classList.add(...['slide-left']);
//                         const player1_rank = document.getElementById('player1-rank');
//                         player1_rank.classList.add(...['slide-left']);
//
//                         //fadein second player
//                         const player2_pic = document.getElementById('player2-picture');
//                         player2_pic.classList.add(...['fade-in']);
//                         const player2_name = document.getElementById('player2-name');
//                         player2_name.classList.add(...['fade-in']);
//                         const player2_rank = document.getElementById('player2-rank');
//                         player2_rank.classList.add(...['fade-in']);
//                         const versus_text = document.getElementById('console.log');
//                         versus_text.classList.add(...['fade-in']);
//
//                         //fadeout loading assets
//                         loadingmodule = false;
//                         const dotdotdot = document.getElementById('loading');
//                         dotdotdot.classList.add(...['fade-out']);
//                         const waiting_text = document.getElementById('opponent-text');
//                         waiting_text.classList.add(...['fade-out']);
//
//                         console.log("lancement dans 3");
//                         await new Promise(resolve => setTimeout(resolve, 1000));
//                         console.log("lancement dans 2");
//                         await new Promise(resolve => setTimeout(resolve, 1000));
//                         console.log("lancement dans 1");
//                         await new Promise(resolve => setTimeout(resolve, 1000));
//                         //goToLegacy(data.id);
//                     }
//                 }
//             }
//             else
//             {
//                 waitingPlayer = 0;
//
//                 //slide first player
//                 const player1_pic = document.getElementById('player1-picture');
//                 player1_pic.classList.add(...['slide-left']);
//                 const player1_name = document.getElementById('player1-name');
//                 player1_name.classList.add(...['slide-left']);
//                 const player1_rank = document.getElementById('player1-rank');
//                 player1_rank.classList.add(...['slide-left']);
//
//                 //fadein second player
//                 const player2_pic = document.getElementById('player2-picture');
//                 player2_pic.classList.add(...['fade-in']);
//                 const player2_name = document.getElementById('player2-name');
//                 player2_name.classList.add(...['fade-in']);
//                 const player2_rank = document.getElementById('player2-rank');
//                 player2_rank.classList.add(...['fade-in']);
//                 const versus_text = document.getElementById('versus-image');
//                 versus_text.classList.add(...['fade-in']);
//
//
//                 //fadeout loading assets
//                 loadingmodule = false;
//                 const dotdotdot = document.getElementById('loading');
//                 dotdotdot.classList.add(...['fade-out']);
//                 const waiting_text = document.getElementById('opponent-text');
//                 waiting_text.classList.add(...['fade-out']);
//
//                 await setTimeout(4000);
//                 // goToLegacy(data.id);
//             }
//
//         }
//     } catch (error) {
//         console.error('Erreur lors de la connexion:', error);
//         alert(i18n.global.t('error_login'));
//     }
// }

    ///////////////////////////////////////////////

    //dynamic "loading" dots 
    // console.log(loadingmodule);
    let dots;
    if (loadingmodule == true)
    {
        dots = window.setInterval( function() {
        var wait = document.getElementById('loading');
        // console.log(wait);
        if ( wait.innerHTML.length >= 3 ) 
            wait.innerHTML = ".";
        else 
            wait.innerHTML += ".";
        }, 1000);
    }

    var tips = [
        'Tip: Reading your phone in the stairs might lead to severe injury.',
        'Tip: Try pressing \'C\' while playing ;)', 
        'Tip: Wash your cereal bowl right after eating',
        'Don\'t forget to put your paddle back in the center!',
        'Recipe for a lribette : one tchoukball ball (?), 50 kilos of pasta, and many many many many many Star Wars anecdotes.',
        'Astuce: Tu es triste? Arrête.',
        '"Jeu de pain, jeu de vilain" - Miro',
        'Bois de l\'eau. Dans 20, 30 ans y\'en aura plus.',
        'Burc\'ya vaal burk\'yc, burc\'ya veman'
    ];
    var tipdisplayed = tips[Math.floor(Math.random()*tips.length)];

    function createPlyInput() {
        waitingPlayer = 0;

        const player1_pic = document.getElementById('player1-picture');
        const player1_name = document.getElementById('player1-name');
        const player1_rank = document.getElementById('player1-rank');

        player1_pic.src = userAccount.profilePicture;
        player1_name.textContent = userAccount.username;
        player1_rank.textContent = `Rank: ${userAccount.rank}`;

        //slide first player
        player1_pic.classList.add(...['slide-left']);
        player1_name.classList.add(...['slide-left']);
        player1_rank.classList.add(...['slide-left']);

        //fadein second player
        const player2_pic = document.getElementById('player2-picture');
        player2_pic.classList.add(...['fade-in']);
        const player2_name = document.getElementById('player2-name');
        player2_name.classList.add(...['fade-in']);
        const player2_rank = document.getElementById('player2-rank');
        player2_rank.classList.add(...['fade-in']);
        const versus_text = document.getElementById('versus-text');
        versus_text.classList.add(...['fade-in']);

        //fadeout loading assets
        loadingmodule = false;
        const dotdotdot = document.getElementById('loading');
        dotdotdot.classList.add(...['fade-out']);
        const waiting_text = document.getElementById('opponent-text');
        waiting_text.classList.add(...['fade-out']);
    }



    // const player1_pic = document.getElementById('player1-picture');
    //     const player1_name = document.getElementById('player1-name');
    //     const player1_rank = document.getElementById('player1-rank');

    //     player1_pic.src = userAccount.profilePicture;
    //     player1_name.textContent = userAccount.username;
    //     player1_rank.textContent = `Rank: ${userAccount.rank}`;

    //     //slide first player
    //     player1_pic.classList.add(...['slide-left']);
    //     player1_name.classList.add(...['slide-left']);
    //     player1_rank.classList.add(...['slide-left']);

    //     //fadein second player
    //     const player2_pic = document.getElementById('player2-picture');
    //     player2_pic.classList.add(...['fade-in']);
    //     const player2_name = document.getElementById('player2-name');
    //     player2_name.classList.add(...['fade-in']);
    //     const player2_rank = document.getElementById('player2-rank');
    //     player2_rank.classList.add(...['fade-in']);
    //     const versus_text = document.getElementById('versus-text');
    //     versus_text.classList.add(...['fade-in']);

    //     //fadeout loading assets
    //     loadingmodule = false;
    //     const dotdotdot = document.getElementById('loading');
    //     dotdotdot.classList.add(...['fade-out']);
    //     const waiting_text = document.getElementById('opponent-text');
    //     waiting_text.classList.add(...['fade-out']);


    async function validGame() {
        console.log(playerName2);
        validateGame = true;
        try {
        const response = await fetch('/api/game/createOneFalsePlayer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                username1: playerName2,
            })
        });
        if (response.ok) {


            const user = await response.json();
            if (user)
            {
                // console.log('Response data:', data);

                console.log("hereee");
                console.log(user);
                console.log(user.username);
                player2 = user
                console.log("hereee222");
                console.log(player2);
                console.log(player2.username);
                console.log(player2.rank);
                console.log(player2.username);

                    // const player2_pic = document.getElementById('player2-picture');
                    const player2_name = document.getElementById('player2-name');
                    // const player2_rank = document.getElementById('player2-rank');

                    // player2_pic.src = player2.profile_picture;
                    player2_name.textContent = player2.username;
                    // player2_rank.textContent = `Rank: ${player2.rank}`; 

                    // player2_pic.classList.add(...['fade-in']);
                    player2_name.classList.add(...['fade-in']);
                    // player2_rank.classList.add(...['fade-in']);

                    await createGameLocal();

            }
        }



            // const data = await response.json();
            // console.log('player Data:', data);

            // player2 = data;

            // console.log(player2);
            // console.log(player2.username);
            // // const player2_pic = document.getElementById('player2-picture');
            // const player2_name = document.getElementById('player2-name');
            // // const player2_rank = document.getElementById('player2-rank');

            // // player2_pic.src = data.profile_picture;
            // player2_name.textContent = data.username;
            // // player2_rank.textContent = `Rank: ${data.rank}`; 

            // // player2_pic.classList.add(...['fade-in']);
            // // player2_name.classList.add(...['fade-in']);
            // // player2_rank.classList.add(...['fade-in']);
        
    }
    catch (error) {
        console.error('Erreur lors de la connexion:', error);
        alert('An error occurred while logging in');
    }

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

#wrapper-matchmaking {
    display: flex;
    justify-content: center;
    align-items: center;
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

#versus-image{
    position: fixed;
    opacity: 0;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    size: 30%;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

#versus-image-new{
    position: fixed;
    left: 50%;
    opacity: 1;
}

.profile-picture-matchmaking-left {
    position: fixed;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 35%;
    left: 42vw;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.fade-in {
    opacity: 1;
    animation: fadeIn 0.7s;
    animation-fill-mode: forwards;
}

@keyframes fadeIn {
    0% { 
        opacity: 0;
    }
    100%
    { 
        opacity: 1;
    }
}

.fade-out {
    opacity: 0;
    animation: fadeOut 0.7s;
    animation-fill-mode: forwards;
}

@keyframes fadeOut {
    0% { 
        opacity: 1;
    }
    100%
    { 
        opacity: 0;
    }
}

.slide-left {
    position: fixed;
	animation: slide-left 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}

@keyframes slide-left {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-450px);
    }
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

#loading {
    position: fixed;
    visibility: visible;
    z-index: 5;
    font-size: 80px;
    font-weight: bold;
    text-align: center;
    top: 72%;
    left: 47.9%;
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.profile-picture-matchmaking-right {
    position: fixed;
    opacity: 0;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    top: 35%;
    left: 73%;
    border: 5px solid white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.opponent-text {
    position: fixed;
    z-index: 5;
    font-size: 30px;
    font-weight: bold;
    top: 24%;
    left: 50.3%;
    transform: translate(-50%, -50%);
    color: white;
    filter: drop-shadow(5px 5px 4px #0000003b);
}

.input-right {
    position: fixed;
    top: 68%;
    left: 74%;
    opacity: 0;
}

.button-valid {
    position: fixed;
    top: 74%;
    left: 77%;
    background-color: rgba(4, 255, 0, 0.25);
}

.button-valid:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>