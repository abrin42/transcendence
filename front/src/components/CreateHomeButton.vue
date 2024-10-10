<script setup>
//imports
    import { useRouter } from 'vue-router';

    const router = useRouter();

    function goToHome() {
    router.push('/');
    }
</script>
``
<template>
    <main>
        <div id="wrapper">
            <button class="button button-transcendence" @click="goToHome()">
                    <img class="img-ft_transcendence" src="../assets/CyberPong.png" alt="CyberPong" />
                </button>
        </div>
    </main>
</template>

<style scoped>
@import './../assets/main.scss';

.img-ft_transcendence {
    display: fixed;
    width: 30vw;
    height: 12vh;
}

.button-transcendence {
    position: fixed;
    width: 15vw;
    height: 6vh;
    left: 42vw;
    top: 1.5vh;
    border: none;
    background-color: transparent;
}
.button-transcendence:hover {
    background-color:transparent;
}
</style>