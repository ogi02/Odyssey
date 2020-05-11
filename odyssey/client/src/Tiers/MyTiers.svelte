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
					<li style="text-align: left; margin-bottom: 10px;">{benefit}</li>
				{/each}	
			</ul>

		</div>

	{/each}

</div>

<style>

	.tiers-container{
		display: flex;
		flex-shrink: 0;
		justify-content: center;
	}

	.tier-box{
		border: 6px solid;
		border-image-source: linear-gradient(#9dcff2, #efacca);
		border-image-slice: 1;
		outline: solid 2px #0f1930;
		min-width: 18em;
		max-width: 18em;
		min-height: 23em;
		margin: 10px;
	}

	.tier-name{
		font-size: 1.3em;
		letter-spacing: 0.5px;
		background-color: #9dcff2;
		color: black;
		margin: 0;
		padding: 0.7em;
		margin-bottom: 1em;
	}

	.tier-price{
		font-size: 1.7em;
		color: black;
		padding: 0;
		margin: 0;
		font-family: "Calistoga";
		text-align: center;
	}

	.tier-price-per-month{
		font-size: 0.8em;
		color: grey;
		padding: 0.5em;
		margin: 0;
		font-weight: bold;
	}

</style>