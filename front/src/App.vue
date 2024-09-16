<script setup>
  import { RouterLink, RouterView } from 'vue-router'
  import AudioBackground from './components/AudioBackground.vue'
  import VideoBackground from './components/VideoBackground.vue'


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
