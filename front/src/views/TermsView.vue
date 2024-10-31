<script setup>
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import CreateHomeButton from '../components/CreateHomeButton.vue';
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="terms-container">
                <!-- Navigation buttons -->
                <div class="buttons-container">
                    <CreateBackButton />
                    <CreateHomeButton />
                    <CreateDropupButton />
                </div>

                <!-- Privacy Policy Text -->
                <div class="terms-text-container">
                    <h1>Privacy Policy</h1>
                    <p><strong>Effective Date:</strong> 20/07/2024</p>

                    <h2>1. Introduction</h2>
                    <p>
                        Welcome to CYBERPONG ("we," "our," or "us"). This Privacy Policy outlines how we collect, use,
                        and
                        protect the personal data you provide when interacting with our website and services. We take
                        your
                        privacy seriously and are committed to ensuring that your personal information is safe and
                        secure.
                    </p>

                    <h2>2. Information We Collect</h2>
                    <h3>2.1. Personal Information</h3>
                    <p>We collect the following personal information to provide and improve our services:</p>
                    <ul>
                        <li>Email Address: Used for account management and communication.</li>
                        <li>Phone Number: Used for two-factor authentication (2FA) to secure your account.</li>
                        <li>Username: Collected and used for gameplay and account purposes.</li>
                    </ul>

                    <h3>2.2. Game Information</h3>
                    <p>
                        Gameplay Data: Includes scores, achievements, and preferences to enhance your gaming experience.
                    </p>

                    <h2>3. How We Use Your Information</h2>
                    <p>We use your personal information for the following purposes:</p>
                    <ul>
                        <li>Account Security: To enable 2FA and safeguard your account.</li>
                        <li>Communication: To send account-related notifications and respond to inquiries.</li>
                        <li>Gameplay Data: To provide relevant game-related information.</li>
                        <li>Service Improvement: To analyze and improve user experience.</li>
                    </ul>

                    <h2>4. Legal Basis for Processing</h2>
                    <p>We process your personal data based on:</p>
                    <ul>
                        <li>Consent: We seek your explicit consent for 2FA and account management purposes.</li>
                        <li>Contractual Necessity: Processing is necessary to provide our services and access to game
                            information.</li>
                        <li>Legitimate Interests: For the security and improvement of our platform and services.</li>
                    </ul>

                    <h2>10. Contact Us</h2>
                    <p>
                        If you have any questions or concerns regarding this Privacy Policy or our data practices,
                        please
                        contact us at:
                    </p>
                    <p>Email: proj42_lh@proton.me</p>
                    <p>Address: 20 Quai Frissard, 76600 Le Havre, [FRANCE]</p>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
#wrapper {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.8);
    padding: 20px;
}

.buttons-container {
    display: flex;
    justify-content: space-between;
    width: 100%;
    padding: 10px;
    position: sticky;
    top: 0;
    z-index: 1000;
    background-color: rgba(0, 0, 0, 0.5);
}

.terms-text-container {
    color: white;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 30px;
    border-radius: 10px;
    max-width: 800px;
    width: 100%;
    max-height: 60vh;
    overflow-y: auto;
    font-size: 1.2rem;
    line-height: 1.6;
    margin: 20px 0;
}

.terms-text-container h1,
.terms-text-container h2,
.terms-text-container h3 {
    color: #ffcc00;
}

.terms-text-container ul {
    padding-left: 20px;
    list-style-type: disc;
}

.terms-text-container li {
    margin-bottom: 10px;
    padding-left: 0;
    text-align: left;
}

@media (max-width: 600px) {
    .terms-text-container {
        font-size: 1rem;
        padding: 15px;
        max-height: 50vh;
    }
}
</style>
