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
		const response = await fetchPost('/editProfile', {
			email: email, password: password
		});

		change = false;
	}

	function cancelEditProfile() {
		change = false;
	}

</script>

<div class="card">
	
	<form autocomplete="off">
		
		<h3 class='title'>Edit your profile</h3>

		<p>You can change your email, your password or both. If you leave it blank it will not be changed.</p>
		
		<Field type='email' id='e_email' placeholder='Email' has_icon={true} />

		<Field type='password' id='e_password' placeholder='Password' has_icon={false} />

		<Field type='password' id='e_confirm' placeholder='Confirm Password' has_icon={false} />

		<div class='buttons'>

			<button type='submit' id='cancel' on:click|preventDefault={() => cancelEditProfile()}>Cancel</button>

			<button type='submit' id='continue' on:click|preventDefault={async () => await editProfile()}>Save Changes</button>

		</div>

	</form>

</div>

<link href='https://fonts.googleapis.com/css?family=Jost' rel='stylesheet'>

<style>

	.card {
		max-width: 400px;
		font-size: 1.1em;
		margin: 100px auto;
		text-align: center;
		font-family: "Jost";
	}

	.title {
		font-size: 1.5em;
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

	#continue {
		color: #0f1931;
		font-weight: bold;
		margin-left: 5px;
		background-color: #9fcdf5;
	}

	#continue:hover {
		cursor: pointer;
		background-color: #8cc2f2;
	}

</style>
