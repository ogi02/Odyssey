<script>
	// Component imports
	import Field from "../Helpers/Field.svelte";

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { displayError } from '../js/helpers.js'

	// Inherited variables
	export let change;
	
	// Edit profile function
	async function editProfile() {
		// Get email, password and confirm password
		let email = document.getElementById('input_e_email').value;
		let password = document.getElementById('input_e_password').value;
		let confirm = document.getElementById('input_e_confirm').value;

		// Check is password is set, but not confirmed
		if(password != '' && confirm == '') {
			displayError('error_e_confirm', 'Confirm Password is required');
			return false;
		}

		// Fetch post request for changing email, password or both
		const response = await fetchPost('http://localhost:3000/editProfile', {
			email: email, password: password
		});
		change = false;
	}

</script>

<div class="card">
	
	<form autocomplete="off">
		
		<h3>Edit your profile</h3>

		<p>You can change your email, your password or both. If you leave it blank it will not be changed.</p>
		
		<Field type='email' id='e_email' placeholder='Email' has_icon={true} />

		<Field type='password' id='e_password' placeholder='Password' has_icon={false} />

		<Field type='password' id='e_confirm' placeholder='Confirm Password' has_icon={false} />

		<button id='info_submit' type='submit' on:click|preventDefault={async () => await editProfile()}>
			Save changes
		</button>

	</form>

</div>

<style>

	.card {
		position: relative;
		top: 50px;
	}
	
</style>
