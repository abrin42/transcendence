<template>
	<div>
		<button @click="getPlayers">Load Players</button>
		<h3 v-if="errorMsg">{{  errorMsg }}</h3>
		<h1>{{ players.id }} {{ players.username }} {{ players.language }}</h1>
	</div>
</template>

<script>
import axios from 'axios'

function logPlayerInfo(players) {
	console.log(`${players.language}`)
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
			getPlayers() {
				axios.get('http://localhost:8080/api/test-api/1?format=json')
					.then((response) => {
						console.log(response.data)
						this.players = response.data
						logPlayerInfo(this.players)
					})
					.catch((error) => {
						console.log(error)
						this.errorMsg = 'Error retrieving data'
					})
			}
		}
	}
// console.log(players.username);
</script>

<style scoped>

</style>