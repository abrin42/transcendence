<template>
    <div class="popup-overlay" @click="close">
        <div class="popup-content" @click.stop>
            <slot></slot>
            <button class="close-button" @click="close">
                <i class="fas fa-times"></i>
            </button>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    show: {
        type: Boolean,
        required: true,
    }
});

const emit = defineEmits(['close']);

function close() {
    emit('close');
}
</script>

<style scoped>
.popup-overlay {
    position: fixed;
    width: 100%;
    height: 100%;

    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.popup-content {
    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;

    padding: 20px;
    border-radius: 10px;
    width: 400px;
    position: relative;
    color: white;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 16px;
    color: white;
    cursor: pointer;
}

.close-button:hover {
    color: rgb(164, 9, 9)
}
</style>