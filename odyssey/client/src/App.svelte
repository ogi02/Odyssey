<script>

	import { Router, Route } from "svelte-routing";
	import NavLink from "./components/NavLink.svelte";
	import { onMount } from 'svelte';
	import Authentication from './Authentication/Authentication.svelte';
	import BecomeCreator from './Authentication/BecomeCreator.svelte'
	import Profile from './Profiles/Profile.svelte'
	export let url = "";
	
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
		console.log(loggedIn);
	});
	

</script>
{#if loggedIn == false}
	<p> Welcome to Odyssey! Log in or register to view content.</p>
	<Authentication />
{:else}
	<Router url="{url}">
	  <nav>
	    <NavLink to="/">Profile</NavLink>
	    <NavLink to="about">About</NavLink>
	    <NavLink to="become_a_creator">Become a creator!</NavLink>
	  </nav>
	  <div>
	    <Route path="about" component="{Profile}" />
	    <Route path="become_a_creator" component="{BecomeCreator}" />
	    <Route path="/" component="{Profile}" />
	  </div>
	</Router>
{/if}

