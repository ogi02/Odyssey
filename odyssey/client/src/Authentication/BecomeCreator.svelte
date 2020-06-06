<script>
	// Library imports
	import router from 'page';
	import { onMount } from 'svelte';

	// Component imports
	import Countries from '../Helpers/Countries.svelte';

	// Javascript imports 
	import { fetchPost } from '../js/fetch.js';
	import { isCreator } from '../js/stores.js';
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
	let userIsCreator;

	onMount(() => {
		isCreator.subscribe(value => {
			userIsCreator = value;
		});

		if(userIsCreator) {
			cancelBecomingCreator();
		}
	});

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
		router.redirect('/profile');
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

			<textarea class='textarea' id='bio' placeholder='About' maxlength='1500' cols='40' rows='5'
				bind:value={result.bio}></textarea>

			<div class='buttons'>

				<button class='pink' type='submit' on:click|preventDefault={() => cancelBecomingCreator()}>Cancel</button>

				<button class='blue' type='submit' on:click|preventDefault={async () => nextPart()}>Next</button>

			</div>
			
		{:else if part == 1}
			
			<h3>What do you do?</h3>
			<p>This will make it easier for people to find you. You can select multiple content types if you feel like it.</p>

			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Podcaster"}>  Podcaster<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Video Creator"}>  Video Creator<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Musician"}>  Musician<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Visual Artist"}>  Visual Artist<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Writer/Journalis"}>  Writer/Journalist<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Gaming Creator"}>  Gaming Creator<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Nonprofit"}>  Nonprofit Organization<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Local Bussiness"}>  Local Bussiness<br>
			<input type="checkbox" class='chk' bind:group={result.content_type} value={"Other"}>  Other<br>

			<div class='buttons'>

				<button class='pink' type='submit' on:click|preventDefault={() => previousPart()}>Previous</button>

				<button class='blue' type='submit' on:click|preventDefault={async () => nextPart()}>Next</button>

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

			<div class='buttons'>

				<button class='pink' type='submit' on:click|preventDefault={() => previousPart()}>Previous</button>

				<button class='blue' type='submit' on:click|preventDefault={async () => nextPart()}>Next</button>

			</div>
		
		{:else}

			<h3>How can people find you on other social media?</h3>
			<p>You can link your accounts on other platforms, so that your followers can see more about you and your creations. You can provide as many accounts to other platforms as you like.</p>

			<input type='text' class='input' id='facebook' placeholder='Facebook'
				bind:value={result.facebook}>

			<input type='text' class='input' id='twitter' placeholder='Twitter'
				bind:value={result.twitter}>

			<input type='text' class='input' id='instagram' placeholder='Instagram'
				bind:value={result.instagram}>

			<input type='text' class='input' id='webtoon' placeholder='Webtoon'
				bind:value={result.webtoon}>

			<input type='text' class='input' id='twitch' placeholder='Twitch'
				bind:value={result.twitch}>

			<input type='text' class='input' id='youtube' placeholder='Youtube'
				bind:value={result.youtube}>

			<div class='buttons'>

				<button class='pink' type='submit' on:click|preventDefault={() => previousPart()}>Previous</button>

				<button class='blue' type='submit' on:click|preventDefault={async () => becomeCreator(result)}>Finish</button>

			</div>

		{/if}

	</form>

</div>

<link href='https://fonts.googleapis.com/css?family=Jost' rel='stylesheet'>

<style>

	.form {
		display: block;
		font-size: 1.1em;
		max-width: 400px;
		margin: 100px auto;
		text-align: center;
		font-family: "Jost";
	}

	.input {
		display: block;
		margin: 10px auto;
	}

	.chk:hover {
		cursor: pointer;
	}

	button {
		width: 300px;
		border-radius: 5px;
	}

	.buttons {
		width: 300px;
		display: flex;
		margin: 15px auto 0;
	}

	.pink {
		color: #0f1931;
		font-weight: bold;
		margin-right: 5px;
		background-color: #e6afcc;
	}

	.pink:hover {
		cursor: pointer;
		background-color: #eca1c9;
	}

	.blue {
		color: #0f1931;
		font-weight: bold;
		margin-left: 5px;
		background-color: #9fcdf5;
	}

	.blue:hover {
		cursor: pointer;
		background-color: #8cc2f2;
	}

</style>