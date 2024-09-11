<template>

  <audio id="background_audio" autoplay="true" loop="loop">
  <source src="./../assets/test.mp3">
      Your browser does not support the audio element.
  </audio>

</template>

<script>
  var myAudio = new Audio('./assets/test.mp3');
  myAudio.addEventListener("click", (event) => {
  if (myAudio.paused())
    myAudio.play();
});

</script>