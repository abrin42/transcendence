<script setup>
    import { ref } from 'vue';
    import Input from './Input.vue';
    import Popup from './Popup.vue';

    const props = defineProps({
        modelValue: {
            type: String,
            default: '',
        },
        placeholderText: {
            type: String,
            default: 'Click to modify',
        },
        type: {
            type: String,
            default: 'text',
        },
        inputIconClass: {
            type: String,
            default: 'fa-solid fa-pen',
        },
        inputPlaceholder: {
            type: String,
            default: 'Modify the value',
        },
        isPassword: {
            type: Boolean,
            default: false,
        },
        isDisabled: {
            type: Boolean,
            default: false,
        },
    });

    const emit = defineEmits(['update:modelValue']);
    const showPopup = ref(false);
    const showErrorPopup = ref(false);
    const localValue = ref(props.modelValue);

    const openPopup = () => {
        if (props.isDisabled) {
            showErrorPopup.value = true;
        } else {
            showPopup.value = true;
        }
    };

    const closePopup = () => {
        showPopup.value = false;
        showErrorPopup.value = false;
    };

    const saveEdit = () => {
        emit('update:modelValue', localValue.value);
        closePopup();
    };
</script>

<template>
    <div class="editableTextContainer">
        <!-- Supprimez l'attribut :disabled et gérez tout via le click -->
        <button class="button button-editInput" @click="openPopup">
            <i class="fas fa-pen" style="margin-right: 0.5vw;"></i>
            <span class="buttonText buttonTextSize">
                {{ isPassword && modelValue ? '******' : (modelValue || placeholderText) }}
            </span>
        </button>

        <!-- Popup d'édition -->
        <Popup v-if="showPopup" @close="closePopup" class="popup-position">
            <label for="editInput">{{ $t('modify_the_value') }}</label>
            <Input :iconClass="inputIconClass" :placeholderText="inputPlaceholder" :isPassword="isPassword"
                v-model="localValue" />
            <button @click="saveEdit" class="save-button">{{ $t('save') }}</button>
        </Popup>

        <!-- Popup d'erreur -->
        <Popup v-if="showErrorPopup" @close="closePopup" class="popup-position">
            <label>{{ $t('prohibited_action') }}</label>
            <p>{{ $t('disabled_button') }}</p>
            <button @click="closePopup" class="save-button">{{ $t('close') }}</button>
        </Popup>
    </div>
</template>

<style scoped>
.editableTextContainer {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 1vw;
    left: 50%;
    max-width: 100%;
}

.buttonTextSize {
    font-size: 0.8rem;
}

.button-editInput {
    font-size: clamp(12px, 2vw, 16px);
    width: 14vw;
    height: 3vh;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
}

.buttonText {
    display: inline-block;
    max-width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.button-editInput[isDisable] {
    background-color: rgba(0, 0, 0, 1);
    cursor: not-allowed;
}

.displayText:hover {
    background-color: rgba(0, 0, 0, 0.75);
}

.fa-pen {
    font-size: 0.8rem;
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

label {
    margin-bottom: 1vw;
    font-size: 1.5rem;
    color: white;
}

.popup-position p {
    font-size: 1rem;
    color: white;
    margin-bottom: 1rem;
}
</style>
