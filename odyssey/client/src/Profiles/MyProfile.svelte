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
	import { isCreator } from '../js/stores.js';
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
		const response = await fetchGet("/profile");
		
		user = response.user;
		isCreator.set(false);

		if(user.role == "creator") {
			isCreator.set(true);
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

	<div class='cover-picture'>
		<img
			alt=''
			id='cover-picture'
			src={cover_picture_src}
			on:click={toggleChangeCoverPic}
			on:error={() => cover_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/cover_picture?t=' + new Date().getTime()}
		>
		<img
			alt=''
			id='change-cover-picture'
			src={'/images/_FpCerpd9Z7SIbjmN81Jy/camera_icon.png'}
		>
	</div>

	<div class='profile-picture'>
		<img
			alt=''
			id='profile-picture'
			src={profile_picture_src}
			on:click={toggleChangeProfilePic}
			on:error={() => profile_picture_src = '/images/_FpCerpd9Z7SIbjmN81Jy/profile_picture?t=' + new Date().getTime()}
		>
		<img
			alt=''
			id='change-profile-picture'
			src={'/images/_FpCerpd9Z7SIbjmN81Jy/camera_icon.png'}
		>
	</div>

	<div class="card">

		<button class='edit-profile-button' on:click={toggleEditProfile}>
			Edit Profile <i class='fa fa-cog edit-profile-icon' aria-hidden='true'></i>
		</button>


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

			<button class='add-tier-button' on:click={toggleAddTier}>
				Add Tier <i class='fa fa-plus add-tier-icon' aria-hidden='true'></i>
			</button>

			<MyTiers bind:tiers={tiers}/>
			
			<div id='menu'>

				<div class='my-feed-div'>
					<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'posts')}>Posts</div>
					<i class='fa fa-plus-square create-event-icon' on:click={toggleCreatePost}></i>
				</div>

				<div class='my-feed-div'>
					<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'giveaways')}>Giveaways</div>
					<i class='fa fa-plus-square create-event-icon' on:click={toggleCreateGiveaway}></i>
				</div>

				<div class='my-feed-div'>
					<div class='my-feed-button' on:click|preventDefault={() => (type_of_display = 'surveys')}>Surveys</div>
					<i class='fa fa-plus-square create-event-icon' on:click={toggleCreateSurvey}></i>
				</div>

			</div>

			{#if type_of_display == 'posts'}

				<MyPosts bind:posts={posts} user={user} />

			{:else if type_of_display == 'surveys'}

				<MySurveys bind:surveys={surveys} user={user} />

			{:else}

				<MyGiveaways bind:giveaways={giveaways} user={user} />

			{/if}

		{/if}

	</div>

{/if}

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

	#cover-picture:hover {
		opacity: 0.5;
	}

	#change-cover-picture {
		top: 10em;
		left: 50%;
		height: 25%;
		z-index: -1;
		position: absolute;
		transform: translate(-50%, -50%);
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

	#profile-picture:hover {
		opacity: 0.5;
	}

	#change-profile-picture {
		top: 7em;
		left: 50%;
		height: 25%;
		z-index: -1;
		position: absolute;
		transform: translate(-50%, -50%);
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

	.add-tier-button, .edit-profile-button {
		width: 8em;
		border: none;
		color: white;
		padding: 0.4em;
		font-size: 18px;
		border-radius: 30px;
		background-color: #080d52;
	}

	.add-tier-button:hover, .edit-profile-button:hover {
		opacity: 0.8;
		cursor: pointer;
	}

	.add-tier-icon, .edit-profile-icon {
		margin-left: 3px;
		vertical-align: text-bottom;
	}

	#menu {
		display: flex;
		color: #080d52;
		margin: 0 auto;
		margin-top: 1em;
		max-width: 800px;
		font-size: 1.5em;
		background: linear-gradient(90deg,
			rgba(252,252,252,1) 2%,
			rgba(148,187,233,1) 18%,
			rgba(238,174,202,1) 76%,
			rgba(255,255,255,1) 96%);
	}

	.my-feed-div {
		flex: 1 1 auto;
		display: inline;
		padding: 0.5em 0;
	}

	.my-feed-button {
		display: inline;
	}

	.my-feed-button:hover {
		opacity: 0.7;
		cursor: pointer;
	}

	.create-event-icon:hover {
		opacity: 0.7;
		color: #2d0a65;
		cursor: pointer;
	}

</style>