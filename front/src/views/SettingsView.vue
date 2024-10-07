<script setup>
import { reactive, ref, onMounted, onBeforeUnmount } from 'vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import CreateDropupButton from '@/components/CreateDropupButton.vue';

const keys = reactive({
    player1Left: 'ArrowLeft',
    player1Right: 'ArrowRight',
    player2Left: 'A',
    player2Right: 'D',
});

const selectedKey = ref(null);

const changeKey = (action) => {
    selectedKey.value = action;
    window.addEventListener('keydown', setKey);
};

const setKey = (event) => {
    const newKey = event.key.toUpperCase();
    if (isKeyAlreadyUsed(newKey)) {
        alert('Cette touche est déjà utilisée.');
        return;
    }
    if (
        (selectedKey.value === 'player1Left' && newKey === keys.player1Right) ||
        (selectedKey.value === 'player1Right' && newKey === keys.player1Left) ||
        (selectedKey.value === 'player2Left' && newKey === keys.player2Right) ||
        (selectedKey.value === 'player2Right' && newKey === keys.player2Left)
    ) {
        alert('Le meme joueur ne peut pas utiliser la meme touche pour gauche et droite.');
        return;
    }

    if (selectedKey.value) {
        keys[selectedKey.value] = newKey;
        selectedKey.value = null;
        window.removeEventListener('keydown', setKey);
    }
};

const isKeyAlreadyUsed = (newKey) => {
    return Object.values(keys).includes(newKey);
};

onBeforeUnmount(() => {
    window.removeEventListener('keydown', setKey);
});
</script>

<template>
    <main>
        <div id="wrapper">
            <CreateBackButton />
            <CreateDropupButton />
            <div class="settingsBackground">
                <span class="titleSettings">{{ $t('settings') }}</span>
                <div class="settingsText">
                    <span>{{ $t('player') }} 1 - {{ $t('right') }}</span>
                    <span>{{ $t('player') }} 1 - {{ $t('left') }}</span>
                    <span>{{ $t('player') }} 2 - {{ $t('right') }}</span>
                    <span>{{ $t('player') }} 2 - {{ $t('left') }}</span>
                </div>
                <div class="buttonContainer">
                    <button class="button" @click="changeKey('player1Right')">
                        <span class="buttonText">{{ keys.player1Right }}</span>
                    </button>
                    <button class="button" @click="changeKey('player1Left')">
                        <span class="buttonText">{{ keys.player1Left }}</span>
                    </button>
                    <button class="button" @click="changeKey('player2Right')">
                        <span class="buttonText">{{ keys.player2Right }}</span>
                    </button>
                    <button class="button" @click="changeKey('player2Left')">
                        <span class="buttonText">{{ keys.player2Left }}</span>
                    </button>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
@import './../assets/main.scss';

.titleSettings {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 2.5rem;
    font-weight: 600;
    color: white;
    text-align: center;
    z-index: 1;
}

#wrapper {
    z-index: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.settingsBackground {
    position: relative;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 0.4vw;
    width: 800px;
    height: 600px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
}

.settingsText {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    font-size: 24px;
    color: rgba(255, 255, 255, 0.75);
    margin-right: 20px;
}

.settingsText span {
    margin-bottom: 15px;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    padding: 10px;
    cursor: pointer;
    width: 250px;
    text-align: center;
}

.buttonContainer {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    height: auto;
}

.buttonText {
    color: rgb(255, 255, 255);
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
