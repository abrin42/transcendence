<template>
    <div class="toggle-container">
        <span class="textToggleButton">{{ buttonText }}</span>
        <label class="switch" @click="checkDisabled">
            <input type="checkbox" :checked="modelValue" @change="onToggle" :disabled="isDisabled">
            <span class="slider"></span>
        </label>
    </div>

    <!-- Popup d'erreur conditionnelle -->
    <Popup v-if="showError" @close="closeError" class="popup-position">
        <label>{{ $t('prohibited_action') }}</label>
        <p>{{ $t('disabled_switch') }}</p>
        <button @click="closeError" class="save-button">{{ $t('close') }}</button>
    </Popup>
</template>

<script setup>
import Popup from './Popup.vue';
// @params buttonText: String
// @params checkedColor: String
// @params modelValue: Boolean
// @params isDisabled: Boolean
const props = defineProps({
    buttonText: {
        type: String,
        default: '2FA',
    },
    checkedColor: {
        type: String,
        default: '#2196F3',
    },
    modelValue: {
        type: Boolean,
        default: false,
    },
    isDisabled: {
        type: Boolean,
        default: false,
    }
});

const emit = defineEmits(['update:modelValue']);

// State to track if the error popup should be shown
import { ref } from 'vue';
const showError = ref(false);

const onToggle = (event) => {
    if (!props.isDisabled) {
        emit('update:modelValue', event.target.checked);
    }
};

// Check if the switch is disabled and show error popup
const checkDisabled = () => {
    if (props.isDisabled) {
        showError.value = true;
    }
};

// Close the error popup
const closeError = () => {
    showError.value = false;
};
</script>

<style scoped>
    .toggle-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .textToggleButton {
        padding: 1vh 1vw;
        max-height: 4vh;
        height: 4vh;
        border-radius: 0.4vw;
        color: white;
        font-size: 1rem;
        margin-bottom: 1vh;
    }

    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }

    .switch input {
        opacity: 0;
        width: 4vw;
        height: 4vh;
    }

    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.25);
        padding: 0.1vh 0.1vw;
        height: 4vh;
        border: 0.15vw solid rgba(0, 0, 0, 0.25);
        border-radius: 0.4vw;
        -webkit-transition: .4s;
        transition: .4s;
    }

    .slider:before {
        position: absolute;
        content: "";
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.25);
        margin: 0.2vh 0.1vw;
        height: 3vh;
        width: 1.5vw;
        border: 0.15vw solid rgba(0, 0, 0, 0.25);
        border-radius: 0.4vw;
        -webkit-transition: .4s;
        transition: .4s;
    }

    input:checked+.slider {
        background-color: v-bind(checkedColor);
    }

    input:checked+.slider:before {
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
    }

    .slider.round {
        border-radius: 34px;
    }

    .slider.round:before {
        border-radius: 50%;
    }

    .popup-position {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 2vw;
        border-radius: 1vw;
    }

    .popup-position p {
        font-size: 1rem;
        color: white;
        margin-bottom: 1rem;
    }

    .save-button {
        margin-top: 10px;
        padding: 0.5vw;
        width: 100px;
        height: 40px;
        background-color: rgba(0, 128, 0, 0.75);
        color: white;
        border: none;
        border-radius: 0.4vw;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: clamp(12px, 2vw, 16px);
    }

    .save-button:hover {
        background-color: rgb(90, 190, 90);
    }
</style>
