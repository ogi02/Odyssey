<script>
	// Library imports
	import page from 'page.js';
	import { onMount } from 'svelte';

	import { Router, Route, NotFound, redirect } from "./router.js";

	// Component imports
	import Home from '../Home.svelte';
	import Search from './Search.svelte';
	import MyProfile from '../Profiles/MyProfile.svelte';
	import UserProfile from '../Profiles/UserProfile.svelte';
	import BecomeCreator from '../Authentication/BecomeCreator.svelte';
	import Authentication from '../Authentication/Authentication.svelte';
	
	// Javascript imports
	import { checkLogin } from '../helpers.js';
	import { logoutUser, loginUser } from '../Authentication/authentication_management.js';	

	// Local variables
	let loggedIn = false;
	let searchedUsername = '';
	let home_picture_src = 'images/src/Home.png';

	onMount(async () => {
		loggedIn = await checkLogin();
	});

	const guard = async (ctx, next) => {
		if (!await checkLogin()) {
			// check if user is logged in
			redirect("/login");
		} else {
			// go to the next callback in the chain
			next();
		}
	};

</script>

{#if loggedIn}
	<nav>
		<a href='/' class='home-icon'><img src={home_picture_src}></a>
		<a href='profile' class='navlink'>My Profile</a>
		<a href='become_a_creator' class='navlink'>Become a creator!</a>
		<a href='login' class='navlink' on:click={async () => loggedIn = await logoutUser()}>Logout</a>
		<Search />
	</nav>
{:else}
	<nav>
		<a href='/' class='home-icon'><img src={home_picture_src}></a>
		<a href='login' class='navlink'>Log in</a>
	</nav>
{/if}

<Router>
	
	<Route path='/' component={Home} />
	
	<Route path='/login'>
		<Authentication bind:loggedIn={loggedIn} />
	</Route>
	
	<Route path='/profile' component={MyProfile} middleware={[guard]} />
	
	<Route path='/become_a_creator' component={BecomeCreator} middleware={[guard]} />

	<Route path='/profile/:username' let:params middleware={[guard]} >
		<UserProfile />
	</Route>

	<NotFound>
		<h1>404 baby</h1>
	</NotFound>

</Router>

<style>

	nav {
		position: fixed;
		top: 0;
		margin: 0;
		left: 0;
		padding: 1.3em 0 1em;
		width: 100%;
		z-index: 1;
		overflow: hidden;
		border-bottom: solid 1.5px #080d52;
		background: linear-gradient(90deg, 
			rgba(223,240,255,1) 0%, 
			rgba(109,178,237,1) 45%, 
			rgba(238,174,202,1) 100%
		);
	}

	nav .navlink {
		text-decoration: none;
		color: #010212;
		font-weight: 450;
		margin: 0;
		left: 0;
		padding: 1.2em 1.2em;
	}

	nav .navlink:hover{
		text-decoration: underline;
		background-color:rgba(41, 94, 179, 0.14);
		box-shadow: 0 0 9em 0 rgba(41, 94, 179, 1);
	}

	nav img {
		position: fixed;
		margin: 0;
		top: 0;
		padding: 0.5em;
		left: 0;
		width: 3.3em;
		height: 3.3em;
	}

	nav img:hover {
		opacity: 0.7;
	}

	nav .home-icon {
		text-decoration: none;
		color: white;
		margin: 0;
		left: 0;
		padding: 0 2.3em;
	}

</style>
