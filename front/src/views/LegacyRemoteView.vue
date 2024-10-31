<template>
  <main>
    <div id="wrapper">
      <div id="black-background">
        <div>
          <canvas id ="board"></canvas>
        </div>
        <div>
          <h2 id="mute">[{{ userAccount.mute }}] {{ $t('to_mute_unmute') }}</h2>
        </div>
      </div>
    </div>
  </main>
</template>

<style lang="scss">
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

<script setup>
import { ref, onMounted, onUnmounted, onBeforeMount } from 'vue';
import paddleHitSound from '../assets/paddle_hit.mp3'
import pointScoredSound from '../assets/point_scored.mp3'
import wallHitSound from '../assets/wall_hit.mp3'
import { useRouter } from 'vue-router';

  ////////////////////////////////////////////////
  /////// GET USER ///////////////////////////////
  ////////////////////////////////////////////////

  import { useUser } from '../useUser.js'; 
  const { getUser, userAccount, is_connected } = useUser(); 

  onBeforeMount(async () => {
      await getUser();
      if (is_connected.value === false)
        __goTo('/')
  });

  let moveUpP1;
  let moveDownP1;
  let mute = userAccount.mute;

  onUnmounted(() => {
  if (canPlay.value == 1 || canPlay.value == 2)
  {
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
    document.removeEventListener('keyup', stopPlayer1);
    document.removeEventListener('keyup', stopPlayer2);
    document.removeEventListener("keydown", muteSound);
  }
  moveInterval1up = null;
  moveInterval1down = null;
  moveInterval2up = null;
  moveInterval2down = null;
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  if (socket.value) {
    socket.value.close();
  }
});

onMounted(async () => {
  await getUser();
  await getIsPlayer();
  connectWebSocket();
  board = document.getElementById("board");
  board.height = boardHeight;
  board.width = boardWidth;
  context = board.getContext("2d");

  /////Game controls//////
  moveUpP1 = userAccount.player1Up;
  moveDownP1 = userAccount.player1Down;
  mute = userAccount.mute;

  context.fillStyle = "white";
  context.fillRect(player1.x, player1.y, player1.width, player1.height);
  animationFrameId = requestAnimationFrame(update);
});

  ////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////

  const router = useRouter();
  const socket = ref(null);
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
const gamePage = `remote_${lastSegment}`;

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

    async function setGameRank() {
    try {
        const response = await fetch('/api/game/setGameRank/', {
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

    async function getIsPlayer() {
    try {
        const response = await fetch('/api/game/getIsPlayer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                player: userAccount.username,
                id: lastSegment,
            }),
        });
        if (response.ok) {
            const responseData = await response.json();
            if (responseData.message == 'isFirstPlayer')
            {
              document.addEventListener("keydown", movePlayer1up);
              document.addEventListener("keydown", movePlayer1down);
              document.addEventListener("keydown", muteSound);
              document.addEventListener('keyup', stopPlayer1);
              canPlay.value = 1;
            }
            else if (responseData.message == 'isSecondePlayer')
            {
              document.addEventListener("keydown", movePlayer2up);
              document.addEventListener("keydown", movePlayer2down);
              document.addEventListener("keydown", muteSound);
              document.addEventListener('keyup', stopPlayer2);

              canPlay.value = 2;
            }
            else if (responseData.message == 'isSpec')
            {
              canPlay.value = 0;
            }
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
                id: lastSegment,
            }),
        });
        if (response.ok) {
            const responseData = await response.json();
        } else {
            const errorData = await response.json();
            console.error('Error:', errorData.error);
        }
    } catch (error) {
        console.error('Error updating game:', error);
    }
  }

    let board;
    let boardWidth = 700;
    let boardHeight = 700;
    let context;

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

    let ballSize = 10;
    let ball = {
      x : boardWidth / 2,
      y : boardHeight / 2,
      width : ballSize,
      height : ballSize,
      speedX: 1, speedY: 2
    }
    let player1Score = 0;
    let player2Score = 0;
    

function  updatePoints(player, updatePts)
{
  if (player == 1 || player == -1)
  {
    player1Score = updatePts;
  }
  else if (player == 2 || player == -2)
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
  let hostName =  window.location.hostname;
  let port = window.location.port || '8443';
  socket.value = new WebSocket(`wss://${hostName}:${port}/ws/websockets/?page=${encodeURIComponent(gamePage)}`);
  socket.value.onopen = () => {

  };
  
  
  socket.value.onmessage = async (event) => {
    const data = JSON.parse(event.data);    
    if (data.type == 'connection_success') 
    {
      connection = 1;
    }
    else if (data.type == 'updatePts')
    {
      updatePoints(data.player, data.updatePts);
      if (soundOnOff == true && (data.player == 1 || data.player == 2))
        pointScoredAudio.play();
      await updateGameInfo();
    } 
    else if (data.type == 'updatePaddle') 
    {
      updatePadel(data.player, data.newY);
    }
    else if (data.type == 'updateBaal' || data.type == 'update_baal')
    {
      updateBaal(data.x, data.y);
    }
    else if (data.type == 'endGame')
    {
      connection = 0;
      await updateGameInfo();
      await setGameRank();
      router.push(`/legacyrecap/${lastSegment}`);
    }
    else if (data.type == 'startGame')
    {
      await updateGameInfo();
    }
    else if (data.type == 'paddleHit')
    {
      if (soundOnOff == true)
        paddleHitAudio.play();
    }
    else if (data.type == 'wallHit')
    { 
      if (soundOnOff == true)
        wallHitAudio.play();
    }
  };

  socket.value.onerror = (error) => {
    console.error('Erreur WebSocket:', error);
  };

  socket.value.onclose = () => {
    setTimeout(() => 
    {
      if (connection != 0)
        connectWebSocket();
    }, 3000);
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
        animationFrameId = requestAnimationFrame(update);
        context.clearRect(0, 0, board.width, board.height);
        context.fillRect(player1.x, player1.y, player1.width, player1.height); 
        context.fillRect(player2.x, player2.y, player2.width, player2.height);
        context.fillStyle = "white";
        context.fillRect(ball.x- (ball.width/2), ball.y, ball.width, ball.height);
        context.font = "100px Arial";
        context.fillText(player1Score, boardWidth/5, 100);
        context.fillText(player2Score, boardWidth*4/5 -50 , 100);
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
        if (e.code == moveUpP1)
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
        if (e.code == moveDownP1)
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
        soundOnOff = !soundOnOff;
s      }
    }

    function stopPlayer1(e) {
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
    }

    function stopPlayer2(e) {
      if (e.code == moveUpP1)
      {  
        clearInterval(moveInterval2up);
        moveInterval2up = null;
      }
      else if (e.code == moveDownP1)
      {
        clearInterval(moveInterval2down);
        moveInterval2down = null;
      }
    }
</script>