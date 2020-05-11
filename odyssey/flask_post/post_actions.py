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
from flask_classes.post import Post
from flask_classes.active_user import ActiveUser
from flask_logging.log_config import info_log, error_log

upload_folder = "./client/public/images"

post_actions_bp = Blueprint('post_actions_bp', __name__)

@post_actions_bp.route('/createPost', methods=['POST'])
def create_post():
	# Get user from session
	username = ActiveUser.username
	user = User.get_from_db(username)
	user_id = user.get('_id')

	# Get image from request
	image = request.files["image"]

	# Check image type
	description = request.args.get("description")
	required_id = request.args.get("required_id")

	# Get time of post creation
	now = datetime.datetime.now()
	
	# Validate image
	if allowed_image(image.filename):

		# Tuple with user's information
		values = (
			None,
			user_id,
			None,
			now, # date
			now.strftime("%m-%d-%Y-%H-%M-%S"), # image_path
			description,
			required_id
		)
		Post(*values).create()

		# Define path where the image will go ("public/images/{user"s username}/)
		path = os.path.join(upload_folder, username)

		# Name for the picture
		filename = now
		
		# Check if path exists and create one if it doesn"t
		if not os.path.exists(path):
			os.makedirs(path)

		# Save image
		image.save(os.path.join(path, now.strftime("%m-%d-%Y-%H-%M-%S")))
		info_log.info("%s added a new post" % username)
	
		return jsonify(success=True, message="%s added a new post" % username)
		
	else:
		error_log.error("Image extension is not allowed or doesn't exist!")

		return jsonify(success=False, message="Allowed extensions: 'pdf', 'png', 'jpeg', 'jpg', 'gif'"), 403


@post_actions_bp.route('/getLikeCount', methods=['POST'])
def get_like_count():
	# Get information about the post
	post_id = request.get_json().get('post_id')

	count = Post.get_likes_count(post_id)
		
	return jsonify(success=True, like_count = count)

@post_actions_bp.route('/likePost', methods=['POST'])
def like_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	post_id = request.get_json().get('post_id')
	
	Post.add_like(activeUser_id, post_id)

	info_log.info("%s liked post with id: %s." % (ActiveUser.username, post_id))
	
	return jsonify(success=True, message='%s liked post with id: %s.' % (ActiveUser.username, post_id))

@post_actions_bp.route('/unlikePost', methods=['POST'])
def unlike_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	post_id = request.get_json().get('post_id')
	
	Post.remove_like(activeUser_id, post_id)

	info_log.info("%s unliked post with id: %s." % (ActiveUser.username, post_id))
	
	return jsonify(success=True, message="%s unliked post with id: %s." % (ActiveUser.username, post_id))

@post_actions_bp.route('/hasLikedPost', methods=['POST'])
def has_liked_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	post_id = request.get_json().get("post_id")

	if Post.has_liked_post(activeUser_id, post_id):
		return jsonify(liked=True)
	
	return jsonify(liked=False)

@post_actions_bp.route('/canViewPost', methods=['POST'])
def can_view_post():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	post_id = request.get_json().get("post_id")
	
	if Post.can_view(activeUser_id, post_id):
		return jsonify(view=True)
	
	return jsonify(view=False)