<script setup> 
// Imports
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateSettingsButton from '../components/CreateSettingsButton.vue';
    import CreateLogButton from '../components/CreateLogButton.vue';

    import { useRouter } from 'vue-router';
    import { reactive, onMounted } from 'vue';
    //api user connected
    const userAccount = reactive({
      date_joined:"",
      email:"",
      email_2fa_active:false,
      lose:0,
      nickname:"",
      password:"",
      phone_number:"",
      profilePicture:"",
      rank:0,
      username:"",
      win:0,
    });
    
    async function getUser() {
      try {
          const response = await fetch(`https://localhost:8443/api/player/connected_user`, {
            method: 'GET',
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          
    const user = await response.json();
    console.log('User data:', user);
    console.log('player data', user[0].fields)
    userAccount.nickname = user[0].fields.nickname;
    userAccount.username = user[0].fields.username;  // Set the username here
    userAccount.email = user[0].fields.email;
    userAccount.password = user[0].fields.password;
    console.log('nickname: ' ,userAccount.nickname)
  } catch (error) {
    console.error('Error retrieving user data:', error);
  }
}




// Routing functions
const router = useRouter();

var myVideo = document.getElementById('videoBG');
myVideo.playbackRate = 1;

function goToModeSelect() {
  router.push('/modeselect');
}

function goToCredits() {
  router.push('/credits');
}

function __goTo(page) {
  if (page == null) {
    return;
  }
  router.push(page);
}
onMounted(async () => {
  await getUser(); // Only call getUser if state.id is available
});

</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button class="button" @click="goToCredits()">
                    <i class="fas fa-play" style="margin-right: 1vw;"></i>
                    <span class="buttonText buttonTextSize">{{ $t('play') }}</span>
                </button>
                <button class="button button-credits" @click="__goTo('/credits')">
                    <span class="buttonText">{{ $t('credits') }}</span>
                </button>
                <div>
                    <CreateSoundButton />
                    <CreateLogButton />
                    <CreateSettingsButton  @click="__goTo('/settings')"/>
                    <CreateDropupButton />
                </div>
            </div>
        </div>
    </main>
</template>


<style>
@import './../assets/main.scss';

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.wrapper {
    z-index: 0;
}

.icon-rotate {
    display: inline-block;
    animation: rotate 1s ease-out;
}

.buttonContainer {
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 140vh;
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

.button i {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.5vw;
    cursor: pointer;
}

.button-credits {
    top: 75vh;
    width: auto;
    min-width: 1vw;
    height: auto;
    padding: 1vh 1vw;
    display: flex;
    justify-content: center;
    align-items: center;
    white-space: nowrap;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
