<script>
import CreateBackButton from '../components/CreateBackButton.vue';

export default {
    data() {
        return {
            keys: {
                player1Left: 'ArrowLeft',
                player1Right: 'ArrowRight',
                player2Left: 'A',
                player2Right: 'D',
            },
            selectedKey: null,
        };
    },
    methods: {
        changeKey(action) {
            this.selectedKey = action;
            window.addEventListener('keydown', this.setKey);
        },
        setKey(event) {
            const newKey = event.key.toUpperCase(); // Convertit la touche en majuscule
            if (this.isKeyAlreadyUsed(newKey)) {
                alert('Cette touche est déjà utilisée !');
                return;
            }
            if (
                (this.selectedKey === 'player1Left' && newKey === this.keys.player1Right) ||
                (this.selectedKey === 'player1Right' && newKey === this.keys.player1Left) ||
                (this.selectedKey === 'player2Left' && newKey === this.keys.player2Right) ||
                (this.selectedKey === 'player2Right' && newKey === this.keys.player2Left)
            ) {
                alert('Le même joueur ne peut pas utiliser la même touche pour gauche et droite.');
                return;
            }

            if (this.selectedKey) {
                this.keys[this.selectedKey] = newKey; // Assigne toujours en majuscule
                this.selectedKey = null;
                window.removeEventListener('keydown', this.setKey);
            }
        },
        isKeyAlreadyUsed(newKey) {
            return Object.values(this.keys).includes(newKey);
        }
    }
};
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="settingsBackground">
                <span class="titleSettings">Settings</span>
                <div class="settingsText">
                    <span>Player 1 - RIGHT</span>
                    <span>Player 1 - LEFT</span>
                    <span>Player 2 - RIGHT</span>
                    <span>Player 2 - LEFT</span>
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

.button {
    background-color: rgba(255, 255, 255, 0.0);
    padding: 0.5rem 1rem;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    margin-bottom: 15px;
    width: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
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
