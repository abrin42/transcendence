<script setup>
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import CreateHomeButton from '../components/CreateHomeButton.vue';
import Input from '../components/Input.vue';
import { useRouter } from 'vue-router';
import { ref, onBeforeMount } from 'vue';
import i18n from '../i18n.js'

////////////////////////////////////////////////
/////// GET USER ///////////////////////////////
////////////////////////////////////////////////

import { useUser } from '../useUser.js'; 
const { getUser, is_connected } = useUser(); 

onBeforeMount(async () => {
    await getUser();  
    if (is_connected.value === true)
        __goTo('/')
});

////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////

const router = useRouter();

function __goTo(page) {
    if (page == null)
        return;
    router.push(page);
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

////////////////////////////////////////////////
////////////////////////////////////////////////
////////////////////////////////////////////////

const username = ref('');
const password = ref('');

async function login() {
    if (!username.value || !password.value) {
        alert(i18n.global.t('please_enter_email_password'));
        return;
    }
    try {
        const response = await fetch('/api/player/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(), 
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data.redirect_url) {
            __goTo(data.redirect_url);
            return;
        } else {
            alert(i18n.global.t('error_user_data_not_found'));
        }
    } catch (error) {
        console.error('Erreur lors de la connexion /login:', error);
        alert(i18n.global.t('invalid_username_or_password'));
    }
}

async function login42() {
    try {
        const response = await fetch('/api/player/login42/', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                hostname: window.location.hostname,
            }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        if (data.url) {
            //////////////////
            /// local or ip ??
            //////////////////

            window.location.href = data.url;
        } else {
            alert(i18n.global.t('error_invalid_URL_login'));
        }
        
    } catch (error) {
        console.error('Error during login:', error);
        alert(i18n.global.t('error_login'));
    }
}

</script>

<template>
    <main>
        <div id="wrapper">
            <h1>{{ $t('LOGIN') }}</h1>

            <div class="logContainer">
                <button class="button button-log42" @click="login42">
                    <img class="img-42" src="../assets/img/42_Logob.png" alt="Logo 42" />
                </button>
                <button class="button button-register" @click="__goTo('/register')">
                    <span class="buttonText buttonTextSize">{{ $t('sign_up') }}</span>
                </button>
                <button class="button button-connect" @click="login">
                    <span class="buttonText buttonTextSize">{{ $t('login') }}</span>
                </button>
            </div>

            <div class="__inputInfo">
                <Input iconClass="fa-user" :placeholderText="$t('enter_username')" v-model="username" />
                <Input iconClass="fa-lock" :placeholderText="$t('enter_password')" isPassword v-model="password" />
            </div>

            <div class="buttonContainer">
                <CreateHomeButton />
                <CreateBackButton />
                <CreateDropupButton />
            </div>
        </div>
    </main>
</template>


<style scoped>
h1 {
    position: fixed;
    left: auto;
    top: 15%;
    font-size: 4vw;
    color: #fff;
    text-shadow:
        0 0 5px rgba(255, 255, 255, 0.8),
        0 0 10px rgba(255, 255, 255, 0.6),
        0 0 20px rgba(255, 20, 147, 0.6),
        0 0 30px rgba(255, 20, 147, 0.6),
        0 0 40px rgba(255, 20, 147, 0.6),
        0 0 50px rgba(255, 20, 147, 0.6),
        0 0 60px rgba(255, 20, 147, 0.6);
    animation: neon-glow 1.5s ease-in-out infinite alternate;
}

@keyframes neon-glow {
    from {
        text-shadow:
            0 0 5px rgba(255, 255, 255, 0.8),
            0 0 10px rgba(255, 255, 255, 0.6),
            0 0 20px rgba(255, 20, 147, 0.6),
            0 0 30px rgba(255, 20, 147, 0.6),
            0 0 40px rgba(255, 20, 147, 0.6),
            0 0 50px rgba(255, 20, 147, 0.6),
            0 0 60px rgba(255, 20, 147, 0.6);
    }

    to {
        text-shadow:
            0 0 10px rgba(255, 255, 255, 1),
            0 0 20px rgba(255, 255, 255, 0.8),
            0 0 30px rgba(255, 20, 147, 0.8),
            0 0 40px rgba(255, 20, 147, 0.8),
            0 0 50px rgba(255, 20, 147, 0.8),
            0 0 60px rgba(255, 20, 147, 0.8),
            0 0 70px rgba(255, 20, 147, 0.8);
    }
}

.logContainer {
    position: fixed;
    width: 25vw;
    height: 40vh;
    left: auto;
    top: 25%;

    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: border-color 0.5s;
    background-color: rgba(0, 0, 0, 0.25);
}

.img-42 {
    width: 5vw;
    height: 5vh;
    align-items: center;
    justify-content: center;
    display: flex;
}

.button-log42 {
    position: fixed;
    width: 3vw;
    height: 6vh;
    left: 42.5%;
    top: 30%;

    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
}

.button-register {
    position: fixed;
    width: 10vw;
    height: 6vh;
    left: 47.5%;
    top: 30%;

    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
}

.button-connect {
    position: fixed;
    width: 15vw;
    height: 6vh;
    left: 42.5%;
    top: 52.5%;

    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
}

.__inputInfo {
    position: fixed;
    left: 42.5%;
    top: 38%;
}

.img-42:hover {
    content: url('../assets/img/42_Logo.png');
    transition: content 0.3s ease;
}

.button-register:hover .buttonText {
    color: rgb(0, 0, 0);
    transition: color 0.3s ease, font-size 0.3s ease;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>