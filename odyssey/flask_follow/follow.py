# Built-in imports 
import json
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, jsonify, session

# Imports from .py files
from flask_classes.user import User
from flask_classes.info import Info
from flask_logging.log_config import info_log, error_log

follow_bp = Blueprint('follow_bp', __name__)

@follow_bp.route('/follow', methods=['POST'])
def follow():
	# Get user from session
	user = User.get_from_db(session.get("USERNAME"))
	user_id = user.get('_id')

	# Get information about the profile to be followed
	result = request.get_json().get('result')
	profile_name = result.get('profile_name')
	user_to_follow = User.get_from_db(profile_name)
	profile_id = user_to_follow.get('_id')

	# Update in DB
	Info.follow(user_id, profile_id)

	# Log
	info_log.info("%s started following %s" % (user.get('username'), profile_name))
	
	return jsonify(success=True, message="%s started following %s" % (user.get('username'), profile_name))

@follow_bp.route('/unfollow', methods=['POST'])
def unfollow():
	# Get user from session
	user = User.get_from_db(session.get("USERNAME"))
	user_id = user.get('_id')

	# Get information about the profile to be followed
	result = request.get_json().get('result')
	profile_name = result.get('profile_name')
	user_to_follow = User.get_from_db(profile_name)
	profile_id = user_to_follow.get('_id')

	# Update in DB
	Info.unfollow(user_id,profile_id)

	# Log
	info_log.info("%s stopped following %s" % (user.get('username'), profile_name))
	
	return jsonify(success=True, message="%s stopped following %s" % (user.get('username'), profile_name))

@follow_bp.route('/isFollowing', methods=['POST'])
def is_following():
	# Get user from session
	user = User.get_from_db(session.get("USERNAME"))
	user_id = user.get('_id')

	# Get information about the profile to be followed
	result = request.get_json().get('result')
	profile_name = result.get('profile_name')
	user_to_follow = User.get_from_db(profile_name)
	profile_id = user_to_follow.get('_id')

	# Update in DB
	if Info.is_following(user_id, profile_id):
		return jsonify(following=True)

	return jsonify(following=False)
