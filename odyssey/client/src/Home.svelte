<script>
	// Library imports
	import router from 'page';
	import { onMount } from 'svelte';

	// Javascript imports
	import { loggedIn } from './js/stores.js';

	// Local variables
	let userLoggedIn;

	onMount(() => {
		loggedIn.subscribe(value => {
			userLoggedIn = value;
		});
	});

</script>

<body>

	<div class='main'>

		<div class='full-width-first dark-field'>

			<div class='wrap'>

				<div>

					<p class='motto'>Be creative!</p>
					<p class='slogan'>Take back creative control. Gain freedom and stability with the support of your fans. Do your best creative work.</p>

					{#if !userLoggedIn}
						<button class='button-join' on:click={() => router.redirect('/login')}>Join Odyssey today!</button>
					{/if}

				</div>

				<div>

					<div>
						<img alt="" class='image-in-container' src='https://i.pinimg.com/originals/f6/5a/53/f65a53be9515951bf9e28504efc5d6b0.jpg'>
						<img alt="" class='image-in-container' src='https://cdn.shopify.com/s/files/1/1734/8431/products/Flying_1024x1024.jpg?v=1491498378'>
						<img alt="" class='image-in-container' src='https://i.pinimg.com/originals/28/72/54/2872549acfb2e0ee8846edc3f973fd2a.jpg'>
					</div>

					<div>
						<img alt="" class='image-in-container' src='https://images.discerningassets.com/image/upload/c_fit,h_1000,w_1000/c_fit,fl_relative,h_1.0,o_100,w_1.0/v1559837064/Giraffe_Gerald_qh7k1j.jpg'>
						<img alt="" class='image-in-container' src='https://i.pinimg.com/originals/07/4c/e9/074ce9b21ed92eaaa6a759dd3863b069.jpg'>
						<img alt="" class='image-in-container' src='https://cdn.shopify.com/s/files/1/1734/8431/products/White_Rooster_1024x1024.jpg?v=1581350689'>
					</div>

				</div>

			</div>

		</div>

		<div class='full-white-field'>
			
			<div class='full-width-join white-field'>
				<div class='wrap-text'>
					<p style='font-size: 2em;'>Join today as a...</p>
				</div>
			</div>

			<div class='full-width-first white-field'>

				<div class='wrap'>

					<div>
						<i class='fa fa-video-camera' aria-hidden='true'></i>
						<span>Video Creator</span>
						<p class='explain-content-type'>Develop new work with the support of your biggest fans, connect with your community in a troll-free environment, and build a predictable revenue stream that doesn’t rely on ads or algorithms.</p>
					</div>

					<div>
						<i class='fa fa-paint-brush' aria-hidden='true'></i>
						<span>Visual Artist</span>
						<p class='explain-content-type'>Earn more than just commissions alone by offering things like behind-the-scenes access, raw files, & walk-throughs of your creative process. Don't rely exclusively on unpredictable revenue streams.</p>
					</div>

					<div>
						<i class='fa fa-podcast' aria-hidden='true'></i>
						<span>Podcaster</span>
						<p class='explain-content-type'>Get to know your most loyal listeners and give them a place to connect, build community, and engage more deeply with you. Deliver bonus content, and establish a reliable revenue stream beyond ads.</p>
					</div>

					<div>
						<i class='fa fa-music' aria-hidden='true'></i>
						<span>Musician</span>
						<p class='explain-content-type'>Connect directly and build community with your most engaged fans. Test new work in a supportive environment. Establish a reliable, recurring revenue stream. Waiting to release an album? You call the shots.</p>
					</div>

					<div>
						<i class='fa fa-book' aria-hidden='true'></i>
						<span>Writer/Journalist</span>
						<p class='explain-content-type'>Don't turn to clickbait to hit pageview targets. Focus on quality over quantity for your biggest readers. Focus your time and energy writing for the people that value your content most.</p>
					</div>

				</div>

				<div class='wrap' style='padding-bottom: 4em'>

					<div>
						<i class='fa fa-gamepad' aria-hidden='true'></i>
						<span>Gaming Creator</span>
						<p class='explain-content-type'>Reinvest funds to grow your community in a sustainable way. Focus your time and energy on the members that add value to your community. Cut out the rest.</p>
					</div>

					<div>
						<i class='fa fa-cutlery' aria-hidden='true'></i>
						<span>Culinary artist</span>
						<p class='explain-content-type'>Gain a platform where you can engage on a deeper level with the members that matter most. Share exclusive shots of your work and your WIP when creating something out of scratch</p>
					</div>

					<div>
						<i class='fa fa-shopping-basket' aria-hidden='true'></i>
						<span>Local Business</span>
						<p class='explain-content-type'>By using out platform you can expand your business's customer range. Communicate better with your clients and learn directly from them how to expand your product range.</p>
					</div>

					<div>
						<i class='fa fa-handshake-o' aria-hidden='true'></i>
						<span>Non-profit</span>
						<p class='explain-content-type'>All charitable nonprofits benefit from public support and donations. What better way to expand your organization than to get to know more people who support your cause? </p>
					</div>

					<div>
						<i class='fa fa-plus-square' aria-hidden='true'></i>
						<span>Something else</span>
						<p class='explain-content-type'>Take back creative control. Gain freedom and stability with the support of your fans. Do your best creative work. And share your work with the people that respect it.</p>
					</div>

				</div>

			</div>

		</div>
		
		<div class='full-width-second dark-field'>
			
			<div class='wrap'>
			
				<p>© Odyssey™</p>
				<p>mail.odyssey.2020@gmail.com</p>
				<div>
					<i class='fa fa-instagram fa-2x ico' aria-hidden='true'></i>
					<i class='fa fa-facebook-official fa-2x ico' aria-hidden='true'></i>
					<i class='fa fa-twitter-square fa-2x ico' aria-hidden='true'></i>
				</div>

			</div>

		</div>

	</div>

</body>

<style>

	body {
		min-width: 103%;
		position: fixed;
		margin-left: -1em;
		overflow-x: hidden;
		overflow-y: scroll;
	}

	.main {
		max-width: 110vw;
	}

	.full-width-first {
		top: 2.5em;
		padding-top: 1em;
		position: relative;
		padding-bottom: 2em;
	}

	.full-width-second {
		position: relative;
		padding-top: 0.5em;
	}

	.full-width-join {
		top: 2.5em;
		position: relative;
	}

	.full-white-field {
		background-size: 974px 944px;
		background-image: url("https://scontent.fsof8-1.fna.fbcdn.net/v/t1.15752-9/102563045_275731906911257_4286511703690051584_n.png?_nc_cat=102&_nc_sid=b96e70&_nc_ohc=1xRNFs4pxDwAX8dwCQN&_nc_ht=scontent.fsof8-1.fna&oh=e445d6d617cf691a91a2c6078fbcc3db&oe=5EFD4C81");
	}

	.white-field {
		color: #080d52;
	}

	.dark-field {
		color: white;
		background-color: #080d52;
	}

	.slogan {
		max-width: 16em; 
		font-size: 1.1em;
	}

	.motto {
		font-size: 3.1em;
	}

	.button-join {
		color: #080d52;
		padding: 0.7em;
		margin-top: 1em;
		border-width: 0;
		font-size: 1.1em;
		font-weight: 450;
		border-radius: 26px;
		background-color: #e0f4ff;
		transition: all 0.3s ease;
	}

	.button-join:hover {
		padding: 0.8em;
		cursor: pointer;
		background-color: #f9c3fa;
	}

	.image-in-container {
		width: 9em;
		height: 12em;
		padding: 0.4em;
		border-radius: 10px;
	}

	.wrap-text {
		display: flex;
		margin: 0 auto;
		justify-content: center;
	}

	.wrap {
		width: 50%;
		padding: 1em;
		display: flex;
		margin: 0 auto;
		justify-content: space-between;
	}

	.explain-content-type {
		max-width: 10em;
	}

	.ico{
		padding: 8px;
	}

</style>