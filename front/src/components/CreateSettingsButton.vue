<script setup>
    import { ref } from 'vue';

    const isRotating = ref(false);

    function rotateIcon() {
        isRotating.value = true;
        setTimeout(() => {
            isRotating.value = false;
        }, 1000);
    }

</script>

<template>
    <button class="button button-settings" @click="rotateIcon">
        <i :class="['fas fa-gear', { 'icon-rotate': isRotating }]"></i>
    </button>
</template>
  
  
<style>
.icon-rotate {
    display: inline-block;
    animation: rotate 1s ease-out;
}

.button-settings {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 10px;
    left: 43vW;
}
</style>