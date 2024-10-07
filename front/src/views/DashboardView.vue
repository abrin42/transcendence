<script setup>
import { ref } from 'vue';
import CreateBackButton from '@/components/CreateBackButton.vue';
import CreateDropupButton from '@/components/CreateDropupButton.vue';
import InputEdit from '@/components/InputEdit.vue';
import profilePicture from '@/assets/img/default-profile.png';
import { reactive, onMounted } from 'vue';

const userAccount = reactive({
  date_joined:"",
  email:"",
  email_2fa_active:false,
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
    const response = await fetch(`http://localhost:8080/api/player/connected_user`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const user = await response.json();
    console.log('User data:', user);
    console.log('player data', user[0].fields)
    userAccount.nickname = user[0].fields.nickname;
    userAccount.username = user[0].fields.username;  // Set the username here
    userAccount.email = user[0].fields.email;
    userAccount.password = user[0].fields.password;
  } catch (error) {
    console.error('Error retrieving user data:', error);
  }
}

onMounted(async () => {
  await getUser(); // Only call getUser if state.id is available
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

                <div class="input-section">
                    <h2 class="category-title">{{ $t('username') }}</h2>
                    <InputEdit class="inputEdit" v-model="userAccount.username" placeholderText="Edit Username" />
                </div>

                <div class="input-section">
                    <h2 class="category-title">{{ $t('email') }}</h2>
                    <InputEdit class="inputEdit" v-model="userAccount.email" placeholderText="Edit Email" />
                </div>

                <div class="input-section">
                    <h2 class="category-title">{{ $t('password') }}</h2>
                    <div class="password-field">
                        <InputEdit class="inputEdit" v-model="userAccount.password" placeholderText="Edit Password"
                            type="password" />
                    </div>
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
    height: auto;
    left: 30%;
    top: 5%;
    padding: 1.5vw;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    background-color: rgba(0, 0, 0, 0.25);
}

.input-section {
    margin: 2vw 0;
}

.inputEdit {
    width: 100%;
    padding: 0.8vw;
    border: 0.1vw solid rgba(255, 255, 255, 0.25);
    border-radius: 0.4vw;
    font-size: 1vw;
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

.upload-btn,
.inputEdit {
    border: 0.15vw solid rgba(255, 255, 255, 0.25);
    border-radius: 0.4vw;
}

.upload-btn:hover,
.custom-file-upload:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.password-field {
    position: relative;
    display: flex;
    align-items: center;
}

.toggle-password {
    position: absolute;
    right: 1vw;
    cursor: pointer;
    font-size: 1.2vw;
    color: rgba(255, 255, 255, 0.6);
}

.toggle-password:hover {
    color: rgba(255, 255, 255, 1);
}
</style>
