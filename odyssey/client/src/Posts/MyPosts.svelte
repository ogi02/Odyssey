<script>
	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	
	// Inherited variables
	export let posts;
	export let user;

	// Get likes on post
	async function getLikesOnPost(post_id) {
		const response = await fetchPost('http://localhost:3000/getLikeCount', {
			post_id: post_id
		});

		let temp = response.like_count;

		return temp;
	}

</script>

<div class="posts-container">
	
	{#each posts as post, i}

		<div class='post-box'>
			<img class="post-image" src={"/images/" + user.username + "/" + post.image_path}>
			
			<div class="text-container">

				<h3>{post.text}</h3>

				{#await getLikesOnPost(post._id.$oid) then like_count}
					<p><i class="fa fa-heart" aria-hidden="true"></i>{like_count || 0}</p>
				{/await}

			</div>
		</div>

	{/each}

</div>

<style>

	.posts-container {
		display: flex;
		margin: 4em;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}

	.post-box {
		border: 2px solid #0f1930;
		min-width: 40em;
		max-width: 30em;
		min-height: 23em;
		margin: 10px;
	}

	.post-image {
		width: 40.2em;
		margin-left: -2px;
		margin: -3px;
		height: 25em;
		margin-top: -4px;
	}

	.text-container {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		margin: 1em;
		align-items: center;
		justify-content: space-between;
	}

	.fa-heart-o:hover {
		color: red;
	}

	.fa-heart {
		color: red;
		transition: 0.3s ease-out;
	}

	.fa-heart:hover {
		color: black;
		transition: 0.3s;
	}

</style>