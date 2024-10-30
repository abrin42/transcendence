<script setup>
import { ref, onMounted } from 'vue';
import CreateDropupButton from '../components/CreateDropupButton.vue';
import CreateBackButton from '../components/CreateBackButton.vue';
import profilePicture from '@/assets/img/default-profile.png';
import { inject } from 'vue';

import { useUser } from '../useUser.js';
const { getUser } = useUser();

const varySpeed = inject('varySpeed');
//varySpeed(0); 

const currentUrl = window.location.href;
const lastSegment = currentUrl.split('/').filter(Boolean).pop();
console.log("user ", lastSegment);

const user = ref([]);
var obj = {};
obj['username'] = "";
obj['nickname'] = "";
obj['last_login'] =  "";
obj['rank'] = "";
obj['win'] = 5;
obj['lose'] = 9;
obj['profilePicture'] = "";
obj['winRate'] = 0;
obj['loseRate'] = 0;
user.value.push(obj);
const games = ref([]);

onMounted(async () => {
    await getUser();
    await getAllUsers();
    await getAllGames();
});

async function getAllGames() {
    try {
        const response = await fetch(`/api/game/get_all_games/`, {
            method: 'GET',
        });
        if (!response.ok) {
            return;
        }
        const users = await response.json();
            const userData = JSON.parse(users);
            console.log("games =", userData);
            userData.forEach((element) => {
                if (element.fields.state == "end"){
                    var obj = {}
                    obj['host'] = element.fields.player1;
                    obj['rival'] = element.fields.player2;
                    if (obj.rival == lastSegment || obj.host == lastSegment ){
                        obj['score_host'] = element.fields.scorep1;
                        obj['score_rival'] = element.fields.scorep2;
                        obj['date'] = element.fields.created_at;
                        games.value.push(obj);
                    }
                }
            });
    } catch (error) {
        console.error('Error retrieving user data /getAllUsers:', error);
    }
}



async function getAllUsers() {
    try {
        const response = await fetch(`/api/player/get_all_user/`, {
            method: 'GET',
        });
        if (!response.ok) {
            return;
        }
        const users = await response.json();
        const userData = JSON.parse(users);
        userData.forEach((element) => {
            if (element.fields.username == lastSegment){
                user._rawValue[0].username = element.fields.username;
                user._rawValue[0].nickname = element.fields.nickname;
                user._rawValue[0].last_login =  element.fields.last_login;
                            
                user._rawValue[0].rank = element.fields.rank;
                user._rawValue[0].win = element.fields.win;
                user._rawValue[0].lose = element.fields.lose;
                user._rawValue[0].profilePicture = element.fields.profile_picture;
                            
                user._rawValue[0].winRate = 0;
                user._rawValue[0].loseRate = 0;
                            
                if ((element.fields.win+element.fields.lose) != 0){
                    user._rawValue[0].winRate = (element.fields.win / (element.fields.win+element.fields.lose) * 100).toFixed(2);
                }
                if (user._rawValue[0].winRate != 0){
                    user._rawValue[0].loseRate = 100 - user._rawValue[0].winRate
                }
            }
        });
        console.log("user is god", user._rawValue[0]);
    } catch (error) {
        console.error('Error retrieving user data /getAllUsers:', error);
    }
}

</script>

<template>
    <main>
        <div id="wrapper">
            <CreateDropupButton />
            <CreateBackButton />
            <h2 class="category-title">{{ $t('LEADERBOARD') }}</h2>
            <div class="leaderboardContainer">
                <div>
                    <button class="button">
                        <img :src="user[0].profilePicture || profilePicture" class="profile-picture" />
                        <div class="divider">&nbsp;</div>
                        <div class="user-info">
                            <span class="username">{{ user[0].username || "John Doe" }}</span>
                            <span class="nickname">{{ user[0].nickname || "_johndoe" }}</span>
                        </div>
                    </button>
                </div>

                <div class="stats-grid">
                    <div class="stat-row">
                        <div class="category-title stat-col">{{ $t('rank') }}</div>
                        <div class="category-title stat-col">{{ $t('victories') }}</div>
                        <div class="category-title stat-col">{{ $t('defeats') }}</div>
                        <div class="category-title stat-col">{{ $t('games') }}</div>
                    </div>
                    <div class="stat-row">
                        <div class="stat-col">{{ user[0].rank }}</div>
                        <div class="stat-col">{{ user[0].win }}</div>
                        <div class="stat-col">{{ user[0].lose }}</div>
                        <div class="stat-col">{{ user[0].win + user[0].lose }}</div>
                    </div>
                </div>

                <!-- Dernières parties -->
                <div class="latestGame">
                    <span class="category-title latestGameTitle">{{ $t('last_games') }}</span>
                    <div v-if="user[0].win + user[0].lose > 0">
                        <div v-for="game in games" :key="game.id">
                            <button class="game-button">
                                <span class="game-match">{{ game.host[0] }} VS {{ game.rival[0] }}</span>
                                <div class="game-score">
                                    <span class="host-pos">{{ game.score_host }}</span>
                                    <div class="divider-score">&nbsp;</div>
                                    <span class="rival-pos">{{ game.score_rival }}</span>
                                </div>
                                <span class="game-date">{{ game.date }}</span>
                            </button>
                        </div>
                    </div>
                    <div class="game-button game-info" v-else>
                        <p>{{ $t('no_games_to_display') }}</p>
                    </div>

                    <h2 class="stat-rate">
                        Statistics
                    </h2>
                    <!-- TO DO MEHDI -->
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
}

h2 {
    font-size: 3.5rem;
    color: #fff;
    z-index: 1;
    text-shadow: 0 0 5px rgba(255, 255, 255, .8), 0 0 10px rgba(255, 255, 255, .6), 0 0 20px rgba(255, 20, 147, .6), 0 0 30px rgba(255, 20, 147, .6), 0 0 40px rgba(255, 20, 147, .6), 0 0 50px rgba(255, 20, 147, .6), 0 0 60px rgba(255, 20, 147, .6);
}

.leaderboardContainer {
    position: fixed;
    height: 40vw;
    width: 88%;
    top: 15%;
    border-radius: 0.5vw;
    padding: 1.5vw;
    background-color: rgba(0, 0, 0, 0.25);
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    overflow-y: auto;
    overflow-x: hidden;
}

.pie-chart-pos {
    position: fixed;
    bottom: 23%;
    left: 42%;
}

.overloadBtn {
    position: fixed;
    width: 3vw;
    height: 6vh;
    bottom: 93vh;
    right: 95vw;
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

.stat-rate {
    position: fixed;
    bottom: 27%;
    left: 20%;
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
    border-bottom: 1px solid rgba(255, 255, 255, 0.3);
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
    border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.stat-col:not(:first-child) {
    border-left: 1px solid rgba(255, 255, 255, 0.3);
}
</style>