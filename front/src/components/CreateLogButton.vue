<template>
    <button class="button button-log" :style="{ width: buttonWidth, left: buttonLeft }">
        <span v-if="isConnect" @click="__goTo('/dashboard')" class="buttonText">{{ login }}</span>
        <span v-else @click="__goTo('/log')" class="buttonText">{{ $t('login') }}</span>
    </button>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

function __goTo(page) {
    if (page == null) {
        return;
    }
    router.push(page);
}

const isConnect = ref(false);
var login = 'Name player';

const minWidth = 7;
const charLimit = 11;
const initialLeft = 87.5;
const buttonWidth = computed(() => {
    const text = isConnect.value ? login : 'Login';
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

<style>
.button-log {
    position: fixed;
    height: 6vh;
    bottom: 93vh;
    transition: width 0.3s ease, left 0.3s ease;
}
</style>
