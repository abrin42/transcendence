<template>
	<div>
		<!-- <button @click="getPlayers">Load Players</button> -->
		<!-- <h3 v-if="errorMsg">{{  errorMsg }}</h3> -->
		<!-- <h1>{{ players.id }} {{ players.username }} {{ players.language }}</h1> -->
	</div>
</template>

<script>
import axios from 'axios'

function logPlayerInfo(players) {
	console.log(`${players.language}`)
}
	
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
	console.log(parts);

    if (parts.length === 2) return parts.pop().split(';').shift();
}

	export default {
		name: 'PlayerList',
		data() {
			return {
				players: [],
				errorMsg: ''
			}
		},
		methods:{
			async getPlayers() {
				const token = getCookie('jwt');
				console.log(token);

				if (!token) 
				{
					this.errorMsg = 'Token not found';
					return;
            	}
				
				const decodedToken = jwtDecode(token);
				console.log(decodedToken);
				// const userId = decodedToken.user_id;

				const response = await axios.get(`http://localhost:8080/api/test-api/${userId}`, 
				{
        			headers: {
          				'Authorization': `Bearer ${token}`,
        			},
					withCredentials: true
      			})		
				.then((response) => 
				{
					console.log(response.data)
					this.players = response.data
					logPlayerInfo(this.players)
				})
				.catch((error) => 
				{
					console.log(error)
					this.errorMsg = 'Error retrieving data'
				})
			}
		},
		mounted() {
    		this.getPlayers();
  		}
	}
	
// console.log(players.username);
</script>

<style scoped>

</style>