<script>
	// Component imports
	import Error from '../Helpers/Error.svelte';

	// Javascript imports
	import { displayError, clearError } from '../js/helpers.js';
	import { fetchFilePost } from '../js/fetch.js';

	// Inherited variables
	export let username;
	export let change;
	export let src;
	export let type;

	// Local variables
	let files;

	// Uploads picture after checking if everything is valid.
	async function uploadPic() {
		// Clear previous errors and check if file is provided
		clearError('picture_error');
		if(files == null) {
			displayError('picture_error', 'Image is required!');
			return false;
		}

		if(files[0].size > 2097152) {
			displayError('picture_error', 'Size must be less than 2 MB');
			return false;
		}

		// Fetch post request for uploading the picture
		const response = await fetchFilePost(
			('/FpCerpd9Z7SIbjmN81Jy/upload_picture?type=' + type), files[0]
		);

		// Check for possible errors
		if(!response.success) {
			displayError('picture_error', response.message)
			return false;
		}

		change = false;
		// Change image source so that page is updated
		src = 'images/' + username + '/' + type + '_picture?t=' + new Date().getTime();
	}

	function removeFile() {
		files = null;
	}

	function cancelUploadPic() {
		change = false;
	}

</script>

<div class='card'>
	
	<form autocomplete='off'>

		<label for='img' class='custom-file-upload'>
			<i class='fa fa-cloud-upload'></i> Upload your new {type} picture!
		</label>
		{#if files}
			<div class='filename'>
				<p>{files[0].name}</p>
				<i class='fa fa-trash-o icons' on:click={() => removeFile()}></i>
			</div>
		{/if}
		<input type='file' id='img' bind:files>
		
		<Error id='picture_error' message='' />
		
		<div class='buttons'>

			<button type='submit' id='cancel' on:click|preventDefault={() => cancelUploadPic()}>Cancel</button>

			<button type='submit' id='create' on:click|preventDefault={async () => uploadPic()}>Continue</button>

		</div>

	</form>

</div>

<link href='https://fonts.googleapis.com/css?family=Jost' rel='stylesheet'>

<style>

	.card {
		max-width: 300px;
		font-size: 1.1em;
		margin: 100px auto;
		text-align: center;
		font-family: "Jost";
	}

	input[type=file] {
		display: none;
	}

	.custom-file-upload {
		max-width: 300px;
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