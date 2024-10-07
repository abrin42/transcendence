<script setup>
import { ref, computed, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const userAccount = reactive({
    username:"",
    is_active:"",
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
    userAccount.username = user[0].fields.username;  // Set the username here
    userAccount.is_active = user[0].fields.is_active;  
} catch (error) {
    console.error('Error retrieving user data:', error);
  }
}

onMounted(async () => {
  await getUser(); // Only call getUser if state.id is available
});

function __goTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}


const minWidth = 7;
const charLimit = 11;
const initialLeft = 87.5;
const buttonWidth = computed(() => {
const text = userAccount.is_active ? userAccount.username : 'Login';
const extraChars = text.length - charLimit;

    if (extraChars > 0) {
        return `${minWidth + extraChars * 0.5}vw`;
    }
    return `${minWidth}vw`;
});

const buttonLeft = computed(() => {
    const currentWidth = parseFloat(buttonWidth.value);
    const widthDifference = currentWidth - minWidth;
    return `${initialLeft - widthDifference}vw`;
});
</script>

<template>
    <button class="button button-log" :style="{ width: buttonWidth, left: buttonLeft }"
        @click="__goTo(userAccount.is_active ? '/dashboard' : '/log')">
        <span class="buttonText">{{ userAccount.is_active ? userAccount.username : $t('login') }}</span>
    </button>
</template>

<style>
.button-log {
    position: fixed;
    height: 6vh;
    bottom: 93vh;
    transition: width 0.3s ease, left 0.3s ease;
}
</style>
