<script>
	// Library imports
	import page from 'page.js';
	import { onMount } from 'svelte';

	// Component imports
	import Home from '../Home.svelte';
	import Route from "./Route.svelte";
	import Router from "./Router.svelte";
	import Profile from '../Profiles/Profile.svelte';
	import BecomeCreator from '../Authentication/BecomeCreator.svelte';
	import Authentication from "../Authentication/Authentication.svelte";
	
	// Javascript imports
	import { checkLogin } from "../helpers.js";
	import { logoutUser, loginUser } from '../Authentication/authentication_management.js';	

	// Local variables
	let loggedIn = false;

	onMount(async () => { 
		loggedIn = await checkLogin();
		console.log(loggedIn);
	});

</script>

{#if loggedIn}
	<nav>
		<a href="/">Home</a>
		<a href="profile">Profile</a>
		<a href="become_a_creator">Become a creator!</a>
		<a href="login" on:click={async () => loggedIn = await logoutUser()}>Logout</a>
	</nav>
{:else}
	<nav>
		<a href="/">Home</a>
		<a href="login">Log in</a>
	</nav>
{/if}

<Router hashbang={true}>
	
	<Route path="/">
		<Home />
	</Route>
	
	<Route path="/login">
		<Authentication bind:loggedIn={loggedIn}/>
	</Route>
	
	<Route path="/profile">
		<Profile />
	</Route>
	
	<Route path="/become_a_creator">
		<BecomeCreator />
	</Route>

</Router>

<style>

	nav {
		position: fixed;
		top: 0;
		left: 0;
		padding: 1.2em 0 1.2em 0;
		width: 100%;
		background-color: tomato;
	}

	nav a {
		text-decoration: none;
		color: white;
		margin: 0;
		left: 0;
		padding: 1.2em;
	}

	nav a:hover{
		text-decoration: none;
		background-color: green;
	}
	
</style>
