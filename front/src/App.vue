<script setup>
  import { RouterLink, RouterView } from 'vue-router'
  import AudioBackground from './components/AudioBackground.vue'
  import VideoBackground from './components/VideoBackground.vue'


</script>

<template>
  <RouterView />
  <AudioBackground />
  <VideoBackground />
</template>

<style scoped>
</style>
