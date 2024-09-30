<script setup>
import { ref } from 'vue';

const props = defineProps({
    modelValue: {
        type: String,
        default: '',
    },
    placeholderText: {
        type: String,
        default: 'Cliquez pour modifier',
    },
    type: {
        type: String,
        default: 'text',
    },
});

const emit = defineEmits(['update:modelValue']);
const isEditing = ref(false);
const localValue = ref(props.modelValue);
const showPassword = ref(false);

const enableEditing = () => {
    isEditing.value = true;
};

const saveEdit = () => {
    isEditing.value = false;
    emit('update:modelValue', localValue.value);
};

const onBlur = () => {
    saveEdit();
};

const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value;
};
</script>

<template>
    <div class="editableTextContainer">
        <span v-if="!isEditing" @click="enableEditing" class="displayText">
            <i class="fas fa-pencil-alt"></i>
            {{ modelValue || placeholderText }}
        </span>

        <div v-else class="inputWrapper">
            <input v-model="localValue" @blur="onBlur" @keyup.enter="saveEdit"
                :type="type === 'password' && !showPassword ? 'password' : 'text'" class="editableInput" />
            <i v-if="type === 'password'" :class="showPassword ? 'fas fa-eye' : 'fas fa-eye-slash'"
                @click="togglePasswordVisibility" class="toggle-password"></i>
        </div>
    </div>
</template>

<style scoped>
.editableTextContainer {
    display: flex;
    align-items: center;
}

.displayText {
    font-size: 1vw;
    color: white;
    cursor: pointer;
    padding: 1vh;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
}

.displayText:hover {
    background-color: rgba(0, 0, 0, 0.75);
}

.inputWrapper {
    position: relative;
    width: 100%;
}

.editableInput {
    font-size: 1vw;
    padding: 1vh;
    background-color: rgba(255, 255, 255, 0.1);
    border: 0.15vw solid rgba(255, 255, 255, 0.75);
    color: white;
    border-radius: 0.4vw;
    width: 100%;
}

.editableInput:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.95);
}

.fas {
    margin-right: 0.5vw;
    font-size: 1vw;
    color: white;
}

.toggle-password {
    position: absolute;
    right: 1vw;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    color: rgba(255, 255, 255, 0.6);
}

.toggle-password:hover {
    color: rgba(255, 255, 255, 1);
}
</style>
