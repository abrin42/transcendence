<template>
    <div class="friends-popup">
        <div class="friends-header">
            <h3>My Friends</h3>
            <button class="close-button" @click="closePopup" aria-label="Close friends list">
                <i class="fas fa-times"></i>
            </button>
        </div>

        <!-- Barre de recherche -->
        <div class="search-bar">
            <Input type="text" v-model="searchQuery" placeholderText="Rechercher joueur..." />
        </div>

        <!-- Liste des résultats de recherche (non amis) -->
        <div class="search-results" v-if="searchQuery.length > 0 && filteredPlayers.length > 0">
            <div v-for="player in filteredPlayers" :key="player.id" class="friend-item">
                <span class="friend-name">{{ player.name }}</span>
                <div class="friend-actions">
                    <button @click="invitePlayer(player.id)" aria-label="Invite player">
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
                    <span class="friend-name">{{ friend.name }}</span>
                </div>
                <div class="friend-actions">
                    <button @click="inviteFriendToPlay(friend.id)" aria-label="Invite friend to play">
                        <i class="fas fa-gamepad icon-items"></i>
                    </button>
                    <button @click="deleteFriend(friend.id)" aria-label="Delete friend">
                        <i class="fas fa-trash-alt icon-items"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Message si aucune recherche ne donne de résultats -->
        <div v-if="searchQuery.length > 0 && filteredPlayers.length === 0" class="no-results">
            <p>Aucun joueur trouvé.</p>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { defineEmits } from 'vue';
import Input from './Input.vue';
import { onMounted } from 'vue';

async function getAllUsers() {
		try {
			const response = await fetch(`https://localhost:8443/api/player/get_all_user`, {
				method: 'GET',
			});

			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}
			const users = await response.json();
			console.log("all users: ", users);
		} catch (error) {
			console.error('Error retrieving user data:', error);
		}
}



const emit = defineEmits(['close']);

// Liste des amis actuels avec un booléen isOnline
const friends = ref([
    { id: 1, name: 'Hugp', isOnline: true },
    { id: 2, name: 'Jason', isOnline: false },
    { id: 3, name: 'Rayan', isOnline: true },
    { id: 4, name: 'Vladimir', isOnline: false },
    { id: 5, name: 'Stephanie', isOnline: true },
    { id: 6, name: 'Pavard', isOnline: false },
    { id: 7, name: 'Ibraima', isOnline: true },
]);

// Liste des joueurs non amis
const allPlayers = ref([
    { id: 6, name: 'Lucie' },
    { id: 7, name: 'Caroline' },
    { id: 8, name: 'Lucas' },
    { id: 9, name: 'Isaac' },
    { id: 10, name: 'Tabata' },
]);

// Barre de recherche
const searchQuery = ref('');

// Fonction pour fermer le popup
function closePopup() {
    emit('close');
}

// Fonction pour inviter un joueur
function invitePlayer(playerId) {
    console.log('Inviting player with ID:', playerId);
    // TODO: Code pour inviter le joueur non ami
}

// Fonction pour supprimer un ami
function deleteFriend(friendId) {
    console.log('Deleting friend with ID:', friendId);
    // TODO: Code pour supprimer l'ami
}

// Fonction pour inviter un ami à jouer
function inviteFriendToPlay(friendId) {
    console.log('Inviting friend with ID:', friendId, 'to play');
    alert(`Invitation envoyée à ${friends.value.find(friend => friend.id === friendId).name} pour jouer.`);
}

// Liste des joueurs non amis filtrée en fonction de la recherche
const filteredPlayers = computed(() => {
    if (searchQuery.value.trim() === '') {
        return [];
    }
    return allPlayers.value.filter((player) =>
        player.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

onMounted(async () => {
		await getAllUsers();
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

.icon-items:hover {
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
</style>
