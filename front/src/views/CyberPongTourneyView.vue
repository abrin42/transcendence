<script setup>
import CreateDropupButton from '@/components/CreateDropupButton.vue';
import CreateBackButton from '@/components/CreateBackButton.vue';
import NeonText from '@/components/NeonText.vue';
import Input from '@/components/Input.vue'; // Assurez-vous que ce composant Input existe

import { useRouter } from 'vue-router';
import { onBeforeMount, ref, watch, onUnmounted } from 'vue';
import { useUser } from '../useUser.js';
import i18n from '../i18n.js';

const { getUser } = useUser();
const router = useRouter();
const timer = ref(10);
let interval = null;

// Charger les utilisateurs et démarrer le timer si 4 participants
onBeforeMount(async () => {
    await getUser();
});

// Navigation vers une autre page
function __goTo(page) {
    if (page) {
        router.push(page);
    }
}

// Liste des participants
const participants = ref([]);

// Référence pour les nouveaux participants
const newParticipants = ref(["", "", "", ""]);

// Matches de tournoi
const matches = ref([
    { round: 'SEMI', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' },
    { round: 'SEMI', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' },
    { round: 'SMALL_FINAL', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' },
    { round: 'FINAL', team1: '', team2: '', score1: 0, score2: 0, winner: '', loser: '' }
]);

// Fonction pour mélanger les participants
function shuffleParticipants() {
    for (let i = participants.value.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [participants.value[i], participants.value[j]] = [participants.value[j], participants.value[i]];
    }
}

// Démarrer le tournoi si le nombre de participants est de 4
async function startTournament() {
    if (participants.value.length === 4) {
        shuffleParticipants(); // Mélange les participants
        setupSemiFinals(); // Configure les demi-finales
        await new Promise(resolve => setTimeout(resolve, 1000));
        updateScore(0);
        await new Promise(resolve => setTimeout(resolve, 1000));
        updateScore(1);
        await new Promise(resolve => setTimeout(resolve, 1000));
        updateScore(2);
        await new Promise(resolve => setTimeout(resolve, 1000));
        updateScore(3);
        // updateFinals();
        // startTimer();
    }
}

// Configuration des demi-finales avec les participants mélangés
function setupSemiFinals() {
    matches.value[0].team1 = participants.value[0].name;
    matches.value[0].team2 = participants.value[1].name;
    matches.value[1].team1 = participants.value[2].name;
    matches.value[1].team2 = participants.value[3].name;
}

function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

async function createFalsePlayer(user1, user2, user3 ,user4)
{
    try {
        const response = await fetch('/api/game/createFalsePlayer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                username1: user1,
                username2: user2,
                username3: user3,
                username4: user4,
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Game Data:', data);
        }
    }
    catch (error) {
        console.error('Erreur lors de la connexion:', error);
        alert(i18n.global.t('error_login'));
    }
}


// Fonction pour ajouter les participants
async function addParticipants() {
    const filteredParticipants = newParticipants.value.filter(name => name.trim() !== "");

    if (filteredParticipants.length === 4) {
        const participantsWithoutDuplicates = new Set(filteredParticipants);
        if (participantsWithoutDuplicates.size !== filteredParticipants.length) {
            alert(i18n.global.t('error_cannot_use_same_nickname'));
        } else {
            participants.value = filteredParticipants.map(name => ({ name }));
            await createFalsePlayer(filteredParticipants[0], filteredParticipants[1], filteredParticipants[2], filteredParticipants[3]);
            startTournament();
        }
    } else {
        alert(i18n.global.t('please_enter_4_valid_names'));
    }
}

// Mettre à jour les finales
function updateScore(match_index) {
    matches.value[match_index].score1 = 8;
    matches.value[match_index].score2 = 10;
    if (matches.value[match_index].score1 > matches.value[match_index].score2) {
        matches.value[match_index].winner = matches.value[match_index].team1;
        matches.value[match_index].loser = matches.value[match_index].team2;
    } else {
        matches.value[match_index].winner = matches.value[match_index].team2;
        matches.value[match_index].loser = matches.value[match_index].team1;
    }
    switch (match_index) {
        case 0:
            matches.value[2].team1 = matches.value[match_index].loser;
            matches.value[3].team1 = matches.value[match_index].winner;
            break;
        case 1:
            matches.value[2].team2 = matches.value[match_index].loser;
            matches.value[3].team2 = matches.value[match_index].winner;
            break;
        default:
            break;
    }
}

// Mettre à jour les finales
function updateFinals() {
    const semi1 = matches.value[0];
    const semi2 = matches.value[1];

    if (semi1.winner && semi2.winner) {
        matches.value[3].team1 = semi1.winner;
        matches.value[3].team2 = semi2.winner;
    }
}

// Fonction pour démarrer le timer
function startTimer() {
    if (!interval) {
        interval = setInterval(() => {
            timer.value--;
            if (timer.value === -1) {
                alert(i18n.global.t('GAME_STARTS_SOON'));
                stopTimer();
            }
        }, 1000);
    }
}

// Fonction pour arrêter le timer
function stopTimer() {
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
}

onUnmounted(() => {
    stopTimer();
});
</script>

<template>
    <main>
        <div id="wrapper">
            <div class="theme">
                <!-- Si le nombre de participants est différent de 4, affiche la configuration -->
                <div v-if="participants.length !== 4" class="custom-content">
                    <h2>{{ $t('add_participants') }}</h2>
                    <div v-for="(participant, index) in newParticipants" :key="index">
                        <Input v-model="newParticipants[index]" :placeholderText="`${$t('name_of_participant')} [${index}]`" />
                    </div>
                    <button class="button buttonText" @click="addParticipants">{{ $t('validate_participants') }}</button>
                </div>

                <!-- Si le nombre de participants est égal à 4, affiche le bracket et le timer -->
                <div v-if="participants.length === 4">
                    <CreateDropupButton />
                    <CreateBackButton />
                    <div class="bracket">
                        <!-- Demi-finales -->
                        <div class="column one">
                            <NeonText :position="{ top: 30, left: 27 }" :fontSize="1">{{ $t('semi_finals') }}</NeonText>
                            <div v-for="(match, index) in matches.slice(0, 2)" :key="index" class="match semi">
                                <div class="match-top team">
                                    <span class="name">{{ match.team1 }}</span>
                                    <span class="score">{{ match.score1 ?? '-' }}</span>
                                </div>
                                <div class="match-bottom team">
                                    <span class="name">{{ match.team2 }}</span>
                                    <span class="score">{{ match.score2 ?? '-' }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Finale -->
                        <div class="column final">
                            <div v-for="(match, index) in matches.slice(3, 4)" :key="index" class="match big-final">
                                <div v-if="match.team1 && match.team2">
                                    <NeonText :position="{ top: 30, left: 46 }" :fontSize="1">{{ $t('final') }}</NeonText>
                                    <div class="match-top team">
                                        <span class="name">{{ match.team1 }}</span>
                                        <span class="score">{{ match.score1 ?? '-' }}</span>
                                    </div>
                                    <div class="match-bottom team">
                                        <span class="name">{{ match.team2 }}</span>
                                        <span class="score">{{ match.score2 ?? '-' }}</span>
                                    </div>
                                </div>
                                <div v-else>
                                    <span class="finale-text">{{ $t('matches_not_yet_decided') }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Petite finale -->
                        <div class="column third-place">
                            <div v-for="(match, index) in matches.slice(2, 3)" :key="index" class="match small-final">
                                <div v-if="match.team1 && match.team2">
                                    <NeonText :position="{ top: 30, left: 68 }" :fontSize="1">{{ $t('small_final') }}</NeonText>
                                    <div class="match-top team">
                                        <span class="name">{{ match.team1 }}</span>
                                        <span class="score">{{ match.score1 ?? '-' }}</span>
                                    </div>
                                    <div class="match-bottom team">
                                        <span class="name">{{ match.team2 }}</span>
                                        <span class="score">{{ match.score2 ?? '-' }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Timer en bas à droite -->
                    <div v-if="participants.length === 4" class="button timer">
                        {{ Math.floor(timer / 60) }}:{{ ('0' + (timer % 60)).slice(-2) }}
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>


<style scoped>
.theme {
    height: 100%;
    width: 100%;
    position: absolute;
    background-color: rgba(0, 0, 0, 0.5);
}

.bracket {
    display: flex;
    flex-direction: row;
    padding: 20vw 0;
    margin-left: 20vw;
}

.column {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
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

.code-content {
    margin-top: 20px;
    background-color: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 10px;
}

.match {
    display: flex;
    flex-direction: column;
    margin: 2vw 4vw;
    position: relative;
}

.match.semi {
    width: 12vw;
    height: 6vh;
}

.match.big-final {
    width: 16vw;
    height: 8vh;
    position: relative;
    bottom: 4vh;
    left: -4vw;
}

.match.small-final {
    width: 14vw;
    height: 7vh;
    position: relative;
    bottom: 2vh;
    left: -4vw;
}

.team {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5vh;
    padding: 0.5vh 0.5vw;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    background-color: rgba(0, 0, 0, 0.25);
    color: rgb(255, 255, 255);
}

.team .score {
    color: rgba(255, 20, 147, 0.6);
}

.finale-text {
    color: white;
    font-size: 1rem;
    position: relative;
    bottom: -12vh;
    left: 15vw;
}

/* Styles pour le timer */
.timer {
    position: fixed;
    bottom: 20px;
    right: 20px;
    font-size: 2em;
    color: white;
    background-color: rgba(0, 0, 0, 0.5);
    border: 0.15vw solid rgba(255, 20, 147, 1);
    border-style: groove;
    padding: 10px;
    border-radius: 5px;
}
</style>
