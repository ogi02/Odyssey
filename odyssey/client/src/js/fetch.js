// Fetch get request
export async function fetchGet(url) {
	const res = await fetch(url);
	const response = await res.json();
	return response;
}

// Fetch post request with JSON body
export async function fetchPost(url, data) {
  const res = await fetch(
	url, {
		method: "POST",
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
export async function fetchFilePost(url, file) {
	const formData = new FormData()
	formData.append('image', file);

	const res = await fetch(url, {
		method: "POST",
		body: formData
	});
	const response = await res.json();
	return response;
}

// Fetch file + json
export async function fetchFileJsonPost(url, data, file) {
	const formData = new FormData()
	formData.append('image', file);
	formData.append('data', data);

	const res = await fetch(url, {
		method: "POST",
		body: formData
	});
	const response = await res.json();
	return response;
}