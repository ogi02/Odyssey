<script>
	// Library imports
	import { onMount } from "svelte";

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';

	// Inherited variables
	export let user;
	export let giveaways;

	// Local variables
	let loadedGiveaways = 0;
	let allGiveawaysLoaded = false;

	onMount(async () => {
		if(user.role == "creator") {
			// sort giveaways by date
			giveaways.sort((a, b) => (a.date > b.date) ? -1 : 1);

			// filter open giveaways
			giveaways = giveaways.filter(giveaway => giveaway.is_open == true);

			// load more giveaways
			await loadMoreGiveaways();
		}
	});

	// Can current user view certain giveaway
	async function canViewGiveaway(giveaway_id) {
		const response = await fetchPost('http://localhost:3000/canViewGiveaway', {
			giveaway_id: giveaway_id
		});

		let temp = response.view;
		return temp;
	}

	// Has current user joined certain giveaway
	async function hasJoined(giveaway_id) {
		const response = await fetchPost('http://localhost:3000/hasJoinedGiveaway', {
			giveaway_id: giveaway_id
		});

		let temp = response.joined;
		return temp;
	}

	// Join certain giveaway
	async function joinGiveaway(giveaway_id) {
		const response = await fetchPost('http://localhost:3000/joinGiveaway', {
			giveaway_id: giveaway_id,
		});

		giveaways.find(giveaway => giveaway._id.$oid === giveaway_id).hasJoined = true;
		giveaways = giveaways;
	}

	// Load more giveaways
	async function loadMoreGiveaways() {
		// Check if there are any giveaways to load
		if(giveaways.length == 0) {
			allGiveawaysLoaded = true;
			return;
		}

		for(let i = loadedGiveaways; i < loadedGiveaways + 10; i++) {

			// Check if current user can view and has joined giveaway
			giveaways[i].hasJoined = await hasJoined(giveaways[i]._id.$oid);
			giveaways[i].canView = await canViewGiveaway(giveaways[i]._id.$oid);

			// Check if there are any more giveaways to load
			if(giveaways.length == i + 1) {
				allGiveawaysLoaded = true;
				loadedGiveaways += i + 1;
				return;
			}
		}

		loadedGiveaways += 10;
	}

</script>

<div class="giveaways-container">
	{#each giveaways as giveaway, i}

		{#if i < loadedGiveaways}

			{#if giveaway.is_open}

				<div class='giveaway-box'>
					{#if giveaway.canView}
			
						<img class="giveaway-image" src={"/images/" + user.username + "/" + giveaway.image_path}>
						
						<div class="text-container">
							<h3>{giveaway.text}</h3>
						</div>
						
						{#if !giveaway.hasJoined}
							<button on:click={async () => await joinGiveaway(giveaway._id.$oid)}>Join</button>
						{:else}
							<p>You have already joined this giveaway!</p>
						{/if}

					{:else}
						
						<div class="cant-view-giveaway-container">
							<img class="giveaway-image-cant-view" src={"/images/" + user.username + "/" + giveaway.image_path}>
							<p class="centered-text-over-image">You can't view this giveaway!</p>
						</div>

						<div class="text-container">
							<h3>{giveaway.text}</h3>
							<i class="fa fa-lock" aria-hidden="true"><span class="locked">Locked</span></i> 
						</div>

					{/if}
				</div>

			{/if}

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

	.giveaway-image-cant-view {
		height: 25em;
		width: 40.2em;
		filter: blur(18px) brightness(0.5);
	}

	.text-container {
		margin: 1em;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
	}

	.cant-view-giveaway-container {
		color: white;
		overflow: hidden;
		position: relative;
	}

	.centered-text-over-image{
		top: 45%;
		left: 50%;
		font-size: 1.5em;
		font-weight: bold;
		position: absolute;
		transform: translate(-50%, -50%);
	}

	.locked {
		margin-left: 5px;
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
