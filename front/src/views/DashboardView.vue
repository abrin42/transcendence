<script setup>
    import CreateBackButton from '@/components/CreateBackButton.vue';
    import CreateDropupButton from '@/components/CreateDropupButton.vue';
    import InputEdit from '@/components/InputEdit.vue';
    import Switch from '@/components/Switch.vue';
    import TextDisplay from './../components/TextDisplay.vue';
    import profilePicture from '@/assets/img/default-profile.png';
    import CreateHomeButton from '../components/CreateHomeButton.vue';
    import Input from '../components/Input.vue';
    import { useRouter } from 'vue-router';
    import { ref, onBeforeMount } from 'vue';
    import i18n from '../i18n.js'
    
    ////////////////////////////////////////////////
    /////// GET USER ///////////////////////////////
    ////////////////////////////////////////////////
    
    import { useUser } from '../useUser.js'; 
    const { getUser, userAccount, is_connected } = useUser(); 
    
    onBeforeMount(async () => {
        await getUser();
        if (is_connected.value === false)
            __goTo('/')
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
    const showAllInfo = ref(false);

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////

    const username = ref('');
    const email = ref('');
    const phone_number = ref('');

    defineExpose({
        email,
        phone_number,
    });

    function isValidNickname(nickname) {
        const dangerousWords = ["admin", "root", "superuser", "user", "hitler", "@AI.Bot"];
        for (let word of dangerousWords) {
            if (new RegExp(`\\b${word}\\b`, "i").test(nickname)) {
                return false;
            }
        }
        const nicknameRegex = /^[a-zA-Z0-9_]+$/;
        return nicknameRegex.test(nickname);
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

    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    ////////////////////////////////////////////////
    
    async function updateAccount() {
        if (!isValidNickname(userAccount.nickname)) {
            alert(i18n.global.t('should_not_contain_spaces'));
            return;
        }

        if (!isValidEmail(userAccount.email)) {
            alert(i18n.global.t('please_enter_valid_email'));
            return;
        }
        
        if (userAccount.phone_number) {
            if (!isValidPhoneNumber(userAccount.phone_number)) {
                alert(i18n.global.t('please_enter_valid_phone_number'));
                return;
            }
        }

        if (userAccount.newpassword) {
            if (!isValidPassword(userAccount.newpassword)) {
                alert(
                    i18n.global.t('should_contain_capital_letter') +
                    i18n.global.t('should_contain_lower_case_letter') +
                    i18n.global.t('should_contain_number') +
                    i18n.global.t('should_contain_special_character') +
                    i18n.global.t('should_be_8_characters_long')
                );
                return;
            }
        }

        try {
            const response = await fetch('/api/player/update_user/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({
                    nickname: userAccount.nickname,
                    email: userAccount.email,
                    phone_number: userAccount.phone_number,
                    password: userAccount.newpassword,
                    profile_picture: userAccount.profilePicture,

                    email_2fa_active: userAccount.email_2fa_active,
                    sms_2fa_active: userAccount.sms_2fa_active,
                    anonymized: userAccount.anonymized,
                    username
                })
            });
            if (response.ok) {
                console.log(userAccount.nickname);
                const responseData = await response.json();
                alert(i18n.global.t('account_updated_successfully'));
            } else {
                const errorData = await response.json();
                console.log(errorData);
            }
        } catch (error) {
            console.error('Error updating account:', error);
            alert(i18n.global.t('error_account_update'));
        }
    }

    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    const handleLogout = async () => {
        try {
            await fetch("api/player/logout/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
            });
            router.push('/log');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    const handleDelete = async () => {
        try {
            await fetch("api/player/delete_account/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
            });
            router.push('/');
        } catch (error) {
            console.error('Deleting account failed:', error);
        }
    };

    const handleProfilePictureChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                userAccount.profilePicture = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    };
</script>

<template>
    <main>
        <div id="wrapper">
            <CreateBackButton />
            <CreateDropupButton />
            <div class="containerDashboard">
                <div class="input-section profile-picture-section">
                    <h2 class="category-title">{{ $t('profile_picture') }}</h2>
                    <img :src="userAccount.profilePicture || profilePicture" alt="Profile Picture" class="profile-picture" />
                    <label for="file-upload" class="custom-file-upload">
                        <i class="fas fa-upload"></i> {{ $t('choose_file') }}
                    </label>
                    <input id="file-upload" type="file" @change="handleProfilePictureChange" accept="image/*" class="hidden-file-input" />
                </div>

                <Switch class="infoGlobal" :buttonText="$t('see_all_information')" v-model="showAllInfo" />

                <div class="TextContainer">
                    <TextDisplay v-if="showAllInfo || !showAllInfo" :textValue="userAccount.email" :nameContainer="$t('email')" />
                    <TextDisplay v-if="showAllInfo || !showAllInfo" :textValue="userAccount.nickname" :nameContainer="$t('nickname')" />
                    <TextDisplay v-if="showAllInfo || !showAllInfo && userAccount.student == false" :textValue="userAccount.phone_number" :nameContainer="$t('phone_number')" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.username" :nameContainer="$t('username')" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.date_joined" :nameContainer="$t('date_joined')" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.win" :nameContainer="$t('number_of_wins')" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.lose" :nameContainer="$t('number_of_defeats')" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.rank" :nameContainer="$t('rank')" />
                </div>

                <div class="editable-input-container">
                    <InputEdit v-model="userAccount.nickname" :placeholderText="$t('change_nickname')" inputIconClass="fa-user" :inputPlaceholder="$t('enter_nickname')" :isPassword="false" />
                    <InputEdit v-model="userAccount.email" :placeholderText="$t('change_email')" inputIconClass="fa-user" :inputPlaceholder="$t('enter_email')" :isPassword="false" :isDisabled="userAccount.student === true" />
                    <InputEdit v-if="userAccount.student === false" v-model="userAccount.phone_number" :placeholderText="$t('change_phone_number')" inputIconClass="fa-user" :inputPlaceholder="$t('enter_phone_number')" :isPassword="false" />
                    <InputEdit v-if="userAccount.student === false" v-model="userAccount.newpassword" :placeholderText="$t('change_password')" inputIconClass="fa-lock" :inputPlaceholder="$t('enter_password')" :isPassword="true" />

                    <div class="___btn-click">
                        <button class="button button-update" @click="updateAccount">
                            <span class="buttonText buttonTextSize" style="font-size: medium;">{{ $t('update_account') }}</span>
                        </button>
                        <button class="button button-logout" @click="handleLogout">
                            <span class="buttonText buttonTextSize" style="font-size: medium;">{{ $t('logout') }}</span>
                        </button>
                        <button class="button button-logout" @click="handleDelete">
                            <span class="buttonText buttonTextSize" style="font-size: medium;">{{ $t('delete_account') }}</span>
                        </button>
                    </div>
                </div>

                <div class="SwitchStyle" v-if="userAccount.student === false">
                    <Switch :buttonText="`${$t('activate')} 2FA (SMS)`" :isDisabled="userAccount.phone_number === '' ? false : true" v-model="userAccount.sms_2fa_active" />
                    <Switch :buttonText="`${$t('activate')} 2FA (${$t('email')})`" v-model="userAccount.email_2fa_active" />
                    <Switch :buttonText="`${$t('activate')} Anonymization`" v-model="userAccount.anonymized" />
                </div>

                <div class="terms-container">
                    <label for="terms"><a href="/terms">Terms of use</a></label>
                </div>
            </div>
        </div>
    </main>
</template>


<style scoped>s
h1,
.category-title {
    font-size: 1.5rem;
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

#wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.8);
    padding: 20px;
}

.containerDashboard {
    position: fixed;
    width: 40vw;
    height: 85vh;
    left: 30%;
    top: 5%;
    border-radius: 0.5vw;
    padding: 1.5vw;
    background-color: rgba(0, 0, 0, 0.25);
    overflow-y: auto;
    overflow-x: hidden;
}

.containerDashboard::-webkit-scrollbar {
    width: 0.6vw;
}

.containerDashboard::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 1vw;
    transition: border-color 0.5s;
}

.containerDashboard::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.25);
    border-radius: 1vw;
    border: 1vw solid rgba(0, 0, 0, 0.25);
    transition: border-color 0.5s;
}

.containerDashboard::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0, 0, 0, 0.4);
    transition: border-color 0.5s;
}

.InputEdit {
    margin-right: 0.1vw;
    margin-top: 0.1vw;
}

.profile-picture-section {
    display: flex;
    align-items: center;
    flex-direction: column;
}

.profile-picture {
    width: 8vw;
    height: 8vw;
    object-fit: cover;
    border-radius: 50%;
    border: 0.2vw solid #fff;
    margin-bottom: 1vw;
}

.category-title {
    margin-bottom: 1vw;
    text-align: left;
}

.hidden-file-input {
    display: none;
}

.custom-file-upload {
    display: inline-block;
    padding: 0.8vw;
    font-size: 1vw;
    border: 0.15vw solid rgba(255, 255, 255, 0.25);
    border-radius: 0.4vw;
    background-color: rgba(0, 0, 0, 0.25);
    cursor: pointer;
    margin-top: 0.8vw;
    color: #fff;
}

.custom-file-upload i {
    margin-right: 0.5vw;
}

.custom-file-upload:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}

.editable-input-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.editable-input-container>* {
    margin: 0.01vw 1vw;
    flex: 4 1 calc(30% - 20px);
    min-width: 200px;
    max-width: 30%;
    box-sizing: border-box;
    height: 80px;
}

.SwitchStyle {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1vw;
    margin-top: 1vw;
}

.TextContainer {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 1vw;
    margin-top: 1vw;
}

.TextContainer div {
    /* margin: 1vw 1vw; */
    min-width: 200px;
    text-align: center;
}

/* Pour chaque bloc de texte */
.TextContainer div:nth-child(2n+1) {}

.___btn-click {
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    white-space: nowrap;
    flex: 1 1 calc(30% - 20px);
    margin: 1vw;
    gap: 10px;
}

.button-update {
    background-color: rgba(74, 143, 74, 0.75);
}

.button-logout {
    background-color: rgba(143, 74, 74, 0.75);
}
</style>