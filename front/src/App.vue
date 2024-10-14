<script setup>
  // imports
  import { RouterLink, RouterView } from 'vue-router';
  import AudioBackground from './components/AudioBackground.vue';
  import VideoBackground from './components/VideoBackground.vue';
  import { ref, provide } from 'vue';
  import { onMounted } from 'vue';

  // provide to inject 'isPlaying' in CreateSoundButton component
  let isPlaying = ref(false);
  provide('isPlaying', isPlaying);
  provide('togglePlay', () => {
    isPlaying.value = !isPlaying.value;
  });

  let current_flag = ref("🇬🇧");
  provide('current_flag', current_flag);
  provide('toggle_flag', (lang) => {
    current_flag = lang;
  });

  let current_lang = ref("EN");
  provide('current_lang', current_lang);
  provide('toggle_lang', (lang) => {
    current_lang = lang;
  });

</script>

<template>
  <AudioBackground />
  <VideoBackground />
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
</style>
