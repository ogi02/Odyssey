<script>
	
	import { fetchPost } from "./helpers.js";
	import Error from "./Error.svelte";
	
	let errorMessage;
	let errorShow;
	
	let username = "";
	let password = "";
	let confirmPassword = "";
	let name = "";
	let email = "";
	let login = true;

	async function loginUser() {
		const response = await fetchPost("http://localhost:3000/login", {username: username, password: password});
		console.log(response)
		if(!response.success) {
			displayError(response.message)
			return false;
		}
		errorShow = false;
	}

	function myFunction() {
		console.log(1)
	}

	async function registerUser() {
		if(password !== confirmPassword) {
			displayError("Passwords do not match!");
			return false;
		}
		const response = await fetchPost("http://localhost:3000/register", {username: username, password: password, name: name, email: email});
		if(!response.success) {
			displayError(response.message);
			return false;
		}
		errorShow = false;
	}

	function toggleLogin() {
		login = !login;
	}

	function displayError(message) {
		errorShow = true
		errorMessage = message
	}

</script>

<div id="card">
	<div class="header">
		{#if login}
			<h1>Login</h1>
		{:else}
			<h1>Register</h1>
		{/if}
	</div>
	
	<div class="form">
		<form>

			<input type="text" placeholder="Username" value={username} required={true} 
				on:input={event => username = event.target.value}
			/>

		{#if !login}

			<input type="password" placeholder="Password" value={password} minlength="8" required={true}
				on:input={event => password = event.target.value}
			/>

			<input type="password" placeholder="Confirm Password" value={confirmPassword} required={true}
				on:input={event => confirmPassword = event.target.value}
			/>

			<input type="text" placeholder="Name" value={name} required={true}
				on:input={event => name = event.target.value}
			/>

			<input type="email" placeholder="Email" value={email} required={true}
				on:input={event => email = event.target.value}
			/>

			<button type="submit" on:click|preventDefault={registerUser}>Register</button>

			<div on:click={toggleLogin}>Log in</div>

		{:else}

			<input type="password" placeholder="Password" value={password} required={true}
				on:input={event => password = event.target.value}
			/>

			<button type="submit" on:click|preventDefault={loginUser}>Login</button>

			<div on:click={toggleLogin}>Register</div>

		{/if}
	
		</form>
	</div>

	<Error show={errorShow} message={errorMessage} on:close-error={() => errorShow = false} />

</div>

<style>
	input {
		display: block;
	}
</style>