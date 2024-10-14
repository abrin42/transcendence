<script setup>
    import { ref } from 'vue';

    // @params {String} textValue - The text to display
    // @params {String} nameContainer - The name of the container
    const props = defineProps({
        textValue: {
            type: String,
            default: '',
        },
        nameContainer: {
            type: String,
            default: '',
        },
    });

    const showPopup = ref(false);

    const openPopup = () => {
        showPopup.value = true;
    };

    const closePopup = () => {
        showPopup.value = false;
    };
</script>

<template>
    <div class="textDisplayContainer">
        <div class="containerName">{{ nameContainer || 'Nom du container' }}</div>
        <div class="textDisplay">
            <span class="displayedText">{{ textValue || $t('no_text_to_display') }}</span>
        </div>
    </div>
</template>

<style scoped>
.textDisplayContainer {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 1vw;
    left: 50%;
    max-width: 100%;
}

.containerName {
    font-size: 1rem;
    /* font-weight: 0.1rem; */
    margin-bottom: 0.5vh;
    color: white;
    text-align: left;
}

.textDisplay {
    font-size: clamp(12px, 2vw, 16px);
    width: 14vw;
    height: 3vh;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;

    color: white;
    padding: 0.5vw;
    border-radius: 0.4vw;
    display: flex;
    align-items: center;
    justify-content: center;

    background-color: rgba(0, 0, 0, 0.25);
    padding: 2vh 2vw;
    border: 0.15vw ridge rgba(255, 124, 216, 0.6);
    border-radius: 0.4vw;
}

.displayedText {
    font-size: 0.8rem;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
}
</style>
