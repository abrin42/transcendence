<template>

  <audio id="background_audio" loop="loop">
  <source src="./../assets/test.mp3" type="audio/mpeg">
      Your browser does not support the audio element.
  </audio>

</template>

<script>
  var myAudio = new Audio('./assets/test.mp3');
  myAudio.load();
</script>