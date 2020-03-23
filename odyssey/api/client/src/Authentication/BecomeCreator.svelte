<script>

	import { fetchPost } from '../fetch.js';
	import Countries from '../Helpers/Countries.svelte';

	let result = {
		country: '',
		about: '',
		shipping_address: {
			full_name: '',
			phone_number: '',
			country_for_shipping: '',
			state: '',
			city: '',
			address: '',
			suite: '',
			postal_code: '',
		},
		social_media_links: {
			facebook: '',
			twitter: '',
			instagram: '',
			webtoon: '',
			twitch: '',
			youtube: '',
		}
	}

	let page = 0;

	function nextPage() {
		page += 1;
	}

	function previousPage() {
		page -= 1;
	}

	function cancelBecomingCreator() {
		console.log('cancel');
	}

	function becomeCreator() {
		console.log('finish');
	}

</script>

<div class='header'>
	<h2>Become a Creator</h2>
</div>

<div class='form'>
	<form autocomplete='off'>
		
		{#if page == 0}
			
			<h3>Who are you?</h3>
			<p>The information you provide will help people know more about their favourite creator, but you can leave it empty if you like.</p>

			<input class='input' list='countries' name='country' placeholder='Country'
				bind:value={result.country}>

			<datalist id='countries'>
				<Countries />
			</datalist>

			<textarea class='input' id='about' placeholder='About' maxlength='1500'
				bind:value={result.about}></textarea>

			<div class='page_buttons red' on:click={cancelBecomingCreator}>
				<h4>Cancel</h4>
			</div>

			<div class='page_buttons green' on:click={nextPage}>
				<h4>Next</h4>
			</div>
			
		{:else if page == 1}
			
			<h3>What do you do?</h3>
			<p>This will make it easier for people to find you. You can select multiple content types if you feel like it.</p>

			<!-- content type -->

			<div class='page_buttons red' on:click={previousPage}>
				<h4>Previous</h4>
			</div>

			<div class='page_buttons green' on:click={nextPage}>
				<h4>Next</h4>
			</div>
		
		{:else if page == 2}

			<h3>How can you receive gifts?</h3>
			<p>This will make it possible for people to send you gifts of any kind. It is entirely optional so you can leave it empty if you like.</p>

			<input type='text' class='input' id='full_name' placeholder='Full Name'
				bind:value={result.shipping_address.full_name}>

			<input type='text' class='input' id='phone_number' placeholder='Phone Number'
				bind:value={result.shipping_address.phone_number}>

			<input class='input' list='shipping_country' placeholder='Country for shipping'
				bind:value={result.shipping_address.country_for_shipping}>
			<datalist id='shipping_country'>
				<Countries />
			</datalist>

			<input type='text' class='input' id='state' placeholder='State / Province'
				bind:value={result.shipping_address.state}>

			<input type='text' class='input' id='city' placeholder='City'
				bind:value={result.shipping_address.city}>

			<input type='text' class='input' id='address' placeholder='Address'
				bind:value={result.shipping_address.address}>

			<input type='text' class='input' id='suite' placeholder='Suite'
				bind:value={result.shipping_address.suite}>

			<input type='text' class='input' id='postal_code' placeholder='Postal Code'
				bind:value={result.shipping_address.postal_code}>

			<div class='page_buttons red' on:click={previousPage}>
				<h4>Previous</h4>
			</div>

			<div class='page_buttons green' on:click={nextPage}>
				<h4>Next</h4>
			</div>
		
		{:else}

			<h3>How can people find you on other social media?</h3>
			<p>You can link your accounts on other platforms, so that your followers can see more about you and your creations. You can provide as many accounts to other platforms as you like.</p>

			<input type='text' class='input social' id='facebook' placeholder='Facebook'
				bind:value={result.social_media_links.facebook}>

			<input type='text' class='input social' id='twitter' placeholder='Twitter'
				bind:value={result.social_media_links.twitter}>

			<input type='text' class='input social' id='instagram' placeholder='Instagram'
				bind:value={result.social_media_links.instagram}>

			<input type='text' class='input social' id='webtoon' placeholder='Webtoon'
				bind:value={result.social_media_links.webtoon}>

			<input type='text' class='input social' id='twitch' placeholder='Twitch'
				bind:value={result.social_media_links.twitch}>

			<input type='text' class='input social' id='youtube' placeholder='Youtube'
				bind:value={result.social_media_links.youtube}>

			<div class='page_buttons red' on:click={previousPage}>
				<h4>Previous</h4>
			</div>

			<div class='page_buttons green' on:click={becomeCreator}>
				<h4>Finish</h4>
			</div>
		
		{/if}

	</form>
</div>

<style>
	.page_buttons {
		text-align: center;
		min-width: 100px;
		padding: 10px;
		border: 1px solid #111;
		margin: 5px;
		display: inline-block;
	}
	.page_buttons:hover {
		cursor: pointer;
	}
	.page_buttons h4 {
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