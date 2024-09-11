<script setup> 
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <div>
                    <CreateBackButton />
                </div>
                <div>
                    <CreateSoundButton />
                </div>
            </div>
        </div>
    </main>
</template>

<style>
    
    #wrapper {
    position: absolute;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    }

    #video {
        z-index: -1;
        position: absolute;
        width: auto;
        height: auto;
        min-width: 100%;
        max-height: 100%;
    }

    .buttonContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 140vh;
    position: relative;
}

    .button {
    background-color: rgba(255, 255, 255, 0.0);
    padding: 1rem 1rem;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    border-width: 0.15vw;
    transition: border-color 0.5s;
    margin-top: 10px;
    width: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

    .buttonText {
    color: rgb(255, 255, 255);
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
    opacity: 1;
}

    .button i {
    color: rgb(255, 255, 255);
    font-size: 1.5rem;
    cursor: pointer;
}

    .button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}

    .button-log {
    position: absolute;
    width: 120px;
    height: 50px;
    top: 10px;
    left: 48vW;
}

    .button-settings {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 10px;
    left: 43vW;
}

    .button-sound {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 10px;
    left: -65vh;
}


</style>