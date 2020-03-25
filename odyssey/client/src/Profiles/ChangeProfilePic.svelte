<script>

	import Error from '../Helpers/Error.svelte';
	import { displayError, clearError } from '../helpers.js';
	import { fetchFilePost } from '../fetch.js';

	let files;
	let picture_type = 'profile_picture';

	async function uploadProfilePic() {
		clearError('profile_picture_error');
		if(files == null) {
			displayError('profile_picture_error', 'Image is required!');
			return false
		}
		console.log(files[0]);
		const response = await fetchFilePost(
			'http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/upload_picture', files[0]
		);
		if(!response.success) {
			displayError('profile_picture_error', response.message)
			return false;
		}
	}

</script>

<div class='card'>
	<form autocomplete='off'>
		<h3>Change your profile picture!</h3>
		<input type='file' id='img' bind:files>
		<Error id='profile_picture_error' message='' />
		<button type='submit' on:click|preventDefault={() => uploadProfilePic()}>Continue</button>
	</form>
</div>