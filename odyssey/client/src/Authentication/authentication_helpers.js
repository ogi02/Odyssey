import { fetchPost } from '../fetch.js';
import { displayError } from '../helpers.js';

// clears all errors and loaders
export function clearErrorsAndLoaders() {
	let errors = document.getElementsByClassName('error');
	for(let i = 0; i < errors.length; i++) {
		errors[i].style.display = 'none';
	}
	let loaders = document.getElementsByClassName('icons');
	for(let i = 0; i < loaders.length; i++) {
		loaders[i].style.display = 'none';
	}
}

// checks if there is any empty input
export function checkEmpty(login) {
	let is_valid = true;

	if(login) {
		let username = document.getElementById('input_l_username').value;
		let password = document.getElementById('input_l_password').value;
		if(username == '') {
			displayError('error_l_username', 'Username is required!');
			is_valid = false;
		}
		if(password == '') {
			displayError('error_l_password', 'Password is required!');
			is_valid = false;
		}
	}

	else {
		let username = document.getElementById('input_r_username').value;
		let email = document.getElementById('input_r_email').value;
		let name = document.getElementById('input_r_name').value;
		let password = document.getElementById('input_r_password').value;
		let confirm = document.getElementById('input_r_confirm').value;
		if(username == '') {
			displayError('error_r_username', 'Username is required!');
			is_valid = false;
		}
		if(email == '') {
			displayError('error_r_email', 'Email is required!');
			is_valid = false;
		}
		if(name == '') {
			displayError('error_r_name', 'Name is required!');
			is_valid = false;
		}
		if(password == '') {
			displayError('error_r_password', 'Password is required!');
			is_valid = false;
		}
		if(confirm == '') {
			displayError('error_r_confirm', 'Confirm Password is required!');
			is_valid = false;
		}
	}

	return is_valid;
}