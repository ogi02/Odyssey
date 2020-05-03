<script>
	// Library imports
	import { onMount } from 'svelte';

	// Component imports
	import ChangePic from './ChangePic.svelte';
	import CreateTier from './CreateTier.svelte';
	import EditProfile from './EditProfile.svelte';
	import CreatePost from '../Posts/CreatePost.svelte';
	import CreateSurvey from '../Surveys/CreateSurvey.svelte';

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
	let social_media_links = {};
	let shipping_info = {};

	let change = false;
	let addTierFlag = false;
	let createPostFlag = false;
	let createSurveyFlag = false;
	
	onMount(async() => {
		// Get users profile and set variables
		const response = await fetchGet("http://localhost:3000/profile");
		
		user = response.user;

		if(user.is_creator) {
			info = response.info;
			tiers = response.tiers;
			posts = response.posts;
			surveys = response.surveys;
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

{:else if addTierFlag && user.is_creator}

	<CreateTier
		bind:addTierFlag={addTierFlag}
	/>

{:else if createPostFlag && user.is_creator}

	<CreatePost
		bind:createPostFlag={createPostFlag}
		tiers={tiers}
	/>

{:else if createSurveyFlag && user.is_creator}

	<CreateSurvey
		bind:createSurveyFlag={createSurveyFlag}
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

		{#if user.is_creator}
			<div class='toggle' on:click={toggleAddTier}>Add Tier</div>
			<div class='toggle' on:click={toggleCreatePost}>Create Post</div>
			<div class='toggle' on:click={toggleCreateSurvey}>Create Survey</div>
		{/if}

		{#each tiers as tier}

			<div class='tier-box'>
			
				<h3>{tier.name}</h3>
				<h4>${tier.price}</h4>
				<p style="color: #666">PER MONTH</p>
			
				<h4>Benefits</h4>

				<ul>
				
					{#each tier.benefits as benefit} 
						
						<li class='benefits'>{benefit}</li>
					
					{/each}

				</ul>

			</div>

		{/each}

		{#each posts as post}
			
			<div class='post-box'>

				<h3>{post.text}</h3>

				<img class="post-image" src={"/images/" + user.username + "/" + post.image_path}>
				
			</div>

		{/each}
		{#each surveys as survey}
			
			<div class='post-box'>

				<h3>{survey.text}</h3>

				<img class="post-image" src={"/images/" + user.username + "/" + survey.image_path}>

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
					<p>{survey.winner}</p>
				{/if}
			</div>

		{/each}

	</div>

{/if}
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

.tier-box, .post-box {
	border: 1px solid #444;
}

.post-image {
	width: 200px;
	height: auto;
}

.benefits {
	text-align: left;
}

</style>