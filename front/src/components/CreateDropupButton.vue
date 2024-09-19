<template>
  <div class="dropup" @mouseleave="hideMenu" @mouseenter="showMenu">
    <button id="p0" class="dropbtn">{{ currentFlag }}</button>
    <div class="dropup-content locale-changer" v-show="menuVisible">
      <a v-if="currentLang !== 'ES'" @click="switchLang('ES')">🇪🇸</a>
      <a v-if="currentLang !== 'FR'" @click="switchLang('FR')">🇫🇷</a>
      <a v-if="currentLang !== 'US'" @click="switchLang('US')">🇺🇸</a>
      <a v-if="currentLang !== 'DE'" @click="switchLang('DE')">🇩🇪</a>
    </div>
  </div>
</template>

      <!-- <div class="dropup-content locale-changer">
        <select v-model="$i18n.locale">
          <option value="EN" @click="switchEN">🇬🇧</option>
          <option value="FR" @click="switchFR">🇫🇷</option>
          <option value="ES" @click="switchES">🇪🇸</option>
          <option value="MA" @click="switchMA">⚔️</option>
        </select>
      </div> -->

<script setup>
import { ref } from 'vue';
import i18n from '../i18n.js'

const currentLang = ref('US');
const currentFlag = ref('🇺🇸');
const menuVisible = ref(false);
let timeoutId;

function switchLang(lang) {
  currentLang.value = lang;
  if (lang === 'US') {
      currentFlag.value = '🇺🇸';
    } else if (lang === 'FR') {
      currentFlag.value = '🇫🇷';
      // $i18n.locale.value='FR';
  } else if (lang === 'ES') {
      currentFlag.value = '🇪🇸';
  } else if (lang === 'DE') {
      currentFlag.value = '🇩🇪';
  }
  console.log(i18n.t);
}

function showMenu() {
  clearTimeout(timeoutId);
  menuVisible.value = true;
}

function hideMenu() {
  timeoutId = setTimeout(() => {
      menuVisible.value = false;
  }, 300);
}
</script>

<style>
.dropbtn {
  position: absolute;
  right: 84vh;
  top: 17vh;
  width: 50px;
  height: 50px;
  background-color: rgba(255, 255, 255, 0.0);
  border: 4px solid rgba(255, 255, 255, 0.5);
  border-radius: 0.4vw;
  border-width: 0.15vw;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  padding: 0;
}

.dropup-content {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.0);
  bottom: -16.5vh;
  right: 84vh;
  display: flex;
  flex-direction: column-reverse;
}

.dropup-content a {
  width: 50px;
  height: 50px;
  margin: 2px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  border-bottom: none;
  background-color: rgba(255, 255, 255, 0.0);
  border: 4px solid rgba(255, 255, 255, 0.5);
  border-width: 0.15vw;
  border-radius: 0.4vw;
}

.dropup-content a:hover {
  border-color: rgba(255, 255, 255, 1);
  background-color: rgba(255, 255, 255, 0.4);
}
</style>