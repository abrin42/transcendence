<script setup>
import { ref } from 'vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import Input from '../components/Input.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref('');
const email = ref('');
const phone_number = ref('');
const password1 = ref('');
const password2 = ref('');

defineExpose({
    username,
    email,
    phone_number,
    password1,
    password2
});

function __goTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}

async function createAccount() {
    if (password1.value !== password2.value) {
        alert('Les mots de passe ne correspondent pas.');
        return;
    }

    console.log(password1.value)
    console.log(password2.value)
    try {
        const response = await fetch('/api/player/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                username: username.value,
                email: email.value,
                phone_number: phone_number.value,
                password1: password1.value,
                password2: password2.value,
            })
        });
        if (response.ok) {
            const responseData = await response.json();
            alert('Compte créé avec succès !');
            __goTo(responseData.redirect_url);
        } else {
            const errorData = await response.json();
            alert('Erreur: ' + errorData.error);
        }
    } catch (error) {
        console.error('Erreur lors de la création du compte:', error);
        alert('Une erreur est survenue pendant la création du compte.');
    }
}

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

</script>

<template>
    <main>
        <div id="wrapper">
            <h1>SIGN UP</h1>
            <div class="logContainer">
                <button class="button button-login" @click="__goTo('/log')">
                    <span class="buttonText buttonTextSize">{{ $t('Login') }}</span>
                </button>
                <button class="button button-createAccount" @click="createAccount">
                    <span class="buttonText buttonTextSize">{{ $t('Create your account') }}</span>
                </button>
            </div>

            <div class="__inputInfo">
                <Input iconClass="fa-user" placeholderText="*Username" v-model="username" />
                <Input iconClass="fa-envelope" placeholderText="*Email" v-model="email" />
                <Input iconClass="fa-phone" placeholderText="Phone Number" v-model="phone_number" />
                <Input iconClass="fa-lock" placeholderText="*Password" isPassword v-model="password1" />
                <Input iconClass="fa-lock" placeholderText="*Confirm password" isPassword v-model="password2" />
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
