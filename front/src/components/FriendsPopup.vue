<template>
    <div>
        <!-- Popup des amis -->
        <div v-if="friendsPopupVisible" class="friends-popup">
            <div class="friends-header">
                <h3>{{ $t('my_friends') }}</h3>
                <button class="close-button" @click="closePopup" aria-label="Close friends list">
                    <i class="fas fa-times"></i>
                </button>
            </div>

            <!-- Barre de recherche -->
            <div class="search-bar">
                <Input type="text" v-model="searchQuery" :placeholderText="$t('search_for_a_player')" />
            </div>

            <!-- Liste des résultats de recherche (non amis) -->
            <div class="search-results" v-if="searchQuery.length > 0 && filteredPlayers.length > 0">
                <div v-for="player in filteredPlayers" :key="player.id" class="friend-item">
                    <span class="friend-name" @click="goProfile(player.username)">{{ player.username }}</span>
                    <div class="friend-actions">
                        <button @click="invitePlayer(player.username)" aria-label="Invite player">
                            <i class="fas fa-user-plus icon-items"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Liste des amis actuels -->
            <div v-if="searchQuery.length === 0" class="friends-list">
                <div v-for="friend in friends" :key="friend.id" class="friend-item">
                    <div class="friend-info">
                        <i :class="['fa-solid', 'fa-globe', 'icon-items', friend.isOnline ? 'online' : 'offline']"></i>
                        <span class="friend-name" @click="__goTo('/leaderboard')">{{ friend.username }}</span>
                    </div>
                    <div class="friend-actions">
                        <button @click="inviteFriendToPlay(friend.id)" aria-label="Invite friend to play">
                            <i class="fas fa-gamepad icon-items"></i>
                        </button>
                        <button @click="deleteFriend(friend.username)" aria-label="Delete friend">
                            <i class="fas fa-trash-alt icon-items"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Message si aucune recherche ne donne de résultats -->
            <div v-if="searchQuery.length > 0 && filteredPlayers.length === 0" class="no-results">
                <p>{{ $t('no_players_found') }}</p>
            </div>

            <!-- Icone de demandes d'amis avec pastille -->
            <div class="friend-request-icon" @click="toggleFriendRequests">
                <i class="fas fa-user-friends"></i>
                <span class="notification-badge" v-if="friendRequests.length > 0">{{ friendRequests.length }}</span>
            </div>
        </div>

        <div class="friends-notification">
            <!-- Popup des demandes d'amis -->
            <div v-if="friendRequestsVisible" class="friend-requests-popup">
                <div class="friends-header">

                    <h3>{{ $t('friend_requests') }}</h3>
                    <button class="close-request-friend" @click="closePopupFriendRequest"
                        aria-label="Close friends list">
                        <i class="fas fa-times"></i>
                    </button>
                </div>

                <div v-if="friendRequests.length > 0" class="friend-requests-list">
                    <div v-for="request in friendRequests" :key="request.id" class="friend-request-item">
                        <span>{{ request.username }}</span>
                        <div class="request-actions">
                            <button @click="acceptRequest(request.username)" class="icon-items">
                                <i class="fas fa-check"></i>
                            </button>
                            <button @click="declineRequest(request.id)" class="icon-items">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <p>{{ $t('no_friend_requests') }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, defineEmits, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Input from './Input.vue';
import i18n from '../i18n.js';

////////////////////////////////////////////////
/////// GET USER ///////////////////////////////
////////////////////////////////////////////////

import { useUser } from '../useUser.js';
const { getUser, userAccount } = useUser();

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

function __goTo(page) {
    if (page == null)
        return;
    router.push(page);
}

const friends = ref([]);
const allPlayers = ref([]);
const friendRequests = ref([]);

const router = useRouter();


async function getFriendsRequest() {
    try {
        const response = await fetch(`/api/friend/pending/`, {
            method: 'GET',
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const users = await response.json();
        console.log(users);
         let users_data = JSON.parse(users)
         console.log("all friends: ", users_data);
         for (let i = 0; i < users_data.length; i++) {
             var obj = {}
             if (users_data[i].fields.friend[0] == userAccount.username) {
                 obj['username'] = users_data[i].fields.user[0];
             } else {
                 obj['username'] = users_data[i].fields.friend[0];
             }
             friendRequests.value.push(obj);
         }
    } catch (error) {
        console.error('Error retrieving user data /getFriendsRequest:', error);
    }
}


// Accepter une demande d'ami
async function acceptRequest(playerUsername) {
    try {
        console.log('Inviting player with ID:', playerUsername);
        const response = await fetch('/api/friend/help/', {
            method: 'POST', // Change to POST to match the Django view
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                username: playerUsername,
            })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        friendRequests.value = friendRequests.value.filter(request => request.username !== playerUsername);
        getFriends();
    } catch (error) {
        console.error('Error while adding friends:', error);
        alert(i18n.global.t('error_adding_a_friend'));
    }
}

async function invitePlayer(playerUsername) {
    try {
        console.log('Inviting player with ID:', playerUsername);
        const response = await fetch('/api/friend/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                username: playerUsername,
            })
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    } catch (error) {
        if (error == "Error: HTTP error! Status: 400") {
            alert(i18n.global.t('error_already_sent_invitation'));
        } else {
            alert(i18n.global.t('error_adding_a_friend'));
        }
    }
    allPlayers.value = allPlayers.value.filter(request => request.username !== playerUsername);
}

// Refuser une demande d'ami
function declineRequest(id) {
    friendRequests.value = friendRequests.value.filter(request => request.id !== id);
    console.log('Demande d\'ami refusée pour ID:', id);
}

//const allPlayers = ref([]);

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
                var obj = {}
                obj['username'] = element.fields.username;
                obj['nickname'] = element.fields.nickname;
                obj['last_login'] =  element.fields.last_login;

                obj['rank'] = element.fields.rank;
                obj['win'] = element.fields.win;
                obj['lose'] = element.fields.lose;
                if (obj['username'][0] != '#'){allPlayers.value.push(obj);}
            });
            console.log("all user", allPlayers._rawValue)
    } catch (error) {
        console.error('Error retrieving user data /getAllUsers:', error);
    }
}

async function getFriends() {
    try {
        const response = await fetch(`/api/friend/list/`, {
            method: 'GET',
        });

        if (!response.ok) {
            return;
        }
        const users = await response.json();
        let users_data = JSON.parse(users)
        console.log("all friends: ", users_data);
        for (let i = 0; i < users_data.length; i++) {
            var obj = {}
            if (users_data[i].fields.friend[0] == userAccount.username) {
                obj['username'] = users_data[i].fields.user[0];
            } else {
                obj['username'] = users_data[i].fields.friend[0];
            }
            const result = allPlayers._rawValue.find(({ username }) => username === obj['username']);
            var last_log = new Date(result.last_login).getTime();
            var now = new Date().getTime()
            if ((now - 600000) < last_log) {
                obj['isOnline'] = true;
            } else {
                obj['isOnline'] = false;
            }
            obj['username'] = result.nickname;
            friends.value.push(obj);
        }
    } catch (error) {
        console.error('Error retrieving user data /getFriends:', error);
    }
}

const emit = defineEmits(['close']);

const searchQuery = ref('');

function closePopup() {
    emit('close');
}


async function deleteFriend(playerUsername) {
    try {
        console.log('delete player with :', playerUsername);
        const response = await fetch('/api/friend/delete/', {
            method: 'POST', // Change to POST to match the Django view
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                username: playerUsername,
            })
        });
        if (!response.ok) {
            return;
        }
        friends.value = friends.value.filter(request => request.username !== playerUsername);
    } catch (error) {
        console.error('Error while adding friends:', error);
        alert(i18n.global.t('error_adding_a_friend'));
    }
}

function inviteFriendToPlay(friendId) {
    console.log('Inviting friend with ID:', friendId, 'to play');
    alert(`${i18n.global.t('invitation_sent_to')} ${friends.value.find(friend => friend.id === friendId).name} ${i18n.global.t('to_play')}`);
}

const filteredPlayers = computed(() => {
    if (searchQuery.value.trim() === '') {
        return [];
    }
    return allPlayers.value.filter((player) =>
        player.username.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

const friendsPopupVisible = ref(true);

const friendRequestsVisible = ref(false);

function toggleFriendRequests() {
    friendRequestsVisible.value = !friendRequestsVisible.value;
    if (friendRequestsVisible.value) {
        friendsPopupVisible.value = false;
    }
}

function closePopupFriendRequest() {
    friendRequestsVisible.value = false;
    friendsPopupVisible.value = true;
}

function goProfile(_username) {
    console.log(_username);
    __goTo(`/leaderboard/${_username}`);
}

onMounted(async () => {
    await getUser();
    await getAllUsers();
    await getFriends();
    await getFriendsRequest();
});

</script>

<style scoped>
.friends-popup {
    position: fixed;
    bottom: 15%;
    right: 1%;
    width: 20vw;
    height: 50vh;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
    padding: 15px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
}

.friends-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.friends-list,
.search-results {
    flex: 1;
    margin-top: 10px;
    overflow-y: auto;
    padding-right: 10px;
}

.search-bar {
    margin-top: 10px;
}

.search-input {
    width: 100%;
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
    font-size: 14px;
}

.friend-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid white;
}

.friend-info {
    display: flex;
    align-items: center;
}

.friend-name {
    margin-left: 10px;
}

.friend-name:hover {
    cursor: pointer;
    opacity: 0.6;
    transition: cubic-bezier(0.165, 0.84, 0.44, 1);
}

.friend-actions {
    display: flex;
    gap: 10px;
}

.friend-connect {
    display: flex;
    gap: 1px;
}

.icon-items {
    cursor: pointer;
    font-size: 16px;
    color: white;
}

.icon-items.online {
    color: rgb(66, 138, 66);
}

.icon-items.offline {
    color: rgb(174, 70, 70);
}

.icon-items:hover,
.friend-request-icon:hover {
    color: rgba(255, 255, 255, 0.5);
}

button {
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 16px;
    color: white;
    cursor: pointer;
}

.close-button:hover {
    color: rgb(164, 9, 9);
}

.friends-list::-webkit-scrollbar,
.search-results::-webkit-scrollbar {
    width: 0.6vw;
}

.friends-list::-webkit-scrollbar-track,
.search-results::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 1vw;
}

.friends-list::-webkit-scrollbar-thumb,
.search-results::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.25);
    border-radius: 1vw;
}

.no-results {
    color: white;
    text-align: center;
    margin-top: 20px;
}

/* Styles pour les demandes d'amis */
.friends-notification {
    position: relative;
    margin-top: 10px;
}

.friend-request-icon {
    position: fixed;
    bottom: 52%;
    right: 2%;
    font-size: 1.5rem;
    cursor: pointer;
}

.notification-badge {
    position: absolute;
    top: -0.5rem;
    right: -0.5rem;
    background-color: rgb(174, 70, 70);
    color: white;
    border-radius: 50%;
    padding: 0.1rem 0.4rem;
    font-size: 0.6rem;
    font-weight: bold;
}

.notification-badge:hover {
    background-color: rgb(236, 15, 15);
}

.friend-requests-popup {
    position: fixed;
    bottom: 15%;
    right: 1%;
    width: 20vw;
    height: 50vh;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    border: 0.15vw solid rgba(0, 0, 0, 0.25);
    border-radius: 0.4vw;
    transition: background-color 0.3s ease;
    padding: 15px;
    z-index: 1200;
    display: flex;
    flex-direction: column;
}

.friend-requests-list {
    max-height: 200px;
    overflow-y: auto;
}

.friend-request-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
}

.close-request-friend {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 16px;
    color: white;
    cursor: pointer;
}

.close-request-friend:hover {
    color: rgb(164, 9, 9);
}

.request-actions {
    display: flex;
    gap: 10px;
}
</style>
