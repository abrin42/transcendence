<script setup>
    import CreateBackButton from '@/components/CreateBackButton.vue';
    import CreateDropupButton from '@/components/CreateDropupButton.vue';
    import InputEdit from '@/components/InputEdit.vue';
    import Switch from '@/components/Switch.vue';
    import TextDisplay from './../components/TextDisplay.vue';
    import profilePicture from '@/assets/img/default-profile.png';
    import { ref } from 'vue';
    import { reactive, onMounted } from 'vue';
    import { useRouter } from 'vue-router';

    const router = useRouter();
    const showAllInfo = ref(false);

    const is_connected = ref('');
    const userAccount = reactive({
        date_joined:"",
        email:"",
        email_2fa_active:"",
        sms_2fa_active:"",
        lose:0,
        nickname:"",
        password:"",
        phone_number:"",
        profilePicture: profilePicture,
        rank:0,
        username:"",
        win:0,
    });
    async function getUser() {
        try {
            const response = await fetch(`api/player/connected_user/`, {
                method: 'GET',
            });
            if (!response.ok) {
                console.warn(`HTTP error! Status: ${response.status}`);
                return;
            }
            const user = await response.json();
            if (user) {
                userAccount.nickname = user[0].fields.nickname;
                userAccount.username = user[0].fields.username;
                userAccount.email = user[0].fields.email;
                userAccount.password = user[0].fields.password;
                userAccount.phone_number = user[0].fields.phone_number;
                userAccount.student = user[0].fields.student;
                userAccount.email_2fa_active = user[0].fields.email_2fa_active;
                userAccount.sms_2fa_active = user[0].fields.sms_2fa_active;
                
                is_connected.value = true;

                console.log(userAccount.student)
                console.log(userAccount.nickname)
                console.log(is_connected.value)
            } else {
                console.log('No user data retrieved.');
                is_connected.value = false;
                return;
            }
        } catch (error) {
            console.error('Error retrieving user data:', error);
        }
    }

    const email_2fa_active = ref('');
    const sms_2fa_active = ref('');
    async function postUser() {
        try {
            const response = await fetch('api/player/update_2fa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({
                    email_2fa_active: userAccount.email_2fa_active,
                    sms_2fa_active: userAccount.sms_2fa_active,
                })
            });
            console.log(email_2fa_active);
            console.log(sms_2fa_active);
        } catch (error) {
            console.error('Erreur lors de la création du compte:', error);
            alert('Une erreur est survenue pendant la création du compte.');
        }
    }

    function getAccountType() {
        if (userAccount.student === true)
            return "42";
        return "normal";
    }
    
    const logoutUrl = "api/player/logout/";

    const handleLogout = async () => {
        try {
            await fetch(logoutUrl, {
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

    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    onMounted(async () => {
        await getUser(); // Only call getUser if state.id is available
        //postUser();
    });

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
                    <img :src="userAccount.profilePicture || 'default-profile.png'" alt="Profile Picture"
                        class="profile-picture" />
                    <label for="file-upload" class="custom-file-upload">
                        <i class="fas fa-upload"></i> {{ $t('choose_file') }}
                    </label>
                    <input id="file-upload" type="file" @change="handleProfilePictureChange" accept="image/*"
                        class="hidden-file-input" />
                </div>

                <Switch class="infoGlobal" buttonText="See all information" v-model="showAllInfo" />

                <div class="TextContainer">
                    <TextDisplay v-if="showAllInfo || !showAllInfo" :textValue="userAccount.email"
                        nameContainer="Email" />
                    <TextDisplay v-if="showAllInfo || !showAllInfo" :textValue="userAccount.nickname"
                        nameContainer="Nickname" />
                    <TextDisplay v-if="showAllInfo || !showAllInfo" :textValue="userAccount.phone_number"
                        nameContainer="Phone number" />

                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.username" nameContainer="Username" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.password" nameContainer="Password" />
                    <!-- Faire en sorte que le password puisse etre afficher vie un oeil -->
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.date_joined" nameContainer="Date joined" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.win" nameContainer="Number of win" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.lose" nameContainer="Number of lose" />
                    <TextDisplay v-if="showAllInfo" :textValue="userAccount.rank" nameContainer="Rank" />
                </div>

                <div class="editable-input-container">

                    <InputEdit v-model="userAccount.nickname" placeholderText="Change your nickname"
                        inputIconClass="fa-user" inputPlaceholder="Enter your nickname" :isPassword="false" />

                    <InputEdit v-model="userAccount.email" placeholderText="Change your email" inputIconClass="fa-user"
                        inputPlaceholder="Enter your email" :isPassword="false"
                        :isDisabled="getAccountType() === '42'" />

                    <!-- Utilisation de v-if pour retirer complètement du DOM les champs non nécessaires pour un compte 42 -->
                    <InputEdit v-if="getAccountType() !== '42'" v-model="userAccount.phone_number"
                        placeholderText="Change your phone number" inputIconClass="fa-user"
                        inputPlaceholder="Enter your phone number" :isPassword="false" />

                    <InputEdit v-if="getAccountType() !== '42'" v-model="userAccount.password"
                        placeholderText="Change your password" inputIconClass="fa-lock"
                        inputPlaceholder="Enter your password" :isPassword="true" />


                    <div class="___btn-click">
                        <button class="button">
                            <span class="buttonText buttonTextSize" style="font-size: medium;">Friends</span>
                        </button>

                        <button class="button">
                            <span class="buttonText buttonTextSize" @click="handleLogout" style="font-size: medium;">Logout</span>
                        </button>

                        <button class="button">
                            <span class="buttonText buttonTextSize" style="font-size: medium;">Delete account</span>
                        </button>
                    </div>
                </div>
                <div class="SwitchStyle" v-if="getAccountType() !== '42'">
                    <Switch buttonText="Activer 2FA (SMS)"
                        :isDisabled="userAccount.phone_number === '' ? false : true" 
                        v-model="userAccount.sms_2fa_active" />
                    <Switch buttonText="Activer 2FA (EMAIL)" 
                        v-model="userAccount.email_2fa_active"/>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
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
.TextContainer div:nth-child(2n+1) {
    /* Ceci pour rendre le premier texte visuellement distinct si nécessaire */
}

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

/* Pour chaque bloc de texte */
.TextContainer div:nth-child(2n+1) {
    /* Ceci pour rendre le premier texte visuellement distinct si nécessaire */
}

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
</style>