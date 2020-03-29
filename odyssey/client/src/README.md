## Conventions for Svelte JS

### Requirements for every .svelte file
Order of code: 
1. Javascript
	- Library imports
	- Component imports 
	- Javascript imports
	- Inherited variables
	- Local variables
	- Local functions
2. HTML
3. CSS

Example:
```javascript
<script>
	// Library imports
	import { onMount } from 'svelte';
	
	// Component imports
	import Component from './Component.svelte';

	// Javascript imports
	import { helperFunction1, helperFunction2 } from './helpers.js';

	// Inherited variables
	export let inheritedVariable;

	// Local variables
	let localVariable1;
	const localVariable2;

	// Explain functionality of the following function
	function f1() {
		...
	}
</script>

<div>
	Insert HTML here
</div>

<style>
	Insert CSS here
</style>
```

> **Note:** Those are just example names. Please use understandable names!

### Requirements for .js files

Javascript files will in most cases store helper functions. Please leave a comment before every function about its functionality and leave comments if there are any tricky parts in the function.

Example:
```javascript
// Explain functionality of the following function
function f1() {
	// explain tricky part 1
	... some code

	// explain tricky part 2
	... some other code
}	
```

> **Note:** Adding few new lines will make the code easier for reading and understanding. 


