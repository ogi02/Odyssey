<script>
	// Library imports
	import { onMount } from 'svelte';

	// Component imports
	import ChangePic from './ChangePic.svelte';
	import EditProfile from './EditProfile.svelte';

	// Javascript imports
	import { fetchGet } from '../fetch.js';
	
	// Local variables
	let profile_picture_src = '';
	let cover_picture_src = '';
	let type_of_change = '';

	let user = {};
	let info = {};
	let social_media_links = {};
	let shipping_info = {};

	let change = false;
	
	onMount(async() => {
		// Get users profile and set variables
		const response = await fetchGet("/profile");
		user = response.user;
		info = response.info;
		if(info != null) {
			social_media_links = response.info.social_media_links;
			shipping_info = response.info.shipping_info;
		}
		// Time is put for easier reactive update if the user uploads a new picture
		profile_picture_src = 'images/' + user.username + '/profile_picture?t=' + new Date().getTime();
		cover_picture_src = 'images/' + user.username + '/cover_picture?t=' + new Date().getTime();
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

{:else}

	<img src={cover_picture_src} id="cover_picture">

	<div class="card">
		
		<div class='profile_pic'>
			
			<img src={profile_picture_src} id="profile_picture">

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

		<p><button>Follow</button></p>

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
	top: 3.5em; 
	left: 0; 
	min-width: 100%; 
	width: 100%; 
	height: 45%; 
	min-height: 300px; 
	object-fit: cover;
}

</style>