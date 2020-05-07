// Display certain error
export function displayError(element, message) {
	document.getElementById(element).style.display = 'block';
	document.getElementById(element).getElementsByTagName('h4')[0].innerHTML = message;
}

// Clear certain error
export function clearError(element) {
	document.getElementById(element).style.display = 'none';
}

// Show certain loader
export function showLoader(element) {
	document.getElementById(element).style.display = 'inline';
}

// Hide certain loader
export function hideLoader(element) {
	document.getElementById(element).style.display = 'none';
}

// Disable certain button
export function disableButton(button) {
	document.getElementById(button).disabled = true;
}

// Enable certain button
export function enableButton(button) {
	document.getElementById(button).disabled = false;
}

// Check if there is a user logged in
export async function checkLogin() {
	const res = await fetch('http://localhost:3000/checkLogin');
	const response = await res.json();
	if (response.logged_in) {
		return true;
	} else {
		return false;
	}
}