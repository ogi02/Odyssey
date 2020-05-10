<script>
	// Javascript imports
	import { fetchPost } from '../js/fetch.js';

	// Inherited variables
	export let giveaways;
	export let user;

	// Generate random giveaway winner
	async function pickRandomGiveawayWinner(giveaway_id) {
		const response = await fetchPost('http://localhost:3000/generateRandomWinner', {
			giveaway_id: giveaway_id
		});

		let temp = response.winner_id;

		return temp;
	}

	// Select giveaway winner
	async function chooseGiveawayWinner(giveaway_id, winner_id) {
		const response = await fetchPost('http://localhost:3000/chooseGiveawayWinner', {
			winner_id: winner_id,
			giveaway_id: giveaway_id
		});

		giveaways.find(giveaway => giveaway._id.$oid === giveaway_id).winner = response.winner;
		giveaways = giveaways;
	}

	// Get participants in giveaway
	async function getParticipantCount(giveaway_id) {
		const response = await fetchPost('http://localhost:3000/getTotalContestantsCount', {
			giveaway_id: giveaway_id,
		});

		let temp = response.participant_count;
		return temp;
	}

	// Close giveaway
	async function closeGiveaway(giveaway_id) {
		const response = await fetchPost('http://localhost:3000/closeGiveaway', {
			giveaway_id: giveaway_id
		});

		giveaways.find(giveaway => giveaway._id.$oid === giveaway_id).is_open = false;
		giveaways = giveaways;
	}

</script>

<div class="giveaways-container">

	{#each giveaways as giveaway}
			
		<div class='giveaway-box'>

			<img class="giveaway-image" src={"/images/" + user.username + "/" + giveaway.image_path}>
			
			<div class="text-container">
				<h3>{giveaway.text}</h3>
			</div>
			
			{#if giveaway.is_open == true}

				<p>Number of contestants: </p>

				{#await getParticipantCount(giveaway._id.$oid) then participants}

					<p>{participants || 0}</p>

					{#if participants}

						<button on:click={async () => {
							await closeGiveaway(giveaway._id.$oid);
							let winner_id = await pickRandomGiveawayWinner(giveaway._id.$oid);
							await chooseGiveawayWinner(giveaway._id.$oid, winner_id);
						}}>Generate Winner</button>

					{/if}

				{/await}

			{:else}
				<p>{giveaway.winner}</p>
			{/if}

		</div>

	{/each}

</div>

<style>

	.giveaways-container{
		display: flex;
		margin: 4em;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}

	.giveaway-box {
		border: 2px solid #0f1930;
		min-width: 40em;
		max-width: 30em;
		min-height: 23em;
		margin: 10px;
	}

	.giveaway-image {
		width: 40.2em;
		margin-left: -2px;
		margin: -3px;
		height: 25em;
		margin-top: -4px;
	}

	.text-container{
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		margin: 1em;
		align-items: center;
		justify-content: space-between;
	}

</style>