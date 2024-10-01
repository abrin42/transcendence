<script setup>
import CreateSoundButton from '../components/CreateSoundButton.vue';
import CreateLogButton from '../components/CreateLogButton.vue';
import CreateSettingsButton from '../components/CreateSettingsButton.vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';

import { useRouter } from 'vue-router';
import { reactive, onMounted } from 'vue'; // Import reactive and onMounted to handle user data

// Reactive state for storing user information
const state = reactive({
  username: '', // Assume an empty username initially
});

async function fetchUserData() {
  try {
    const response = await fetch('/api/player/verify-jwt/', {
      credentials: 'include',
    });
    const text = await response.text(); // Get the response as text to inspect
    console.log('Raw response:', text);

    // Parse the text if it appears to be JSON
    const data = JSON.parse(text);

    if (data.valid) {
      state.username = data.user.username; // Set the username if valid
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
  }
}


// Fetch user data when component is mounted
onMounted(() => {
  fetchUserData();
});

const router = useRouter();
function __goTo(page) {
  if (page == null) {
    return;
  }
  router.push(page);
}

var myVideo = document.getElementById('videoBG');
if (myVideo) {
  myVideo.playbackRate = 1;
}
</script>

<template>
  <main>
    <div id="wrapper">
      <div class="buttonContainer">
        <!-- Display Username -->
        <div v-if="state.username" class="welcome-message">
          <p>Welcome, {{ state.username }}!</p>
        </div>

        <!-- Navigation Buttons -->
        <button class="button" @click="__goTo('/modeselect')">
          <i class="fas fa-play" style="margin-right: 1vw;"></i>
          <span class="buttonText buttonTextSize">{{ $t('play') }}</span>
        </button>
        <button class="button button-credits" @click="__goTo('/credits')">
          <span class="buttonText">{{ $t('credits') }}</span>
        </button>

        <!-- * BUTTONS OTHERS * -->
        <CreateSoundButton />
        <CreateLogButton />
        <CreateSettingsButton @click="__goTo('/settings')" />
        <CreateDropupButton />
      </div>
    </div>
  </main>
</template>

<style scoped>
@import './../assets/main.scss';

.buttonContainer {
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 140vh;
}

.welcome-message {
  margin-bottom: 2vh;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.8);
}

.button {
  background-color: rgba(0, 0, 0, 0.25);
  padding: 2vh 2vw;
  border: 0.15vw solid rgba(0, 0, 0, 0.25);
  border-radius: 0.4vw;
  transition: border-color 0.5s;
  margin-top: 1vh;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}

.buttonText {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.5rem;
  font-weight: 600;
  cursor: pointer;
  opacity: 1;
  white-space: nowrap;
}

.button:hover {
  border-color: rgba(255, 255, 255, 1);
  background-color: rgba(255, 255, 255, 0.4);
  transition: border-color, background-color 0.5s;
}
</style>