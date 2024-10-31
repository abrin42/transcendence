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
                    <h1>{{ $t('privacy_policy') }}</h1>
                    <p><strong>{{ $t('effective_date') }}</strong> {{ $t('date') }}</p>

                    <h2>{{ $t('introduction') }}</h2>
                    <p>
                        {{ $t('welcome_to_pong_wars') }}
                    </p>

                    <h2>{{ $t('information_we_collect') }}</h2>
                    <h3>{{ $t('personal_information') }}</h3>
                    <p>{{ $t('we_collect_following_informations') }}</p>
                    <ul>
                        <li>{{ $t('we_collect_email_address') }}</li>
                        <li>{{ $t('we_collect_phone_number') }}</li>
                        <li>{{ $t('we_collect_username') }}</li>
                    </ul>

                    <h3>{{ $t('game_information') }}</h3>
                    <p>
                        {{ $t('gameplay_data') }}
                    </p>

                    <h2>{{ $t('how_we_use_your_information') }}</h2>
                    <p>{{ $t('we_use_your_information_for') }}</p>
                    <ul>
                        <li>{{ $t('for_account_security') }}</li>
                        <li>{{ $t('for_communication') }}</li>
                        <li>{{ $t('for_gameplay_data') }}</li>
                        <li>{{ $t('for_service_improvement') }}</li>
                    </ul>

                    <h2>{{ $t('legal_basis_for_processing') }}</h2>
                    <p>{{ $t('we_process_your_data_based_on') }}</p>
                    <ul>
                        <li>{{ $t('consent') }}</li>
                        <li>{{ $t('contractual_necessity') }}</li>
                        <li>{{ $t('legitimate_interests') }}</li>
                    </ul>

                    <h2>{{ $t('contact_us') }}</h2>
                    <p>
                        {{ $t('any_questions_contact_us') }}
                    </p>
                    <p>{{ $t('email') }}: proj42_lh@proton.me</p>
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
