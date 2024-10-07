<template>
    <div id ="wrapper">
        <div id="video">
            <video id="videoBG" loop autoplay muted preload="true" class="flex">
                <source src="./../assets/MainMenuScene.mp4" type="video/mp4">
                    Your browser does not support the video element.
            </video>
        </div>
    </div>

</template>

<script>
</script>

<style>
    #video {
        z-index: -1;
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