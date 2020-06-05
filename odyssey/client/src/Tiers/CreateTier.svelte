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
		const response = await fetchPost('/createTier', {
			result: result
		});

		// Get back to profile page
		addTierFlag = false;

		location.reload();
	}

	function cancelAddTier() {
		addTierFlag = false;
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
		// Check for empty tier name
		if(checkEmptyTierName()) {
			displayError('name_error', 'Tier name is required!');
			disableButton('create');
			return false;
		}

		// Clear tier name error, enable 'Continue' button, show 'Loader' icon
		clearError('name_error');
		showLoader('loader_name');
		enableButton('create');

		// Fetch post request for checking if such tier name exists in the database for the current user
		const response = await fetchPost('/FpCerpd9Z7SIbjmN81Jy/tier_name', {
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
		// Check for empty tier price
		if(checkEmptyTierPrice()) {
			displayError('price_error', 'Price must be between 1 and 1000!');
			disableButton('create');
			return false;
		}

		// Clear tier name error, enable 'Continue' button, show 'Loader' icon
		clearError('price_error');
		showLoader('loader_price');
		enableButton('create');

		// Fetch post request for checking if such tier name exists in the database for the current user
		const response = await fetchPost('/FpCerpd9Z7SIbjmN81Jy/tier_price', {
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

		<div class='field'>

			<input type='text' id='name' placeholder='Name' bind:value={name} class='input'
				on:input={async() => await checkTierName()}
			>

			<i id='loader_name' class='icons bx bx-loader'></i>
			<Error id='name_error' message='' />

		</div>

		<div class='field'>

			<input type='number' id='price' placeholder='Price' bind:value={price} class='input'
				on:input={async() => await checkTierPrice()}
			>

			<i id='loader_price' class='icons bx bx-loader'></i>
			<Error id='price_error' message='' />

		</div>

		<div class='benefits'>

			<button id='benefits_button' on:click|preventDefault={() => addBenefitField()}>Add benefit</button><br>

			<Error id='benefits_error' message='' />

			{#each benefits as benefit, i}
				<div class='benefit-field'>

					<input type='text' class='benefit-input' bind:value={benefit} placeholder='Benefit'>

					{#if benefits.length > 1}
						<button id={i} class='remove' on:click|preventDefault={() => removeBenefit(i)}>Remove</button>
					{/if}

				</div>
			{/each}

			<p>Keep in mind that all of the benefits from the less expensive tiers will be applied for this tier.</p>

		</div>

		<div class='buttons'>

			<button id='cancel' type='submit' on:click|preventDefault={() => cancelAddTier()}>Cancel</button>

			<button id='create' type='submit' on:click|preventDefault={async () => addTier()}>Continue</button>

		</div>

	</form>

</div>

<link href='https://fonts.googleapis.com/css?family=Jost' rel='stylesheet'>

<style>

	.form {
		display: block;
		font-size: 1.1em;
		max-width: 400px;
		margin: 100px auto;
		text-align: center;
		font-family: "Jost";
	}

	.input {
		padding: 10px;
		display: block;
		min-width: 300px;
		border-radius: 5px;
		font-weight: 100px;
		margin: 10px 0 2px;
		outline-color: #bcdcfa;
	}

	.benefits {
		width: 300px;
		margin: 2em auto 0;
	}

	.benefit-input, .remove {
		display: inline;
	}

	.benefit-input {
		padding: 10px;
		border-radius: 5px;
		font-weight: 100px;
		margin: 10px 0 2px;
		outline-color: #bcdcfa;
	}

	.input, .icons {
		display: inline;
	}

	.icons {
		top: 25px;
		right: 10px;
		display: none;
		font-size: 16px;
		position: absolute;
		color: rgba(0, 0, 0, 0,7);
	}

	.field {
		width: 300px;
		margin: 0 auto;
		position: relative;
	}

	button {
		border-radius: 5px;
	}

	button:not(.remove) {
		width: 300px;
	}

	.buttons {
		width: 300px;
		display: flex;
		margin: 0 auto;
	}

	#benefits_button {
		background-color: #fff4f9;
	}

	#benefits_button:hover {
		cursor: pointer;
		background-color: #fff0f5;
	}

	#cancel {
		color: #0f1931;
		font-weight: bold;
		margin-right: 5px;
		background-color: #e6afcc;
	}

	#cancel:hover {
		cursor: pointer;
		background-color: #eca1c9;
	}

	#create {
		color: #0f1931;
		font-weight: bold;
		margin-left: 5px;
		background-color: #9fcdf5;
	}

	#create:hover {
		cursor: pointer;
		background-color: #8cc2f2;
	}

</style>