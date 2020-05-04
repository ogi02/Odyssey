<script>
	// Library imports
	import { onMount } from 'svelte';

	// Component imports
	import ChangePic from './ChangePic.svelte';
	import CreateTier from './CreateTier.svelte';
	import EditProfile from './EditProfile.svelte';
	import CreatePost from '../Posts/CreatePost.svelte';
	import CreateSurvey from '../Surveys/CreateSurvey.svelte';
	import CreateGiveaway from '../Giveaways/CreateGiveaway.svelte';

	// Javascript imports
	import { fetchGet, fetchPost } from '../js/fetch.js';
	
	// Local variables
	let profile_picture_src = '';
	let cover_picture_src = '';
	let type_of_change = '';

	let user = {};
	let info = {};
	let tiers = [];
	let posts = [];
	let surveys = [];
	let giveaways = [];	
	let shipping_info = {};
	let social_media_links = {};

	let change = false;
	let addTierFlag = false;
	let createPostFlag = false;
	let createSurveyFlag = false;
	let createGiveawayFlag = false;
	
	onMount(async() => {
		// Get users profile and set variables
		const response = await fetchGet("http://localhost:3000/profile");
		
		user = response.user;

		if(user.role == "creator") {
			info = response.info;
			tiers = response.tiers;
			posts = response.posts;
			surveys = response.surveys;
			giveaways = response.giveaways;
			shipping_info = response.info.shipping_info;
			social_media_links = response.info.social_media_links;
		}
		
		// Time is put for easier reactive update if the user uploads a new picture
		profile_picture_src = '/images/' + user.username + '/profile_picture?t=' + new Date().getTime();
		cover_picture_src = '/images/' + user.username + '/cover_picture?t=' + new Date().getTime();
	});

	// Trigger change of profile picture
	function toggleChangeProfilePic() {
		type_of_change = 'profile';
		change = true;
	}

	// Trigger change of cover picture
	function toggleChangeCoverPic() {
		type_of_change = 'cover';
		change = true;
	}

	// Trigger edit profile
	function toggleEditProfile() {
		type_of_change = 'profile_info';
		change = true;
	}

	// Trigger add tier
	function toggleAddTier() {
		addTierFlag = true;
	}

	// Trigger create post
	function toggleCreatePost() {
		createPostFlag = true;
	}

	// Trigger create survey
	function toggleCreateSurvey() {
		createSurveyFlag = true;
	}

	// Trigger create giveaway	
	function toggleCreateGiveaway() {	
		createGiveawayFlag = true;	
	}

	// Close survey
	async function closeSurvey(survey_id) {
		const response = await fetchPost('http://localhost:3000/closeSurvey', {
			survey_id: survey_id
		});

		surveys.find(survey => survey._id.$oid === survey_id).is_open = false;
		surveys = surveys;
	}

	//Set winner
	async function electWinner(survey_id) {
		const response = await fetchPost('http://localhost:3000/chooseWinningOption', {
			survey_id: survey_id
		});

		surveys.find(survey => survey._id.$oid === survey_id).winner = response.winner;
		surveys = surveys;
	}

	// Get voted per option
	async function getVotesPerOption(survey_id, option_id) {
		const response = await fetchPost('http://localhost:3000/voteCountByOption', {
			survey_id: survey_id,
			option_id: option_id
		});

		let temp = response.vote_count;

		return temp;
	}

	// Get likes on post
	async function getLikesOnPost(post_id) {
		const response = await fetchPost('http://localhost:3000/getLikeCount', {
			post_id: post_id
		});

		let temp = response.like_count;

		return temp;
	}

	// Close giveaway	
	async function closeGiveaway(giveaway_id) {	
		const response = await fetchPost('http://localhost:3000/closeGiveaway', {	
			giveaway_id: giveaway_id	
		});	
		giveaways.find(giveaway => giveaway._id.$oid === giveaway_id).is_open = false;	
		giveaways = giveaways;	
	}	

	// Generate random giveaway winner	
	async function pickRandomGiveawayWinner(giveaway_id) {	
		const response = await fetchPost('http://localhost:3000/generateRandomWinner', {	
			giveaway_id: giveaway_id	
		});	
		let temp = response.winner_id;	
		return temp;	
	}

	// Select giveaway winner	
	async function chooseGiveawayWinner(giveaway_id, winner_id) {	
		const response = await fetchPost('http://localhost:3000/chooseGiveawayWinner', {	
			winner_id: winner_id,	
			giveaway_id: giveaway_id	
		});	
		giveaways.find(giveaway => giveaway._id.$oid === giveaway_id).winner = response.winner;	
		giveaways = giveaways;	
	}

	// Get participants in giveaway	
	async function getParticipantCount(giveaway_id) {	
		const response = await fetchPost('http://localhost:3000/getTotalContestantsCount', {	
			giveaway_id: giveaway_id,	
		});	
		let temp = response.participant_count;	
		return temp;	
	}	


</script>
{#if change}
	
	{#if type_of_change == 'profile'} 
		
		<ChangePic 
			bind:change={change} 
			bind:src={profile_picture_src} 
			username={user.username} 
			bind:type={type_of_change}
		/>

	{:else if type_of_change == 'cover'}
		
		<ChangePic 
			bind:change={change} 
			bind:src={cover_picture_src} 
			username={user.username} 
			bind:type={type_of_change}
		/>

	{:else}

		<EditProfile
			bind:change={change} 
		/>

	{/if}

{:else if addTierFlag && user.role == "creator"}

	<CreateTier
		bind:addTierFlag={addTierFlag}
	/>

{:else if createPostFlag && user.role == "creator"}

	<CreatePost
		bind:createPostFlag={createPostFlag}
		tiers={tiers}
	/>

{:else if createSurveyFlag && user.role == "creator"}

	<CreateSurvey
		bind:createSurveyFlag={createSurveyFlag}
		tiers={tiers}
	/>	

{:else if createGiveawayFlag && user.role == "creator"}	
	<CreateGiveaway	
		bind:createGiveawayFlag={createGiveawayFlag}	
		tiers={tiers}	
	/>

{:else}

	<img src={cover_picture_src} id="cover_picture" on:error={
		() => cover_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/cover_picture?t=' + new Date().getTime()
	}>

	<div class="card">
		
		<div class='profile_pic'>
			
			<img src={profile_picture_src} id="profile_picture" on:error={() => profile_picture_src = 
				'/images/_FpCerpd9Z7SIbjmN81Jy/profile_picture?t=' + new Date().getTime()}>

			<div class='toggle' on:click={toggleChangeProfilePic}>Change Profile Pic</div>
			<div class='toggle' on:click={toggleChangeCoverPic}>Change Cover Pic</div>
			<div class='toggle' on:click={toggleEditProfile}>Edit Profile</div>
			
		</div>

		<h1>{user.username}</h1>

		<p class="title">{(info == null) ? "" : info.bio}</p>

		<p>{(info == null) ? "" : info.country_of_residence}</p>

		<div style="margin: 24px 0;">
			<a href="#"><i class="fa fa-twitch"></i></a> 
			<a href="#"><i class="fa fa-twitter"></i></a>  
			<a href="#"><img src="https://cdn4.iconfinder.com/data/icons/logos-brands-5/24/linewebtoon-512.png" style="width: 7%"></a> 
			<a href="#"><i class="fa fa-facebook"></i></a> 
			<a href="#"><i class="fa fa-youtube"></i></a> 
		</div>

		{#if user.role == "creator"}
			<div class='toggle' on:click={toggleAddTier}>Add Tier</div>
			<div class='toggle' on:click={toggleCreatePost}>Create Post</div>
			<div class='toggle' on:click={toggleCreateSurvey}>Create Survey</div>
			<div class='toggle' on:click={toggleCreateGiveaway}>Create Giveaway</div>
		{/if}

		<div class="tiers-container">
			{#each tiers as tier}
				<div class='tier-box'>
					
					<h3 class="tier-name">{tier.name}</h3>
					<p class="tier-price">${tier.price}</p>
					<p class="tier-price-per-month">PER MONTH</p>
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

				<div class='post-box'>
					<img class="post-image" src={"/images/" + user.username + "/" + post.image_path}>
					<div class="text-container">
						<h3>{post.text}</h3>
						{#await getLikesOnPost(post._id.$oid, i) then like_count}
							<p><i class="fa fa-heart" aria-hidden="true"></i>  {like_count || 0}</p>
						{/await}
					</div>
				</div>

			{/each}
		</div>

		<div class="posts-container">
			{#each surveys as survey}
				
				<div class='post-box'>

					<img class="post-image" src={"/images/" + user.username + "/" + survey.image_path}>

					<div class="text-container">
						<h3>{survey.text}</h3>
					</div>
					{#if survey.is_open == true}
						{#each survey.options as option, i}
							<p>{option}</p>
							{#await getVotesPerOption(survey._id.$oid, i) then vote_count}
								<p>{vote_count || 0}</p>
							{/await}
									
						{/each}
						<button on:click={async () => {
							await closeSurvey(survey._id.$oid);
							await electWinner(survey._id.$oid);
						}}>Close</button>

					{:else}
						<p>Winning option: {survey.winner}</p>
					{/if}
				</div>

			{/each}
		</div>
		<div class="posts-container">
			{#each giveaways as giveaway}	
					
				<div class='post-box'>	
					<img class="post-image" src={"/images/" + user.username + "/" + giveaway.image_path}>	
					<div class="text-container">
						<h3>{giveaway.text}</h3>	
					</div>
					{#if giveaway.is_open == true}	
							
						<p>Number of contestants: </p>	
						{#await getParticipantCount(giveaway._id.$oid) then participants}	
							<p>{participants || 0}</p>	
							{#if participants}	
								<button on:click={async () => {	
									await closeGiveaway(giveaway._id.$oid);	
									let winner_id = await pickRandomGiveawayWinner(giveaway._id.$oid);	
									await chooseGiveawayWinner(giveaway._id.$oid, winner_id);	
								}}>Generate Winner</button>	
							{/if}	
						{/await}	
					{:else}	
						<p>{giveaway.winner}</p>	
					{/if}	
				</div>	
			{/each}
		</div>

	</div>

{/if}
<link href='https://fonts.googleapis.com/css?family=Calistoga' rel='stylesheet'>
<style>
	
.card {
	position: relative;
	max-width: 300px;
	margin: auto;
	margin-top: 33vh;
	text-align: center;
	font-family: arial;
}

.title {
	color: grey;
	font-size: 18px;
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
	max-width: 30em;	
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