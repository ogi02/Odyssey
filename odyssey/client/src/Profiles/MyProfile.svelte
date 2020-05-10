<script>
	// Library imports
	import { onMount } from 'svelte';

	// Component imports
	import ChangePic from './ChangePic.svelte';
	import EditProfile from './EditProfile.svelte';

	import CreateTier from '../Tiers/CreateTier.svelte';
	import CreatePost from '../Posts/CreatePost.svelte';
	import CreateSurvey from '../Surveys/CreateSurvey.svelte';
	import CreateGiveaway from '../Giveaways/CreateGiveaway.svelte';

	import MyTiers from '../Tiers/MyTiers.svelte';
	import MyPosts from '../Posts/MyPosts.svelte';
	import MySurveys from '../Surveys/MySurveys.svelte';
	import MyGiveaways from '../Giveaways/MyGiveaways.svelte';

	// Javascript imports
	import { fetchGet, fetchPost } from '../js/fetch.js';
	
	// Local variables
	let profile_picture_src = '';
	let cover_picture_src = '';

	let user = {};
	let info = {};
	let tiers = [];
	let posts = [];
	let surveys = [];
	let giveaways = [];	
	let shipping_info = {};
	let social_media_links = {};

	let addTierFlag = false;
	let createPostFlag = false;
	let createSurveyFlag = false;
	let createGiveawayFlag = false;

	let picture_type = '';
	let changePictureFlag = false;
	let editProfileInfoFlag = false;

	let type_of_display = 'posts';
	
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
		changePictureFlag = true;
		picture_type = 'profile';
	}

	// Trigger change of cover picture
	function toggleChangeCoverPic() {
		changePictureFlag = true;
		picture_type = 'cover';
	}

	// Trigger edit profile
	function toggleEditProfile() {
		editProfileInfoFlag = true;
	}

	// Trigger add tier
	function toggleAddTier() {
		addTierFlag = true;
	}

	// Trigger create survey
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

</script>

{#if changePictureFlag && picture_type == 'profile'}

	<ChangePic
		bind:change={changePictureFlag}
		bind:src={profile_picture_src}
		username={user.username}
		bind:type={picture_type}
	/>

{:else if changePictureFlag && picture_type == 'cover'}

	<ChangePic
		bind:change={changePictureFlag}
		bind:src={cover_picture_src}
		username={user.username}
		bind:type={picture_type}
	/>

{:else if editProfileInfoFlag}

	<EditProfile bind:change={editProfileInfoFlag} />

{:else if addTierFlag && user.role == "creator"}

	<CreateTier bind:addTierFlag={addTierFlag} />

{:else if createPostFlag && user.role == "creator"}

	<CreatePost bind:createPostFlag={createPostFlag} tiers={tiers} />

{:else if createSurveyFlag && user.role == "creator"}

	<CreateSurvey bind:createSurveyFlag={createSurveyFlag} tiers={tiers} />

{:else if createGiveawayFlag && user.role == "creator"}

	<CreateGiveaway bind:createGiveawayFlag={createGiveawayFlag} tiers={tiers} />

{:else}

	<img src={cover_picture_src} id="cover_picture" on:error={
		() => cover_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/cover_picture?t=' + new Date().getTime()
	}>

	<div class="card">
		
		<div class='profile_pic'>

			<img src={profile_picture_src} id="profile_picture" on:error={
				() => profile_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/profile_picture?t=' + new Date().getTime()
			}>

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

			<MyTiers bind:tiers={tiers}/>

			<div class='toggle' on:click={toggleAddTier}>Add Tier</div>
			<div class='toggle' on:click={toggleCreatePost}>Create Post</div>
			<div class='toggle' on:click={toggleCreateSurvey}>Create Survey</div>
			<div class='toggle' on:click={toggleCreateGiveaway}>Create Giveaway</div>

			<ul id="menu">
				<li><button on:click|preventDefault={() => (type_of_display = 'posts')}>Posts</button></li>
				<li><button on:click|preventDefault={() => (type_of_display = 'surveys')}>Surveys</button></li>
				<li><button on:click|preventDefault={() => (type_of_display = 'giveaways')}>Giveaways</button><li>
			</ul>

			{#if type_of_display == 'posts'}

				<MyPosts bind:posts={posts} user={user} />

			{:else if type_of_display == 'surveys'}

				<MySurveys bind:surveys={surveys} user={user} />

			<!-- {:else if type_of_display == 'giveaways'} -->
			{:else}

				<MyGiveaways bind:giveaways={giveaways} user={user} />

			{/if}

		{/if}

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

	li {
		margin: 0.4em;
	}

	ul#menu {
		list-style-type: none;
	}

	ul#menu li {
		display: inline;
	}

</style>