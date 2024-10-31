<script setup>
    import Input from '../components/Input.vue';
    import Popup from '../components/Popup.vue';
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import { useRouter } from 'vue-router';
    import { onBeforeMount, ref } from 'vue';
    import i18n from '../i18n.js';

    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////

    import { useUser } from '../useUser.js'; 
    
    const { getUser, is_connected } = useUser(); 

    onBeforeMount(async () => {
        await get2FAUser();
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
    
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    const sms2FA = ref("");
    const email2FA = ref("");

    async function get2FAUser() {
    try {
        const response = await fetch('/api/player/verify_user/', {
            method: 'GET',
            credentials: 'include',  
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.player_data) {
            const playerData = JSON.parse(data.player_data);  
            console.log('Player Data:', playerData);

            if (playerData.length > 0) {
                const user = playerData[0];  
                const userFields = user.fields; 
                console.log('User:', userFields);

                // Safely retrieve properties
                const username = userFields.username;
                sms2FA.value = userFields.sms_2fa_active;
                email2FA.value = userFields.email_2fa_active;

                console.log('Username:', username);
                console.log('SMS 2FA Active:', sms2FA);
                console.log('email 2FA Active:', email2FA);

            } else {
                alert(i18n.global.t('error_user_data_not_found'));
            }
        } else {
            alert(i18n.global.t('invalid_data_received'));
        }
    } catch (error) {
        console.error('Error during 2FA user fetch:', error);
        alert(i18n.global.t('error_login'));
    }
}

    async function handleNext() {
        try {
            const response = await fetch('/api/player/otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ user_otp: code.value })
            });
            if (response.status === 400) {
                alert(i18n.global.t('problem_with_code'), error);
                //throw new Error(`Code error! Status: ${response.status}`);
            }
            if (response.status !== 302 && response.status !== 200)
                __goTo('/2fa')

            else
                __goTo('/')

        } catch (error) {
            alert(i18n.global.t('problem_with_code'), error);
            //alert(i18n.global.t('error_OTPPP_setup'));
        }
    }

    async function choose_tfa(method) {
        try {
            const response = await fetch('/api/player/tfa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ otp_method: method })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            if (method === 'sms') {
                openPhonePopup();
            } else if (method === 'email') {
                openMailPopup();
            }
        } catch (error) {
            console.error('Error during TFA setup:', error);
            alert(i18n.global.t('error_TFA_setup'));
        }
    }
    function resendCode(method) {
        choose_tfa(method);
        alert(i18n.global.t('resend_code'));
    }
</script>

<template>
    <main>
        <div id="wrapper">
            <div v-if="!showMailPopup && !showPhonePopup" class="TwoFAContainer">
                <h1>{{ $t('send_code_question') }}</h1>
                <button v-if="sms2FA" class="button button-fa __button-phone" @click="() => {choose_tfa('sms')}">
                    <i class="fas fa-mobile-button" style="margin: 0.1vw;"></i>
                    <span>SMS</span>
                </button>
                <button v-if="email2FA" class="button button-fa __button-mail" @click="() => {choose_tfa('email')}">
                    <i class="fas fa-envelope" style="margin: 0.1vw;"></i>
                    <span>{{ $t('email') }}</span>
                </button>
            </div>
            <div class="buttonContainer">
                <CreateBackButton />
                <CreateDropupButton />
            </div>
        </div>

        <Popup v-if="showPhonePopup" @close="closePopup">
            <h2 class="__title-popup">{{  $t('phone_authentication') }}</h2>
            <p>{{ $t('enter_sms') }}</p>
            <Input iconClass="fa-shield" :placeholderText="$t('enter_your_code')" v-model="code" />
            <button class="button __button-send-code" @click="resendCode('sms')">
                <span>{{ $t('resend_the_code') }}</span>
            </button>
            <button class="button __button-next" @click="handleNext">
                <span>{{ $t('next') }}</span>
            </button>
        </Popup>

        <Popup v-if="showMailPopup" @close="closePopup">
            <h2 class="__title-popup">{{ $t('email_authentication') }}</h2>
            <p>{{ $t('enter_mail') }}</p>
            <Input iconClass="fa-shield" :placeholderText="$t('enter_your_code')" v-model="code" />
            <button class="button __button-send-code" @click="resendCode('email')">
                <span>{{ $t('resend_the_code') }}</span>
            </button>
            <button class="button __button-next" @click="handleNext">
                <span>{{ $t('next') }}</span>
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

@media (max-width: 480px) {false
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