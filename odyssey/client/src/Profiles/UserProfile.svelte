<script>
	// Library imports
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { username } from '../js/stores.js';
	import { followUser, unfollowUser, isFollowing } from './profile_management.js';

	// Component imports
	import UserTiers from '../Tiers/UserTiers.svelte';
	import UserPosts from '../Posts/UserPosts.svelte';
	import UserSurveys from '../Surveys/UserSurveys.svelte';
	import UserGiveaways from '../Giveaways/UserGiveaways.svelte';

	// Local variables
	let cover_picture_src = '';
	let profile_picture_src = '';
	
	let is_following = false;
	
	let user = {};
	let info = {};
	let tiers = {};
	let posts = {};
	let surveys = {};
	let giveaways = {};
	let subscribedTierId;

	let type_of_display = 'posts';

	username.subscribe(async (newValue) => {
		if(newValue == '') {
			username.set(window.location.href.substr(window.location.href.lastIndexOf('/') + 1));
			return false;
		}

		const response = await fetchPost("http://localhost:3000/profile/" + newValue, {
			username: newValue
		});

		user = response.user;
		profile_picture_src = '/images/' + user.username + '/profile_picture';
		cover_picture_src = '/images/' + user.username + '/cover_picture';

		if(user.role == "creator") {
			info = response.info;
			tiers = response.tiers;
			posts = response.posts;
			surveys = response.surveys;
			giveaways = response.giveaways;
			subscribedTierId = response.tier_id;
		}

		is_following = await isFollowing(user.username);
	});

</script>

<img src={cover_picture_src} id="cover_picture" on:error={() => cover_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/cover_picture'}>

<div class="card">

	<div class='profile_pic'>

		<img src={profile_picture_src} id="profile_picture" on:error={() => profile_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/profile_picture'}>

	</div>

	<h1>{user.username}</h1>

	<div style="margin: 24px 0;">
		<a href="#"><i class="fa fa-twitch"></i></a> 
		<a href="#"><i class="fa fa-twitter"></i></a>  
		<a href="#"><i class="fa fa-instagram"></i></a> 
		<a href="#"><i class="fa fa-youtube"></i></a> 
		<a href="#"><i class="fa fa-facebook"></i></a> 
	</div>

	{#if is_following}
		<button class="follow-button" on:click={async () => is_following = await unfollowUser(user.username)}>Unfollow</button>
	{:else}
		<button class="follow-button" on:click={async () => is_following = await followUser(user.username)}>Follow</button>
	{/if}

	{#if user.role == "creator"}

		<UserTiers user={user} tiers={tiers} subscribedTierId={subscribedTierId} />

		<div id="menu">

			<div class="my-feed-div">
				<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'posts')}>Posts</div>
			</div>

			<div class="my-feed-div">
				<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'surveys')}>Surveys</div>
			</div>

			<div class="my-feed-div">
				<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'giveaways')}>Giveaways</div>
			</div>

		</div>

		{#if type_of_display == 'posts'}

			<UserPosts user={user} posts={posts} />

		{:else if type_of_display == 'surveys'}

			<UserSurveys user={user} surveys={surveys} />

		{:else}

			<UserGiveaways user={user} giveaways={giveaways} />

		{/if}

	{/if}

</div>

<style>

	.card {
		position: relative;
		max-width: 60em;
		margin: auto;
		margin-top: 33vh;
		text-align: center;
		font-family: arial;
	}

	button {
		width: 8em;
		color: white;
		border: none;
		cursor: pointer;
		font-size: 18px;
		margin-top: 1em;
		border-radius: 50px;
		background-color: #0f1930;
	}

	a {
		text-decoration: none;
		font-size: 22px;
		color: black;
	}

	button:hover, a:hover {
		opacity: 0.7;
	}

	.toggle:hover {
		background-color: #eee;
	}

	#profile_picture {
		margin-top: 4em;
		border: 4px solid #fff;
		object-fit: cover;
		border-radius: 50%;
		height: 175px;
		width: 175px;
	}

	#cover_picture {
		position: absolute; 
		top: 3.6em; 
		left: 0; 
		min-width: 100%; 
		width: 100%; 
		height: 45%; 
		min-height: 300px; 
		object-fit: cover;
	}

	.follow-button {
		max-width: 8em;
		margin-bottom: 3em;
	}

	li {
		margin: 0.4em;
	}

	#menu {
		display: flex;
		color: #080d52;
		max-width: 800px;
		font-size: 1.5em;
		margin: 1em auto 0;
		background: linear-gradient(90deg, 
			rgba(252,252,252,1) 2%, 
			rgba(148,187,233,1) 18%, 
			rgba(238,174,202,1) 76%, 
			rgba(255,255,255,1) 96%
		);
	}

	.my-feed-div {
		flex: 1 1 auto;
		padding: 0.5em 0;
	}

	.my-feed-button:hover {
		opacity: 0.7;
		cursor: pointer;
	}

</style>