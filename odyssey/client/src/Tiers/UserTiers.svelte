<script>
	// Javascript imports
	import { fetchPost } from "../js/fetch.js";

	// Inherited variables
	export let user;
	export let tiers;
	export let subscribedTierId;

	// Choose certain tier
	async function chooseTier(self_id) {
		let result = {
			tier_id: self_id,
			creator_id: user._id.$oid
		};

		subscribedTierId = self_id;

		const response = await fetchPost("http://localhost:3000/chooseTier", {
			result: result
		});
	}

	// Remove certain tier
	async function removeTier(self_id) {
		let result = {
			tier_id: self_id,
			creator_id: user._id.$oid
		}

		subscribedTierId = null;

		const response = await fetchPost("http://localhost:3000/removeTier", {
			result: result
		});
	}

</script>

<div class="tiers-container">

	{#each tiers as tier}

		<div class="tier-box">
			
			<h3 class="tier-name">{tier.name}</h3>
			<p class="tier-price">${tier.price}</p>
			<p class="tier-price-per-month">PER MONTH</p>

			{#if tier._id.$oid == subscribedTierId}
				<button id="{tier._id.$oid}" on:click={async () => await removeTier(tier._id.$oid)}>Unsubcribe</button>
			{:else}
				<button id="{tier._id.$oid}" on:click={async () => await chooseTier(tier._id.$oid)}>Join</button>
			{/if}

			<ul>

				{#each tier.benefits as benefit}
					<li class="benefit">{benefit}</li>
				{/each}

			</ul>

		</div>

	{/each}

</div>

<link href='https://fonts.googleapis.com/css?family=Calistoga' rel='stylesheet'>

<style>

	.tiers-container {
		display: flex;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}

	.tier-box {
		width: 18em;
		margin: 10px;
		min-height: 23em;
		border: 6px solid;
		border-image-slice: 1;
		border-image-source: linear-gradient(#9dcff2, #efacca);
		outline: solid 2px #0f1930;
	}

	.tier-name {
		margin: 0;
		padding: 0.7em;
		font-size: 1.3em;
		margin-bottom: 1em;
		background-color: #9dcff2;
	}

	.tier-price {
		margin: 0;
		color: black;
		font-size: 1.7em;
		font-family: "Calistoga";
	}

	.tier-price-per-month {
		margin: 0;
		color: grey;
		padding: 0.5em;
		font-size: 0.8em;
		font-weight: bold;
	}

	.benefit {
		text-align: left;
		margin-bottom: 10px;
	}

	button {
		width: 8em;
		color: white;
		border: none;
		cursor: pointer;
		font-size: 18px;
		margin-top: 1em;
		border-radius: 50px;
		background-color: #0f1930;
	}

</style>