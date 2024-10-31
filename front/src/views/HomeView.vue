<script setup>
// Imports
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateSettingsButton from '../components/CreateSettingsButton.vue';
    import CreateLogButton from '../components/CreateLogButton.vue';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import { useRouter } from 'vue-router';
    import { onMounted } from 'vue';
    import { inject } from 'vue';
    
    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////
    
    import { useUser } from '../useUser.js'; 
    const { getUser, is_connected } = useUser(); 
    
    onMounted(async () => {
        await getUser();
        await getCSRF();
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    function __goTo(page) {
        if (page == null)
            return;
        router.push(page);
    }
    const router = useRouter();
    const gameSelection = inject('gameSelection');
    const varySpeed = inject('varySpeed');
    const game = inject('game');
    const mode1 = inject('mode1');
    const mode2 = inject('mode2');


    game.value = '';
    mode1.value = '';
    mode2.value = '';

    
    varySpeed(1); //sets speed to average in App.vue
    gameSelection(game.value, mode1.value, mode2.value); //sets game selected back to empty if user uses back button

    async function getCSRF() {
        try {
            const response = await fetch('/api/player/get_csrf_token/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
        } catch (error) {
            console.error('Error during fetch operation:', error);
        }
    }
    

    function goToGameSelect() {
        router.push('/gameselect');
    }

    function goToCredits() {
        router.push('/credits');
    }

</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <button v-if="is_connected === true" class="button" @click="goToGameSelect()">
                    <i class="fas fa-play" style="margin-right: 1vw;"></i>
                    <span class="buttonText buttonTextSize">{{ $t('play') }}</span>
                </button>
                <button class="button button-credits" @click="goToCredits()">
                    <i class="fa-solid fa-copyright" style="margin-right: 1vw;"></i>
                    <span class="buttonText">{{ $t('credits') }}</span>
                </button>
                <div>
                    <CreateHomeButton />
                    <CreateSoundButton />
                    <CreateLogButton />
                    <CreateSettingsButton @click="__goTo('/settings')" />
                    <CreateDropupButton />
                </div>
            </div>
        </div>
    </main>
</template>


<style>
@import './../assets/main.scss';

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.wrapper {
    z-index: 0;
}

.icon-rotate {
    display: inline-block;
    animation: rotate 1s ease-out;
}

.buttonContainer {
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 140vh;
}

.button {
    background-color: rgba(0, 0, 0, 0.25);
    padding: 2vh 2vw;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: border-color 0.5s;
    margin-top: 1vh;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}

.buttonText {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.5rem;
    font-weight: 600;
    cursor: pointer;
    opacity: 1;
    white-space: nowrap;
}

.button i {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.5vw;
    cursor: pointer;
}

.button-credits {
    top: 75vh;
    width: auto;
    min-width: 1vw;
    height: auto;
    padding: 1vh 1vw;
    display: flex;
    justify-content: center;
    align-items: center;
    white-space: nowrap;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
