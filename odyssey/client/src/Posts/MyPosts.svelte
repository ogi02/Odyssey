<script>
	// Library imports
	import { onMount } from "svelte";

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	
	// Inherited variables
	export let posts;
	export let user;

	// Local variables
	let loadedPosts = 0;
	let allPostsLoaded = false;

	onMount(async () => {
		if(user.role == "creator") {
			// sort surveys by date
			posts.sort((a, b) => (a.date > b.date) ? -1 : 1);

			// load more surveys
			await loadMorePosts();
		}
	});

	// Get likes on post
	async function getLikesOnPost(post_id) {
		const response = await fetchPost('http://localhost:3000/getLikeCount', {
			post_id: post_id
		});

		let temp = response.like_count;

		return temp;
	}

	// Load more posts
	async function loadMorePosts() {
		for(let i = loadedPosts; i < loadedPosts + 10; i++) {
			// Check if there are any more posts to load
			if(posts.length == i) {
				allPostsLoaded = true;
				loadedPosts += i;
				return;
			}
		}

		loadedPosts += 10;

		// Removes button after last post is loaded
		if(posts.length == loadedPosts) {
			allPostsLoaded = true;
			return;
		}
	}

</script>

<div class="posts-container">
	
	{#each posts as post, i}

		{#if i < loadedPosts}

			<div class='post-box'>
				<img class="post-image" src={"/images/" + user.username + "/" + post.image_path}>
				
				<div class="text-container">

					<h3>{post.text}</h3>

					{#await getLikesOnPost(post._id.$oid) then like_count}
						<p><i class="fa fa-heart" aria-hidden="true"></i>{like_count || 0}</p>
					{/await}

				</div>
			</div>

		{/if}

	{/each}

	{#if !allPostsLoaded}
		<button on:click={async () => await loadMorePosts()}>Load More Posts</button>
	{/if}

</div>

<style>

	.posts-container {
		margin: 4em;
		display: flex;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}

	.post-box {
		width: 40em;
		margin: 10px;
		min-height: 23em;
		border: 2px solid #0f1930;
	}

	.post-image {
		height: 25em;
		width: 40.3em;
		margin: -4px -2px;
	}

	.text-container {
		margin: 1em;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
	}

	.fa-heart-o:hover {
		color: red;
	}

	.fa-heart {
		color: red;
		padding-right: 10px;
		transition: 0.3s ease-out;
	}

	.fa-heart:hover {
		color: black;
		transition: 0.3s;
	}

	button {
		width: 12em;
		color: white;
		border: none;
		cursor: pointer;
		font-size: 18px;
		margin-top: 1em;
		border-radius: 50px;
		background-color: #0f1930;
	}

</style>