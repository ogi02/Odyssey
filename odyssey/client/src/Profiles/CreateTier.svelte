<script>
	// Javascript imports
	import { fetchPost } from '../js/fetch.js';

	// Inherited variables
	export let addTierFlag;

	// Local variables
	let result = {};
	let benefits = [''];

	async function addTier() {
		// Remove empty benefits from array
		benefits = benefits.filter(benefit => benefit !== '');

		// Create result with tier information
		result = {
			name: document.getElementById('name').value,
			price: document.getElementById('price').value,
			benefits: benefits
		}

		// Fetch POST request for creating a tier
		const response = await fetchPost('http://localhost:3000/createTier', {
			result: result
		});

		// Get back to profile page
		addTierFlag = false;
	}

	function addBenefitField() {
		// Add new empty benefit
		benefits = benefits.concat('');
	}

</script>

<div class='form'>

	<form autocomplete="off">

		<h3>Add a New Tier!</h3>

		<input type='text' id='name' placeholder='Name' required>
		
		<input type='number' id='price' placeholder='Price' min='1' max='1000' required>

		<button on:click|preventDefault={() => addBenefitField()}>Add benefit</button>

		{#each benefits as benefit}

			<input type='text' class='benefits' bind:value={benefit} placeholder='Benefit'>

		{/each}

		<p>Keep in mind that all of the benefits for the previous tiers will be applied for this tier.</p>
		
		<button type='submit' on:click|preventDefault={() => addTier()}>Continue</button>

	</form>

</div>

<style>

	/* Chrome, Safari, Edge, Opera */
	input::-webkit-outer-spin-button,
	input::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	/* Firefox */
	input[type=number] {
		-moz-appearance: textfield;
	}

	.form {
		margin-top: 80px;
	}

	input {
		display: block;
		width: 200px;
	}

</style>