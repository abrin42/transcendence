<script setup>
import { ref } from 'vue';
import Input from '../components/Input.vue';
import Popup from '../components/Popup.vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';

const showPhonePopup = ref(false);
const showMailPopup = ref(false);
const code = ref('');

function openPhonePopup() {
    showPhonePopup.value = true;
}

function openMailPopup() {
    showMailPopup.value = true;
}

function closePopup() {
    showPhonePopup.value = false;
    showMailPopup.value = false;
}

function handleNext() {
    alert(`Code: ${code.value}`);
}
</script>

<template>
    <main>
        <div id="wrapper">
            <div v-if="!showMailPopup && !showPhonePopup" class="TwoFAContainer">
                <h1>Send code by e-mail or sms?</h1>
                <button class="button button-fa __button-phone" @click="openPhonePopup">
                    <i class="fas fa-mobile-button" style="margin: 0.1vw;"></i>
                    <span>Phone</span>
                </button>
                <button class="button button-fa __button-mail" @click="openMailPopup">
                    <i class="fas fa-envelope" style="margin: 0.1vw;"></i>
                    <span>Email</span>
                </button>
            </div>
            <div class="buttonContainer">
                <CreateBackButton />
                <CreateDropupButton />
            </div>
        </div>

        <Popup v-if="showPhonePopup" @close="closePopup">
            <h2 class="__title-popup">Telephone authentication</h2>
            <p>Enter the code you received by SMS.</p>
            <Input iconClass="fa-shield" placeholderText="Enter your code" v-model="code" />
            <button class="button __button-send-code">
                <span>Resend the code</span>
            </button>
            <button class="button __button-next" @click="handleNext">
                <span>Next</span>
            </button>
        </Popup>

        <Popup v-if="showMailPopup" @close="closePopup">
            <h2 class="__title-popup">E-mail authentication</h2>
            <p>Enter the code you received by e-mail.</p>
            <Input iconClass="fa-shield" placeholderText="Enter your code" v-model="code" />
            <button class="button __button-send-code" @click="console.log('todo alexxxxxxx')">
                <span>Resend the code</span>
            </button>
            <button class="button __button-next" @click="handleNext">
                <span>Next</span>
            </button>
        </Popup>
    </main>
</template>

<style scoped>
h1 {
    position: absolute;
    top: 20%;
    right: 50%;
    transform: translate(50%, 0);
    align-items: center;
    font-size: 2.5rem;
    white-space: nowrap;
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

@media (max-width: 1024px) {
    h1 {
        font-size: 2rem;
        top: 25%;
    }
}

@media (max-width: 768px) {
    h1 {
        font-size: 1.5rem;
        top: 30%;
    }
}

@media (max-width: 480px) {
    h1 {
        font-size: 1.2rem;
        top: 35%;
        right: 50%;
        transform: translate(50%, 0);
    }
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

.TwoFAContainer {
    z-index: 1;
    display: flex;
    margin-left: 50%;
    margin-right: 50%;
    align-items: center;
    height: 100vh;
    position: relative;
}

.button-fa {
    height: 30vh;
    width: 30vw;
}

.__button-phone,
.__button-mail,
i {
    color: #fff;
    margin-left: 5vh;
    font-size: 3vw;
}

.__title-popup {
    color: #fff;
    font-size: 1.7rem;
}

.__button-send-code {
    position: absolute;
    color: #fff;
    font-size: 0.6rem;
    font-weight: 100;
    max-width: 6vw;
    width: 6vw;
    left: 75%;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    white-space: nowrap;
    padding: 0.5vh 1vw;
}

.__button-next {
    position: relative;
    color: #fff;
    font-size: 0.6rem;
    font-weight: 100;
    max-width: 6vw;
    width: 6vw;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    white-space: nowrap;
    padding: 0.5vh 1vw;
}
</style>
