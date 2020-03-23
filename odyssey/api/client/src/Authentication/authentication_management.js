import { fetchPost } from '../fetch.js';
import { 
	clearErrorsAndLoaders, checkEmpty, displayError, clearError, showLoader, hideLoader, disableButton, enableButton
} from './authentication_helpers.js';


// login function
export async function loginUser(login) {
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
}

// register function
export async function registerUser(login) {
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
	loggedIn = false;
	const res = await fetch('http://localhost:3000/logout');
	const response = await res.json();
}

// asynchronous input validation for registration
export async function checkInput(element) {
	switch(element.id) {
		case 'r_username':
			checkUsername();
			break;
		case 'r_email':
			checkEmail();
			break;
		case 'r_password':
			checkPassword();
			break;
		case 'r_confirm':
			checkConfirm();
			break;
		default:
			break;
	}
}

async function checkUsername() {
	let username = document.getElementById('input_r_username').value;
	clearError('error_r_username');
	enableButton('register_button');
	showLoader('loader_r_username');
	const usrnm_response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/username', {
		username: username
	});
	hideLoader('loader_r_username');
	if(!usrnm_response.success) {
		displayError('error_r_username', usrnm_response.message);
		disableButton('register_button');
	}
}

async function checkEmail() {
	let email = document.getElementById('input_r_email').value;
	clearError('error_r_email');
	enableButton('register_button');
	showLoader('loader_r_email');
	const email_response = await fetchPost('http://localhost:3000/FpCerpd9Z7SIbjmN81Jy/email', {
		email: email
	});
	hideLoader('loader_r_email');
	if(!email_response.success) {
		displayError('error_r_email', email_response.message);
		disableButton('register_button');
	}
}

function checkPassword() {
	let password = document.getElementById('input_r_password').value;
	clearError('error_r_password');
	enableButton('register_button');
	if(password.length < 8) {
		displayError('error_r_password', 'Password must be at least 8 characters long!');
		disableButton('register_button');
	}
}

function checkConfirm() {
	let password = document.getElementById('input_r_password').value;
	let confirm = document.getElementById('input_r_confirm').value;
	clearError('error_r_confirm');
	enableButton('register_button');
	if(password != confirm) {
		displayError('error_r_confirm', 'Passwords must match!');
		disableButton('register_button');
	}
}