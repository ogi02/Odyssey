// display certain error
export function displayError(element, message) {
	document.getElementById(element).style.display = 'inline';
	document.getElementById(element).getElementsByTagName('h4')[0].innerHTML = message;
}

// clear certain error
export function clearError(element) {
	document.getElementById(element).style.display = 'none';
}

// show certain loader
export function showLoader(element) {
	document.getElementById(element).style.display = 'inline';
}

// hide certain loader
export function hideLoader(element) {
	document.getElementById(element).style.display = 'none';
}

export function disableButton(button) {
	document.getElementById(button).disabled = true;
}

export function enableButton(button) {
	document.getElementById(button).disabled = false;
}

export async function checkLogin() {
	const res = await fetch('http://localhost:3000/checkLogin');
	const response = await res.json();
	if (response.logged_in) {
		return true;
	} else {
		return false;
	}
}