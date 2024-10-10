<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const socket = ref(null);
// const message = ref('');
const messages = ref([]);
const connectionStatus = ref('');
let connection = 0;



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
  socket.value = new WebSocket('wss://localhost:8443/ws/websockets/');
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
        document.addEventListener("keydown", movePlayer);
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

    
    let keysPressed = {};
    let moveInterval1up = null;
    let moveInterval1down = null;
    let tickPadel = 10;



    function movePlayer(e) 
    {
      keysPressed[e.code] = true;

      if (keysPressed["KeyW"]) 
      {
        if (!moveInterval1up)
        {
          moveInterval1up = setInterval(() => {
            const message = 
            {
              type: "mouvUp",
              player: "1",
            };
            sendMessage(message);                    
          }, tickPadel );
        }
      } 
      else if (keysPressed["KeyS"])
      {
        if (!moveInterval1down)
        {
          moveInterval1down = setInterval(() => {
            const message = 
            {
              type: "mouvDown",
              player: "1",
            };
            sendMessage(message);                    
          }, tickPadel );
        }                        
      }
        document.addEventListener('keyup', stopPlayer);
    }

    function stopPlayer(e) {
      delete keysPressed[e.code];
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
      <div id>
          <canvas id ="board"></canvas>
      </div>
  </main>
</template>

<style lang="scss">
body {
  text-align: center;
}

#board {
  background-color: black;
  border: 5px solid white;
}
</style>
