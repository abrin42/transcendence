<script setup> 
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
        x : 10, y: boardHeight/5*2, width : playerWidth, height : playerHeight, speed : playerSpeed
    }

    let player2 = {
        x : boardWidth - playerWidth - 10, y: boardHeight/5*2, width : playerWidth, height : playerHeight, speed: playerSpeed
    }

    //ball properties
    let ballSize = 10;
    let ball = {x : boardWidth / 2, y : boardHeight / 2, width : ballSize, height : ballSize, speedX: 1, speedY: 2}

    //score
    let player1Score = 0;
    let player2Score = 0;

    //game launch
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
        document.addEventListener("keydown", leaveGame);
    }

    function update() {
        requestAnimationFrame(update);
        context.clearRect(0, 0, board.width, board.height); // clear rectangle after movement (remove previous paddle position)

        //draw player 1 over and over;
        context.fillStyle = "white";
        // player1.y += player1.speed;
        let nextPlayer1 = player1.y + player1.speed;
        if (!limits(nextPlayer1)){
            player1.y = nextPlayer1;
        }

        context.fillRect(player1.x, player1.y, player1.width, player1.height);

        //draw player 2 over and over;
        //player2.y += player2.speed;
        let nextPlayer2 = player2.y + player2.speed;
        if (!limits(nextPlayer2)){
            player2.y = nextPlayer2;
        }
        context.fillRect(player2.x, player2.y, player2.width, player2.height);

        //draw ball
        ball.x += ball.speedX;
        ball.y += ball.speedY;
        context.fillRect(ball.x, ball.y, ball.width, ball.height);

        //handling redirection when hitting top or bottom
        if (ball.y <= 0 || (ball.y + ball.height >= boardHeight)){
            ball.speedY *= -1;
        }
        // paddle collision
        if (paddleCollision(ball, player1)){
            if (ball.x <= player1.x + player1.width){
                //left side of ball touches right side of left paddle
                ball.speedX *= -1; //changes direction 
            }
        }
        else if (paddleCollision(ball, player2)){
            if ( ball.x + ball.width >= player2.x)
            {
                //right side of ball touches left side of right paddle
                ball.speedX *= -1; // changes direction
            }
        }

        // point scored
        if (ball.x < 0){
            player2Score++;
            resetGame(1);
        }
        else if (ball.x + ballSize > boardWidth){
            player1Score++;
            resetGame(-1);
        }

        //draw score
        context.font = "100px Arial";
        context.fillText(player1Score, boardWidth/5, 100);
        context.fillText(player2Score, boardWidth*4/5 -50 , 100); //subtract -45 for width of text
        
        //draw middle line
        for (let i = 10; i < board.height; i += 25)
        {
            context.fillRect(board.width / 2 - 10, i, 2, 15);
        }

        //draw start message
        context.font = "25px Courier New";
        context.fillText("Press any key to begin", boardWidth -500 , boardHeight /2 + 15)

        //make view responsive
        //game over function redirect to menu, or congrats screen
        //add "press any key to start" function
        //add a sound key
        //add sound effects on impact
        //add an esc key function
        //add an AI
        //adapt ball speed, and dimensions to real pong game
        //add paddle redirections: top goes to top, bottom to bottom and center straight line
    }

    function limits(yPosition){
        return(yPosition < 0 || yPosition + playerHeight > boardHeight); //Yposition is our left corner so we add playerHeight
    }

    function movePlayer(e){
        //player1
        if (e.code == "KeyW")
        {
            player1.speed = -3;
        }
        else if (e.code == "KeyS")
        {
            player1.speed = 3;
        }
        //player2
        if (e.code == "ArrowUp")
        {
            player2.speed = -3;
        }
        else if (e.code == "ArrowDown")
        {
            player2.speed = 3;
        }
        document.addEventListener('keyup', stopPlayer); //enables player to stay idle
    }

    function stopPlayer(e){
        //player1
        player1.speed = 0;
        //player2
        player2.speed= 0;
    }

    function paddleCollision(a, b){
        return a.x <b.x + b.width && //top left corner of a doesnt touch top right corner of b
            a.x +a.width > b.x && // top right corner of a past top left corner of b
            a.y < b.y + b.height && // top left corner of a doesnt touch bottom left corner of b
            a.y + a.height > b.y; // bottom left corner of a past top left corner of b
    }

    function resetGame(direction){
        ball = {x : boardWidth / 2, y : boardHeight / 2, width : ballSize, height : ballSize, speedX: direction, speedY: 2}

    }











    export default {
  data() {
    return {
      socket: null, // Contiendra l'objet WebSocket
      message: '', // Message à envoyer
      messages: [] // Liste des messages reçus
    };
  },
  created() {
    // Établir la connexion WebSocket lorsque le composant est créé
    this.connectWebSocket();
  },
  methods: {
    connectWebSocket() {
      // Crée une nouvelle connexion WebSocket à l'URL spécifiée
      this.socket = new WebSocket('ws://localhost:8000/ws/some_path/');

      // Événement déclenché lorsque la connexion WebSocket est ouverte
      this.socket.onopen = () => {
        console.log('WebSocket connected');
      };

      // Événement déclenché lorsque le WebSocket reçoit un message
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data); // Parse le message JSON
        this.messages.push(data.message); // Ajoute le message reçu à la liste
      };

      // Événement déclenché lorsque la connexion WebSocket est fermée
      this.socket.onclose = () => {
        console.log('WebSocket disconnected');
      };

      // Événement déclenché lorsqu'une erreur survient sur la connexion WebSocket
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    },
    sendMessage() {
      if (this.message.trim() !== '') {
        // Envoie le message saisi au serveur via le WebSocket
        this.socket.send(JSON.stringify({
          'message': this.message // Envoie le message sous forme de JSON
        }));
        this.message = ''; // Réinitialise l'input après l'envoi
      }
    }
  },
  beforeDestroy() {
    // Ferme la connexion WebSocket lorsque le composant est détruit
    if (this.socket) {
      this.socket.close();
    }
  }
};






</script>

<template>
    <main>
        <!-- <div id="wrapper">
            <canvas id ="board"></canvas>

        </div> -->





        <div>
            <h2>Chat WebSocket</h2>
                <input 
                    v-model="message" 
                    placeholder="Type your message" 
                    @keyup.enter="sendMessage" 
                />
                <button @click="sendMessage">Send</button>
                <div v-for="(msg, index) in messages" :key="index">
                    {{ msg }}
                </div>
        </div>



    </main>
</template>

<style lang="scss">
    @import './../assets/main.scss';
    
    body {
        text-align: center;
    }

    #wrapper {
        background-color: black;
    }

    #board {
        background-color: black;
        border-top: 5px solid white;
        border-bottom: 5px solid white;
        border-left: 5px solid white;
        border-right: 5px solid white;
    }
</style>