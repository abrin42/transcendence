<script setup>
import { ref } from 'vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import Input from '../components/Input.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const email = ref('');
const password = ref('');
const is2FA = ref(true);

function __goTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}

function login() {
    if (!email.value || !password.value) {
        alert('Veuillez entrer un email et un mot de passe.');
        return;
    }

    console.log('Tentative de connexion avec:', email.value, password.value);
    if (is2FA.value)
        __goTo('/2fa');
    else
        alert('Connexion réussie avec l\'email: ' + email.value);
}
</script>

<template>
    <main>
        <div id="wrapper">
            <h1>LOGIN</h1>
            <div class="logContainer">
                <button class="button button-log42">
                    <img class="img-42" src="../assets/img/42_Logob.png" alt="Logo 42" />
                </button>
                <button class="button button-register" @click="__goTo('/register')">
                    <span class="buttonText buttonTextSize">{{ $t('Sign-up') }}</span>
                </button>
                <button class="button button-connect" @click="login">
                    <span class="buttonText buttonTextSize">{{ $t('Login') }}</span>
                </button>
            </div>

            <div class="__inputInfo">
                <Input iconClass="fa-envelope" placeholderText="Enter your email" v-model="email" />
                <Input iconClass="fa-lock" placeholderText="Enter your password" isPassword v-model="password" />
            </div>

            <div class="buttonContainer">
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
    top: 10%;
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
