<script>
	// Javascript imports
	import { fetchPost } from '../js/fetch.js';

	// Inherited variables
	export let surveys;
	export let user;

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

</script>

<div class="surveys-container">
	
	{#each surveys as survey}
		
		<div class='survey-box'>

			<img class="survey-image" src={"/images/" + user.username + "/" + survey.image_path}>

			<div class="text-container">
				<h3>{survey.text}</h3>
			</div>

			{#if survey.is_open == true}
				
				{#await getVotesOnSurvey(survey._id.$oid) then votes}

					{#each survey.options as option, i}
					
						<div class="survey-options-container">
							
							<p style="padding-left: 1.5em">{option}</p>
							
							{#await getVotesPerOption(survey._id.$oid, i) then vote_count}
								
								{#if vote_count != 0}
									<p style="background: rgb(160, 207, 245);
									border-radius: 16px;
									padding-left: calc((({vote_count}/{votes})*100)*0.3em);
									margin-left: 5em;
									position: absolute;
									">{vote_count/votes*100}%</p>
								
								{:else}
									<p style="
									margin-left: 6em;
									position: absolute;
									">0%</p>
								
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

	{/each}

</div>

<style>

	.surveys-container{
		display: flex;
		margin: 4em;
		flex-shrink: 0;
		flex-wrap: wrap;
		justify-content: center;
	}

	.survey-box {
		border: 2px solid #0f1930;
		min-width: 40em;
		max-width: 30em;
		min-height: 23em;
		margin: 10px;
	}

	.survey-image {
		width: 40.2em;
		margin-left: -2px;
		margin: -3px;
		height: 25em;
		margin-top: -4px;
	}

	.text-container{
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		margin: 1em;
		align-items: center;
		justify-content: space-between;
	}

	.survey-options-container{
		display: flex;
		align-items: flex-start;
	}

</style>