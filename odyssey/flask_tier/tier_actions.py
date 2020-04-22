# Built-in imports 
import json
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from flask_classes.user import User
from flask_classes.info import Info
from flask_classes.active_user import ActiveUser
from flask_logging.log_config import info_log, error_log
from flask_classes.tier import Tier

tier_actions_bp = Blueprint('tier_actions_bp', __name__)

@tier_actions_bp.route('/addTier', methods=['POST'])
def create_tier():
	# Get user from session
	user = User.get_from_db(ActiveUser.username)
	user_id = user.get('_id')

	# Get information about the future creator
	result = request.get_json().get('result')
	
	# Tuple with user's information
	values = (
		None,
		user_id,
		result.get('benefits'),
		result.get('price'),
		result.get('name'),
	)
	Tier(*values).create()

	info_log.info("%s added a new tier named %s." % (ActiveUser.username, result.get('name')))
	
	return jsonify(success=True, message='Successfully added new tier!')

@tier_actions_bp.route('/chooseTier', methods=['POST'])
def choose_tier():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the future creator
	result = request.get_json().get('result')
	
	Info.become_patreon(activeUser_id, result.get('creator_id'), result.get('tier_id'))

	info_log.info("%s became patreon with tier %s." % (ActiveUser.username, result.get('tier_id')))
	
	return jsonify(success=True, message='Successfully added new tier!')