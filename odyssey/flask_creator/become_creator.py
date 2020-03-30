# Built-in imports 
import json
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, session, jsonify

# Imports from .py files
from flask_classes.user import User
from flask_classes.info import Info
from flask_logging.log_config import info_log, error_log
from flask_classes.creator_specific import CreatorSpecific

become_creator_bp = Blueprint('become_creator_bp', __name__)

@become_creator_bp.route('/becomeCreator', methods=['POST'])
def become_creator():
	# Get user from session
	user = User.get_from_db(session.get('USERNAME'))
	user_id = user.get('_id')

	# Get information about the future creator
	result = request.get_json().get('result')
	
	# Tuple with user's information
	values = (
		None,
		user_id,
		result.get('country_of_residence'),
		result.get('country_for_shipping'),
		result.get('full_name'),
		result.get('address'),
		result.get('suite'),
		result.get('city'),
		result.get('state'),
		result.get('postal_code'),
		result.get('phone_number'),
		result.get('facebook'), 
		result.get('twitter'),
		result.get('instagram'), 
		result.get('webtoon'),
		result.get('twitch'),
		result.get('youtube'),
		result.get('bio'),
		result.get('working_on'),
		None,
		None
	)
	Info(*values).create()

	# Tuple with user's creator specific information
	values = (
		None,
		user_id,
		None,
		None,
		result.get('content_type')
	)
	CreatorSpecific(*values).create()

	info_log.info("%s became a creator." % session.get("USERNAME"))
	
	return jsonify(success=True, message='Successfully updated to creator!')