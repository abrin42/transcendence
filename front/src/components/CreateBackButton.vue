<template>
    <button class="button overloadBtn" @click="goBack">
        <i class="fa-solid fa-backward"></i>
    </button>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
function goBack() {
    router.go(-1);
}
</script>

<style>
.overloadBtn {
    position: absolute;
    height: 50px;
    width: 50px;
    left: 83.5vh;
    top: 90vh;
}
</style>
