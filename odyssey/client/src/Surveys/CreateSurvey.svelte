<script>
	// Component imports
	import Error from '../Helpers/Error.svelte';

	// Javascript imports
	import { fetchPost, fetchFilePost, fetchFileJsonPost } from '../js/fetch.js';
	import { displayError, clearError } from '../js/helpers.js';

	// Inherited variables
	export let tiers;
	export let createSurveyFlag;

	// Local variables
	let result = {};
	let files;
	let required_id;
	let description = '';
	let options = [''];

	tiers.sort((a, b) => (parseInt(a.price) > parseInt(b.price)) ? 1 : ((parseInt(a.price) < parseInt(b.price)) ? -1 : 0));

	async function createSurvey() {

		// Clear previous errors
		clearError('options_error');

		// Remove empty options from array
		let temp = options.filter(option => option.replace(/\s/g, '') !== '');

		if(temp.length < 2) {
			displayError('options_error', 'You must fill in at least two options!');
			return false;
		}

		// Get required id for survey
		required_id = document.querySelector('input[name=tier]:checked').value;

		// Clear previous possible errors
		clearError('picture_error');

		// Check for image
		if(files == null) {
			displayError('picture_error', 'Image for survey is mandatory');
			return false;
		}

		// Check for picture size limit
		if(files[0].size > 2097152) {
			displayError('picture_error', 'Size must be less than 2 MB');
			return false;
		}

		result = {
			description: description,
			required_id: required_id,
			options: options
		}
		
		// Fetch post request for uploading the picture
		const response = await fetchFileJsonPost(
			('http://localhost:3000/createSurvey'), result, files[0]
		);

		// Check for possible errors
		if(!response.success) {
			displayError('picture_error', response.message)
			return false;
		}

		createSurveyFlag = false;
		location.reload();
	}

	function addOptionField() {
		// Add new empty benefit
		options = options.concat('');
	}

	function removeOption(index) {
		options.splice(index, 1);
		options = options;
	}

</script>

<div class='form'>

	<form autocomplete="off">

		<h3>Create a new survey!</h3>

		<textarea id='description' placeholder='Description' bind:value={description}></textarea>

		<p>Choose a photo for the survey</p>
		<input type='file' id='img' bind:files>

		<Error id='picture_error' message='' />

		<p>Select which is the lowest tier that can participate in your survey</p>
		
		{#each tiers as tier, i}
			<div>
				{#if i == 0}
					<input type="radio" id={tier._id.$oid} name="tier" value={tier._id.$oid} checked="checked">
				{:else}
					<input type="radio" id={tier._id.$oid} name="tier" value={tier._id.$oid}>
				{/if}

				<label for={tier._id.$oid}>{tier.name} ({tier.price}$)</label>
			</div>
		{/each}

		<p>Options for survey</p>

		<button id='options_button' on:click|preventDefault={() => addOptionField()}>Add option</button>

		<Error id='options_error' message='' />

		{#each options as option, i}
			<div>

				<input type='text' class='options' bind:value={option} placeholder='Option'>
			
				{#if options.length > 1}
					<button id={i} class='remove' on:click|preventDefault={() => removeOption(i)}>Remove</button>
				{/if}

			</div>
		{/each}

		<button type='submit' on:click|preventDefault={async () => createSurvey()}>Create Survey</button>

	</form>

</div>

<style>

	.form {
		margin-top: 80px;
	}

	input[type=radio],
	label {
		display: inline-block;
	}

</style>