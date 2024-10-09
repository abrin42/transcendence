<template>
    <div class="friends-popup">
        <div class="friends-header">
            <h3>My Friends</h3>
            <button class="close-button" @click="closePopup">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="friends-list">
            <div v-for="friend in friends" :key="friend.id" class="friend-item">
                {{ friend.name }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['close']);

const friends = ref([
    { id: 1, name: 'Friend 1' },
    { id: 2, name: 'Friend 2' },
    { id: 3, name: 'Friend 3' },
]);

function closePopup() {
    emit('close');
}
</script>

<style scoped>
.friends-popup {
    position: fixed;
    bottom: 15%;
    right: 1%;
    width: 20vw;
    height: 40vh;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;

    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;

    padding: 15px;
    z-index: 1000;
}

.friends-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.friends-list {
    margin-top: 10px;
    overflow-y: auto;
    max-height: 30vh;
}

.friend-item {
    padding: 8px;
    border-bottom: 1px solid white;
}

/* Close button */
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

/* Scroll bar */
.friends-popup::-webkit-scrollbar {
    width: 0.6vw;
}

.friends-popup::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 1vw;
    transition: border-color 0.5s;
}

.friends-popup::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.25);
    border-radius: 1vw;
    border: 1vw solid rgba(0, 0, 0, 0.25);
    transition: border-color 0.5s;
}

.friends-popup::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0, 0, 0, 0.4);
    transition: border-color 0.5s;
}
</style>