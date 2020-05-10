<!-- Used as input field for login, registration and profile editing forms -->

<script>
	// Component imports
	import Error from './Error.svelte';

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';
	import { checkInput } from '../Authentication/authentication_management.js'

	// Inherited variables
	export let type;
	export let id;
	export let placeholder;
	export let has_icon;

	// Local variables
	let username = '';
	let email = '';
	let password = '';
	let confirm = '';

</script>

<div class='field'>

	<input
		id={'input_' + id}
		type={type}
		class='input'
		value=''
		placeholder={placeholder}
		on:input={() => checkInput({id})}
	/>

	{#if has_icon}
		
		<i id={'loader_' + id} class='icons bx bx-loader'></i>
		
	{/if}

	<Error id={'error_' + id} message=''/>

</div>

<style>

	.field {
		width: 300px;
		margin: 0 auto;
		position: relative;
	}

	.input {
		display: block;
		padding: 10px;
		border-radius: 5px;
		font-weight: 100px;
		min-width: 300px;
		margin: 10px 0 2px;
		outline-color: #bcdcfa;
	}

	.input, .icons {
		display: inline;
	}

	.icons {
		position: absolute;
		color: rgba(0, 0, 0, 0,7);
		font-size: 16px;
		display: none;
		top: 25px;
		right: 10px;
	}

</style>