<script>
	// Library imports
	import page from "page.js";
	import { getContext } from "svelte";

	// Inherited variables
	export let path;

	// Local variables
	const current_path = getContext("current_path");

	page(path, () => ($current_path = path));
	
</script>

{#if path == $current_path}
	<slot />
{/if}