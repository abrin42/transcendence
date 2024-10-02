<script setup>
import CreateSoundButton from '../components/CreateSoundButton.vue';
import CreateLogButton from '../components/CreateLogButton.vue';
import CreateSettingsButton from '../components/CreateSettingsButton.vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';

import { useRouter } from 'vue-router';
import { reactive, onMounted } from 'vue';

const state = reactive({
  id: '',
  username: '',
  nickname: '',
});

async function fetchUserData() {
  try {
    const response = await fetch('/api/player/verify-jwt/', {
      credentials: 'include',
    });
    const text = await response.text();
    console.log('Raw response:', text);

    let data;
    try {
      data = JSON.parse(text);
    } catch (err) {
      console.error('Error parsing response:', err);
      return;
    }

    if (data.valid) {
      state.id = data.user.id;
    }
  } catch (error) {
    console.error('Error fetching user data:', error);
  }
}

async function getUser() {
  try {
    const response = await fetch(`http://localhost:8080/api/test-api/${state.id}`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const user = await response.json();
    console.log('User data:', user);
    state.nickname = user.nickname;
    state.username = user.username;  // Set the username here
  } catch (error) {
    console.error('Error retrieving user data:', error);
  }
}


onMounted(async () => {
  await fetchUserData(); // Wait for fetchUserData to complete
  if (state.id) {
    await getUser(); // Only call getUser if state.id is available
  }
  const myVideo = document.getElementById('videoBG');
  if (myVideo) {
    myVideo.playbackRate = 1;
  }
});


const router = useRouter();
function __goTo(page) {
  if (!page) {
    return;
  }
  router.push(page);
}
</script>

<template>
  <main>
    <div id="wrapper">
      <div class="buttonContainer">
        <div v-if="state.username && state.username.length" class="welcome-message">
          <p>Welcome, {{ state.username }}, {{ state.id }}!</p>
        </div>


        <button class="button" @click="__goTo('/modeselect')">
          <i class="fas fa-play" style="margin-right: 1vw;"></i>
          <span class="buttonText buttonTextSize">{{ $t('play') }}</span>
        </button>
        <button class="button button-credits" @click="__goTo('/credits')">
          <span class="buttonText">{{ $t('credits') }}</span>
        </button>

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