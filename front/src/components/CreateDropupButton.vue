<template>
  <div class="dropup">
    <button id="p0" class="dropbtn" ref="p0">🇺🇸</button>
      <div class="dropup-content">
        <a @click="switchES">🇪🇸</a>
        <a @click="switchFR">🇫🇷</a>
        <a @click="switchEN">🇺🇸</a>
      </div>
  </div>
</template>

<script setup>

function switchEN() {
  document.getElementById("p0").innerHTML = "🇺🇸";
  // this.$refs.p0.innerHTML = "🇺🇸";
}

function switchFR() {
  document.getElementById("p0").innerHTML = "🇫🇷";
  // this.$refs.p0.innerHTML = "🇫🇷";
}

function switchES() {
  document.getElementById("p0").innerHTML = "🇪🇸";
  // this.$refs.p0.innerHTML = "🇪🇸";
}

</script>

<style>
/* Dropup Button */
.dropbtn {
  background-color: rgba(0,0,0,0.0);
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
}

/* The container <div> - needed to position the dropup content */
  .dropup {
    position: relative;
    display: inline-block;
}

/* Dropup content (Hidden by Default) */
.dropup-content {
  display: none;
  position: absolute;
  bottom: 50px;
  background-color: #f1f1f1;
  min-width: 100%;
  overflow: auto;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

/* Links inside the dropup */
.dropup-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropup links on hover */
.dropup-content a:hover {background-color: #ddd}

/* Show the dropup menu on hover */
.dropup:hover .dropup-content {
  display: block;
}

/* Change the background color of the dropup button when the dropup content is shown */
.dropup:hover .dropbtn {
  background-color: #c3c3c3;
}
</style>