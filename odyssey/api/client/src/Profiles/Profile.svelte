<script>
	import { fetchGet } from '../fetch.js';
	import { onMount } from 'svelte';
	onMount(()=>{
		get_user();
	});
	let user = {};
	async function get_user(){
		const response = await fetchGet("/profile");
		user = response.user;
		console.log(user);
	}
	
</script>
<p>{user.username}</p>
