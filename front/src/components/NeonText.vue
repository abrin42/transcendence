<template>
    <div>
        <h1 :class="['category-title', { 'font-bold': isBold, 'font-italic': isItalic }]" :style="{
            fontSize: fontSize + 'rem',
            top: position.top + '%',
            left: position.left + '%',
            right: position.right + '%',
            bottom: position.bottom + '%',
        }">
            <slot></slot>
        </h1>
    </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'TextComponent',
    props: {
        isBold: {
            type: Boolean,
            default: false,
        },
        isItalic: {
            type: Boolean,
            default: false,
        },
        fontSize: {
            type: Number,
            default: 3.5, // Taille de police par défaut
        },
        position: {
            type: Object,
            default: () => ({
                top: 10, // Position par défaut en haut à 10%
                left: 'auto',
                right: 'auto',
                bottom: 'auto',
            }),
        },
    },
});
</script>

<style scoped>
.category-title {
    color: #fff;
    position: fixed;
    z-index: 1;
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.8),
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
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.8),
            0 0 10px rgba(255, 255, 255, 0.6),
            0 0 20px rgba(255, 20, 147, 0.6),
            0 0 30px rgba(255, 20, 147, 0.6),
            0 0 40px rgba(255, 20, 147, 0.6),
            0 0 50px rgba(255, 20, 147, 0.6),
            0 0 60px rgba(255, 20, 147, 0.6);
    }

    to {
        text-shadow: 0 0 10px rgba(255, 255, 255, 1),
            0 0 20px rgba(255, 255, 255, 0.8),
            0 0 30px rgba(255, 20, 147, 0.8),
            0 0 40px rgba(255, 20, 147, 0.8),
            0 0 50px rgba(255, 20, 147, 0.8),
            0 0 60px rgba(255, 20, 147, 0.8),
            0 0 70px rgba(255, 20, 147, 0.8);
    }
}

/* Styles pour le gras et l'italique */
.font-bold {
    font-weight: bold;
}

.font-italic {
    font-style: italic;
}
</style>