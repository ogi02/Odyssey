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

	function removeFile() {
		files = null;
	}

	function cancelCreateSurvey() {
		createSurveyFlag = false;
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

	<form autocomplete='off'>

		<h3>Create a new survey!</h3>

		<textarea id='description' placeholder='Description' bind:value={description} rows='5' cols='40'></textarea>

		<div class='field'>

			<label for='img' class='custom-file-upload'>
				<i class='fa fa-cloud-upload'></i> Upload Survey image
			</label>

			{#if files}
				<div class='filename'>
					<p>{files[0].name}</p>
					<i class='fa fa-trash-o icons' on:click={() => removeFile()}></i>
				</div>
			{/if}
			<input type='file' id='img' bind:files>

		</div>

		<Error id='picture_error' message='' />

		<p>Select which is the lowest tier that can participate in your survey</p>
		
		{#each tiers as tier, i}
			<div>
				{#if i == 0}
					<input type='radio' id={tier._id.$oid} name='tier' value={tier._id.$oid} checked='checked'>
				{:else}
					<input type='radio' id={tier._id.$oid} name='tier' value={tier._id.$oid}>
				{/if}

				<label for={tier._id.$oid}>{tier.name} ({tier.price}$)</label>
			</div>
		{/each}

		<div class='field'>

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

		</div>

		<div class='buttons'>

			<button type='submit' id='cancel' on:click|preventDefault={() => cancelCreateSurvey()}>Cancel</button>

			<button type='submit' id='create' on:click|preventDefault={async () => createSurvey()}>Create Survey</button>

		</div>

	</form>

</div>

<link href='https://fonts.googleapis.com/css?family=Jost' rel='stylesheet'>

<style>

	.form {
		max-width: 400px;
		font-size: 1.1em;
		margin: 100px auto;
		text-align: center;
		font-family: "Jost";
	}

	.field {
		width: 300px;
		margin: 0 auto;
		position: relative;
	}

	input[type=file] {
		display: none;
	}

	.custom-file-upload {
		padding: 10px;
		display: block;
		margin: 0 auto;
		border: 1px solid #333;
	}

	.custom-file-upload:hover {
		cursor: pointer;
		background-color: #f6f6f6;
	}

	.filename {
		display: flex;
		margin-top: 5px;
		margin-bottom: 0;
		align-items: center;
		justify-content: center;
	}

	.filename p {
		margin: 0;
		width: 250px;
		overflow: hidden;
		white-space: nowrap;
		display: inline-block;
		text-overflow: ellipsis;
	}

	.icons {
		display: inline;
	}

	.icons:hover {
		cursor: pointer;
	}

	.tier-paragraph {
		margin-top: 30px;
	}

	input[type=radio],
	label {
		display: inline-block;
	}

	button:not(.remove) {
		width: 300px;
	}

	button {
		border-radius: 5px;
	}

	.buttons {
		width: 300px;
		display: flex;
		margin: 20px auto;
	}

	#options_button {
		background-color: #fff4f9;
	}

	#options_button:hover {
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