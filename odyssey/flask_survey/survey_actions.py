# Built-in imports 
import os
import json
import datetime
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from helpers import allowed_image
from flask_classes.user import User
from flask_classes.active_user import ActiveUser
from flask_logging.log_config import info_log, error_log
from flask_classes.survey import Survey

upload_folder = "./client/public/images"

survey_actions_bp = Blueprint('survey_actions_bp', __name__)

@survey_actions_bp.route('/createSurvey', methods=['POST'])
def create_survey():
	# Get user from session
	username = ActiveUser.username
	user = User.get_from_db(username)
	user_id = user.get('_id')

	# Get image from request
	image = request.files["image"]

	# Get information about the future survey
	result = json.loads(request.form["data"])

	# Get time of post creation
	now = datetime.datetime.now()

	# Validate image
	if allowed_image(image.filename):

		# Tuple with user's information
		values = (
			None, #_id
			user_id,
			None, #votes
			now,  #date
			now.strftime("%m-%d-%Y-%H-%M-%S"), # image_path
			result.get('description'),
			result.get('required_id'),
			result.get('options'),
			None, #open/closed
			None, #deadline
			None  #winner
		)
		Survey(*values).create()

		# Define path where the image will go ("public/images/{user"s username}/)
		path = os.path.join(upload_folder, username)

		# Name for the picture
		filename = now
		
		# Check if path exists and create one if it doesn"t
		if not os.path.exists(path):
			os.makedirs(path)

		# Save image
		image.save(os.path.join(path, now.strftime("%m-%d-%Y-%H-%M-%S")))

		info_log.info("%s added a new survey" % username)
		
		return jsonify(success=True, message='Successfully created a new survey!')

	else:
		error_log.error("Image extension is not allowed or doesn't exist!")

		return jsonify(success=False, message="Allowed extensions: 'pdf', 'png', 'jpeg', 'jpg', 'gif'"), 403

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
	survey_id = request.get_json().get("survey_id")
	option_id = request.get_json().get("option_id")
	
	Survey.vote(activeUser_id, survey_id, option_id)

	info_log.info("%s voted on survey with id: %s." % (ActiveUser.username, survey_id))
	
	return jsonify(success=True, message='Successfully voted on survey!')

@survey_actions_bp.route('/voteCountByOption', methods=['POST'])
def get_votes_by_option():
	# Get information about the survey
	survey_id = request.get_json().get("survey_id")
	option_id = request.get_json().get("option_id")
	
	count = Survey.get_votes_count_by_option(survey_id, option_id)

	return jsonify(success=True, vote_count = count)

@survey_actions_bp.route('/hasVotedOnSurvey', methods=['POST'])
def has_voted_on_survey():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the survey
	survey_id = request.get_json().get("survey_id")
	
	if Survey.has_voted(activeUser_id, survey_id):
		return jsonify(voted=True)
	
	return jsonify(voted=False)

@survey_actions_bp.route('/closeSurvey', methods=['POST'])
def close_survey():
	# Get information about the survey
	survey_id = request.get_json().get("survey_id")
	
	Survey.close(survey_id)
	info_log.info("Successfully closed survey with id: %s" % survey_id)
	
	return jsonify(success=True, message='Successfully closed survey!')

@survey_actions_bp.route('/chooseWinningOption', methods=['POST'])
def get_winning_option():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the survey
	survey_id = request.get_json().get("survey_id")

	Survey.get_wining_option(survey_id)

	win = Survey.get_wining_option(survey_id)
	info_log.info("Successfully option %s won survey with id: %s" % (activeUser_id, survey_id))

	return jsonify(success=True, message='Successfully anounced winning option!', winner = win)

@survey_actions_bp.route('/canViewSurvey', methods=['POST'])
def can_view_survey():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	survey_id = request.get_json().get("survey_id")
	
	if Survey.can_view(activeUser_id, survey_id):
		return jsonify(view=True)
	
	return jsonify(view=False)