<script>
	
	import { onMount } from "svelte";
	import Register from "./Register.svelte";
	
	let loggedIn;
	
	onMount(async () => {
		const res = await fetch(
			"http://localhost:3000/checkLogin");
		const response = await res.json();
		if (response.logged_in) {
			loggedIn = true;
		} else {
			loggedIn = false;
		}
	});
	
	async function logoutUser() {
		loggedIn = false;
		const res = await fetch('http://localhost:3000/logout');
		const response = await res.json();
	}
	

</script>

{#if loggedIn == false}
	<Register/>
{:else}
	<div></div>
{/if}