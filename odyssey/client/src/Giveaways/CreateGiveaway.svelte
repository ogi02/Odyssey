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
			('http://localhost:3000/createGiveaway?description=' + description + '&required_id=' + required_id), files[0]
		);

		// Check for possible errors
		if(!response.success) {
			displayError('picture_error', response.message)
			return false;
		}

		createGiveawayFlag = false;
		location.reload();
	}

</script>

<div class='form'>

	<form autocomplete="off">

		<h3>Create a new giveaway!</h3>

		<textarea id='description' placeholder='Description' bind:value={description}></textarea>

		<p>Choose a photo for the giveaway</p>
		<input type='file' id='img' bind:files>

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

		<button type='submit' on:click|preventDefault={async () => createGiveaway()}>Create Giveaway</button>

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