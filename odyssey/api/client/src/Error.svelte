<script>
	export let message;
	export let id;
	export let classes;
</script>

<div id={id} class={classes}>
	<h4>{message}</h4>
</div>

<style>
.error {
	margin: 0;
	padding: 0;
	display: none;
}
h4 {
	color: tomato;
}
</style>