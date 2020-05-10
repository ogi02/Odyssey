<script>
	// Component imports
	import Error from '../Helpers/Error.svelte';

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { displayError, clearError } from '../js/helpers.js';

	// Inherited variables
	export let addTierFlag;

	// Local variables
	let result = {};
	let benefits = [''];

	async function addTier() {

		// Clear previous errors
		clearError('benefits_error');

		// Remove empty benefits from array
		let temp = benefits.filter(benefit => benefit.replace(/\s/g, '') !== '');

		if(temp.length == 0) {
			displayError('benefits_error', 'You must fill in at least one benefit!');
			return false;
		}

		// Create result with tier information
		result = {
			name: document.getElementById('name').value,
			price: document.getElementById('price').value,
			benefits: temp
		}

		// Fetch POST request for creating a tier
		const response = await fetchPost('http://localhost:3000/createTier', {
			result: result
		});

		// Get back to profile page
		addTierFlag = false;

		location.reload();
	}

	function addBenefitField() {
		// Add new empty benefit
		benefits = benefits.concat('');
	}

	function removeBenefit(index) {
		benefits.splice(index, 1);
		benefits = benefits;
	}

</script>

<div class='form'>

	<form autocomplete="off">

		<h3>Add a New Tier!</h3>

		<input type='text' id='name' placeholder='Name' required>
		
		<input type='number' id='price' placeholder='Price' min='1' max='1000' required>

		<button id='benefits_button' on:click|preventDefault={() => addBenefitField()}>Add benefit</button>

		<Error id='benefits_error' message='' />

		{#each benefits as benefit, i}
			<div>

				<input type='text' class='benefits' bind:value={benefit} placeholder='Benefit'>
			
				{#if benefits.length > 1}
					<button id={i} class='remove' on:click|preventDefault={() => removeBenefit(i)}>Remove</button>
				{/if}

			</div>
		{/each}

		<p>Keep in mind that all of the benefits for the previous tiers will be applied for this tier.</p>
		
		<button type='submit' on:click|preventDefault={async () => addTier()}>Continue</button>

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

	button {
		display: block;
	}

	.remove, .benefits {
		display: inline-block;
	}

	#benefits_error, #benefits_button {
		display: inline;
	}

</style>