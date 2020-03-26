export async function fetchGet(url) {
  const res = await fetch(url);
  const response = await res.json();
  return response;
}

export async function fetchPost(url, data) {
  const res = await fetch(
    url, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(data),
    }
  );
  const response = await res.json();
  return response;
}

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