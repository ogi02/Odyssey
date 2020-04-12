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
from flask_classes.creator_specific import CreatorSpecific

become_creator_bp = Blueprint('become_creator_bp', __name__)

@become_creator_bp.route('/becomeCreator', methods=['POST'])
def become_creator():
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

	info_log.info("%s added a new tier named %s." % (ActiveUser.username, return)
	
	return jsonify(success=True, message='Successfully updated to creator!')