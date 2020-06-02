<script>
	// Library imports
	import { onMount } from "svelte";

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';

	// Inherited variables
	export let surveys;
	export let user;

	// Local variables
	let loadedSurveys = 0;
	let allSurveysLoaded = false;

	onMount(async () => {
		if(user.role == "creator") {
			// sort surveys by date
			surveys.sort((a, b) => (a.date > b.date) ? -1 : 1);

			// load more surveys
			await loadMoreSurveys();
		}
	});

	// Get voted per option
	async function getVotesPerOption(survey_id, option_id) {
		const response = await fetchPost('http://localhost:3000/voteCountByOption', {
			survey_id: survey_id,
			option_id: option_id
		});

		let temp = response.vote_count;

		return temp;
	}

	// Close survey
	async function closeSurvey(survey_id) {
		const response = await fetchPost('http://localhost:3000/closeSurvey', {
			survey_id: survey_id
		});

		surveys.find(survey => survey._id.$oid === survey_id).is_open = false;
		surveys = surveys;
	}

	// Set winner
	async function electWinner(survey_id) {
		const response = await fetchPost('http://localhost:3000/chooseWinningOption', {
			survey_id: survey_id
		});

		surveys.find(survey => survey._id.$oid === survey_id).winner = response.winner;
		surveys = surveys;
	}

	// Get all votes
	async function getVotesOnSurvey(survey_id) {
		const response = await fetchPost('http://localhost:3000/getTotalVoteCount', {
			survey_id: survey_id
		});

		let temp = response.votes;
		return temp;
	}

	// Load more surveys
	async function loadMoreSurveys() {
		for(let i = loadedSurveys; i < loadedSurveys + 10; i++) {
			// Check if there are any more surveys to load
			if(surveys.length == i) {
				allSurveysLoaded = true;
				loadedSurveys += i;
				return;
			}
		}

		loadedSurveys += 10;

		// Removes button after last survey is loaded
		if(surveys.length == loadedSurveys) {
			allSurveysLoaded = true;
			return;
		}
	}

</script>

<div class="surveys-container">
	
	{#each surveys as survey, i}

		{#if i < loadedSurveys}

			<div class='survey-box'>

				<img class="survey-image" src={"/images/" + user.username + "/" + survey.image_path}>

				<div class="text-container">
					<h3>{survey.text}</h3>
				</div>

				{#if survey.is_open}
					
					{#await getVotesOnSurvey(survey._id.$oid) then votes}

						{#each survey.options as option, i}

							<div class="survey-options-container">

								<p class="option">{option}</p>

								{#await getVotesPerOption(survey._id.$oid, i) then vote_count}
									
									{#if vote_count != 0}
										<p 
											class="any-percent"
											style="padding-left: calc((({vote_count}/{votes})*100)*0.3em);"
										>{vote_count/votes*100}%</p>
									{:else}
										<p class="zero-percent">0%</p>
									{/if}

								{/await}

							</div>

						{/each}

						{#if votes != 0}
							<button on:click={async () => {
								await closeSurvey(survey._id.$oid);
								await electWinner(survey._id.$oid);
							}}>Close</button>
						{/if}

					{/await}

				{:else}

					<p>Winning option: {survey.winner}</p>

				{/if}

			</div>

		{/if}

	{/each}

	{#if !allSurveysLoaded}
		<button on:click={async () => await loadMoreSurveys()}>Load More Surveys</button>
	{/if}

</div>

<style>

	.surveys-container {
		margin: 4em;
		display: flex;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}

	.survey-box {
		width: 40em;
		margin: 10px;
		min-height: 23em;
		border: 2px solid #0f1930;
	}

	.survey-image {
		height: 25em;
		width: 40.2em;
		margin: -4px -2px;
	}

	.survey-options-container{
		display: flex;
		align-items: flex-start;
	}

	.text-container {
		margin: 1em;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
	}

	.option {
		padding-left: 1.5em;
	}

	.zero-percent {
		margin-left: 5em;
		position: absolute;
	}

	.any-percent {
		font-size: 10pt;
		margin-left: 6em;
		padding: 2px 10px;
		position: absolute;
		border-radius: 16px;
		background: rgb(160, 207, 245);
	}

	button {
		width: 12em;
		color: white;
		border: none;
		cursor: pointer;
		font-size: 18px;
		margin-top: 1em;
		border-radius: 50px;
		background-color: #0f1930;
	}

</style>