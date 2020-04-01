// Javascript imports
import { fetchPost } from '../fetch.js';
import { clearErrorsAndLoaders, checkEmpty } from './authentication_helpers.js';
import { displayError, clearError, showLoader, hideLoader, disableButton, enableButton } from '../helpers.js';

// Login function
export async function loginUser(login) {
	
	// Clear current errors and check if there are any empty input fields.
	clearErrorsAndLoaders();
	if(!checkEmpty(login)) {
		return false;
	}

	// Get username and password
	let username = document.getElementById('input_l_username').value;
	let password = document.getElementById('input_l_password').value;
	
	// Fetch post request for login
	const response = await fetchPost('http://localhost:3000/login', {
		username: username, password: password
	});

	// Check for possible error
	if(!response.success) {
		displayError('error_l_password', response.message)
		return false;
	}
	return true;
}

// Register function
export async function registerUser(login) {

	// Clear current errors and check if there are any empty input fields.
	clearErrorsAndLoaders();
	if(!checkEmpty(login)) {
		return false;
	}
	if(!(await checkAllRegistrationInputs())) {
		return false;
	}

	// Get username, email, name and password
	let username = document.getElementById('input_r_username').value;
	let email = document.getElementById('input_r_email').value;
	let name = document.getElementById('input_r_name').value;
	let password = document.getElementById('input_r_password').value;

	// Fetch post request for registration
	const response = await fetchPost('http://localhost:3000/register', {
		username: username, email: email, name: name, password: password
	});
	return true;
}

// Become creator function 
export async function becomeCreator(result) {
	// result -> json object, containing all information for becoming a creator

	// Fetch post request for becoming a creator
	const response = await fetchPost('http://localhost:3000/becomeCreator', {
		result: result
	});
}

// Logout function 
export async function logoutUser() {
	// loggedIn is used for rendering the Authentication component after logout
	let loggedIn = false;

	// Fetch post request for logout
	const res = await fetch('http://localhost:3000/logout');
	const response = await res.json();
	return loggedIn;
}

// Reactive input validation for registration, login and profile edit
export async function checkInput(element) {
	switch(element.id.split('_')[1]) {
		case 'username':
			// While login, there is no need to check if username is valid, this is done in Flask.
			if(element.id.split('_')[0] != 'l') {
				checkUsername(element.id);
			}
			break;
		case 'email':
			checkEmail(element.id);
			break;
		case 'password':
			// While login, there is no need to check if password is valid, this is done in Flask.
			if(element.id.split('_')[0] != 'l') {
				checkPassword(element.id);
			}
			break;
		case 'confirm':
			checkConfirm(element.id);
			break;
		default:
			break;
	}
}

// Checks all registration inputs
async function checkAllRegistrationInputs() {
	let username = await checkUsername('r_username');
	let email = await checkEmail('r_email');
	let password = await checkPassword('r_password');
	let confirm = await checkConfirm('r_confirm');

	return username && email && password && confirm
}

// Reactive validation of username field during registration
async function checkUsername(id) {
	let username = document.getElementById('input_' + id).value;

	// Clear username's error, enable 'Register' button, show 'Loader' icon
	clearError('error_' + id);
	enableButton('info_submit');
	showLoader('loader_' + id);

	// Fetch post request for checking if such username exists in the database
	const usrnm_response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/username', {
		username: username
	});

	// Hide 'Loader' icon
	hideLoader('loader_' + id);

	// Check for possible error
	if(!usrnm_response.success) {
		displayError(('error_' + id), usrnm_response.message);
		disableButton('info_submit');
		return false;
	}

	return true;
}

// Reactive validation of email field during registration and profile editing
async function checkEmail(id) {
	let email = document.getElementById('input_' + id).value;

	// Clear username's error, enable 'Register' button, show 'Loader' icon
	clearError('error_' + id);
	enableButton('info_submit');
	showLoader('loader_' + id);

	// Fetch post request for checking if such email exists in the database
	const email_response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/email', {
		email: email
	});

	// Hide 'Loader' icon
	hideLoader('loader_' + id);

	// Check for possible error
	if(!email_response.success) {
		displayError(('error_' + id), email_response.message);
		disableButton('info_submit');
		return false;
	}

	return true;
}

// Reactive validation of password field during registration and profile editing
function checkPassword(id) {
	let password = document.getElementById('input_' + id).value;

	// Clear username's error, enable 'Register' button
	clearError('error_' + id);
	enableButton('info_submit');

	// Check if password's length is valid and display error if it's not
	if(password.length < 8) {
		displayError(('error_' + id), 'Password must be at least 8 characters long!');
		disableButton('info_submit');
		return false;
	}

	return true;
}

// Reactive validation of confirm password field during registration and profile editing
function checkConfirm(id) {
	let password = document.getElementById('input_' + id.split('_')[0] + '_password').value;
	let confirm = document.getElementById('input_' + id).value;

	// Clear username's error, enable 'Register' button
	clearError('error_' + id);
	enableButton('info_submit');

	// Check if password is the same as confirm password and display error if it's not
	if(password != confirm) {
		displayError(('error_' + id), 'Passwords must match!');
		disableButton('info_submit');
		return false;
	}
	return true;
}