<!-- @lribette todo translate -->
<template>
    <main>
        <div id="wrapper">
            <div class="theme">
                <div class="custom-content">
                    <h1>ERROR 404 - NOT FOUND</h1>
                    <p>Please contact the developers if you think this is a mistake.</p>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
#wrapper {
    height: 100%;
    width: 100%;
    position: absolute;
    background-color: rgba(0, 0, 0, 0.5);
}

/* Styles pour la section de configuration si participants !== 4 */
.custom-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    color: white;
}
</style>
