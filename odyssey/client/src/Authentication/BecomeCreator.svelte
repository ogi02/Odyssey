<script>
	// Library imports
	import page from "page.js"

	// Component imports
	import Countries from '../Helpers/Countries.svelte';

	// Javascript imports
	import { fetchPost } from '../fetch.js';
	import { becomeCreator } from './authentication_management.js';

	// Local Variables
	let result = {
		country_of_residence: '',
		bio: '',
		working_on: '',
		full_name: '',
		phone_number: '',
		country_for_shipping: '',
		state: '',
		city: '',
		address: '',
		suite: '',
		postal_code: '',
		facebook: '',
		twitter: '',
		instagram: '',
		webtoon: '',
		twitch: '',
		youtube: '',
		content_type: []
	}

	let part = 0;

	// Show next part of the form
	function nextPart() {
		part += 1;
	}

	// Show previous part of the form
	function previousPart() {
		part -= 1;
	}

	// Cancel button onclick
	function cancelBecomingCreator() {
		page.redirect('/profile');
	}

</script>

<div class='header'>
	<h2>Become a Creator</h2>
</div>

<div class='form'>
	
	<form autocomplete='off'>
		
		{#if part == 0}
			
			<h3>Who are you?</h3>
			<p>The information you provide will help people know more about their favourite creator, but you can leave it empty if you like.</p>

			<input type='text' class='input' id='working_on' placeholder='Creator of ...'
				bind:value={result.working_on}>

			<input class='input' list='countries' name='country_of_residence' placeholder='Country'
				bind:value={result.country_of_residence}>

			<datalist id='countries'>
				<Countries />
			</datalist>

			<textarea class='input' id='bio' placeholder='About' maxlength='1500'
				bind:value={result.bio}></textarea>

			<div class='part_buttons red' on:click={cancelBecomingCreator}>
				<h4>Cancel</h4>
			</div>

			<div class='part_buttons green' on:click={nextPart}>
				<h4>Next</h4>
			</div>
			
		{:else if part == 1}
			
			<h3>What do you do?</h3>
			<p>This will make it easier for people to find you. You can select multiple content types if you feel like it.</p>

			<input type="checkbox" bind:group={result.content_type} value={"Podcaster"}>Podcaster<br>
			<input type="checkbox" bind:group={result.content_type} value={"Video Creator"}>Video Creator<br>
			<input type="checkbox" bind:group={result.content_type} value={"Musician"}>Musician<br>
			<input type="checkbox" bind:group={result.content_type} value={"Visual Artist"}>Visual Artist<br>
			<input type="checkbox" bind:group={result.content_type} value={"Writer/Journalis"}>Writer/Journalist<br>
			<input type="checkbox" bind:group={result.content_type} value={"Gaming Creator"}>Gaming Creator<br>
			<input type="checkbox" bind:group={result.content_type} value={"Nonprofit"}>Nonprofit Organization<br>
			<input type="checkbox" bind:group={result.content_type} value={"Local Bussiness"}>Local Bussiness<br>
			<input type="checkbox" bind:group={result.content_type} value={"Other"}>Other<br>

			<div class='part_buttons red' on:click={previousPart}>
				<h4>Previous</h4>
			</div>

			<div class='part_buttons green' on:click={nextPart}>
				<h4>Next</h4>
			</div>
		
		{:else if part == 2}

			<h3>How can you receive gifts?</h3>
			<p>This will make it possible for people to send you gifts of any kind. It is entirely optional so you can leave it empty if you like.</p>

			<input type='text' class='input' id='full_name' placeholder='Full Name'
				bind:value={result.full_name}>

			<input type='text' class='input' id='phone_number' placeholder='Phone Number'
				bind:value={result.phone_number}>

			<input class='input' list='shipping_country' placeholder='Country for shipping'
				bind:value={result.country_for_shipping}>
			<datalist id='shipping_country'>
				<Countries />
			</datalist>

			<input type='text' class='input' id='state' placeholder='State / Province'
				bind:value={result.state}>

			<input type='text' class='input' id='city' placeholder='City'
				bind:value={result.city}>

			<input type='text' class='input' id='address' placeholder='Address'
				bind:value={result.address}>

			<input type='text' class='input' id='suite' placeholder='Suite'
				bind:value={result.suite}>

			<input type='text' class='input' id='postal_code' placeholder='Postal Code'
				bind:value={result.postal_code}>

			<div class='part_buttons red' on:click={previousPart}>
				<h4>Previous</h4>
			</div>

			<div class='part_buttons green' on:click={nextPart}>
				<h4>Next</h4>
			</div>
		
		{:else}

			<h3>How can people find you on other social media?</h3>
			<p>You can link your accounts on other platforms, so that your followers can see more about you and your creations. You can provide as many accounts to other platforms as you like.</p>

			<input type='text' class='input social' id='facebook' placeholder='Facebook'
				bind:value={result.facebook}>

			<input type='text' class='input social' id='twitter' placeholder='Twitter'
				bind:value={result.twitter}>

			<input type='text' class='input social' id='instagram' placeholder='Instagram'
				bind:value={result.instagram}>

			<input type='text' class='input social' id='webtoon' placeholder='Webtoon'
				bind:value={result.webtoon}>

			<input type='text' class='input social' id='twitch' placeholder='Twitch'
				bind:value={result.twitch}>

			<input type='text' class='input social' id='youtube' placeholder='Youtube'
				bind:value={result.youtube}>

			<div class='part_buttons red' on:click={previousPart}>
				<h4>Previous</h4>
			</div>

			<div class='part_buttons green' on:click={() => becomeCreator(result)}>
				<h4>Finish</h4>
			</div>
		
		{/if}

	</form>
	
</div>

<style>

	.part_buttons {
		text-align: center;
		min-width: 100px;
		padding: 10px;
		border: 1px solid #111;
		margin: 5px;
		display: inline-block;
	}

	.part_buttons:hover {
		cursor: pointer;
	}

	.part_buttons h4 {
		margin: 0;
	}

	.red {
		background-color: #ff6347;
	}

	.red:hover {
		background-color: #ff4327;
	}

	.green {
		background-color: #63ff47;
	}

	.green:hover {
		background-color: #43ff27;
	}

	.input {
		display: block;
	}
	
	#about {
		width: 450px;
		height: 300px;
	}

</style>