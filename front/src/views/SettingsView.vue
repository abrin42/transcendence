<script setup>
    import { reactive, ref, onBeforeUnmount, onMounted } from 'vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateDropupButton from '@/components/CreateDropupButton.vue';
    import CreateHomeButton from '@/components/CreateHomeButton.vue';

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 

    onMounted(async () => {
        await getUser();
    });

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    function __goTo(page) {
    if (page == null)
        return;
    router.push(page);
    }

    const keys = {
        player1Up: userAccount.player1Up,
        player1Down: userAccount.player1Down,
        player2Up: userAccount.player2Up,
        player2Down: userAccount.player2Down,
        pause: userAccount.pause,
        mute: userAccount.mute,
    };

    async function update_keys() {
    try {
        const response = await fetch('api/player/update_keys/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), // Assuming CSRF protection is enabled
            },
            body: JSON.stringify({
                moveUpP1: userAccount.player1Up,
                moveDownP1: userAccount.player1Down,
                moveUpP2: userAccount.player2Up,
                moveDownP2: userAccount.player2Down,
                pause: userAccount.pause,
                mute: userAccount.mute
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        
    } catch (error) {
        console.error('Could not change', error);
        alert('An error occurred during updating keys.');
    }
}

    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    const selectedKey = ref(null);

    const changeKey = (action) => {
        selectedKey.value = action;
        window.addEventListener('keydown', setKey);

    };

    const setKey = (event) => {
        const newKey = event.key.toUpperCase();
        if (isKeyAlreadyUsed(newKey)) {
            alert('This key is already in use.');
            return;
        }
        if (
            (selectedKey.value === 'player1Down' && newKey === userAccount.player1Up) ||
            (selectedKey.value === 'player1Up' && newKey === userAccount.player1Down) ||
            (selectedKey.value === 'player2Down' && newKey === userAccount.player2Up) ||
            (selectedKey.value === 'player2Up' && newKey === userAccount.player2Down) ||
            (selectedKey.value === 'pause' && newKey === userAccount.pause) ||
            (selectedKey.value === 'mute' && newKey === userAccount.mute)
        ) {
            alert('The same player cannot use the same key for left and right.');
            return;
        }

        if (selectedKey.value) {
            keys[selectedKey.value] = newKey;
            if(selectedKey.value === 'player1Down')
                userAccount.player1Down = event.code;
            else if(selectedKey.value === 'player1Up')
                userAccount.player1Up = event.code;
            else if(selectedKey.value === 'player2Down')
                userAccount.player2Down = event.code;
            else if(selectedKey.value === 'player2Up')
                userAccount.player2Up = event.code;
            else if(selectedKey.value === 'pause')
                userAccount.pause = event.code;
            else if(selectedKey.value === 'mute')
                userAccount.mute = event.code;
            update_keys();
            console.log("changing");
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
            <CreateHomeButton />
            <div class="settingsBackground">
                <span class="titleSettings">{{ $t('settings') }}</span>
                <div class="settingsText">
                    <span>{{ $t('player') }} 1 - {{ $t('UP') }}</span>
                    <span>{{ $t('player') }} 1 - {{ $t('DOWN') }}</span>
                    <span>{{ $t('player') }} 2 - {{ $t('UP') }}</span>
                    <span>{{ $t('player') }} 2 - {{ $t('DOWN') }}</span>
                    <span>{{ $t('MUTE_SOUND') }}</span>
                </div>
                <div class="buttonContainer">
                    <button id="bouton-touche" class="button" @click="changeKey('player1Up')">
                        <span class="buttonText">{{ keys.player1Up }}</span>
                    </button>
                    <button id="bouton-touche" class="button" @click="changeKey('player1Down')">
                        <span class="buttonText">{{ keys.player1Down }}</span>
                    </button>
                    <button id="bouton-touche" class="button" @click="changeKey('player2Up')">
                        <span class="buttonText">{{ keys.player2Up }}</span>
                    </button>
                    <button id="bouton-touche" class="button" @click="changeKey('player2Down')">
                        <span class="buttonText">{{ keys.player2Down }}</span>
                    </button>
                    <button id="bouton-touche" class="button" @click="changeKey('mute')">
                        <span class="buttonText">{{ keys.mute }}</span>
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

#bouton-touche{
    width: 10vw;
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
