<script>
	import Field from "../Helpers/Field.svelte";
	import { fetchPost } from '../fetch.js';
	export let change;
	async function editProfile() {
		let email = document.getElementById('input_r_email').value;
		let password = document.getElementById('input_r_password').value;
		const response = await fetchPost('http://localhost:3000/editProfile', {
			email:email, password:password
		});
		change = false;

	}
</script>

<form autocomplete="off">
	<h3>Edit your profile</h3>
	
	<Field type='email' id='r_email' placeholder='Email' has_icon={true} />

	<Field type='password' id='r_password' placeholder='Password' has_icon={false} />

	<button type='submit' on:click|preventDefault={() => editProfile()}>Save changes</button>

</form>
