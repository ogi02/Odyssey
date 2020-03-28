<script>
	export let path;
	import { getContext } from "svelte";
	import page from "page.js";
	const current_path = getContext("current_path");
	page(path, () => ($current_path = path));
</script>

{#if path == $current_path}
	<slot />
{/if}