<script>
	// Inherited variables
	export let tiers;

</script>

<div class="tiers-container">
	
	{#each tiers as tier}
		
		<div class='tier-box'>
			
			<h3 class="tier-name">{tier.name}</h3>

			<p class="tier-price">${tier.price}</p>

			<p class="tier-price-per-month">PER MONTH</p>

			<ul>
				{#each tier.benefits as benefit}
					<li class="benefit">{benefit}</li>
				{/each}	
			</ul>

		</div>

	{/each}

</div>

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

</style>