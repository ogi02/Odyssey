<script>
	// Library imports
	import router from 'page';
	import { onMount } from 'svelte';
	
	// Component imports
	import Search from './Search.svelte';
	
	// Javascript imports
	import routes from '../js/routes'
	import { loggedIn } from '../js/stores.js';
	import { checkLogin } from '../js/helpers.js';
	import { logoutUser, loginUser } from '../Authentication/authentication_management.js';	

	// Local variables
	let page;
	let params;
	let userLoggedIn;
	let home_picture_src = '/images/src/Home.png';

	onMount(async () => {
		await loggedIn.set(await checkLogin());

		// Loop around all of the routes and create a new instance of
		// router for reach one with some rudimentary checks.
		routes.forEach(route => {
			router(
				route.path, 
				
				// Set the params variable to the context.
				// We use this on the component initialisation
				(ctx, next) => {
					params = ctx.params
					next()
				},
				
				// Check if auth is valid. If so, set the page to the component
				// otherwise redirect to login.
				() => {
					if (route.auth && !$loggedIn) {
						router.redirect('/login');
					} else {
						page = route.component;
					}
				}
			)
		});

		router.start();
	});

	const unsubscribe = loggedIn.subscribe(value => {
		userLoggedIn = value;
	});

</script>

{#if userLoggedIn}
	<nav>
		<a href='/' class='home-icon'><img src={home_picture_src}></a>
		<a href='/profile' class='navlink'>My Profile</a>
		<a href='/become_a_creator' class='navlink'>Become a creator!</a>
		<a href='/login' class='navlink' on:click={async () => await logoutUser()}>Logout</a>
		<Search />
	</nav>
{:else}
	<nav>
		<a href='/' class='home-icon'><img src={home_picture_src}></a>
		<a href='/login' class='navlink'>Log in</a>
	</nav>
{/if}

<svelte:component this={page} params={params} />

<style>

	nav {
		top: 0;
		left: 0;
		z-index: 1;
		width: 100%;
		padding: 1.6em;
		position: fixed;
		overflow: hidden;
		border-bottom: solid 1.5px #080d52;
		background: linear-gradient(90deg, 
			rgba(223,240,255,1) 0%, 
			rgba(109,178,237,1) 45%, 
			rgba(238,174,202,1) 100%
		);
	}

	.home-icon {
		padding: 0.5em 2em;
	}

	.home-icon img {
		top: 0.5em;
		left: 1.5em;
		width: 3.3em;
		position: fixed;
	}

	.home-icon img:hover {
		opacity: 0.7;
	}

	nav .navlink {
		color: #010212;
		font-weight: 450;
		padding: 1em 1em;
		text-decoration: none;
	}

	nav .navlink:hover{
		text-decoration: underline;
		background-color:rgba(41, 94, 179, 0.14);
		box-shadow: 0 0 9em 0 rgba(41, 94, 179, 1);
	}

</style>