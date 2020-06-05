<script>
	// Library imports
	import { onMount } from "svelte";

	// Javascript imports
	import { fetchPost } from "../js/fetch.js";
	
	// Inherited variables
	export let user;
	export let posts;

	// Local variables
	let loadedPosts = 0;
	let allPostsLoaded = false;

	onMount(async () => {
		if(user.role == "creator") {
			// sort posts by date
			posts.sort((a, b) => (a.date > b.date) ? -1 : 1);

			// load posts
			await loadMorePosts();
		}
	});

	// Is post liked
	async function isLiked(post_id) {
		const response = await fetchPost("/hasLikedPost", {
			post_id: post_id
		});

		let temp = response.liked;
		return temp;
	}

	// Can a user view post (by tier_id)
	async function canViewPost(post_id) {
		const response = await fetchPost("/canViewPost", {
			post_id: post_id
		});

		let temp = response.view;
		return temp;
	}

	// Like post
	async function likePost(post_id) {
		const response = await fetchPost("/likePost", {
			post_id: post_id
		});

		posts.find(post => post._id.$oid === post_id).isLiked = true;
		posts = posts;
	}

	// Unlike post
	async function unlikePost(post_id) {
		const response = await fetchPost("/unlikePost", {
			post_id: post_id
		});

		posts.find(post => post._id.$oid === post_id).isLiked = false;
		posts = posts;
	}

	// Load more posts (chunk of 10 posts)
	async function loadMorePosts() {
		// Check if there are any posts to load
		if(posts.length == 0) {
			allPostsLoaded = true;
			return;
		}

		for(let i = loadedPosts; i < loadedPosts + 10; i++) {
			
			// Check if current user can view and has liked the post
			posts[i].isLiked = await isLiked(posts[i]._id.$oid);
			posts[i].canView = await canViewPost(posts[i]._id.$oid);

			// Check if there are ay more posts to load
			if(posts.length == i + 1) {
				allPostsLoaded = true;
				loadedPosts += i + 1;
				return;
			}
		}

		loadedPosts += 10;
	}

</script>

<div class="posts-container">
	{#each posts as post, i}
		
		{#if i < loadedPosts}

			<div class="post-box">
				{#if post.canView}

					<img alt="" class="post-image" src={"/images/" + user.username + "/" + post.image_path}>

					<div class="text-container">
						
						<h3>{post.text}</h3>
						
						<div class="heart-container">
							{#if post.isLiked}

								<i class="fa fa-heart fa-2x" aria-hidden="true" on:click={
									async () => await unlikePost(post._id.$oid)
								}></i>

							{:else}

								<i class="fa fa-heart-o fa-2x" aria-hidden="true" on:click={
									async () => await likePost(post._id.$oid)
								}></i>

							{/if}
						</div>

					</div>

				{:else}

					<div class="cant-view-post-container">
						<img alt="" class="post-image-cant-view" src={"/images/" + user.username + "/" + post.image_path}>
						<p class="centered-text-over-image">You can't view this post!</p>
					</div>

					<div class="text-container">
						<h3>{post.text}</h3>
						<i class="fa fa-lock" aria-hidden="true"><span class="locked">Locked</span></i> 
					</div>

				{/if}
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

	.post-image-cant-view {
		height: 25em;
		width: 40.2em;
		filter: blur(18px) brightness(0.5);
	}

	.text-container {
		margin: 1em;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
	}

	.cant-view-post-container {
		color: white;
		overflow: hidden;
		position: relative;
	}

	.centered-text-over-image {
		top: 45%;
		left: 50%;
		font-size: 1.5em;
		font-weight: bold;
		position: absolute;
		transform: translate(-50%, -50%);
	}

	.heart-container {
		margin: 5px;
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

	.locked {
		margin-left: 5px;
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