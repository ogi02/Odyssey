<script>
	// Library imports
	import router from 'page';
	import { onMount } from 'svelte';

	// Component imports
	import Field from '../Helpers/Field.svelte';

	// Javascript imports
	import { loggedIn } from '../js/stores.js'
	import { loginUser, registerUser } from './authentication_management.js';

	// Local variables
	let login = true;
	let userLoggedIn;
	let registered = false;

	onMount(() => {
		loggedIn.subscribe(value => {
			userLoggedIn = value;
		});

		if(userLoggedIn) {
			router.redirect('/profile');
		}
	});

	// Change between login and registration
	function toggleLogin() { 
		login = !login;
	}

</script>

<div class='main'>

	<div class='header'>
		{#if login}
			<h1>Login</h1>
		{:else}
			<h1>Register</h1>
		{/if}
	</div>
	
	<div class='form'>
		
		<form autocomplete="off">
			{#if registered}
				<p>Grumni se ognqne! :)</p>
			{:else if login}

				<Field type='text' id='l_username' placeholder='Username' has_icon={false} />

				<Field type='password' id='l_password' placeholder='Password' has_icon={false} />

				<button id='info_submit' type='submit' class='submit' on:click|preventDefault={async () => {
					await loginUser(true);
				}}>Continue</button>

				<div class='switch' on:click={toggleLogin}>Don't have an account? Register now!</div>

			{:else}

				<Field type='text' id='r_username' placeholder='Username' has_icon={true} />

				<Field type='email' id='r_email' placeholder='Email' has_icon={true} />

				<Field type='text' id='r_name' placeholder='Name' has_icon={false} />

				<Field type='password' id='r_password' placeholder='Password' has_icon={false} />

				<Field type='password' id='r_confirm' placeholder='Confirm Password' has_icon={false} />

				<button id='info_submit' type='submit' class='submit' on:click|preventDefault={async () => {
					registered = await registerUser(false);
				}}>Continue</button>

				<div class='switch' on:click={toggleLogin}>Already have an account? Log in!</div>

			{/if}

		</form>

	</div>

</div>

<link href='https://fonts.googleapis.com/css?family=Jost' rel='stylesheet'>

<style>

	.main {
		font-family: "Jost";
		display: block;
		max-width: 400px;
		margin: 100px auto;
		text-align: center;
		font-size: 1.1em;
	}

	.switch:hover {
		text-decoration: underline;
		cursor: pointer;
	}

	.submit {
		margin: 15px 0;
		background-color: #9fcdf5;
		padding: 10px;
		width: 300px;
		border-radius: 5px;
		font-weight: bold;
		color: #0f1931;
	}

	.submit:hover {
		background-color: #8cc2f2;
		cursor: pointer;
	}

</style>