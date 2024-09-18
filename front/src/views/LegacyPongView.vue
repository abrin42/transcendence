<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// Variables pour le WebSocket
const socket = ref(null);
const message = ref('');
const messages = ref([]);
const connectionStatus = ref('');

// Créer une connexion WebSocket
function connectWebSocket() {
  socket.value = new WebSocket('ws://localhost:8080/ws/websockets/');
  console.log('WebSocket test 2');
  socket.value.onopen = () => {
    console.log('WebSocket connecté');
  };

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'connection_success') {
      connectionStatus.value = data.message;
    } else {
      messages.value.push(data.message);
    }
  };

  socket.value.onerror = (error) => {
    console.error('Erreur WebSocket:', error);
  };

  socket.value.onclose = () => {
    console.log('WebSocket déconnecté, tentative de reconnexion...');
    setTimeout(() => {
      connectWebSocket();  // Reconnexion automatique
    }, 3000);  // 3 secondes avant la reconnexion
  };
}

// Envoyer un message via WebSocket
function sendMessage() {
  if (message.value.trim() !== '') {
    socket.value.send(JSON.stringify({
      'message': message.value
    }));
    message.value = '';
  }
}

// Nettoyer la connexion WebSocket à la destruction du composant
onUnmounted(() => {
  if (socket.value) {
    socket.value.close();
  }
});

// Initialiser la connexion WebSocket lors du montage du composant
onMounted(() => {
  connectWebSocket();
});
</script>

<template>
  <main>
    <div>
      <h2>Chat WebSocket</h2>
      <p>{{ connectionStatus }}</p>
      <input 
        v-model="message" 
        placeholder="Tapez votre message" 
        @keyup.enter="sendMessage" 
      />
      <button @click="sendMessage">Envoyer</button>
      <div v-for="(msg, index) in messages" :key="index">
        {{ msg }}
      </div>
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
