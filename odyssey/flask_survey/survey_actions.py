# Built-in imports 
import json
import datetime
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from flask_classes.user import User
from flask_classes.active_user import ActiveUser
from flask_logging.log_config import info_log, error_log
from flask_classes.survey import Survey

survey_actions_bp = Blueprint('survey_actions_bp', __name__)

@survey_actions_bp.route('/createSurvey', methods=['POST'])
def create_survey():
	# Get user from session
	user = User.get_from_db(ActiveUser.username)
	user_id = user.get('_id')

	# Get information about the future survey
	result = request.get_json().get('result')
	
	# Tuple with user's information
	if result.get('image_path') != None:
		survey_type = "image"
	else:
		survey_type = "text"
	values = (
		None,
		user_id,
		None,
		datetime.datetime.now(),
		result.get('image_path'),
		result.get('text'),
		result.get('restriction_type_id'),
		result.get('options'),
		True,
		survey_type,
		result.get('deadline'),
		None
	)
	Survey(*values).create()

	info_log.info("%s added a new survey" % ActiveUser.username)
	
	return jsonify(success=True, message='Successfully created a new survey!')

@survey_actions_bp.route('/getTotalVoteCount', methods=['POST'])
def get_total_vote_count():
	# Get information about the survey
	result = request.get_json().get('result')
	count = Survey.get_all_votes_count(result.get('survey_id'))
		
	return jsonify(success=True, count = count)

@survey_actions_bp.route('/voteOnSurvey', methods=['POST'])
def vote_on_survey():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the survey
	result = request.get_json().get('result')
	
	Survey.vote(activeUser_id, result.get('survey_id'), result.get('option_number'))

	info_log.info("%s voted on survey with id: %s." % (ActiveUser.username, result.get('survey_id')))
	
	return jsonify(success=True, message='Successfully voted on survey!')

@survey_actions_bp.route('/VoteCountByOption', methods=['POST'])
def get_votes_by_option():
	# Get information about the survey
	result = request.get_json().get('result')
	
	count = Survey.get_votes_count_by_option(result.get('survey_id'), result.get('option_number'))

	return jsonify(success=True, count = count)

@survey_actions_bp.route('/hasVotedOnSurvey', methods=['POST'])
def has_voted_on_survey():
	# Get information about the survey
	result = request.get_json().get('result')
	
	if Survey.has_voted(activeUser_id, result.get('survey_id')):
		return jsonify(liked=True)
	
	return jsonify(liked=False)

@survey_actions_bp.route('/closeSurvey', methods=['POST'])
def close_survey():
	# Get information about the survey
	result = request.get_json().get('result')
	
	Survey.close(result.get('survey_id'))
	info_log.info("Successfully closed survey with id: %s" % result.get('survey_id'))
	
	return jsonify(success=True, message='Successfully closed survey!')

@survey_actions_bp.route('/chooseWinner', methods=['POST'])
def choose_winner():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')
	
	# Get information about the survey
	result = request.get_json().get('result')
	
	Survey.choose_winner(result.get('survey_id'), activeUser_id)
	info_log.info("Successfully anounced winner with id: %s on survey with id: %s" % (activeUser_id, result.get('survey_id')))
	
	return jsonify(success=True, message='Successfully anounced winner!')


@survey_actions_bp.route('/generateRandomWinner', methods=['POST'])
def generate_random_winner():
	# Get information about the survey
	result = request.get_json().get('result')
	
	winner_id = Survey.get_random_winner(result.get('survey_id'))

	return jsonify(success=True, winner_id = winner_id)
	