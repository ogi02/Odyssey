<script>
	export let message;
	export let id;
</script>

<div id={id} class="error">
	<h4>{message}</h4>
</div>

<style>
.error {
	margin: 0;
	padding: 0;
	display: none;
}
h4 {
	display: inline;
	color: tomato;
}
</style>