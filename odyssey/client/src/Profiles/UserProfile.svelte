<script>
	// Library imports
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { username } from '../js/stores.js';
	import { followUser, unfollowUser, isFollowing } from './profile_management.js';

	// Inherited variables
	// export const params;

	// Local variables
	let cover_picture_src = '';
	let profile_picture_src = '';
	
	let is_following = false;
	
	let user = {};
	let info = {};
	let tiers = {};
	let is_creator;
	let subscribedTierId;
	
	let result = {};

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

		is_creator = user.is_creator;

		if(is_creator) {
			info = response.info;
			tiers = response.tiers;
		}

		result = {
			profile_name: user.username
		};

		is_following = await isFollowing(result);
	});

	async function chooseTier(self_id) {
		result = {
			tier_id: self_id,
			creator_id: user._id.$oid
		};

		subscribedTierId = self_id;

		const response = await fetchPost('http://localhost:3000/chooseTier', {
			result: result
		});
	}

	async function removeTier(self_id) {
		result = {
			tier_id: self_id,
			creator_id: user._id.$oid
		}

		subscribedTierId = null;

		const response = await fetchPost('http://localhost:3000/removeTier', {
			result: result
		});

	}



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
		<a href="#"><img src="https://cdn4.iconfinder.com/data/icons/logos-brands-5/24/linewebtoon-512.png" style="width: 7%"></a> 
		<a href="#"><i class="fa fa-facebook"></i></a> 
		<a href="#"><i class="fa fa-youtube"></i></a> 
	</div>

	{#if is_following}
		<button on:click={async () => is_following = await unfollowUser(result)}>Unfollow</button>
	{:else}
		<button on:click={async () => is_following = await followUser(result)}>Follow</button>
	{/if}

	{#if is_creator}
		{#each tiers as tier}
			<div class='tier-box'>
				
				<h3>{tier.name}</h3>
				<h4>${tier.price}</h4>
				<p style="color: #666">PER MONTH</p>

				{#if tier._id.$oid == subscribedTierId}
					<button id='{tier._id.$oid}' on:click={async () => await removeTier(tier._id.$oid)}>Remove</button>
				{:else}
					<button id='{tier._id.$oid}' on:click={async () => await chooseTier(tier._id.$oid)}>Join</button>
				{/if}
				
				<p>{tier.benefits}</p>
			</div>
		{/each}
	{/if}

</div>

<style>

	.card {
		position: relative;
		max-width: 300px;
		margin: auto;
		margin-top: 33vh;
		text-align: center;
		font-family: arial;
	}

	button {
		border: none;
		border-radius: 50px;
		outline: 0;
		display: inline-block;
		padding: 8px;
		color: white;
		background-color: #000;
		text-align: center;
		cursor: pointer;
		width: 50%;
		font-size: 18px;
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

	.tier-box {
		border: 1px solid #444;
	}

</style>