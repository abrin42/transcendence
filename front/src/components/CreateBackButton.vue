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
        position: fixed;
        width: 3vw;
        height: 6vh;
        bottom: 93vh;
        right: 95vw;
    }
</style>
