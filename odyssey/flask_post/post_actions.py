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
from flask_classes.post import Post

post_actions_bp = Blueprint('post_actions_bp', __name__)

@post_actions_bp.route('/createPost', methods=['POST'])
def create_post():
	# Get user from session
	user = User.get_from_db(ActiveUser.username)
	user_id = user.get('_id')

	# Get information about the future post
	result = request.get_json().get('result')
	
	# Tuple with user's information
	values = (
		None,
		user_id,
		None,
		datetime.datetime.now(),
		result.get('image_path'),
		result.get('text'),
		result.get('restriction_type_id')
	)
	Post(*values).create()

	info_log.info("%s added a new post" % ActiveUser.username)
	
	return jsonify(success=True, message='Successfully created a new post!')

@post_actions_bp.route('/getLikeCount', methods=['POST'])
def get_like_count():
	
	# Get information about the post
	result = request.get_json().get('result')
	count = Post.get_likes_count(result.get('post_id'))
		
	return jsonify(success=True, count = count)

@post_actions_bp.route('/likePost', methods=['POST'])
def like_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	result = request.get_json().get('result')
	
	Post.add_like(activeUser_id, result.get('post_id'))

	info_log.info("%s liked post with id: %s." % (ActiveUser.username, result.get('post_id')))
	
	return jsonify(success=True, message='Successfully liked post!')

@post_actions_bp.route('/unlikePost', methods=['POST'])
def unlike_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	result = request.get_json().get('result')
	
	Post.remove_like(activeUser_id, result.get('post_id'))

	info_log.info("%s unliked post with id: %s." % (ActiveUser.username, result.get('post_id')))
	
	return jsonify(success=True, message='Successfully unliked post!')

@post_actions_bp.route('/hasLikedPost', methods=['POST'])
def has_liked_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	result = request.get_json().get('result')
	
	if Post.has_liked_post(activeUser_id, result.get('post_id')):
		return jsonify(liked=True)
	
	return jsonify(liked=False)

@post_actions_bp.route('/canViewPost', methods=['POST'])
def can_view_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	result = request.get_json().get('result')
	
	if Post.can_view(activeUser_id, result.get('post_id')):
		return jsonify(liked=True)
	
	return jsonify(liked=False)