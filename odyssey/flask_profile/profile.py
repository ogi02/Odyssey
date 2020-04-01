# Built-in imports
import os
import json
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, session, jsonify

# Imports from .py files
from helpers import allowed_image
from flask_classes.user import User
from flask_classes.info import Info
from flask_logging.log_config import info_log, error_log

profile_bp = Blueprint('profile_bp', __name__)

upload_folder = './client/public/images'

@profile_bp.route('/profile')
def user_profile():
	if(session.get('LOGGED_IN')):
		# Get user from session and information about the user from the database 
		user = User.get_from_db(session.get('USERNAME'))
		user = json.loads(json_util.dumps(user))
		info = Info.find_by_user_id(user.get('_id').get('$oid'))
		info = json.loads(json_util.dumps(info))
		return jsonify(success=True, user = user, info = info)
	return jsonify(success=False)

@profile_bp.route('/FpCerpd9Z7SIbjmN81Jy/upload_picture', methods=['POST'])
def upload_picture():
	# Get image from request
	image = request.files['image']

	# Check image type
	picture_type = request.args.get('type')

	# Get user
	username = session.get('USERNAME')
	
	# Validate image
	if allowed_image(image.filename):
		# Define path where the image will go ('public/images/{user's username}/)
		path = os.path.join(upload_folder, username)

		# Name for the picture
		filename = picture_type + '_picture'
		
		# Check if path exists and create one if it doesn't
		if not os.path.exists(path):
			os.makedirs(path)

		# Save image
		image.save(os.path.join(path, filename))
		info_log.info("New %s picture saved for %s" % (picture_type,username))

		return jsonify(success=True)
		
	else:
		error_log.error("Image extension is not allowed or doesn't exist!")

		return jsonify(success=False, message='Allowed extensions: "pdf", "png", "jpeg", "jpg", "gif".')

@profile_bp.route('/editProfile', methods = ['POST'])
def edit_profile():
	# Get user from session
	username = session.get('USERNAME')

	# Get user's new email and password
	password = request.get_json().get('password')
	email = request.get_json().get('email')
	
	# Change password
	if password:
		User.change_password(username, password)
		info_log.info("Changed password for %s" % username)
	
	# Change email
	if email:
		User.change_email(username, email)
		info_log.info("Changed email for %s" % username)
		
	return jsonify(success=True, message='Profile edited successful!')