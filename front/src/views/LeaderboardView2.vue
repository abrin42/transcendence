<!-- @lribette todo translate -->
<script setup>
import { ref, computed, defineEmits, onMounted } from 'vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';

// const latestGames = ref([ // Exemple de parties récentes
//     { id: 6, username: "Lionel Messi", points: 43 },
//     { id: 7, username: "Cristiano Ronaldo", points: 3700000 },
//     { id: 8, username: "Neymar", points: 25 },
//     { id: 9, username: "Kylian Mbappé", points: 48 },
//     { id: 10, username: "Kevin De Bruyne", points: 29 },
//     { id: 11, username: "Mohamed Salah", points: 36 },
//     { id: 12, username: "Virgil van Dijk", points: 18 },
//     { id: 13, username: "Robert Lewandowski", points: 32 },
//     { id: 14, username: "Sadio Mané", points: 27 },
//     { id: 15, username: "Harry Kane", points: 21 },
//     { id: 16, username: "Luka Modrić", points: 15 },
//     { id: 17, username: "Gareth Bale", points: 11 },
//     { id: 18, username: "Raheem Sterling", points: 34 },
//     { id: 19, username: "Sergio Ramos", points: 26 },
//     { id: 20, username: "Paul Pogba", points: 22 },
//     { id: 21, username: "N'Golo Kanté", points: 19 },
//     { id: 22, username: "Antoine Griezmann", points: 16 },
//     { id: 23, username: "Edinson Cavani", points: 203 },
//     { id: 24, username: "Karim Benzema", points: 389 },
//     { id: 25, username: "Gianluigi Buffon", points: 187 },
//     { id: 26, username: "Manuel Neuer", points: 265 },
//     { id: 27, username: "Kepa Arrizabalaga", points: 175 },
//     { id: 28, username: "Alisson Becker", points: 120 },
//     { id: 29, username: "Marc-André ter Stegen", points: 222 },
//     { id: 30, username: "Riyad Mahrez", points: 142 },
//     { id: 31, username: "Isco", points: 97 },
//     { id: 32, username: "Dani Carvajal", points: 75 },
//     { id: 33, username: "Gerard Piqué", points: 195 },
//     { id: 34, username: "Jordi Alba", points: 145 },
//     { id: 35, username: "Thiago Silva", points: 120 },
//     { id: 36, username: "Pepe", points: 30 },
//     { id: 37, username: "César Azpilicueta", points: 58 },
//     { id: 38, username: "Ben Chilwell", points: 76 },
//     { id: 39, username: "Reece James", points: 82 },
//     { id: 40, username: "Trent Alexander-Arnold", points: 250 },
//     { id: 41, username: "Andrew Robertson", points: 191 },
//     { id: 42, username: "Bruno Fernandes", points: 214 },
//     { id: 43, username: "Marcus Rashford", points: 180 },
//     { id: 44, username: "Jadon Sancho", points: 100 },
//     { id: 45, username: "Phil Foden", points: 88 },
//     { id: 46, username: "Jack Grealish", points: 200 },
//     { id: 47, username: "Frenkie de Jong", points: 185 },
//     { id: 48, username: "Mason Mount", points: 172 },
//     { id: 49, username: "Declan Rice", points: 150 },
//     { id: 50, username: "Youri Tielemans", points: 145 },
//     { id: 51, username: "Nico Williams", points: 120 },
//     { id: 52, username: "Christian Pulisic", points: 110 },
//     { id: 53, username: "Gio Reyna", points: 98 },
//     { id: 54, username: "Claudio Marchisio", points: 50 },
//     { id: 55, username: "Zlatan Ibrahimović", points: 230 },
//     { id: 56, username: "Álvaro Morata", points: 112 },
//     { id: 57, username: "Gerard Moreno", points: 90 },
//     { id: 58, username: "David Silva", points: 165 },
//     { id: 59, username: "Cesc Fàbregas", points: 99 },
//     { id: 60, username: "Xavi Hernández", points: 88 },
//     { id: 61, username: "Andrés Iniesta", points: 70 },
//     { id: 62, username: "Ivan Rakitić", points: 85 },
//     { id: 63, username: "Mauro Icardi", points: 77 },
//     { id: 64, username: "Lautaro Martínez", points: 155 },
//     { id: 65, username: "Marco Verratti", points: 120 },
//     { id: 66, username: "Saúl Ñíguez", points: 130 },
//     { id: 67, username: "Thomas Müller", points: 210 },
//     { id: 68, username: "Gareth Bale", points: 135 },
//     { id: 69, username: "David De Gea", points: 190 },
//     { id: 70, username: "Hugo Lloris", points: 160 },
//     { id: 71, username: "Petr Čech", points: 150 },
//     { id: 72, username: "Carlos Tévez", points: 90 },
//     { id: 73, username: "Ronaldinho", points: 480 },
//     { id: 74, username: "Rivaldo", points: 470 },
//     { id: 75, username: "Ronald Koeman", points: 130 },
//     { id: 76, username: "Sergio Busquets", points: 105 },
//     { id: 77, username: "Coutinho", points: 85 },
//     { id: 78, username: "Mário Götze", points: 78 },
//     { id: 79, username: "Mario Mandzukic", points: 70 },
//     { id: 80, username: "Dani Alves", points: 110 },
//     { id: 81, username: "Thierry Henry", points: 495 },
//     { id: 82, username: "George Best", points: 450 },
//     { id: 83, username: "Zinedine Zidane", points: 475 },
//     { id: 84, username: "Diego Maradona", points: 460 },
//     { id: 85, username: "Pelé", points: 500 },
//     { id: 86, username: "Bobby Moore", points: 365 },
//     { id: 87, username: "Garrincha", points: 450 },
//     { id: 88, username: "Ronnie O'Sullivan", points: 285 },
//     { id: 89, username: "Rinus Michels", points: 250 },
//     { id: 90, username: "Franz Beckenbauer", points: 415 },
//     { id: 91, username: "Alfredo Di Stéfano", points: 360 },
//     { id: 92, username: "Marco van Basten", points: 300 },
//     { id: 93, username: "Dino Zoff", points: 375 },
//     { id: 94, username: "Kenny Dalglish", points: 280 },
//     { id: 95, username: "Lothar Matthäus", points: 295 },
//     { id: 96, username: "Cafu", points: 295 },
//     { id: 97, username: "Roberto Carlos", points: 320 },
//     { id: 98, username: "Michael Owen", points: 290 },
//     { id: 99, username: "Wayne Rooney", points: 325 },
//     { id: 100, username: "Samuel Eto'o", points: 370 },
//     { id: 101, username: "Robbie Keane", points: 250 },
// ]);

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
                allPlayers.value.push(obj);
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
