<script setup>
  import { RouterLink, RouterView } from 'vue-router'
  import AudioBackground from './components/AudioBackground.vue'
  import VideoBackground from './components/VideoBackground.vue'
  import { ref, provide } from 'vue';
  const isPlaying = ref(false);
  provide('isPlaying', isPlaying);
  provide('togglePlay', () => {
  isPlaying.value = !isPlaying.value;
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
</style>
