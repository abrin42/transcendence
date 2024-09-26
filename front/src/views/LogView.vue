<script setup>
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="logContainer">
                <h1>Log</h1>
                <p>Log content</p>
            </div>
            <div class="buttonContainer">
                <CreateBackButton />
                <CreateDropupButton />
            </div>
        </div>
    </main>
</template>

<style scoped>
.logContainer {
    position: fixed;
    width: 50vw;
    height: 50vh;
    left: auto;
    top: 25%;
    background-color: rgba(0, 0, 0, 0.75);
}

</style>
