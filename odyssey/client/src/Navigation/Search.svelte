<script>
	// Library imports
	import router from 'page';

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { username } from '../js/stores.js';

	// Local variables
	let value = '';
	let foundUsernames = [];

	async function getUsernames() {
		if(value != '') {
			const response = await fetchPost("http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/getUsernames", {
				value: value
			});
			document.getElementsByClassName('usernames')[0].style.display = 'block';
			foundUsernames = response.usernames;
		}
		else {
			document.getElementsByClassName('usernames')[0].style.display = 'none';
		}
	}

	async function searchProfile(searchedUsername) {
		value = '';
		document.getElementsByClassName('usernames')[0].style.display = 'none';
		username.set(searchedUsername)
		router.redirect('/profile/' + searchedUsername);
	}

</script>

<div class='main'>
	<form autocomplete='off'>
		<i class="fa fa-search" aria-hidden="true"></i>
		<input bind:value={value} id='search' type='text' placeholder='Search..' 
			on:input={async () => await getUsernames()}>
	</form>
	<div class='usernames'>
		{#each foundUsernames as i }
			<div class='username-box' on:click={async () => await searchProfile(i)}>{i}</div>
		{/each}
	</div>
</div>

<style>
	.main {
		display: inline-block;
		margin: -1em 0.9em;
	}

	::placeholder { 
		color: #080d52;
		opacity: 0.8;
	}

	input[type=text] {
		padding-left: 18px;
		box-sizing: border-box;
	}

	input {
		border-radius: 25px;
		background-color: #f6f8fa;
		width: 10em;
		outline: none;
		font-weight: 5em;
		color: #080d52;
		padding: 5px;
	}

	.usernames {
		width: 10em;
		display: block;
		position: fixed;
	}

	.username-box {
		width: 10em;
		position: relative;
		display: block;
		background-color: #eee;
		border: 0.5px solid #ddd;
		padding: 5px;
		position: relative;
		color: #111;
	}

	.username-box:hover {
		cursor: pointer;
		background-color: #ddd;
		border-color: #ccc;
		text-decoration: none;
	}

</style>