<script setup>
    import { ref, computed } from 'vue';

    const props = defineProps({
        modelValue: {
            type: String,
            default: '',
        },
        iconClass: {
            type: String,
            default: 'fa-user'
        },
        placeholderText: {
            type: String,
            default: 'Enter your text'
        },
        isPassword: {
            type: Boolean,
            default: false
        }
    });

    const isPasswordVisible = ref(false);
    const inputType = computed(() => {
        return props.isPassword && !isPasswordVisible.value ? 'password' : 'text';
    });

    const togglePasswordVisibility = () => {
        isPasswordVisible.value = !isPasswordVisible.value;
    };

    const emit = defineEmits(['update:modelValue']);
</script>

<template>
    <div class="inputContainer">
        <i :class="`fa-solid ${iconClass}`" class="inputIcon"></i>

        <input :type="inputType" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"
            :placeholder="placeholderText" class="textInput" />

        <i v-if="isPassword" :class="`fa-solid ${isPasswordVisible ? 'fa-eye' : 'fa-eye-slash'}`"
            class="togglePasswordIcon" @click="togglePasswordVisibility">
        </i>
    </div>
</template>

<style scoped>
.inputContainer {
    position: relative;
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.inputIcon {
    opacity: 0.8;
    position: absolute;
    left: 10px;
    color: rgb(255, 255, 255);
    font-size: 1.5rem;
    z-index: 1;
}

.textInput {
    width: 15vw;
    height: 5vh;
    padding-left: 3rem;
    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    font-size: larger;
    color: white;
    transition: background-color 0.3s ease;
}

.textInput::placeholder {
    position: fixed;
    top: 1.5vh;
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.5);
}

.textInput:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.75);
}

.togglePasswordIcon {
    position: absolute;
    right: 10px;
    color: rgb(255, 255, 255);
    font-size: 1rem;
    opacity: 0.5;
    cursor: pointer;
}
</style>
