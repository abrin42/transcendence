<script setup>
  // imports
  import { RouterLink, RouterView } from 'vue-router';
  import AudioBackground from './components/AudioBackground.vue';
  import VideoBackground from './components/VideoBackground.vue';
  import { ref, provide } from 'vue';
  
  // provide to inject 'isPlaying' in CreateSoundButton component
  let isPlaying = ref(false);
  provide('isPlaying', isPlaying);
  provide('togglePlay', () => {
    isPlaying.value = !isPlaying.value;
  });

  //provide that injects function to change video background speed
  provide('varySpeed', (speed) => {
    var myVideo = document.getElementById('videoBG')
    if(speed == 0)
      myVideo.pause();
    else if (myVideo.paused == true)
    {
      myVideo.play();
      myVideo.playbackRate = speed;
    }
    else
      myVideo.playbackRate = speed;
  });

  //provide that injects selected game mode
  let gameModeSelected = ref('');
  const game = ref('');
  const mode1 = ref('');
  const mode2 = ref('');
  provide('game', game);
  provide('mode1', mode1);
  provide('mode2', mode2);
  provide('gameModeSelected', gameModeSelected);
  provide('gameSelection', (game, mode1, mode2) => {
    gameModeSelected = game + mode1 + mode2;
  });

  // provide that injects visual assets matching selected language
  let current_flag = ref("🇬🇧");
  provide('current_flag', current_flag);
  provide('toggle_flag', (lang) => {
    current_flag = lang;
  });

  //provide that injects the currently selected asset
  let current_lang = ref("EN");
  provide('current_lang', current_lang);
  provide('toggle_lang', (lang) => {
    current_lang = lang;
  }); 

</script>

<template>
  <AudioBackground  />
  <VideoBackground/>
  <div id ="wrapper">
        <div id="video">
            <video id="videoBG" loop autoplay muted preload="true" class="flex">
                <source src="./assets/MainMenuScene.mp4" type="video/mp4">
                    Your browser does not support the video element.
            </video>
        </div>
    </div>
  <RouterView v-slot="{Component}">
    <transition name="route" mode="out-in">
      <component :is="Component"></component>
    </transition>
  </RouterView>
</template>

<style scoped>

/*route transitions */
.route-enter-from{
  opacity: 0;
  transform: translateX(100px);
}

.route-enter-active{
  transition: all 0.3s ease-out;
}

.route-leave-to{
  opacity: 0;
  transform: translateX(-100px);
}

.route-leave-active{
  transition: all 0.3s ease-in;
}
/*****************/

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

#CurtainsCanvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
}

#video {
        z-index: -1;
        position: absolute;
        width: auto;
        height: auto;
        min-width: 100%;
        max-height: 100%;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: flex-start;
    }

    #wrapper {
    position: absolute;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    }
</style>
