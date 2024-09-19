<template>

    <button class="button" @click="goBack">
        <!-- ajouter icone retour? -->
        <span class="buttonText buttonTextSize">{{ $t('back') }}</span>
    </button>

</template>
  
<script setup>
    import { useRouter } from 'vue-router';

    const router = useRouter();
    function goBack() {
        router.go(-1);
    }
</script>
  
<style>
</style>