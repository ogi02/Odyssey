<script>
	
	import { onMount } from "svelte";
	import Authentication from "./Authentication/Authentication.svelte";
	
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

</script>

{#if loggedIn == false}
	<Authentication />
{:else}
	<div></div>
{/if}