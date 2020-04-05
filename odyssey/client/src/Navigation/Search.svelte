<script>
	// Library imports
	import page from 'page.js';

	// Javascript imports
	import { fetchPost } from '../fetch.js';

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

	function searchProfile(searchedUsername) {
		value = '';
		document.getElementsByClassName('usernames')[0].style.display = 'none';
		page.redirect('/profile/' + searchedUsername);
	}

</script>

<div class='main'>
	<form autocomplete='off'>
		<input bind:value={value} id='search' type='text' on:input={async () => await getUsernames()}>
	</form>
	<div class='usernames'>
		{#each foundUsernames as username }
			<div class='username-box' on:click={() => searchProfile(username)}>{username}</div>
		{/each}
	</div>
</div>

<style>
	.main {
		display: inline-block;
		margin: 0;
		padding: 0;
	}

	input {
		width: 10em;
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