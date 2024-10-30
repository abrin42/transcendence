<script setup>
import CreateDropupButton from '@/components/CreateDropupButton.vue';
import CreateBackButton from '@/components/CreateBackButton.vue';
import NeonText from '@/components/NeonText.vue';
import Input from '@/components/Input.vue'; // Assurez-vous que ce composant Input existe

import { useRouter } from 'vue-router';
import { onBeforeMount, ref, watch, onUnmounted } from 'vue';
import { useUser } from '../useUser.js';
import i18n from '../i18n.js';

const { getUser, userAccount, is_connected } = useUser();
const router = useRouter();
const timer = ref(10);
let interval = null;

// Charger les utilisateurs et démarrer le timer si 4 participants
onBeforeMount(async () => {
    await getUser();
});

// Navigation vers une autre page
function __goTo(page) {
    if (page) {
        router.push(page);
    }
}

// Liste des participants
const participants = ref([]);

// Référence pour les nouveaux participants
const newParticipants = ref(["", "", "", ""]);

// Matches de tournoi
const matches = ref([
    { round: 'SEMI', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' },
    { round: 'SEMI', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' },
    { round: 'SMALL_FINAL', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' },
    { round: 'FINAL', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' }
]);

// Fonction pour mélanger les participants
function shuffleParticipants() {
    for (let i = participants.value.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [participants.value[i], participants.value[j]] = [participants.value[j], participants.value[i]];
    }
}

// Démarrer le tournoi si le nombre de participants est de 4
async function startTournament() {

    if (participants.value.length === 4) {
        createFalsePlayer(participants.value[0].name, participants.value[1].name, participants.value[2].name, participants.value[3].name);

        shuffleParticipants(); // Mélange les participants
        setupSemiFinals(); // Configure les demi-finales
        for (let i = 0; i < 4; ++i) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            await start_game(i);
            updateScore(i);
            // await new Promise(resolve => setTimeout(resolve, 1000));
            // await start_game();
            // updateScore(1);
            // await new Promise(resolve => setTimeout(resolve, 1000));
            // await start_game();
            // updateScore(2);
            // await new Promise(resolve => setTimeout(resolve, 1000));
            // await start_game();
            // updateScore(3);
        }
        // updateFinals();
        // startTimer();
    }
}

// Configuration des demi-finales avec les participants mélangés
function setupSemiFinals() {
    matches.value[0].team1 = '#' + participants.value[0].name;
    matches.value[0].team2 = '#' + participants.value[1].name;
    matches.value[1].team1 = '#' + participants.value[2].name;
    matches.value[1].team2 = '#' + participants.value[3].name;
}

// Fonction pour ajouter les participants
function addParticipants() {
    const filteredParticipants = newParticipants.value.filter(name => name.trim() !== "");

    if (filteredParticipants.length === 4) {
        const participantsWithoutDuplicates = new Set(filteredParticipants);
        if (participantsWithoutDuplicates.size !== filteredParticipants.length) {
            alert(i18n.global.t('error_cannot_use_same_nickname'));
        } else {
            participants.value = filteredParticipants.map(name => ({ name }));
            startTournament();
        }
    } else {
        alert(i18n.global.t('please_enter_4_valid_names'));
    }
}

// Mettre à jour les finales
function updateScore(match_index) {
    matches.value[match_index].score1 = player1Score;
    matches.value[match_index].score2 = player2Score;
    player1Score = 0;
    player2Score = 0;
    if (matches.value[match_index].score1 > matches.value[match_index].score2) {
        matches.value[match_index].winner = matches.value[match_index].team1;
        matches.value[match_index].loser = matches.value[match_index].team2;
    } else {
        matches.value[match_index].winner = matches.value[match_index].team2;
        matches.value[match_index].loser = matches.value[match_index].team1;
    }
    switch (match_index) {
        case 0:
            matches.value[2].team1 = matches.value[match_index].loser;
            matches.value[3].team1 = matches.value[match_index].winner;
            break;
        case 1:
            matches.value[2].team2 = matches.value[match_index].loser;
            matches.value[3].team2 = matches.value[match_index].winner;
            break;
        default:
            break;
    }
}

// Mettre à jour les finales
function updateFinals() {
    const semi1 = matches.value[0];
    const semi2 = matches.value[1];

    if (semi1.winner && semi2.winner) {
        matches.value[3].team1 = semi1.winner;
        matches.value[3].team2 = semi2.winner;
    }
}

// Fonction pour démarrer le timer
function startTimer() {
    if (!interval) {
        interval = setInterval(() => {
            timer.value--;
            if (timer.value === -1) {
                alert(i18n.global.t('GAME_STARTS_SOON'));
                stopTimer();
            }
        }, 1000);
    }
}

// Fonction pour arrêter le timer
function stopTimer() {
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
}

onUnmounted(() => {
    stopTimer();
});




import paddleHitSound from '../assets/paddle_hit.mp3'
import pointScoredSound from '../assets/point_scored.mp3'
import wallHitSound from '../assets/wall_hit.mp3'

////////////////////////////////////////////////
/////// GET USER ///////////////////////////////
////////////////////////////////////////////////

onBeforeMount(async () => {
      await getUser();
      if (is_connected.value === false)
          __goTo('/')
  });

async function end_game()
{
    // if (canPlay.value == 1)
    // {
        clearInterval(moveInterval1up);
        moveInterval1up = null;
        document.removeEventListener("keydown", movePlayer1up);
        clearInterval(moveInterval1down);
        moveInterval1down = null;
        document.removeEventListener("keydown", movePlayer1down);
        clearInterval(moveInterval2up);
        moveInterval2up = null;
        document.removeEventListener("keydown", movePlayer2up);
        clearInterval(moveInterval2down);
        moveInterval2down = null;
        document.removeEventListener("keydown", movePlayer2down);
        document.removeEventListener('keyup', stopPlayer);
        document.removeEventListener("keydown", muteSound);
    // }
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
    if (socket.value) {
        socket.value.close();
    }
    canPlay.value = 0;
    ball.x  =  boardWidth / 2;
    ball.y = boardHeight / 2;
    player1.y =  boardHeight/5*2;
    player2.y =  boardHeight/5*2;
}

let moveUpP1;
let moveDownP1;
let moveUpP2;
let moveDownP2;
let mute;

async function start_game(i) {

    await getUser();
    await createGameLocal(i);
    connectWebSocket();
    board = document.getElementById("board");
    board.height = boardHeight;
    board.width = boardWidth;
    context = board.getContext("2d"); //Drawing on board

    context.fillStyle = "white";
    context.fillRect(player1.x, player1.y, player1.width, player1.height);

    /////Game controls//////
    moveUpP1 = userAccount.player1Up;
    moveDownP1 = userAccount.player1Down;
    moveUpP2 = userAccount.player2Up;
    moveDownP2 = userAccount.player2Down;
    mute = userAccount.mute;

    animationFrameId = requestAnimationFrame(update); // Gameloop

    // if (canPlay.value == 1)
    // {
        document.addEventListener("keydown", movePlayer1up);
        document.addEventListener("keydown", movePlayer1down);
        document.addEventListener("keydown", movePlayer2up);
        document.addEventListener("keydown", movePlayer2down);
        document.addEventListener("keydown", muteSound);
        document.addEventListener('keyup', stopPlayer);
    // }
    canPlay.value = 1;
    while (canPlay.value == 1)
    {
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}

////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////

const socket = ref(null);
// const message = ref('');
const messages = ref([]);
const connectionStatus = ref('');
let connection = 0;
let canPlay = ref(0);

////////////Audio Variables///////////////
const wallHitAudio = new Audio(wallHitSound);
const paddleHitAudio = new Audio(paddleHitSound);
const pointScoredAudio = new Audio(pointScoredSound);
let soundOnOff = true;
const currentUrl = window.location.href; 
const lastSegment = currentUrl.split('/').filter(Boolean).pop();
const gamePage = `game_${lastSegment}`;

let current_game_id = ref(0);


function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }


    async function createGameLocal(i)
{
    try {
        const response = await fetch('/api/game/create_game_local/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken() // Assuming you have CSRF protection enabled
            },
            body: JSON.stringify({
                username1: matches.value[i].team1,
                username2: matches.value[i].team2, //change to seconde player
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log('---Game Data:', data);

            current_game_id.value = data.id;

        }
    }
    catch (error) {
        console.error('Erreur lors de la connexion:', error);
        alert(i18n.global.t('error_login'));
    }
}




async function createFalsePlayer(user1, user2, user3 ,user4)
{
    try {
        const response = await fetch('/api/game/createFalsePlayer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                username1: user1,
                username2: user2,
                username3: user3,
                username4: user4,
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Game Data:', data);
        }
    }
    catch (error) {
        console.error('Erreur lors de la connexion:', error);
        alert(i18n.global.t('error_login'));
    }
}



//     async function setGameRank() {
//     try {
//         const response = await fetch('/api/game/setGameRank/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCsrfToken(),
//             },
//             body: JSON.stringify({
//                 id: lastSegment,
//             }),
//         });
//         if (response.ok) {
//             const responseData = await response.json();
//             console.log('rank updated successfully!', responseData);
//         }
//         else
//         {
//             const errorData = await response.json();
//             console.error('Error:', errorData.error);
//         }
//     } catch (error) {
//         console.error('Error updating game:', error);
//     }
// }


async function updateGameInfo() {
    try {
        const response = await fetch('/api/game/update_game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                mode: "legacy",
                scorep1: player1Score,
                scorep2: player2Score,
                id: current_game_id.value,
            }),
        });
        if (response.ok) {
            const responseData = await response.json();
            console.log('Game updated successfully!', responseData);
        } else {
            const errorData = await response.json();
            console.error('Error:', errorData.error);
        }
    } catch (error) {
        console.error('Error updating game:', error);
    }
}

    //board properties
    let board;
    let boardWidth = 700;
    let boardHeight = 700;
    let context;

    //players propertiesupdate_game
    let playerWidth = 20;
    let playerHeight = boardHeight/5;
    let playerSpeed = 0;

    let player1 = {
        x : 10,
        y: boardHeight/5*2,
        width : playerWidth,
        height : playerHeight,
        speed : playerSpeed
    }

    let player2 = {
        x : boardWidth - playerWidth - 10,
        y: boardHeight/5*2, 
        width : playerWidth,
        height : playerHeight,
        speed: playerSpeed
    }

    //ball properties
    let ballSize = 10;
    let ball = {
    x : boardWidth / 2,
    y : boardHeight / 2,
    width : ballSize,
    height : ballSize,
    }
    
    //score
    let player1Score = 0;
    let player2Score = 0;
    

function  updatePoints(player, updatePts)
{
// console.log(player);
// console.log(updatePts);
if (player == 1)
{
    player1Score = updatePts;
}
else if (player == 2)
{
    player2Score = updatePts;
}
}

function  updatePadel(player, newY)
{
if (player == 1)
{
    player1.y = newY;
}
else if (player == 2)
{
    player2.y = newY;
}
}

function updateBaal(x, y)
{
ball.x = x;
ball.y = y;
}

function connectWebSocket() {
console.log(lastSegment);
let hostName =  window.location.hostname;
let port = window.location.port || '8443';
socket.value = new WebSocket(`wss://${hostName}:${port}/ws/websockets/?page=${encodeURIComponent(gamePage)}`);

socket.value.onopen = () => {
    console.log('WebSocket connecté');
    console.log(socket.value);
};


socket.value.onmessage = async (event) => {
    // console.log("---ON MESSAGE---");
    
    const data = JSON.parse(event.data);
    
    if (data.type == 'connection_success') 
    {

    // console.log(data.type);
    // console.log(data.message);
    // connectionStatus.value = data.message;
    connection = 1;
    }
    else if (data.type == 'updatePts') //sound
    {
    // console.log(data.type);
    // console.log(data.updatePts);
    // console.log(data.player);
    updatePoints(data.player, data.updatePts);
    if (soundOnOff == true)
    pointScoredAudio.play();
    await updateGameInfo();
    } 
    else if (data.type == 'updatePaddle')
    {
    updatePadel(data.player, data.newY);
    // messages.value.push(data.type);
    }
    else if (data.type == 'updateBaal')
    {
    // console.log(data.x);
    // console.log(data.y);
    updateBaal(data.x, data.y);
    }
    else if (data.type == 'endGame')
    {
    connection = 0;
    // console.log(data.type);
    await updateGameInfo();
    // await setGameRank();
    await end_game();
    // socket.value.close();
    // router.push(`/legacyrecap/${lastSegment}`);
    }
    else if (data.type == 'startGame')
    {
    await updateGameInfo();
    // console.log(data.type);
    }
    else if (data.type == 'paddleHit')
    {
    // console.log(data.type);
    if (soundOnOff == true)
        paddleHitAudio.play();
    }
    else if (data.type == 'wallHit')
    { 
    // console.log(data.type);
    if (soundOnOff == true)
        wallHitAudio.play();
    }
    else if (data.type == 'info_back') //a enlever test
    {
    // console.log(data.type);
    // console.log(data.value_back1);
    // console.log(data.value_back2);
    // console.log(data.value_back3);
    }
    // console.log("---END ON MESSAGE---");
};
}


function sendMessage(msg) {
if (socket.value && socket.value.readyState === WebSocket.OPEN) 
{
    socket.value.send(JSON.stringify({
    'type': msg.type,
    'player': msg.player,
    }));
}
else 
{
    console.error('WebSocket non connecté');
}
}

let animationFrameId = null;


    function update() 
    {
        // console.log("boucle game update");
        animationFrameId = requestAnimationFrame(update);
        console.log();
        context.clearRect(0, 0, board.width, board.height); // clear rectangle after movement (remove previous paddle position)
        context.fillRect(player1.x, player1.y, player1.width, player1.height); 
        context.fillRect(player2.x, player2.y, player2.width, player2.height);
        context.fillStyle = "white";
        context.fillRect(ball.x- (ball.width/2), ball.y, ball.width, ball.height);
        //draw score
        context.font = "100px Arial";
        context.fillText(player1Score, boardWidth/5, 100);
        context.fillText(player2Score, boardWidth*4/5 -50 , 100); //subtract -45 for width of tex
        
        //draw middle line
        for (let i = 10; i < board.height; i += 25)
        {
            context.fillRect(board.width / 2 - 1, i, 2, 15);
        }
    }
    
    let moveInterval1up = null;
    let moveInterval1down = null;
    let moveInterval2up = null;
    let moveInterval2down = null;
    let tickPadel = 10;

    function movePlayer1up(e)
    {
    if (!moveInterval1up)
    {
        if (e.code == moveUpP1)
        {
        moveInterval1up = setInterval(() => 
        {
            const message = 
            {
            type: "mouvUp",
            player: "1",
            };
            sendMessage(message);                    
            
        },
        tickPadel);
        }
    }
    }

    function movePlayer1down(e)
    {
    if (!moveInterval1down)
    {
        if (e.code == moveDownP1)
        {
        moveInterval1down = setInterval(() => 
        {
            const message = 
            {
            type: "mouvDown",
            player: "1",
            };
            sendMessage(message);                    
        },
        tickPadel);
        }
    }
    }
    
    function movePlayer2up(e)
    {
    if (!moveInterval2up)
    {
        if (e.code == moveUpP2)
        {
        moveInterval2up = setInterval(() => 
        {
            const message = 
            {
            type: "mouvUp",
            player: "2",
            };
            sendMessage(message);                    
            
        },
        tickPadel);
        }
    }
    }

    function movePlayer2down(e)
    {
    if (!moveInterval2down)
    {
        if (e.code == moveDownP2)
        {
        moveInterval2down = setInterval(() => 
        {
            const message = 
            {
            type: "mouvDown",
            player: "2",
            };
            sendMessage(message);                    
        },
        tickPadel);
        }
    }
    }

    function muteSound(e)
    {
    if (e.code == mute)
    {
        console.log(soundOnOff);
        soundOnOff = !soundOnOff;
        console.log(soundOnOff);
    }
    }


    function stopPlayer(e) {
    if (e.code == moveUpP1)
    {  
        clearInterval(moveInterval1up);
        moveInterval1up = null;
    }
    else if(e.code == moveDownP1)
    {
        clearInterval(moveInterval1down);
        moveInterval1down = null;
    }
    else if (e.code == moveUpP2)
    {  
        clearInterval(moveInterval2up);
        moveInterval2up = null;
    }
    else if (e.code == moveDownP2)
    {
        clearInterval(moveInterval2down);
        moveInterval2down = null;
    }
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div id="black-background">
                <div>
                    <canvas id ="board" ></canvas>
                </div>
                <div>
                    <h2 id="mute">[{{ userAccount.mute }}] {{ $t('to_mute_unmute') }}</h2>
                </div>
            </div>
            <div class="theme">
                <!-- Si le nombre de participants est différent de 4, affiche la configuration -->
                <div v-if="participants.length !== 4" class="custom-content">
                    <h2>{{ $t('add_participants') }}</h2>
                    <div v-for="(participant, index) in newParticipants" :key="index">
                        <Input v-model="newParticipants[index]" :placeholderText="`${$t('name_of_participant')} [${index}]`" />
                    </div>
                    <button class="button buttonText" @click="addParticipants">{{ $t('validate_participants') }}</button>
                </div>

                <!-- Si le nombre de participants est égal à 4, affiche le bracket et le timer -->
                <div v-if="participants.length === 4">
                    <CreateDropupButton />
                    <CreateBackButton />
                    <div class="bracket">
                        <!-- Demi-finales -->
                        <div class="column one">
                            <NeonText :position="{ top: 30, left: 27 }" :fontSize="1">{{ $t('semi_finals') }}</NeonText>
                            <div v-for="(match, index) in matches.slice(0, 2)" :key="index" class="match semi">
                                <div class="match-top team">
                                    <span class="name">{{ match.team1 }}</span>
                                    <span class="score">{{ match.score1 ?? '-' }}</span>
                                </div>
                                <div class="match-bottom team">
                                    <span class="name">{{ match.team2 }}</span>
                                    <span class="score">{{ match.score2 ?? '-' }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Finale -->
                        <div class="column final">
                            <div v-for="(match, index) in matches.slice(3, 4)" :key="index" class="match big-final">
                                <div v-if="match.team1 && match.team2">
                                    <NeonText :position="{ top: 30, left: 46 }" :fontSize="1">{{ $t('final') }}</NeonText>
                                    <div class="match-top team">
                                        <span class="name">{{ match.team1 }}</span>
                                        <span class="score">{{ match.score1 ?? '-' }}</span>
                                    </div>
                                    <div class="match-bottom team">
                                        <span class="name">{{ match.team2 }}</span>
                                        <span class="score">{{ match.score2 ?? '-' }}</span>
                                    </div>
                                </div>
                                <div v-else>
                                    <span class="finale-text">{{ $t('matches_not_yet_decided') }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Petite finale -->
                        <div class="column third-place">
                            <div v-for="(match, index) in matches.slice(2, 3)" :key="index" class="match small-final">
                                <div v-if="match.team1 && match.team2">
                                    <NeonText :position="{ top: 30, left: 68 }" :fontSize="1">{{ $t('small_final') }}</NeonText>
                                    <div class="match-top team">
                                        <span class="name">{{ match.team1 }}</span>
                                        <span class="score">{{ match.score1 ?? '-' }}</span>
                                    </div>
                                    <div class="match-bottom team">
                                        <span class="name">{{ match.team2 }}</span>
                                        <span class="score">{{ match.score2 ?? '-' }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Timer en bas à droite -->
                    <div v-if="participants.length === 4" class="button timer">
                        {{ Math.floor(timer / 60) }}:{{ ('0' + (timer % 60)).slice(-2) }}
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>


<style scoped lang="scss">
.wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.theme {
    height: 100%;
    width: 100%;
    position: absolute;
    background-color: rgba(0, 0, 0, 0.5);
}

.bracket {
    display: flex;
    flex-direction: row;
    padding: 20vw 0;
    margin-left: 20vw;
}

.column {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
}

/* Styles pour la section de configuration si participants !== 4 */
.custom-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: white;
}

.code-content {
    margin-top: 20px;
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 10px;
}

.match {
    display: flex;
    flex-direction: column;
    margin: 2vw 4vw;
    position: relative;
}

.match.semi {
    width: 12vw;
    height: 6vh;
}

.match.big-final {
    width: 16vw;
    height: 8vh;
    position: relative;
    bottom: 4vh;
    left: -4vw;
}

.match.small-final {
    width: 14vw;
    height: 7vh;
    position: relative;
    bottom: 2vh;
    left: -4vw;
}

.team {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5vh;
    padding: 0.5vh 0.5vw;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    background-color: rgba(0, 0, 0, 0.25);
    color: rgb(255, 255, 255);
}

.team .score {
    color: rgba(255, 20, 147, 0.6);
}

.finale-text {
    color: white;
    font-size: 1rem;
    position: relative;
    bottom: -12vh;
    left: 15vw;
}

/* Styles pour le timer */
.timer {
    position: fixed;
    bottom: 20px;
    right: 20px;
    font-size: 2em;
    color: white;
    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(255, 20, 147, 1);
    border-style: groove;
    padding: 10px;
    border-radius: 5px;
}

  body {
    text-align: center;
  }
  
  #mute {
    color: rgb(114, 114, 114);
    font-size: 25px;
    left: 20%;
    top: 67%;
  }
  
  #black-background{
    height: 100vh;
    width: 100vw;
    background-color: black;
  }
  
  #board {
    background-color: black;
    border: 5px solid white;
    width: 700px;
    height: 700px;
  }
  </style>
  
  