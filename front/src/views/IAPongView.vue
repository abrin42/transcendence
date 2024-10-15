<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const socket = ref(null);
// const message = ref('');
const messages = ref([]);
const connectionStatus = ref('');
let connection = 0;

////////////////////////////////////////////////
/////// GET USER ///////////////////////////////
////////////////////////////////////////////////

import { useUser } from '../useUser.js'; 
const { getUser, userAccount, is_connected } = useUser(); 

onMounted(async () => {
    await getUser();
    if (is_connected.value === false)
      __goTo('/')
      connectWebSocket();
  board = document.getElementById("board"); //link board element in template to board variable
  board.height = boardHeight;
  board.width = boardWidth;
  context = board.getContext("2d"); //Drawing on board

  context.fillStyle = "white";
  context.fillRect(player1.x, player1.y, player1.width, player1.height);
  requestAnimationFrame(update); // Gameloop
  document.addEventListener("keydown", movePlayer1up);
  document.addEventListener("keydown", movePlayer1down);
  document.addEventListener("keydown", muteSound);
  document.addEventListener("keydown", pauseGame);
  document.addEventListener('keyup', stopPlayer);
});

////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////


////////////Audio Variables///////////////
const wallHitAudio = new Audio(wallHitSound);
const paddleHitAudio = new Audio(paddleHitSound);
const pointScoredAudio = new Audio(pointScoredSound);
let soundOnOff = true;

function __goTo(page) {
  if (page == null)
      return;
  router.push(page);
}

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
  // console.log(player);
  // console.log(newY);
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
  const currentUrl = window.location.href; 
  const lastSegment = currentUrl.split('/').filter(Boolean).pop();
  socket.value = new WebSocket(`wss://localhost:8443/ws/websockets/?page=${encodeURIComponent(lastSegment)}`);
  socket.value.onopen = () => {
    console.log('WebSocket connecté');
  };


  socket.value.onmessage = (event) => {
    // console.log("---ON MESSAGE---");

    const data = JSON.parse(event.data);
    // console.log(data.type);
    // console.log(data.x);
    // console.log(data.y);
    // console.log(data.message);
    // message_type = data.get('type');
    // message_content = data.get('message');

    if (data.type == 'connection_success') 
    {
      // console.log(data.type);
      // console.log(data.message);
      // connectionStatus.value = data.message;

      // console.log(data.type);
      const message =
      {
        type: "GameIA",
        player: "2",
      };
      sendMessage(message);

      connection = 1;
    }
    else if (data.type == 'updatePts')
    {
      // console.log(data.type);
      // console.log(data.updatePts);
      // console.log(data.player);
      updatePoints(data.player, data.updatePts);
      if (soundOnOff == true)
        pointScoredAudio.play();
    } 
    else if (data.type == 'mouvUp' || data.type == 'mouvDown')
    {
      // console.log(data.type);
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
      router.push('/'); //========================================== Erreur
    }
    //   console.log(data.type);
    // }
    // else if (data.type == 'startGame')
    // {
    //   console.log(data.type);
    // }
    else if (data.type == 'paddleHit') //sound
    {
      console.log(data.type);
      if (soundOnOff == true)
        paddleHitAudio.play();
    }
    else if (data.type == 'wallHit')//sound
    { 
      console.log(data.type);
      if (soundOnOff == true)
        wallHitAudio.play();
    }
    else if (data.type == 'info_back') //a enlever test
    {
      console.log(data.type + " : " + data.value_back1 + "; " + data.value_back2 + "; " + data.value_back3);
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
  // console.log(msg);
  if (socket.value && socket.value.readyState === WebSocket.OPEN) 
  {
    // console.log("---SEND MESSAGE---");
    // console.log(msg.type);
    // console.log(msg.player);
    // console.log(msg.posPad);
    socket.value.send(JSON.stringify({
      'type': msg.type,
      'player': msg.player,
    }));
    // console.log("---END SEND MESSAGE---");
  }
  else 
  {
    console.error('WebSocket non connecté');
  }
}






onUnmounted(() => {
  if (socket.value) {
    socket.value.close();
  }
});

onMounted(() => {
  connectWebSocket();
});


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

    window.onload = function() {
        board = document.getElementById("board"); //link board element in template to board variable
        board.height = boardHeight;
        board.width = boardWidth;
        context = board.getContext("2d"); //Drawing on board

        //draw player1
        context.fillStyle = "white";
        context.fillRect(player1.x, player1.y, player1.width, player1.height);

        requestAnimationFrame(update); // Gameloop
        document.addEventListener("keydown", movePlayer1up);
        document.addEventListener("keydown", movePlayer1down);
        document.addEventListener('keyup', stopPlayer);
        // document.addEventListener("keydown", leaveGame);
    }

    function update() {
        requestAnimationFrame(update);
        
        context.clearRect(0, 0, board.width, board.height); // clear rectangle after movement (remove previous paddle position)
        context.fillRect(player1.x, player1.y, player1.width, player1.height); // redesine tous 
        context.fillRect(player2.x, player2.y, player2.width, player2.height);
        context.fillStyle = "white";
        context.fillRect(ball.x, ball.y, ball.width, ball.height);

        //draw score
        context.font = "100px Arial";
        context.fillText(player1Score, boardWidth/5, 100);
        context.fillText(player2Score, boardWidth*4/5 -50 , 100); //subtract -45 for width of text
        
        //draw middle line
        for (let i = 10; i < board.height; i += 25)
        {
            context.fillRect(board.width / 2 - 10, i, 2, 15);
        }

    }

    
    let moveInterval1up = null;
    let moveInterval1down = null;
    let tickPadel = 10;


    function movePlayer1up(e)
    {
      if (!moveInterval1up)
      {
        if (e.code == "KeyW")
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
        if (e.code == "KeyS")
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

    function pauseGame(e)
    {
      if (e.code == pause)
      {
        const message = 
            {
              type: "pause",
              player: "2",
            };
            sendMessage(message);        
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
      if (e.code == "KeyW")
      {  
        clearInterval(moveInterval1up);
        moveInterval1up = null;
      }
      else if(e.code == "KeyS")
      {
        clearInterval(moveInterval1down);
        moveInterval1down = null;
      }
    }


</script>

<template>
  <main>
    <div id="wrapper">
      <div id="black-background">
        <div>
          <canvas id ="board"></canvas>
      </div>
      <div>
          <h2 id="pause">[P] to Pause/Unpause</h2>
          <h2 id="mute">[M] to Mute/Unmute</h2>
        </div>
      </div>
    </div>
  </main>
</template>

<style lang="scss">
body {
  text-align: center;
}

#pause {
  color: rgb(114, 114, 114);
  font-size: 25px;
  left: 20%;
  top: 70%;
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
}
</style>
