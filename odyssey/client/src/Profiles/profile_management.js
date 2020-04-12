// Library imports
import router from 'page';

// Javascript imports
import { loggedIn } from '../js/stores.js';
import { fetchPost } from '../js/fetch.js';

// Follow another user function
export async function followUser(result) {
	// Fetch post request for following
	const response = await fetchPost('http://localhost:3000/follow', {
		result: result
	});

	//RESTfully update unfollow/follow button
	return true;
}

// Unfollow another user function
export async function unfollowUser(result) {
	// Fetch post request for unfollowing
	const response = await fetchPost('http://localhost:3000/unfollow', {
		result: result
	});

	//RESTfully update unfollow/follow button
	return false;
}


// Check if a user is following another user
export async function isFollowing(result) {
	// Fetch post request for check
	const res = await fetchPost('http://localhost:3000/isFollowing', {
		result: result
	});
	if (res.following) {
		return true;
	} else {
		return false;
	}

}