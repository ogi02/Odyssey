<script>

	export let username;
	export let change;
	export let src;
	export let type;
	import Error from '../Helpers/Error.svelte';
	import { displayError, clearError } from '../helpers.js';
	import { fetchFilePost } from '../fetch.js';

	let files;

	async function uploadPic() {
		clearError('picture_error');
		if(files == null) {
			displayError('picture_error', 'Image is required!');
			return false
		}
		console.log(files[0]);
		const response = await fetchFilePost(
			('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/upload_picture?type=' + type), files[0]
		);
		if(!response.success) {
			displayError('picture_error', response.message)
			return false;
		}
		change = false;
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