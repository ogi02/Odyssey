<script>
	// Library imports
	import { onMount } from "svelte";

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';

	// Inherited variables
	export let giveaways;
	export let user;

	// Local variables
	let loadedGiveaways = 0;
	let allGiveawaysLoaded = false;

	onMount(async () => {
		if(user.role == "creator") {
			// sort giveaways by date
			giveaways.sort((a, b) => (a.date > b.date) ? -1 : 1);

			// load more giveaways
			await loadMoreGiveaways();
		}
	});

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

	// Load more giveaways
	async function loadMoreGiveaways() {
		for(let i = loadedGiveaways; i < loadedGiveaways + 10; i++) {
			// Check if there are any more giveaways to load
			if(giveaways.length == (loadedGiveaways + i)) {
				allGiveawaysLoaded = true;
				loadedGiveaways += i;
				return;
			}
		}

		loadedGiveaways += 10;

		// Remove button after last giveaway is loaded
		if(giveaways.length == loadedGiveaways) {
			allGiveawaysLoaded = true;
			return;
		}
	}

</script>

<div class="giveaways-container">

	{#each giveaways as giveaway, i}

		{#if i < loadedGiveaways}

			<div class='giveaway-box'>

				<img class="giveaway-image" src={"/images/" + user.username + "/" + giveaway.image_path}>
				
				<div class="text-container">
					<h3>{giveaway.text}</h3>
				</div>
				
				{#if giveaway.is_open}

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

		{/if}

	{/each}

	{#if !allGiveawaysLoaded}
		<button on:click={async () => await loadMoreGiveaways()}>Load More Giveaways</button>
	{/if}

</div>

<style>

	.giveaways-container {
		margin: 4em;
		display: flex;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}

	.giveaway-box {
		width: 40em;
		margin: 10px;
		min-height: 23em;
		border: 2px solid #0f1930;
	}

	.giveaway-image {
		height: 25em;
		width: 40.2em;
		margin: -4px -2px;
	}

	.text-container {
		margin: 1em;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
	}

	button {
		width: 12em;
		color: white;
		border: none;
		cursor: pointer;
		font-size: 18px;
		margin-top: 1em;
		border-radius: 50px;
		background-color: #0f1930;
	}

</style>
