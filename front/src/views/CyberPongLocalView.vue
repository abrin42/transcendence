<template>
  <main>
    <div id="wrapper">
      <CreateSoundButton id="sound-button-cyber" />
      <video id="video-cyber" loop autoplay muted preload="true" class="flex">
                <source src="./../assets/GameScene.mp4" type="video/mp4">
                    Your browser does not support the video element.
            </video>
      <div id="black-background">
        <div>
          <canvas id="board-cyber"></canvas>
        </div>
        <div>
          <h2 id="mute-cyber">{{ userAccount.mute }} {{ $t('to_mute_unmute') }}</h2>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
#app {
    position: relative; 
    height: 100vh; 
    overflow: hidden; 
}

body {
  padding: 0;
  margin: 0;
  text-align: center;
}

#sound-button-cyber{
  z-index: 4;
}

#video-cyber {
    z-index: 0;
    position: absolute;
    min-width: 100%;
    max-height: 100%;
    top: 50%;
    left: 50%;
    width: auto;
    height: auto;
    transform: translate(-50%, -50%);
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: flex-start;
}

#mute-cyber {
  position: absolute;
  font-family: 'CyberFont';
  font-size: 25px;
  z-index: 3;
  color: rgba(0, 255, 255, 0.8);
  left: 3%;
  top: 3%;
}

#black-background{
  height: 100vh;
  width: 100vw;
}

#board-cyber {
  position: absolute;
  z-index: 2;
  width: 70%;
  height: 100%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

@font-face {
  font-family: 'CyberFont';
  src: url('../assets/Cyberway-Riders.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}
</style>

<script setup>
  import { ref, inject, onMounted, onUnmounted } from 'vue';
  import paddleHitSound from '../assets/cyber_paddle_hit.mp3'
  import pointScoredSound from '../assets/cyber_point_scored.mp3'
  import wallHitSound from '../assets/cyber_wall_hit.mp3'
  import CreateSoundButton from '../components/CreateSoundButton.vue';
  import { useRouter } from 'vue-router';

  ////////////////////////////////////////////////
  /////// GET USER ///////////////////////////////
  ////////////////////////////////////////////////

  import { useUser } from '../useUser.js'; 
  const { getUser, userAccount, is_connected } = useUser(); 

  ////////////////////////////////////////////////
  ////////////////////////////////////////////////
  ////////////////////////////////////////////////
  
  const router = useRouter();
  const socket = ref(null);
  // const message = ref('');
  const messages = ref([]);
  const connectionStatus = ref('');
  let connection = 0;
  let canPlay = ref(0);
  
  ////////////Audio Variables///////////////
  const wallHitAudio = new Audio(wallHitSound);
  wallHitAudio.volume = 0.6;
  const paddleHitAudio = new Audio(paddleHitSound);
  paddleHitAudio.volume = 0.6;
  const pointScoredAudio = new Audio(pointScoredSound);
  pointScoredAudio.volume = 0.6;
  const isPlaying = inject('isPlaying');
  let soundOnOff;
  if (isPlaying == true)
    soundOnOff = true;
  else
    soundOnOff = false;
  /////////////////////////////////////////

  ///////////??????????////////////////////
  const currentUrl = window.location.href; 
  const lastSegment = currentUrl.split('/').filter(Boolean).pop();
  const gamePage = `game_${lastSegment}`;
  /////////////////////////////////////////
  
  //////////////BORDEL DU BACK///////////////////
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
            player1Score = responseData.scorep1;
            player2Score = responseData.scorep2;
            
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
    } catch (error) {
        console.error('Error updating game:', error);
    }
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
            console.log('rank updated successfully!', responseData);
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
            console.log('Game updated successfully!', responseData);

            if (responseData.message == 'isFirstPlayer' || responseData.message == 'isSecondePlayer')
            {
              canPlay.value = 1;
              console.log ("is player");
            }
            else if (responseData.message == 'isSpec')
            {
              canPlay.value = 0;
              console.log ("is spec");
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
          mode: "legacy",//CHANGER CA ICI???
          scorep1: player1Score,
          scorep2: player2Score,
          id: lastSegment,
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
    
  function connectWebSocket() {
  console.log(lastSegment);
  let hostName =  window.location.hostname;
  let port = window.location.port || '8443';
  socket.value = new WebSocket(`wss://${hostName}:${port}/ws/websockets/?page=${encodeURIComponent(gamePage)}`);
  socket.value.onopen = () => {
    console.log('WebSocket connecté');
    console.log(socket.value);
    socket.value.send(JSON.stringify({
      'type': "pointInit",
      'player': "1",
      'p1PTS': player1Score,
      'p2PTS': player2Score,
    }));
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
      // socket.value.close();
      await updateGameInfo();
      await setGameRank();
      router.push(`/legacyrecap/${lastSegment}`);
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
  //////////////////////////////////////////////////

  let moveUpP1;
  let moveDownP1;
  let moveUpP2;
  let moveDownP2;
  let mute;

  /////////////MOUNTED/////////////
  onMounted(async () => {
    await getUser();
    if (is_connected.value === false)
    __goTo('/');
    await getIsPlayer();
    await getGameInfo();
    connectWebSocket();
    board = document.getElementById("board-cyber");
    board.height = boardHeight;
    board.width = boardWidth;
    context = board.getContext("2d");

    /////Game controls//////
    moveUpP1 = userAccount.player1Up;
    moveDownP1 = userAccount.player1Down;
    moveUpP2 = userAccount.player2Up;
    moveDownP2 = userAccount.player2Down;
    mute = userAccount.mute;

    animationFrameId = requestAnimationFrame(update); // Gameloop

    if (canPlay.value == 1)
    {
      document.addEventListener("keydown", movePlayer1up);
      document.addEventListener("keydown", movePlayer1down);
      document.addEventListener("keydown", movePlayer2up);
      document.addEventListener("keydown", movePlayer2down);
      document.addEventListener("keydown", muteSound);
      document.addEventListener('keyup', stopPlayer);
    }
  });
  //////////////////////////////////

  /////////////UNMOUNTED/////////////
  onUnmounted(() => {
  if (canPlay.value == 1)
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
    document.removeEventListener('keyup', stopPlayer);
    document.removeEventListener("keydown", muteSound);
  }
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
  if (socket.value) {
    socket.value.close();
  }
});
  //////////////////////////////////

  /////////////GAME AKA MY SHIT/////////////
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
    speedX: 1, speedY: 2,
    trail: []
  }
    
  //score
  let player1Score = 0;
  let player2Score = 0;
    
function  updatePoints(player, updatePts)
{
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

  let animationFrameId = null;

  function update() 
    {
      //LES POSITIONS DES PLAYERS NE CHANGENT PAS
      // console.log(player1.x);
      // console.log(player1.y);
        animationFrameId = requestAnimationFrame(update);
        context.clearRect(0, 0, board.width, board.height); // clear rectangle after movement (remove previous paddle position)
        //PLAYER SETTINGS
        context.shadowBlur = 15;
        context.shadowOffsetX = 0;
        context.shadowOffsetY = 0;
        context.font = "125px CyberFont";
        //PLAYER 1
        context.fillStyle = 'rgba(0, 255, 255, 0.9)';
        context.shadowColor = 'rgba(0, 255, 255, 0.8)'; // cyan
        context.fillRect(player1.x, player1.y, player1.width, player1.height); 
        //P1 SCORE
        context.fillStyle = 'rgba(0, 255, 255)';
        context.fillText(player1Score, boardWidth/5, 125);
        //PLAYER 2
        context.fillStyle = 'rgba(255, 0, 255, 0.9)';
        context.shadowColor = 'rgba(255, 0, 255, 0.8)'; // Neon pink
        context.fillRect(player2.x, player2.y, player2.width, player2.height);
        //P2 SCORE
        context.fillStyle = 'rgba(255, 0, 255)';
        context.fillText(player2Score, boardWidth*4/5 -50 , 125);
        //BALL
        //DRAW LIGHT TRAIL EFFECT TEST ON PRIE LA TEAM
        let effectOpacity = 0.1;
        let fadeDistance = 10;
        // Store the current position before updating
        ball.trail.push({ x: ball.x, y: ball.y });
        // Limit the trail length
        if (ball.trail.length > fadeDistance) {
          ball.trail.shift();
        }
        ball.trail.forEach((pos, index) => {
          context.fillStyle = `rgba(255, 255, 51, ${effectOpacity - index * (effectOpacity / fadeDistance)})`;
          context.shadowBlur = 25;
          context.shadowColor = 'rgba(255, 255, 51)';
          //CHATGPT DID THIS
          let maxOpacity = 0.7;
          const distance = Math.sqrt(
            Math.pow(pos.x - ball.x, 2) + Math.pow(pos.y - ball.y, 2)
          );
          const opacity = Math.max(0, maxOpacity - (distance / 70));
          //////////////////
          context.fillStyle = `rgba(255, 255, 51, ${opacity})`;
          context.fillRect(pos.x -5, pos.y, ball.width, ball.height);
          context.fillStyle = 'rgba(255, 255, 51)'; //yellow
          context.shadowColor = 'rgba(255, 255, 51, 0.5)'; //yellow shadow
          //DRAW BALL ON TOP OF TRAIL
          context.fillRect(ball.x- (ball.width/2), ball.y, ball.width, ball.height);
        });
  }
    
  let moveInterval1up = null;
  let moveInterval1down = null;
  let moveInterval2up = null;
  let moveInterval2down = null;
  let tickPadel = 10;

  //////Movement functions//////
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