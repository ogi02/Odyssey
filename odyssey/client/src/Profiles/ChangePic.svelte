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

		// Fetch post request for uploading the picture
		const response = await fetchFilePost(
			('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/upload_picture?type=' + type), files[0]
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

</script>

<div class='card'>
	
	<form autocomplete='off'>
		
		<h3>Change your {type} picture!</h3>
		
		<input type='file' id='img' bind:files>
		
		<Error id='picture_error' message='' />
		
		<button type='submit' on:click|preventDefault={() => uploadPic()}>Continue</button>
	
	</form>
</div>