<!-- Used in forms for displaying errors in inputs -->

<script>
	// Inherited variables
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
		display: block;
		float: right;
		font-size: 16px;
	}
	
	h4 {
		display: inline;
		color: #9a0e61;
	}

</style>