<template>
    <button class="button button-log">
        <span class="buttonText">{{ $t('login') }}</span>
    </button>
</template>

<script setup>
import { ref } from 'vue';

</script>

<style>
.button-log {
    position: fixed;
    width: 7vw;
    height: 6vh;
    bottom: 93vh;
    left: 87.5vw;
}
</style>