<script>
	// Library imports
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { username } from '../js/stores.js';
	import { followUser, unfollowUser, isFollowing } from './profile_management.js';

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
	
	let result = {};
	let follow_result = {};

	let loadedPosts = 0;
	let allPostsLoaded = false;

	let loadedSurveys = 0;
	let allSurveysLoaded = false;

	let loadedGiveaways = 0;	
	let allGiveawaysLoaded = false;

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
			posts.sort((a, b) => (a.date > b.date) ? 1 : -1);
		}

		follow_result = {
			profile_name: user.username
		};

		is_following = await isFollowing(follow_result);

		if (user.role == "creator") {
			await loadMorePosts();
			await loadMoreSurveys();
			await loadMoreGiveaways();

		}

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

	async function isLiked(post_id) {
		const response = await fetchPost('http://localhost:3000/hasLikedPost', {
			post_id: post_id
		});

		let temp = response.liked;

		return temp;
	}

	async function canViewPost(post_id) {
		const response = await fetchPost('http://localhost:3000/canViewPost', {
			post_id: post_id
		});

		let temp = response.view;

		return temp;
	}

	async function likePost(post_id) {
		const response = await fetchPost('http://localhost:3000/likePost', {
			post_id: post_id
		});

		posts.find(post => post._id.$oid === post_id).isLiked = true;
		posts = posts;
	}

	async function unlikePost(post_id) {
		const response = await fetchPost('http://localhost:3000/unlikePost', {
			post_id: post_id
		});

		posts.find(post => post._id.$oid === post_id).isLiked = false;
		posts = posts;
	}

	async function loadMorePosts() {
		for(let i = loadedPosts; i < loadedPosts + 10; i++) {
			if(posts.length == (loadedPosts + i)) {
				allPostsLoaded = true;
				loadedPosts += i;
				return;
			}
			posts[i].isLiked = await isLiked(posts[i]._id.$oid);
			posts[i].canView = await canViewPost(posts[i]._id.$oid);
		}
		loadedPosts += 10;
	}

	async function hasVoted(survey_id) {
		const response = await fetchPost('http://localhost:3000/hasVotedOnSurvey', {
			survey_id: survey_id
		});

		let temp = response.voted;

		return temp;
	}

	async function canViewSurvey(survey_id) {
		const response = await fetchPost('http://localhost:3000/canViewSurvey', {
			survey_id: survey_id
		});

		let temp = response.view;

		return temp;
	}

	async function voteOnSurvey(survey_id, option_id) {
		const response = await fetchPost('http://localhost:3000/voteOnSurvey', {
			survey_id: survey_id,
			option_id: option_id
		});

		surveys.find(survey => survey._id.$oid === survey_id).hasVoted = true;
		surveys = surveys;
	}

	async function getVotesPerOption(survey_id, option_id) {
		const response = await fetchPost('http://localhost:3000/voteCountByOption', {
			survey_id: survey_id,
			option_id: option_id
		});

		let temp = response.vote_count;

		return temp;
	}

	async function loadMoreSurveys() {
		for(let i = loadedSurveys; i < loadedSurveys + 10; i++) {
			if(surveys.length == (loadedSurveys + i)) {
				allSurveysLoaded = true;
				loadedSurveys += i;
				return;
			}
			surveys[i].hasVoted = await hasVoted(surveys[i]._id.$oid);
			surveys[i].canView = await canViewSurvey(surveys[i]._id.$oid);

		}
		loadedSurveys += 10;
	}

	async function canViewGiveaway(giveaway_id) {	
		const response = await fetchPost('http://localhost:3000/canViewGiveaway', {	
			giveaway_id: giveaway_id	
		});	
		let temp = response.view;	
		return temp;	
	}	
	async function hasJoined(giveaway_id) {	
		const response = await fetchPost('http://localhost:3000/hasJoinedGiveaway', {	
			giveaway_id: giveaway_id	
		});	
		let temp = response.joined;	
		return temp;	
	}	
	async function loadMoreGiveaways() {	
		for(let i = loadedGiveaways; i < loadedGiveaways + 10; i++) {	
			if(giveaways.length == (loadedGiveaways + i)) {	
				allGiveawaysLoaded = true;	
				loadedGiveaways += i;	
				return;	
			}	
			giveaways[i].hasJoined = await hasJoined(giveaways[i]._id.$oid);	
			giveaways[i].canView = await canViewGiveaway(giveaways[i]._id.$oid);	
		}	
		loadedGiveaways += 10;	
	}	
	async function joinGiveaway(giveaway_id) {	
		const response = await fetchPost('http://localhost:3000/joinGiveaway', {	
			giveaway_id: giveaway_id,	
		});	
		giveaways.find(giveaway => giveaway._id.$oid === giveaway_id).hasJoined = true;	
		giveaways = giveaways;	
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
		<a href="#"><i class="fa fa-instagram"></i></a> 
		<a href="#"><i class="fa fa-youtube"></i></a> 
		<a href="#"><i class="fa fa-facebook"></i></a> 
	</div>

	{#if is_following}
		<button class="follow-button" on:click={async () => is_following = await unfollowUser(follow_result)}>Unfollow</button>
	{:else}
		<button  class="follow-button" on:click={async () => is_following = await followUser(follow_result)}>Follow</button>
	{/if}

	{#if user.role == "creator"}
		<div class="tiers-container">
			{#each tiers as tier}
				<div class='tier-box'>
					
					<h3 class="tier-name">{tier.name}</h3>
					<p class="tier-price">${tier.price}</p>
					<p class="tier-price-per-month">PER MONTH</p>

					{#if tier._id.$oid == subscribedTierId}
						<button class="join-button" id='{tier._id.$oid}' on:click={async () => await removeTier(tier._id.$oid)}>Unsubcribe</button>
					{:else}
						<button class="join-button" id='{tier._id.$oid}' on:click={async () => await chooseTier(tier._id.$oid)}>Join</button>
					{/if}
					<ul>
						{#each tier.benefits as benefit}
							<li style="text-align: left;">{benefit}</li>
						{/each}	
					</ul>
				</div>
			{/each}
		</div>
		<div class="posts-container">
			{#each posts as post, i}
				
				{#if i < loadedPosts}
					<div class='post-box'>

						{#if post.canView}

							<img class="post-image" src={"/images/" + user.username + "/" + post.image_path}>
							<div class="text-container">
								<h3>{post.text}</h3>
								<div style="margin: 5px;">
									{#if post.isLiked}
										<i class="fa fa-heart fa-2x" aria-hidden="true" 
										on:click={async () => await unlikePost(post._id.$oid)}></i>
									{:else}
										<i class="fa fa-heart-o fa-2x" aria-hidden="true" 
										on:click={async () => await likePost(post._id.$oid)}></i>
									{/if}
								</div>
							</div>
						{:else}

							<div class="view-post-container">
								<img class="post-image-cant-view" src={"/images/" + user.username + "/" + post.image_path}>
								<p class="centered-text-over-image">You can't view this post!</p>
							</div>
							<div class="text-container">
									<h3>{post.text}</h3>
									<i class="fa fa-lock" aria-hidden="true"><span style="margin-left: 5px">Locked</span></i> 
							</div>
						{/if}
							
					</div>

				{/if}

			{/each}
		</div>

		{#if !allPostsLoaded}
			<button on:click={async () => await loadMorePosts()}>Load More</button>
		{/if}

		<div class="posts-container">
			{#each surveys as survey, i}
				
				{#if i < loadedSurveys}
					{#if survey.is_open == true}
						<div class='post-box'>
						{#if survey.canView}
							{#if survey.is_open == true}
								
									
									<img class="post-image" src={"/images/" + user.username + "/" + survey.image_path}>
									<div class="text-container">
										<h3>{survey.text}</h3>
									</div>
									{#if survey.hasVoted == false}

										{#each survey.options as option, i}
											<p>{option}</p>
											<button on:click={async () => await voteOnSurvey(survey._id.$oid, i)}>Vote</button>
										
										{/each}
									{:else}
										{#each survey.options as option, i}
											<p>{option}</p>
											{#await getVotesPerOption(survey._id.$oid, i) then vote_count}
												<p>{vote_count || 0}</p>
											{/await}
										
										{/each}
										
									{/if}
								
							{/if}

						{:else if survey.is_open == true}

							<div class="view-post-container">
									<img class="post-image-cant-view" src={"/images/" + user.username + "/" + survey.image_path}>
									<p class="centered-text-over-image">You can't view this survey!</p>
								</div>
								<div class="text-container">
										<h3>{survey.text}</h3>
										<i class="fa fa-lock" aria-hidden="true"><span style="margin-left: 5px">Locked</span></i> 
								</div>

						{/if}
						</div>
					{/if}
				{/if}

			{/each}

		</div>

		{#if !allSurveysLoaded}
			<button on:click={async () => await loadMoreSurveys()}>Load More</button>
		{/if}

		<div class="posts-container">
			{#each giveaways as giveaway, i}	
					
				{#if i < loadedGiveaways}	
					{#if giveaway.is_open == true}
						<div class='post-box'>	
							{#if giveaway.canView}	
								<img class="post-image" src={"/images/" + user.username + "/" + giveaway.image_path}>	
								<div class="text-container">
									<h3>{giveaway.text}</h3>	
								</div>
								{#if giveaway.hasJoined == false}	
									<button on:click={async () => await joinGiveaway(giveaway._id.$oid)}>Join</button>	
								{:else}	
									<p>You have already joined this giveaway!</p>	
								{/if}	
							{:else if giveaway.is_open == true}	
														<div class="view-post-container">
									<img class="post-image-cant-view" src={"/images/" + user.username + "/" + giveaway.image_path}>
									<p class="centered-text-over-image">You can't view this giveaway!</p>
								</div>
								<div class="text-container">
										<h3>{giveaway.text}</h3>
										<i class="fa fa-lock" aria-hidden="true"><span style="margin-left: 5px">Locked</span></i> 
							</div>	
							{/if}	
									
						</div>	
					{/if}
				{/if}	
			{/each}
		</div>	
		{#if !allGiveawaysLoaded}	
			<button on:click={async () => await loadMoreGiveaways()}>Load More Giveaways</button>	
		{/if}

	{/if}

</div>

<link href='https://fonts.googleapis.com/css?family=Calistoga' rel='stylesheet'>
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
		border: none;
		border-radius: 50px;
		outline: 0;
		display: inline-block;
		padding: 8px;
		color: white;
		background-color: #0f1930;
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

	.tier-box{
		border: 6px solid;
  		border-image-source: linear-gradient(#9dcff2, 	#efacca);
  		border-image-slice: 1;
  		outline: solid  2px #0f1930;
		min-width: 18em;
		max-width: 18em;	
		min-height: 23em;
		margin: 10px;

	}
	.post-box {
		border: 2px solid #0f1930;
		min-width: 40em;
		max-width: 40em;	
		min-height: 23em;
		margin: 10px;
	}

	.tier-name{
		font-size: 1.3em;
		background-color: #9dcff2;
		margin: 0;
		padding: 0.7em;
		margin-bottom: 1em;
	}

	.tier-price{
		font-size: 1.7em;
		color: black;
		padding: 0;
		margin: 0;
		font-family: "Calistoga";
		text-align: center;
	}

	.tier-price-per-month{
		font-size: 0.8em;
		color: grey;
		padding: 0.5em;
		margin: 0;
		font-weight: bold;
	}

	.post-image {
		width: 40.2em;
		padding: 2px;
		margin: -3px;
		height: 25em;
		margin-top: -4px;
	}
	.post-image-cant-view{
		filter: blur(18px) brightness(0.5);
		width: 40.2em;
		padding: 2px;
		margin: -5px -10px -10px -5px;
		height: 25em;
		margin-top: -4px;
	}

	.tiers-container{
		display: flex;
		flex-wrap: wrap;
		flex-shrink: 0;
		justify-content: center;
		
	}
	.posts-container{
		display: flex;
		margin: 4em;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}
	.text-container{
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		margin: 1em;
		align-items: center;
		justify-content: space-between;

	}

	.follow-button{
		max-width: 8em;
		margin-bottom: 3em;
	}

	.join-button{
		max-width: 8em;
		margin-top: 1em;
	}

	li{
		margin: 0.4em;
	}
	.fa-heart-o:hover{
		color: red;
	}
	.fa-heart{
		color: red;
		transition: 0.3s ease-out;
	}
	.fa-heart:hover{
		color: black;
		transition: 0.3s;
	}

	.view-post-container {
		position: relative;
		text-align: center;
		overflow: hidden;
		min-width: 10em;
		color: white;
	}

	.centered-text-over-image{
		position: absolute;
		font-weight: bold;
		font-size: 1.5em;
		top: 45%;
		left: 50%;
		transform: translate(-50%, -50%);
	}


</style>
