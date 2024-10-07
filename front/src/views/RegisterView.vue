<script setup>
import { ref } from 'vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import Input from '../components/Input.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

defineExpose({
    username,
    email,
    password,
    confirmPassword
});

function __goTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}

function createAccount() {
    if (password.value !== confirmPassword.value) {
        alert('Les mots de passe ne correspondent pas.');
        return;
    }

    const newUser = {
        username: username.value,
        email: email.value,
        password: password.value,
    };

    console.log('Données utilisateur prêtes pour être envoyées à la base de données :', newUser);
    alert('Compte créé avec succès !');
}
</script>

<template>
    <main>
        <div id="wrapper">
            <h1>SIGN UP</h1>
            <div class="logContainer">
                <button class="button button-log42">
                    <img class="img-42" src="../assets/img/42_Logob.png" alt="Logo 42" />
                </button>
                <button class="button button-login" @click="__goTo('/log')">
                    <span class="buttonText buttonTextSize">{{ $t('Login') }}</span>
                </button>
                <button class="button button-createAccount" @click="createAccount">
                    <span class="buttonText buttonTextSize buttonCreateAcc">{{ $t('Create your account') }}</span>
                </button>
            </div>

            <div class="__inputInfo">
                <Input iconClass="fa-user" placeholderText="Username" v-model="username" />
                <Input iconClass="fa-envelope" placeholderText="Email" v-model="email" />
                <Input iconClass="fa-lock" placeholderText="Password" isPassword v-model="password" />
                <Input iconClass="fa-lock" placeholderText="Confirm password" isPassword v-model="confirmPassword" />
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
    height: 52.5vh;
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

.button-createAccount {
    position: fixed;
    width: 15vw;
    height: 6vh;
    left: 42.5%;
    top: 65%;

    background-color: rgba(202, 149, 128, 0.5);
    border: 0.15vw solid rgba(202, 149, 128, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
}

.buttonCreateAcc {
    font-size: large;
}

.button-login {
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

.__inputInfo {
    position: fixed;
    left: 42.5%;
    top: 38%;
}

.img-42:hover {
    content: url('../assets/img/42_Logo.png');
    transition: content 0.3s ease;
}

.button-login:hover .buttonText {
    color: rgb(0, 0, 0);
    transition: color 0.3s ease, font-size 0.3s ease;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
