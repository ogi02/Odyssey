<script>

	import { fetchPost } from '../fetch.js';

	let page = 0;

	function nextPage() {
		page += 1;
	}

	function previousPage() {
		page -= 1;
	}

	function doNothing() {
		nothing = 1;
	}

</script>

<div class='header'>
	<h2>Become a Creator</h2>
</div>

<div class='form'>
	<form autocomplete='off'>
		
		{#if page == 0}
			
			<h4>Who are you?</h4>
			<p>The information you provide will help people know more about their favourite creator, but you can leave it empty if you like.</p>
			
			<!-- <input type='text' id='about' placeholder='About' maxlength='1500' /> -->

			<div class='page_buttons red' on:click={doNothing}>
				<h4>Cancel</h4>
			</div>

			<div class='page_buttons green' on:click={nextPage}>
				<h4>Next</h4>
			</div>
			
		{:else if page == 1}
			
			<h4>What do you do?</h4>
			<p>This will make it easier for people to find you. You can select multiple content types if you feel like it.</p>

			<div class='page_buttons red' on:click={previousPage}>
				<h4>Previous</h4>
			</div>

			<div class='page_buttons green' on:click={nextPage}>
				<h4>Next</h4>
			</div>
		
		{:else if page == 2}

			<h4>How can you receive gifts?</h4>
			<p>This will make it possible for people to send you gifts of any kind. It is entirely optional so you can leave it empty if you like.</p>

			<div class='page_buttons red' on:click={previousPage}>
				<h4>Previous</h4>
			</div>

			<div class='page_buttons green' on:click={nextPage}>
				<h4>Next</h4>
			</div>
		
		{:else}

			<h4>How can people find you on other social media?</h4>
			<p>You can link your accounts on other platforms, so that your followers can see more about you and your creations. You can provide as many accounts to other platforms as you like.</p>

			<div class='page_buttons red' on:click={previousPage}>
				<h4>Previous</h4>
			</div>

			<div class='page_buttons green' on:click={doNothing}>
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
</style>