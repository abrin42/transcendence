<script setup>
import { ref, computed, defineEmits, onMounted } from 'vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';

const allPlayers = ref([]);
// Trier les parties par ordre décroissant de points
allPlayers.value.sort((a, b) => b.rank - a.rank);

const formatPoints = (points) => {
    return points.toLocaleString('fr-FR');
};

async function getAllUsers() {
    try {
        const response = await fetch(`/api/player/get_all_user/`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const users = await response.json();
        if (users) {
            const userData = JSON.parse(users);
            userData.forEach((element) => {
                var obj = {}
                obj['id'] = element.pk;
                obj['username'] = element.fields.username;
                obj['rank'] = element.fields.rank;
                obj['win'] = element.fields.win;
                obj['lose'] = element.fields.lose;
                if (obj['username'][0] != '#'){allPlayers.value.push(obj);}
            });
        }
    } catch (error) {
        console.error('Error retrieving user data /Leaderboard:', error);
    }
}

function lengthOfAllPlayers() {
    return allPlayers.value.length;
}

onMounted(async () => {
    // await getUser();
    await getAllUsers();
});
</script>

<template>
    <main>
        <div id="wrapper">
            <CreateBackButton />
            <CreateDropupButton />
            <h2 class="category-title">{{ $t('LEADERBOARD') }}</h2>
            <div class="leaderboardContainer">
                <div class="latestGame">
                    <div v-if="lengthOfAllPlayers() > 0">
                        <div v-for="(game, index) in allPlayers" :key="game.id">
                            <button :class="['game-button',
                                index === 0 ? 'first-place' : '',
                                index === 1 ? 'second-place' : '',
                                index === 2 ? 'third-place' : '']">
                                <div class="ranking-left">{{ index + 1 }}.</div>
                                <span class="game-match"> {{ game.username }}
                                    <i v-if="index < 3" class="fa-solid fa-trophy trophy-icon"></i>
                                </span>
                                <!-- Utilisez la méthode formatPoints ici -->
                                <div class="points-right">{{ formatPoints(game.rank) }} {{ $t('RANK') }}</div>
                            </button>
                        </div>
                    </div>
                    <div class="game-info" v-else>
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

.leaderboardContainer {
    position: fixed;
    height: 40vw;
    width: 120vh;
    top: 15%;
    border-radius: 0.5vw;
    padding: 1.5vw;
    background-color: rgba(0, 0, 0, 0.25);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    overflow-y: auto;
    overflow-x: hidden;
}

.latestGame {
    max-height: calc(5 * 13vh);
    overflow-y: auto;
    margin-top: 3vh;
}

.game-button {
    display: flex;
    position: relative;
    width: 100%;
    height: 6vh;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 0.5vh 2vw;
    border: 0.1vw solid rgba(255, 255, 255, 0.3);
    border-radius: 0.4vw;
    margin-top: 0.5vh;
    justify-content: space-between;
    align-items: center;
    transition: background-color 0.3s ease;
}

.first-place {
    background-color: rgba(255, 215, 0, 0.7);
    color: #000;
}

.second-place {
    background-color: rgba(192, 192, 192, 0.7);
    color: #000;
}

.third-place {
    background-color: rgba(205, 127, 50, 0.7);
    color: #000;
}

.ranking-left {
    position: absolute;
    left: 1vw;
    font-size: 1.2vw;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.6);
}

.points-right {
    position: absolute;
    right: 1vw;
    font-size: 1.2vw;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.6);
}

.trophy-icon {
    color: #FFD700;
    margin-left: 0.5vw;
}

.game-match {
    font-weight: bold;
    color: #f4f4f4;
    margin-left: 1vw;
    display: flex;
    align-items: left;
    justify-content: left;
    flex-grow: 1;
    text-align: center;
}

.game-info {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: #fff;
}
</style>
