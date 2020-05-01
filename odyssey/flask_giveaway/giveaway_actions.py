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
from flask_classes.giveaway import Giveaway

giveaway_actions_bp = Blueprint('giveaway_actions_bp', __name__)

@giveaway_actions_bp.route('/createGiveaway', methods=['POST'])
def create_giveaway():
	# Get user from session
	user = User.get_from_db(ActiveUser.username)
	user_id = user.get('_id')

	# Get information about the future giveaway
	result = request.get_json().get('result')
	
	# Tuple with user's information
	if result.get('image_path') != None:
		giveaway_type = "image"
	else:
		giveaway_type = "text"
	values = (
		None,
		user_id,
		None,
		datetime.datetime.now(),
		result.get('image_path'),
		result.get('text'),
		result.get('restriction_type_id'),
		True,
		giveaway_type,
		result.get('deadline'),
		None
	)
	Giveaway(*values).create()

	info_log.info("%s added a new giveaway" % ActiveUser.username)
	
	return jsonify(success=True, message='Successfully created a new giveaway!')

@giveaway_actions_bp.route('/getTotalContestantsCount', methods=['POST'])
def get_total_contestants_count():
	# Get information about the giveaway
	result = request.get_json().get('result')
	count = giveaway.get_all_contestants_count(result.get('giveaway_id'))
		
	return jsonify(success=True, count = count)

@giveaway_actions_bp.route('/joinGiveaway', methods=['POST'])
def join_giveaway():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the giveaway
	result = request.get_json().get('result')
	
	giveaway.join(activeUser_id, result.get('giveaway_id'))

	info_log.info("%s joined giveaway with id: %s." % (ActiveUser.username, result.get('giveaway_id')))
	
	return jsonify(success=True, message='Successfully joined giveaway!')

@giveaway_actions_bp.route('/hasJoinedGiveaway', methods=['POST'])
def has_joined_giveaway():
	# Get information about the giveaway
	result = request.get_json().get('result')
	
	if giveaway.has_joined(activeUser_id, result.get('giveaway_id')):
		return jsonify(liked=True)
	
	return jsonify(liked=False)

@giveaway_actions_bp.route('/closeGiveaway', methods=['POST'])
def close_giveaway():
	# Get information about the giveaway
	result = request.get_json().get('result')
	
	giveaway.close(result.get('giveaway_id'))
	info_log.info("Successfully closed giveaway with id: %s" % result.get('giveaway_id'))
	
	return jsonify(success=True, message='Successfully closed giveaway!')

@giveaway_actions_bp.route('/chooseWinner', methods=['POST'])
def choose_winner():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the survey
	result = request.get_json().get('result')

	Giveaway.choose_winner(result.get('survey_id'), activeUser_id)
	info_log.info("Successfully anounced winner with id: %s on giveaway with id: %s" % (activeUser_id, result.get('giveaway_id')))

	return jsonify(success=True, message='Successfully anounced winner!')


@giveaway_actions_bp.route('/generateRandomWinner', methods=['POST'])
def generate_random_winner():
	# Get information about the survey
	result = request.get_json().get('result')

	winner_id = Survey.get_random_winner(result.get('giveaway_id'))

	return jsonify(success=True, winner_id = winner_id)
