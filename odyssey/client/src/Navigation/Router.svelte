<script>
	// Library imports
	import page from "page.js";
	import { setContext, afterUpdate } from "svelte";
	import { writable } from "svelte/store";

	// Inherited variables
	export let hashbang = true;

	// Local variables
	let started = false;
	const current_path = writable("/");

	setContext("current_path", current_path);

	afterUpdate(() => {
		if (!started) {
			started = true;
			page("*", ctx => {
				$current_path = ctx.path;
				console.log("NOT FOUND!");
			});
			page.start({ hashbang });
		}
	});
</script>

<slot />