<template>
  <main>
    <div id="wrapper">
      <div id="black-background">
        <div>
          <canvas id="board" ref="neonLayer"></canvas>
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
  padding: 0;
  margin: 0;
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
  padding: 0;
  margin: 0;
  border: 0;
  width: 700px;
  height: 700px;
}

@font-face {
  font-family: 'CyberFont';
  src: url('../assets/Cyberway-Riders.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}
</style>

<script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import paddleHitSound from '../assets/paddle_hit.mp3'
  import pointScoredSound from '../assets/point_scored.mp3'
  import wallHitSound from '../assets/wall_hit.mp3'
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
  const paddleHitAudio = new Audio(paddleHitSound);
  const pointScoredAudio = new Audio(pointScoredSound);
  let soundOnOff = true;
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

            if (responseData.message == 'isPlayer')
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
          mode: "legacy",
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
    
  function connectWebSocket()
  {
    console.log(lastSegment);
    socket.value = new WebSocket(`wss://localhost:8443/ws/websockets/?page=${encodeURIComponent(gamePage)}`);
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
      else if (data.type == 'mouvUp' || data.type == 'mouvDown')
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

    socket.value.onerror = (error) => {
      console.error('Erreur WebSocket:', error);
    };

    socket.value.onclose = () => {
      console.log('WebSocket déconnecté, tentative de reconnexion...');
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
  //////////////////////////////////////////////////

  /////////////MOUNTED/////////////
  onMounted(async () => {
    await getUser();
    if (is_connected.value === false)
    __goTo('/');
    await getIsPlayer();
    connectWebSocket();
    board = document.getElementById("board");
    board.height = boardHeight;
    board.width = boardWidth;
    context = board.getContext("2d"); //Drawing on board
    context.fillStyle = "white";
    context.fillRect(player1.x, player1.y, player1.width, player1.height);
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
      document.removeEventListener("keydown", movePlayer1up);
      document.removeEventListener("keydown", movePlayer1down);
      document.removeEventListener("keydown", movePlayer2up);
      document.removeEventListener("keydown", movePlayer2down);
      document.removeEventListener("keydown", muteSound);
      document.removeEventListener('keyup', stopPlayer);
    }
    moveInterval1up = null;
    moveInterval1down = null;
    moveInterval2up = null;
    moveInterval2down = null;
    if (animationFrameId)
    {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
    }
    if (socket.value) 
    {
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

  //players properties
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
    speedX: 1, speedY: 2
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
    
  let moveInterval1up = null;
  let moveInterval1down = null;
  let moveInterval2up = null;
  let moveInterval2down = null;
  let tickPadel = 10;

  /////Game controls//////
  let moveUpP1 = "KeyW";
  let moveDownP1 = "KeyS";
  let moveUpP2 = "ArrowUp";
  let moveDownP2 = "ArrowDown";
  let mute = userAccount.mute;

  //////Movement functions//////
  function movePlayer1up(e)
  {
    console.log("key pressed up");
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