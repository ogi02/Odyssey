// Library imports
import router from 'page';

// Javascript imports
import { loggedIn } from '../js/stores.js';
import { fetchPost } from '../js/fetch.js';

// Follow another user function
export async function followUser(username) {
	let result = {
		profile_name: username
	}

	// Fetch post request for following
	const response = await fetchPost('/follow', {
		result: result
	});

	// RESTfully update unfollow/follow button
	return true;
}

// Unfollow another user function
export async function unfollowUser(username) {
	let result = {
		profile_name: username
	}

	// Fetch post request for unfollowing
	const response = await fetchPost('/unfollow', {
		result: result
	});

	// RESTfully update unfollow/follow button
	return false;
}


// Check if a user is following another user
export async function isFollowing(username) {
	let result = {
		profile_name: username
	}

	// Fetch post request for check
	const res = await fetchPost('/isFollowing', {
		result: result
	});
	if (res.following) {
		return true;
	} else {
		return false;
	}

}