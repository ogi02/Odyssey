<script>
	import { fetchGet } from '../fetch.js';
	import { onMount } from 'svelte';

	let user = {};
	let info = {};
	let social_media_links = {};
	let shipping_info = {};
	onMount(async()=>{
		const response = await fetchGet("/profile");
		user = response.user;
		info = response.info;
		social_media_links = response.info.social_media_links;
		shipping_info = response.info.shipping_info;


	});

	
</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<img src="https://thewideawakening.com/wp-content/uploads/2016/03/TWA-Header-Background-1600x400.jpg" style="position: absolute; top: 0; left: 0; min-width: 100%; width: 100%; height: 45%; min-height: 300px; object-fit: cover;">
<div class="card">
  <img src="https://www.stylist.co.uk/images/app/uploads/2016/09/21140727/gettyimages-1029935574.jpg?w=1640&h=1&fit=max&auto=format%2Ccompress" alt="ProfilePic" style="width:11rem; height: 11rem; margin-top: 1em; border: 5px; border-color: white; border-style: solid; border-radius: 95px;">
  <h1>{user.username}</h1>
  <p class="title">{info.bio}</p>
  <p>{info.country_of_residence}</p>
  <div style="margin: 24px 0;">
    <a href="#"><i class="fa fa-twitch"></i></a> 
    <a href="#"><i class="fa fa-twitter"></i></a>  
    <a href="#"><img src="https://cdn4.iconfinder.com/data/icons/logos-brands-5/24/linewebtoon-512.png" style="width: 7%"></a>  
    <a href="#"><i class="fa fa-facebook"></i></a> 
    <a href="#"><i class="fa fa-youtube"></i></a> 
  </div>
  <p><button>Follow</button></p>
</div>

<style>
.card {
  position: relative;
  max-width: 300px;
  margin: auto;
  margin-top: 33vh;
  text-align: center;
  font-family: arial;
}

.title {
  color: grey;
  font-size: 18px;
}

button {
  border: none;
  border-radius: 50px;
  outline: 0;
  display: inline-block;
  padding: 8px;
  color: white;
  background-color: #000;
  text-align: center;
  cursor: pointer;
  width: 50%;
  font-size: 18px;
}

a {
  text-decoration: none;
  font-size: 22px;
  color: black;
}

button:hover, a:hover {
  opacity: 0.7;
}
</style>