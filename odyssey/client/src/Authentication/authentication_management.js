import { fetchPost } from '../fetch.js';
import { clearErrorsAndLoaders, checkEmpty } from './authentication_helpers.js';
import { displayError, clearError, showLoader, hideLoader, disableButton, enableButton } from '../helpers.js';

// login function
export async function loginUser(login, dispatch) {
	clearErrorsAndLoaders();
	if(!checkEmpty(login)) {
		return false;
	}
	let username = document.getElementById('input_l_username').value;
	let password = document.getElementById('input_l_password').value;
	const response = await fetchPost('http://localhost:3000/login', {
		username: username, password: password
	});
	if(!response.success) {
		displayError('error_l_password', response.message)
		return false;
	}
	return true;
}

// register function
export async function registerUser(login, dispatch) {
	clearErrorsAndLoaders();
	if(!checkEmpty(login)) {
		return false;
	}
	let username = document.getElementById('input_r_username').value;
	let email = document.getElementById('input_r_email').value;
	let name = document.getElementById('input_r_name').value;
	let password = document.getElementById('input_r_password').value;
	const response = await fetchPost('http://localhost:3000/register', {
		username: username, email: email, name: name, password: password
	});
	return true;
}

// become creator function 
export async function becomeCreator(result) {
	console.log(result)
	const response = await fetchPost('http://localhost:3000/becomeCreator', {
		result: result
	});
}

// logout function 
export async function logoutUser() {
	let loggedIn = false;
	const res = await fetch('http://localhost:3000/logout');
	const response = await res.json();
	return loggedIn;
}

// asynchronous input validation for registration
export async function checkInput(element) {
	switch(element.id.split('_')[1]) {
		case 'username':
			if(element.id.split('_')[0] != 'l') {
				checkUsername(element.id);
			}
			break;
		case 'email':
			checkEmail(element.id);
			break;
		case 'password':
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

async function checkUsername(id) {
	let username = document.getElementById('input_' + id).value;
	clearError('error_' + id);
	enableButton('info_submit');
	showLoader('loader_' + id);
	const usrnm_response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/username', {
		username: username
	});
	hideLoader('loader_' + id);
	if(!usrnm_response.success) {
		displayError(('error_' + id), usrnm_response.message);
		disableButton('info_submit');
	}
}

async function checkEmail(id) {
	let email = document.getElementById('input_' + id).value;
	clearError('error_' + id);
	enableButton('info_submit');
	showLoader('loader_' + id);
	const email_response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/email', {
		email: email
	});
	hideLoader('loader_' + id);
	if(!email_response.success) {
		displayError(('error_' + id), email_response.message);
		disableButton('info_submit');
	}
}

function checkPassword(id) {
	let password = document.getElementById('input_' + id).value;
	clearError('error_' + id);
	enableButton('info_submit');
	if(password.length < 8) {
		displayError(('error_' + id), 'Password must be at least 8 characters long!');
		disableButton('info_submit');
	}
}

function checkConfirm(id) {
	let password = document.getElementById('input_' + id.split('_')[0] + '_password').value;
	let confirm = document.getElementById('input_' + id).value;
	clearError('error_' + id);
	enableButton('info_submit');
	if(password != confirm) {
		displayError(('error_' + id), 'Passwords must match!');
		disableButton('info_submit');
	}
}