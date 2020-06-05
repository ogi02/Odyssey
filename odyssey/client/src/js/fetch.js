const domain = 'http://192.168.1.132:3000';

// Fetch get request
export async function fetchGet(relative_url) {

	let url = domain.concat(relative_url);

	const res = await fetch(url);
	const response = await res.json();
	return response;
}

// Fetch post request with JSON body
export async function fetchPost(relative_url, data) {

	let url = domain.concat(relative_url);

	const res = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		},
		body: JSON.stringify(data),
	});

	const response = await res.json();
	return response;
}

// Fetch post request with File body
export async function fetchFilePost(relative_url, file) {
	const formData = new FormData()
	formData.append('image', file);

	let url = domain.concat(relative_url);

	const res = await fetch(url, {
		method: 'POST',
		body: formData
	});

	const response = await res.json();
	return response;
}

// Fetch file + json
export async function fetchFileJsonPost(relative_url, data, file) {
	const formData = new FormData()
	formData.append('image', file);
	formData.append('data', JSON.stringify(data));

	let url = domain.concat(relative_url);

	const res = await fetch(url, {
		method: 'POST',
		body: formData
	});

	const response = await res.json();
	return response;
}