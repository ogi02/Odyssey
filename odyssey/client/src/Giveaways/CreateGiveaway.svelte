<script>
	// Component imports
	import Error from '../Helpers/Error.svelte';

	// Javascript imports
	import { fetchPost, fetchFilePost } from '../js/fetch.js';
	import { displayError, clearError } from '../js/helpers.js';

	// Inherited variables
	export let tiers;
	export let createGiveawayFlag;

	// Local variables
	let files;
	let required_id;
	let description = '';

	tiers.sort((a, b) => (parseInt(a.price) > parseInt(b.price)) ? 1 : ((parseInt(a.price) < parseInt(b.price)) ? -1 : 0));

	async function createGiveaway() {
		// Get required id for post
		required_id = document.querySelector('input[name=tier]:checked').value;

		// Clear previous possible errors
		clearError('picture_error');

		// Check for image
		if(files == null) {
			displayError('picture_error', 'Image for giveaway is mandatory');
			return false;
		}

		// Check for picture size limit
		if(files[0].size > 2097152) {
			displayError('picture_error', 'Size must be less than 2 MB');
			return false;
		}

		// Fetch post request for uploading the picture
		const response = await fetchFilePost(
			('/createGiveaway?description=' + description + '&required_id=' + required_id), files[0]
		);

		// Check for possible errors
		if(!response.success) {
			displayError('picture_error', response.message)
			return false;
		}

		createGiveawayFlag = false;
		location.reload();
	}

	function removeFile() {
		files = null;
	}

	function cancelCreateGiveaway() {
		createGiveawayFlag = false;
	}

</script>

<div class='form'>

	<form autocomplete="off">

		<h3>Create a new giveaway!</h3>

		<textarea id='description' placeholder='Description' bind:value={description} rows='5' cols='40'></textarea>

		<div class='field'>

			<label for='img' class='custom-file-upload'>
				<i class='fa fa-cloud-upload'></i> Upload Giveaway image
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

		<p>Select which is the lowest tier that can see your giveaway</p>
		
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

		<div class='buttons'>

			<button type='submit' id='cancel' on:click|preventDefault={() => cancelCreateGiveaway()}>Cancel</button>

			<button type='submit' id='create' on:click|preventDefault={async () => createGiveaway()}>Create Giveaway</button>

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

	button {
		width: 300px;
		border-radius: 5px;
	}

	.buttons {
		width: 300px;
		display: flex;
		margin: 20px auto;
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