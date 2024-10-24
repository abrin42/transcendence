<template>
    <div id ="wrapper">
        <div id="video">
        </div>
    </div>

</template>

<script setup>

</script>

<style>
    #video {
        z-index: -3;
        position: absolute;
        width: auto;
        height: auto;
        min-width: 100%;
        max-height: 100%;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: flex-start;
    }

    #wrapper {
    position: absolute;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    }
</style>