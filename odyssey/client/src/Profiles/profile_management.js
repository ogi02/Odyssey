// Library imports
import router from 'page';

// Javascript imports
import { loggedIn } from '../js/stores.js';
import { fetchPost } from '../js/fetch.js';

// Follow another user function
export async function followUser(result) {
	// result -> json object, containing all information for becoming a creator

	// Fetch post request for becoming a creator
	const response = await fetchPost('http://localhost:3000/follow', {
		result: result
	});

}