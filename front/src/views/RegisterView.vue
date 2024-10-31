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

    const username = ref('');
    const email = ref('');
    const phone_number = ref('');
    const password1 = ref('');
    const password2 = ref('');
    const acceptTerms = ref(false);

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

    function isValidUsername(username) {
        const dangerousWords = ["admin", "root", "superuser", "user", "hitler", "@AI.Bot"];
        for (let word of dangerousWords) {
            if (new RegExp(`\\b${word}\\b`, "i").test(username)) {
                return false;
            }
        }
        const usernameRegex = /^[a-zA-Z0-9_]+$/;
        return usernameRegex.test(username);
    }

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[\W_]).{8,}$/;
        return passwordRegex.test(password);
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPhoneNumber(phone) {
        const phoneRegex = /^(?:\+33\s?[1-9](?:\s?\d{2}){4}|0[1-9](?:\s?\d{2}){4})$/;
        return phoneRegex.test(phone);
    }

    //////////////////////////////////////////////

    async function createAccount() {
        if (!username.value || !email.value || !password1.value || !password2.value) {
            alert(i18n.global.t('please_complete_required_fields'));
            return;
        }

        if (!isValidUsername(username.value)) {
            alert(i18n.global.t('should_not_contain_spaces'));
            return;
        }
        
        if (!isValidEmail(email.value)) {
            alert(i18n.global.t('please_enter_valid_email'));
            return;
        }
        
        if (phone_number.value) {
            if (!isValidPhoneNumber(phone_number.value)) {
                alert(i18n.global.t('please_enter_valid_phone_number'));
                return;
            }
        }

        if (!acceptTerms.value) {
            alert(i18n.global.t('please_accept_terms_of_use'));
            return;
        }
        
        if (password1.value !== password2.value) {
            alert(i18n.global.t('error_passwords_do_not_match'));
            return;
        }

        if (!isValidPassword(password1.value)) {
            alert(
                i18n.global.t('should_contain_capital_letter') +
                i18n.global.t('should_contain_lower_case_letter') +
                i18n.global.t('should_contain_number') +
                i18n.global.t('should_contain_special_character') +
                i18n.global.t('should_be_8_characters_long')
            );
            return;
        }

        try {
            const response = await fetch('/api/player/register/', {
                method: 'POST',
                headers: {
                    'Content-usernameType': 'application/json',
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
                alert(i18n.global.t('successful_registration'));
                __goTo('/')
            } else {
                const errorData = await response.json();
                console.error('Error:', JSON.stringify(errorData, null, 2));

                const errorMessage = 
                    errorData.error || errorData.detail || 
                    errorData.non_field_errors?.join(', ') || 
                    'An unknown error has occurred';
                alert('Error: ' + errorMessage);
            }
        } catch (error) {
            console.error('Network error:', error);
            alert(i18n.global.t('network_error_occurred'));
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
        <div id="wrapper" @keydown.enter="handleEnter">
            <h1>{{ $t('SIGN_UP') }}</h1>
            <div class="logContainer">
                <button class="button button-login" @click="__goTo('/log')">
                    <span class="buttonText buttonTextSize">{{ $t('login') }}</span>
                </button>

                <div class="terms-container">
                    <input type="checkbox" id="terms" v-model="acceptTerms" />
                    <label for="terms">{{ $t('i_accept_the') }}<a href="/terms">{{ $t('terms_of_use') }}</a></label>
                </div>

                <button class="button button-createAccount" @click="createAccount">
                    <span class="buttonText buttonTextSize">{{ $t('create_account') }}</span>
                </button>
            </div>

            <div class="__inputInfo">
                <Input iconClass="fa-user" :placeholderText="`*${$t('username')}`" v-model="username" />
                <Input iconClass="fa-envelope" :placeholderText="`*${$t('email')}`" v-model="email" />
                <Input iconClass="fa-phone" :placeholderText="`${$t('phone_number')}`" v-model="phone_number" />
                <Input iconClass="fa-lock" :placeholderText="`*${$t('password')}`" isPassword v-model="password1" />
                <Input iconClass="fa-lock" :placeholderText="`*${$t('confirm_password')}`" isPassword
                    v-model="password2" />
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
        0 0 5px rgba(255, 255, 255s, 0.8),
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
    height: 59vh;
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
    top: 72%;

    background-color: rgba(202, 149, 128, 0.5);
    border: 0.15vw solid rgba(237, 230, 228, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
}

.button-login {
    position: fixed;
    width: 15vw;
    height: 6vh;
    left: 42.5%;
    top: 26.5%;

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

.button-createAccount:hover {
    border-color: rgb(185, 248, 252);
    text-decoration-color: rgb(185, 248, 252);
    background-color: rgba(0, 204, 227, 0.247);
    transition: border-color, background-color 0.5s;
    filter: drop-shadow(5px 5px 4px #ff04d585);
    transition: color 0.3s ease, font-size 0.3s ease;
}

.buttonText {
    font-size: 22px;
    color: rgb(255, 255, 255);
}

.button-createAccount:hover .buttonText {
    font-size: 23px;
    transition: color 0.3s ease, font-size 0.3s ease;
}

.terms-container {
    position: fixed;
    left: 40%;
    top: 69%;
    display: flex;
    align-items: center;
    font-size: 1.2vw;
    color: #fff;
}

.terms-container input[type="checkbox"] {
    margin-right: 0.5vw;
}

.terms-container a {
    color: #0dcaf0;
    text-decoration: none;
}

.terms-container a:hover {
    text-decoration: underline;
}

.button-createAccount {
    top: 73%;
    /* Ajusté pour rapprocher le bouton de la checkbox */
}

.__inputInfo {
    top: 35%;
    /* Vous pouvez ajuster selon votre design global */
}
</style>
