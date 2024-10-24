<script setup>
import { ref } from 'vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import profilePicture from '@/assets/img/default-profile.png';
import { inject } from 'vue';

const varySpeed = inject('varySpeed');
varySpeed(0); 

// Importation de la classe PlayerStats
class PlayerStats {
    constructor() {
        this.wins = 0;
        this.looses = 0;
    }

    addWin() {
        this.wins++;
    }

    addLoss() {
        this.looses++;
    }

    getStats() {
        const totalGames = this.wins + this.looses;
        const winRate = totalGames ? (this.wins / totalGames) * 100 : 0;
        const looseRate = totalGames ? (this.looses / totalGames) * 100 : 0;
        return {
            wins: this.wins,
            looses: this.looses,
            winRate: winRate.toFixed(2),
            looseRate: looseRate.toFixed(2),
            rank: Math.floor(this.wins / 5) + 1,
        };
    }
}

const userAccount = ref({
    profilePicture: null, // ou insérez une URL d'image pour tester
    username: null,
    nickname: null,
});

const latestGames = ref([
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 1, host: "_johndoe", rival: "abrin", score: { host: 5, rival: 1 }, date: "12/12/1200" },
    { id: 1, host: "_johndoe", rival: "abrin", score: { host: 5, rival: 1 }, date: "12/12/1200" },
    { id: 1, host: "_johndoe", rival: "abrin", score: { host: 5, rival: 1 }, date: "12/12/1200" },
    { id: 1, host: "_johndoe", rival: "abrin", score: { host: 5, rival: 1 }, date: "12/12/1200" },
    { id: 1, host: "_johndoe", rival: "abrin", score: { host: 5, rival: 1 }, date: "12/12/1200" },
    { id: 1, host: "_johndoe", rival: "abrin", score: { host: 5, rival: 1 }, date: "12/12/1200" },
    { id: 1, host: "_johndoe", rival: "abrin", score: { host: 5, rival: 1 }, date: "12/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
    { id: 2, host: "_johndoe", rival: "abrin", score: { host: 2, rival: 5 }, date: "13/12/1200" },
]);

const playerStats = ref(new PlayerStats());

latestGames.value.forEach(game => {
    if (game.score.host > game.score.rival) {
        playerStats.value.addWin();
    } else {
        playerStats.value.addLoss();
    }
});

const playerWinLoss = ref(playerStats.value.getStats());
</script>

<template>
    <main>
        <div id="wrapper">
            <CreateBackButton />
            <CreateDropupButton />

            <h2 class="category-title">{{ $t('LEADERBOARD') }}</h2>
            <div class="leaderboardContainer">
                <div>
                    <button class="button">
                        <img :src="userAccount.profilePicture || profilePicture" class="profile-picture" />
                        <div class="divider">&nbsp;</div>
                        <div class="user-info">
                            <span class="username">{{ userAccount.username || "John Doe" }}</span>
                            <span class="nickname">{{ userAccount.nickname || "_johndoe" }}</span>
                        </div>
                    </button>
                </div>

                <!-- Section des statistiques stylisée -->
                <div class="stats-grid">
                    <div class="stat-row">
                        <div class="category-title stat-col">{{ $t('win_rate') }}</div>
                        <div class="category-title stat-col">{{ $t('rank') }}</div>
                        <div class="category-title stat-col">{{ $t('loose_rate') }}</div>
                    </div>
                    <div class="stat-row">
                        <div class="stat-col">{{ playerWinLoss.winRate }}%</div>
                        <div class="stat-col">{{ playerWinLoss.rank }} lvl</div>
                        <div class="stat-col">{{ playerWinLoss.looseRate }}%</div>
                    </div>
                    <div class="stat-row">
                        <div class="category-title stat-col">{{ $t('victories') }}</div>
                        <div class="category-title stat-col">{{ $t('defeats') }}</div>
                        <div class="category-title stat-col">{{ $t('games') }}</div>
                    </div>
                    <div class="stat-row">
                        <div class="stat-col">{{ playerWinLoss.wins }}</div>
                        <div class="stat-col">{{ playerWinLoss.looses }}</div>
                        <div class="stat-col">{{ latestGames.length }}</div>
                    </div>
                </div>

                <!-- Dernières parties -->
                <div class="latestGame">
                    <span class="category-title latestGameTitle">{{ $t('last_games') }}</span>
                    <div v-if="latestGames.length > 0">
                        <div v-for="game in latestGames" :key="game.id">
                            <button class="game-button">
                                <span class="game-match">{{ game.host }} VS {{ game.rival }}</span>
                                <div class="game-score">
                                    <span class="host-pos">{{ game.score.host }}</span>
                                    <div class="divider-score">&nbsp;</div>
                                    <span class="rival-pos">{{ game.score.rival }}</span>
                                </div>
                                <span class="game-date">{{ game.date }}</span>
                            </button>
                        </div>
                    </div>
                    <div class="game-button game-info" v-else>
                        <p>{{ $t('no_games_to_display') }}</p>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>
<style scoped>
h1,
.category-title {
    font-size: 3.5rem;
    color: #fff;
    position: fixed;
    z-index: 1;
    top: 10%;
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

.leaderboardContainer {
    position: fixed;
    height: 40vw;
    width: 140vh;
    top: 15%;
    border-radius: 0.5vw;
    padding: 1.5vw;
    background-color: rgba(0, 0, 0, 0.25);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    overflow-y: auto;
    overflow-x: hidden;
}

.profile-picture {
    width: 4vw;
    height: 4vw;
    object-fit: cover;
    border-radius: 50%;
    border: 0.2vw solid #fff;
    margin-right: 1vw;
}

.divider {
    width: 0.2vw;
    height: 3vw;
    background-color: #fff;
    margin-right: 1vw;
}

.user-info {
    display: flex;
    flex-direction: column;
    justify-content: left;
}

.button {
    background-color: rgba(0, 0, 0, 0.25);
    padding: 2vh 2vw;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: border-color 0.5s, width 0.3s ease;
    margin-top: 1vh;
    display: flex;
    align-items: center;
    position: relative;
    white-space: nowrap;
    min-width: 25%;
    width: auto;
    height: 10vh;
    font-size: 1.8vw;
    color: #fff;
}

.username,
.nickname {
    white-space: nowrap;
}

.username {
    font-size: 2vw;
    font-weight: bold;
    color: #fff;
    text-align: left;
    width: 100%;
    right: auto;
}

.nickname {
    font-size: 1.5vw;
    color: #bbb;
    text-align: left;
    width: 100%;
    right: auto;
}
</style>

<style scoped>
.latestGame {
    max-height: calc(5 * 8vh);
    overflow-y: auto;
    margin-top: 3vh;
}

.latestGameTitle {
    font-size: 2vw;
    color: #fff;
    margin-bottom: 1vh;
    left: 64%;
    top: 25%;
}

.game-button {
    display: flex;
    position: relative;
    width: 18vw;
    height: 6vh;
    left: 70%;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 0.5vh 2vw;
    border: 0.1vw solid rgba(255, 255, 255, 0.3);
    border-radius: 0.4vw;
    margin-top: 0.3vh;
    justify-content: space-between;
    align-items: center;
}

.game-match {
    position: absolute;
    top: 0.3vw;
    left: 0.5vw;
    font-weight: bold;
    color: #f4f4f4;
    white-space: nowrap;
}

.game-date {
    position: absolute;
    top: 1.6vw;
    left: 0.5vw;
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.8vw;
    white-space: nowrap;
}

.game-score {
    position: relative;
    left: 100%;
    font-weight: bold;
    font-size: 1.2vw;
    color: rgba(255, 20, 147, 0.6);
}

.host-pos {
    position: absolute;
    bottom: -0.2vw;
    right: -1.2vw;

}

.rival-pos {
    position: absolute;
    top: 0vw;
    right: -1.2vw;
}

.divider-score {
    position: absolute;
    height: 0.2vw;
    width: 1.6vw;
    background-color: #fff;
}
</style>


<style scoped>
.stats-grid {
    display: flex;
    flex-direction: column;
    margin-top: 20px;
    padding: 20px;
    border-radius: 10px;
    font-size: 1.5vw;
    color: #fff;
    text-align: center;
    position: absolute;
    width: 65%;
}

.stat-row {
    display: flex;
    justify-content: space-around;
    margin-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3); /* Ajoute une bordure en bas des lignes */
}

.stat-col {
    width: 30%;
    position: relative;
    padding: 10px 0;
    font-size: larger;
    white-space: nowrap;
}

.stat-row:first-child .stat-col {
    font-weight: bold;
    border-top: 1px solid rgba(255, 255, 255, 0.3); /* Ajoute une bordure en bas des lignes */

}

.stat-col:not(:first-child) {
    border-left: 1px solid rgba(255, 255, 255, 0.3); /* Ajoute une bordure à gauche sauf pour la première colonne */
}
</style>