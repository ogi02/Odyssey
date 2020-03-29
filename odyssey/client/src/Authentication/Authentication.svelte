<script>
	// Library imports
	import page from "page.js"

	// Component imports
	import Field from '../Helpers/Field.svelte';

	// Javascript imports
	import { loginUser, registerUser } from './authentication_management.js';

	// Inherited variables
	export let loggedIn;

	// Local variables
	let login = true;

	// Change between login and registration
	function toggleLogin() { 
		login = !login;
	}

</script>

<div id='card'>

	<p>Welcome to Odyssey! Log in or register to view content.</p>

	<div class='header'>
		{#if login}
			<h1>Login</h1>
		{:else}
			<h1>Register</h1>
		{/if}
	</div>
	
	<div class='form'>
		
		<form autocomplete="off">

			{#if login}

				<Field type='text' id='l_username' placeholder='Username' has_icon={false} />

				<Field type='password' id='l_password' placeholder='Password' has_icon={false} />

				<button id='info_submit' type='submit' on:click|preventDefault={async () => {
					loggedIn = await loginUser(true);
					if(loggedIn == true) {
						page.redirect('/profile');
					}
				}}>Login</button>

				<div class='switch' on:click={toggleLogin}>Don't have an account? Register now!</div>

			{:else}

				<Field type='text' id='r_username' placeholder='Username' has_icon={true} />

				<Field type='email' id='r_email' placeholder='Email' has_icon={true} />

				<Field type='text' id='r_name' placeholder='Name' has_icon={false} />

				<Field type='password' id='r_password' placeholder='Password' has_icon={false} />

				<Field type='password' id='r_confirm' placeholder='Confirm Password' has_icon={false} />

				<button id='info_submit' type='submit' on:click|preventDefault={async () => {
					loggedIn = await registerUser(false);
					if(loggedIn == true) {
						page.redirect('/profile');
					}
				}}>Register</button>

				<div class='switch' on:click={toggleLogin}>Already have an account? Log in!</div>

			{/if}

		</form>

	</div>

</div>

<style>

	.switch:hover {
		text-decoration: underline;
		cursor: pointer;
	}

</style>