<script>
	// Library imports
	import { onMount } from "svelte";

	// Javascript imports
	import { fetchPost } from '../js/fetch.js';

	// Inherited variables
	export let user;
	export let surveys;

	// Local variables
	let loadedSurveys = 0;
	let allSurveysLoaded = false;

	onMount(async () => {
		if(user.role == "creator") {
			// sort surveys by date
			surveys.sort((a, b) => (a.date > b.date) ? -1 : 1);

			// filter open surveys
			surveys = surveys.filter(survey => survey.is_open == true);

			// load more surveys
			await loadMoreSurveys();
		}
	});

	// Has current user voted on certain survey
	async function hasVoted(survey_id) {
		const response = await fetchPost('http://localhost:3000/hasVotedOnSurvey', {
			survey_id: survey_id
		});

		let temp = response.voted;
		return temp;
	}

	// Can current user view a certain survey
	async function canViewSurvey(survey_id) {
		const response = await fetchPost('http://localhost:3000/canViewSurvey', {
			survey_id: survey_id
		});

		let temp = response.view;
		return temp;
	}

	// Vote on a selected survey
	async function voteOnSurvey(survey_id, option_id) {
		const response = await fetchPost('http://localhost:3000/voteOnSurvey', {
			survey_id: survey_id,
			option_id: option_id
		});

		surveys.find(survey => survey._id.$oid === survey_id).hasVoted = true;
		surveys = surveys;
	}

	// Get votes on a certain option for a certain survey
	async function getVotesPerOption(survey_id, option_id) {
		const response = await fetchPost('http://localhost:3000/voteCountByOption', {
			survey_id: survey_id,
			option_id: option_id
		});

		let temp = response.vote_count;
		return temp;
	}

	// Get all votes on a certain survey
	async function getVotesOnSurvey(survey_id) {
		const response = await fetchPost('http://localhost:3000/getTotalVoteCount', {
			survey_id: survey_id
		});

		let temp = response.votes;
		return temp;
	}

	// Load more surveys
	async function loadMoreSurveys() {
		// Check if there are any surveys to load
		if(surveys.length == 0) {
			allSurveysLoaded = true;
			return;
		}

		for(let i = loadedSurveys; i < loadedSurveys + 10; i++) {

			// Check if current user can view and has voted on survey
			surveys[i].hasVoted = await hasVoted(surveys[i]._id.$oid);
			surveys[i].canView = await canViewSurvey(surveys[i]._id.$oid);

			// Check if there are any more surveys to load
			if(surveys.length == i + 1) {
				allSurveysLoaded = true;
				loadedSurveys += i + 1;
				return;
			}

		}

		loadedSurveys += 10;
	}

</script>

<div class="surveys-container">
	{#each surveys as survey, i}
		
		{#if i < loadedSurveys}

			{#if survey.is_open}

				<div class='survey-box'>
					{#if survey.canView}

						{#await getVotesOnSurvey(survey._id.$oid) then votes}

							<img class="survey-image" src={"/images/" + user.username + "/" + survey.image_path}>
							
							<div class="text-container">
								<h3>{survey.text}</h3>
							</div>
							
							{#if !survey.hasVoted}

								{#each survey.options as option, i}
									<p>{option}</p>
									<button on:click={async () => await voteOnSurvey(survey._id.$oid, i)}>Vote</button>
								{/each}

							{:else}

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

							
							{/if}

						{/await}

					{:else if survey.is_open}

						<div class="cant-view-survey-container">
							<img class="survey-image-cant-view" src={"/images/" + user.username + "/" + survey.image_path}>
							<p class="centered-text-over-image">You can't view this survey!</p>
						</div>

						<div class="text-container">
							<h3>{survey.text}</h3>
							<i class="fa fa-lock" aria-hidden="true"><span style="margin-left: 5px">Locked</span></i> 
						</div>

					{/if}
				</div>

			{/if}

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
		width: 40.3em;
		margin: -4px -2px;
	}

	.survey-image-cant-view {
		height: 25em;
		width: 40.2em;
		filter: blur(18px) brightness(0.5);
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

	.cant-view-survey-container {
		color: white;
		overflow: hidden;
		position: relative;
	}

	.centered-text-over-image {
		top: 45%;
		left: 50%;
		font-size: 1.5em;
		font-weight: bold;
		position: absolute;
		transform: translate(-50%, -50%);
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