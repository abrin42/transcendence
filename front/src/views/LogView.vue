<template>
    <main>
        <div id="wrapper">
            <CreateBackButton />
            <div class="loginBackground">
                <span class="titleLogin">Login</span>
                <form class="loginForm" @submit.prevent="submitLogin">
                    <div class="inputGroup">
                        <span>Email</span>
                        <input v-model="email" type="email" id="email" placeholder="Enter your email" required />
                    </div>
                    <div class="inputGroup">
                        <span>Password</span>
                        <input v-model="password" type="password" id="password" placeholder="Enter your password" required />
                    </div>
                    <div class="buttonContainer">
                        <button class="button" type="submit">
                            <span class="buttonText">Login</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </main>
</template>

<script>
import CreateBackButton from '../components/CreateBackButton.vue';

export default {
    data() {
        return {
            email: '',
            password: '',
        };
    },
    methods: {
        submitLogin() {
            // Logique de soumission des informations de connexion
            console.log('Email:', this.email);
            console.log('Password:', this.password);
        },
    },
};
</script>

<style scoped>
@import './../assets/main.scss';

.titleLogin {
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

.loginBackground {
    position: relative;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 0.4vw;
    width: 800px;
    height: 500px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.loginForm {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.inputGroup {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    font-size: 24px;
    border: none;
    border-radius: 0.4;
    color: rgba(255, 255, 255, 0.75);
    margin-bottom: 20px;
    width: 100%;
}

.inputGroup span {
    margin-bottom: 10px;
    color: rgba(255, 255, 255, 0.75);
}

.inputGroup input {
    background-color: rgba(255, 255, 255, 0.0);
    padding: 10px;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    width: 100%;
    color: white;
    font-size: 1.25rem;
}

.inputGroup input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.inputGroup input:focus {
    border-color: rgba(255, 255, 255, 1);
    outline: none;
    background-color: rgba(255, 255, 255, 0.1);
    transition: border-color, background-color 0.5s;
}

.buttonContainer {
    display: flex;
    justify-content: center;
    align-items: center;
}

.button {
    background-color: rgba(255, 255, 255, 0.0);
    padding: 0.5rem 1rem;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    width: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.buttonText {
    color: rgb(255, 255, 255);
    font-size: 1.25rem;
    font-weight: 600;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}
</style>
