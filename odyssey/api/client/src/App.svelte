<script>
	
	import { onMount } from 'svelte';
	import Authentication from './Authentication/Authentication.svelte';
	import BecomeCreator from './Authentication/BecomeCreator.svelte'
	import Profile from './Profiles/Profile.svelte'
	
	let loggedIn;
	
	onMount(async () => {
		const res = await fetch(
			'http://localhost:3000/checkLogin');
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
	<Profile />
{/if}