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
	let shipping_info = {};
	let social_media_links = {};

	let type_of_display = 'posts';

	username.subscribe(async (newValue) => {
		if(newValue == '') {
			username.set(window.location.href.substr(window.location.href.lastIndexOf('/') + 1));
			return false;
		}

		const response = await fetchPost("/profile/" + newValue, {
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
			shipping_info = response.info.shipping_info;
			social_media_links = response.info.social_media_links;
		}

		is_following = await isFollowing(user.username);
	});

</script>

<div class='cover-picture'>
	<img
		alt=''
		id='cover-picture'
		src={cover_picture_src}
		on:error={() => cover_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/cover_picture'}
	>
</div>

<div class='profile-picture'>
	<img
		alt=''
		id='profile-picture'
		src={profile_picture_src}
		on:error={() => profile_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/profile_picture'}
	>
</div>

<div class='card'>

	<h1>{user.username}</h1>

	{#if user.role == 'creator'}

		<p class='title'>{info.bio}</p>

		<p>{info.country_of_residence}</p>

		<div class='social-media-links'>

			{#if info.social_media_links.facebook}
				<a class='social-link' href={info.social_media_links.facebook}>
					<i class="fa fa-facebook"></i>
				</a>
			{/if}

			{#if info.social_media_links.instagram}
				<a class='social-link' href={info.social_media_links.instagram}>
					<i class="fa fa-instagram"></i>
				</a>
			{/if}

			{#if info.social_media_links.webtoon}
				<a class='social-link' href={info.social_media_links.webtoon}>
					<img alt="" id='webtoon' src='https://cdn4.iconfinder.com/data/icons/logos-brands-5/24/linewebtoon-512.png'>
				</a>
			{/if}

			{#if info.social_media_links.twitter}
				<a class='social-link' href={info.social_media_links.twitter}>
					<i class="fa fa-twitter"></i>
				</a>
			{/if}

			{#if info.social_media_links.youtube}
				<a class='social-link' href={info.social_media_links.youtube}>
					<i class="fa fa-youtube"></i>
				</a>
			{/if}

			{#if info.social_media_links.twitch}
				<a class='social-link' href={info.social_media_links.twitch}>
					<i class="fa fa-twitch"></i>
				</a>
			{/if}

		</div>

	{/if}

	{#if is_following}
		<button class='follow-button' on:click={async () => is_following = await unfollowUser(user.username)}>Unfollow</button>
	{:else}
		<button class='follow-button' on:click={async () => is_following = await followUser(user.username)}>Follow</button>
	{/if}

	{#if user.role == 'creator'}

		<UserTiers user={user} tiers={tiers} subscribedTierId={subscribedTierId} />

		<div id="menu">

			<div class='my-feed-div'>
				<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'posts')}>Posts</div>
			</div>

			<div class='my-feed-div'>
				<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'giveaways')}>Giveaways</div>
			</div>

			<div class='my-feed-div'>
				<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'surveys')}>Surveys</div>
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

	.cover-picture {
		left: 0;
		top: 3.8em;
		width: 100%;
		height: 45%;
		position: absolute;
	}

	#cover-picture {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.profile-picture {
		top: -1.5em;
		max-width: 180px;
		max-height: 180px;
		position: relative;
		margin: 25em auto 0;
	}

	#profile-picture {
		width: 175px;
		height: 175px;
		object-fit: cover;
		border-radius: 50%;
		border: 4px solid #fff;
	}

	.card {
		margin: auto;
		max-width: 60em;
		position: relative;
		text-align: center;
		font-family: arial;
	}

	.title {
		color: grey;
		margin: 0 auto;
		font-size: 18px;
		max-width: 400px;
	}

	.social-media-links {
		margin: 2em 0;
	}

	#webtoon {
		width: 20px;
	}

	.social-link {
		color: black;
		margin: 0 5px;
		font-size: 22px;
		text-decoration: none;
	}

	.social-link:hover {
		opacity: 0.8;
		cursor: pointer;
	}

	.follow-button {
		width: 8em;
		color: white;
		border: none;
		font-size: 18px;
		margin-bottom: 1em;
		border-radius: 50px;
		background-color: #0f1930;
	}

	.follow-button:hover {
		cursor: pointer;
		background-color: #1f2940;
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