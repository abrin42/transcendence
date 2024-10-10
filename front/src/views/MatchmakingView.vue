<script setup>
//imports
    import CreateDropupButton from '../components/CreateDropupButton.vue';
    import CreateBackButton from '../components/CreateBackButton.vue';
    import CreateSoundButton from '../components/CreateSoundButton.vue';
    import { reactive, onMounted } from 'vue';
    import { useRouter } from 'vue-router';

    var myVideo = document.getElementById('videoBG');
    myVideo.playbackRate = 1.3;
    
    const router = useRouter();

    const userAccount = reactive({
        nickname:"", 
        // profilePicture: profilePicture,
        rank:0,
    });


    function goToLegacy(id) {
    router.push(`/legacy/${id}`);
}


    



    onMounted(async () => {
        // await postUser();
    });
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="buttonContainer">
                <div>
                    <CreateSoundButton />
                </div>
                <div>
                    <CreateDropupButton />
                </div>
                <div>
                    <CreateBackButton />
                </div>
            </div>
        </div>
    </main>
</template>

<style lang="scss">
@import './../assets/main.scss';


</style>