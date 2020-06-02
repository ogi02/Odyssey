<script>
	// Component imports
	import Error from '../Helpers/Error.svelte';

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { displayError, clearError, showLoader, hideLoader, enableButton, disableButton } from '../js/helpers.js';

	// Inherited variables
	export let addTierFlag;

	// Local variables
	let name;
	let price;
	let result = {};
	let benefits = [''];

	async function addTier() {
		// Check for duplicate tier name
		if(!(await checkTierName(name))) {
			return false;
		}

		// Check for duplicate tier price
		if(!(await checkTierPrice(price))) {
			return false;
		}

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
			name: name,
			price: price,
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
		// Remove benefit at certain index
		benefits.splice(index, 1);
		benefits = benefits;
	}

	function checkEmptyTierName() {
		return name == null;
	}

	function checkEmptyTierPrice() {
		return price < 1 || price > 1000 || price == null;
	}

	async function checkTierName() {
		// Clear tier name error, enable 'Continue' button, show 'Loader' icon
		clearError('name_error');
		showLoader('loader_name');
		enableButton('create');

		// Check for empty tier name
		if(checkEmptyTierName()) {
			displayError('name_error', 'Tier name is required!');
			disableButton('create');
			return false;
		}

		// Fetch post request for checking if such tier name exists in the database for the current user
		const response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/tier_name', {
			tier_name: name
		});

		// Hide 'Loader' icon
		hideLoader('loader_name');

		// Check for possible error
		if(!response.success) {
			displayError('name_error', response.message);
			disableButton('create');
			return false;
		}

		return true;
	}

	async function checkTierPrice() {
		// Clear tier name error, enable 'Continue' button, show 'Loader' icon
		clearError('price_error');
		showLoader('loader_price');
		enableButton('create');

		// Check for empty tier price
		if(checkEmptyTierPrice()) {
			displayError('price_error', 'Price must be between 1 and 1000!');
			disableButton('create');
			return false;
		}

		// Fetch post request for checking if such tier name exists in the database for the current user
		const response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/tier_price', {
			tier_price: price
		});

		// Hide 'Loader' icon
		hideLoader('loader_price');

		// Check for possible error
		if(!response.success) {
			displayError('price_error', response.message);
			disableButton('create');
			return false;
		}

		return true;
	}

</script>

<div class='form'>

	<form autocomplete="off">

		<h3>Add a New Tier!</h3>

		<input type='text' id='name' placeholder='Name' bind:value={name}
			on:input={async() => await checkTierName()}
		>

		<i id='loader_name' class='icons bx bx-loader'></i>
		<Error id='name_error' message='' />

		<input type='number' id='price' placeholder='Price' bind:value={price}
			on:input={async() => await checkTierPrice()}
		>

		<i id='loader_price' class='icons bx bx-loader'></i>
		<Error id='price_error' message='' />

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

		<button id='create' type='submit' on:click|preventDefault={async () => addTier()}>Continue</button>

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

	.input {
		display: block;
		padding: 10px;
		border-radius: 5px;
		font-weight: 100px;
		min-width: 300px;
		margin: 10px 0 2px;
		outline-color: #bcdcfa;
	}

	.input, .icons {
		display: inline;
	}

	.icons {
		position: absolute;
		color: rgba(0, 0, 0, 0,7);
		font-size: 16px;
		display: none;
		top: 25px;
		right: 10px;
	}

</style>