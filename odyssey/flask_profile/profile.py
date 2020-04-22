# Built-in imports
import os
import json
from bson import json_util, ObjectId

# Third party library imports
from flask_session import Session
from flask import Blueprint, request, session, jsonify

# Imports from .py files
from helpers import allowed_image
from flask_classes.user import User
from flask_classes.info import Info
from flask_classes.tier import Tier
from flask_classes.active_user import ActiveUser
from flask_logging.log_config import info_log, error_log

profile_bp = Blueprint("profile_bp", __name__)

upload_folder = "./client/public/images"

@profile_bp.route("/profile")
def my_profile():
	if ActiveUser.logged_in:
		# Get user from session and information about the user from the database 
		user = User.get_from_db(ActiveUser.username)
		user = json.loads(json_util.dumps(user))
		
		if user.get('is_creator'):
			info = Info.find_by_user_id(user.get("_id").get("$oid"))
			info = json.loads(json_util.dumps(info))

			tier = Tier.find_all_by_user_id(user.get("_id").get("$oid"))
			tier = json.loads(json_util.dumps(tier))

			return jsonify(success=True, user = user, info = info, tier = tier)
			
		return jsonify(success=True, user = user)
		
	return jsonify(success=False)

@profile_bp.route("/profile/<username>", methods=["POST"])
def user_profile(username):
	searchedUser = User.get_from_db(username)
	searchedUser = json.loads(json_util.dumps(searchedUser))
	searchedUser_id = searchedUser.get('_id').get('$oid')

	activeUser = User.get_from_db(ActiveUser.username)
	activeUser = json.loads(json_util.dumps(activeUser))
	activeUser_id = activeUser.get('_id').get('$oid')

	if searchedUser.get('is_creator'):
		# Get info is user is creator
		info = Info.find_by_user_id(searchedUser_id)
		info = json.loads(json_util.dumps(info))

		tier = Tier.find_all_by_user_id(searchedUser_id)
		tier = json.loads(json_util.dumps(tier))

		if Info.is_patreon(searchedUser_id, activeUser_id):
			# Get tier id of chosen tier
			tier_id = get_tier_id(searchedUser_id, activeUser_id)

			return jsonify(success = True, user = searchedUser, info = info, tier = tier, tier_id = tier_id)
		
		return jsonify(success = True, user = searchedUser, info = info, tier = tier)

	return jsonify(success = True, user = searchedUser)

@profile_bp.route("/FpCerpd9Z7SIbjmN81Jy/upload_picture", methods=["POST"])
def upload_picture():
	# Get image from request
	image = request.files["image"]

	# Check image type
	picture_type = request.args.get("type")

	# Get user
	username = ActiveUser.username
	
	# Validate image
	if allowed_image(image.filename):
		# Define path where the image will go ("public/images/{user"s username}/)
		path = os.path.join(upload_folder, username)

		# Name for the picture
		filename = picture_type + "_picture"
		
		# Check if path exists and create one if it doesn"t
		if not os.path.exists(path):
			os.makedirs(path)

		# Save image
		image.save(os.path.join(path, filename))
		info_log.info("New %s picture saved for %s" % (picture_type,username))

		return jsonify(success=True)
		
	else:
		error_log.error("Image extension is not allowed or doesn't exist!")

		return jsonify(success=False, message="Allowed extensions: 'pdf', 'png', 'jpeg', 'jpg', 'gif'.")

@profile_bp.route("/editProfile", methods = ["POST"])
def edit_profile():
	# Get user from session
	username = ActiveUser.username

	# Get user"s new email and password
	password = request.get_json().get("password")
	email = request.get_json().get("email")
	
	# Change password
	if password:
		User.change_password(username, password)
		info_log.info("Changed password for %s" % username)
	
	# Change email
	if email:
		User.change_email(username, email)
		info_log.info("Changed email for %s" % username)
		
	return jsonify(success=True, message="Profile edited successful!")

@profile_bp.route("/FpCerpd9Z7SIbjmN81Jy/getUsernames", methods = ["POST"])
def get_usernames():
	# Get current input state
	value = request.get_json().get("value")

	usernames = User.get_searched_usernames(value, ActiveUser.username)

	return jsonify(success = True, usernames = usernames)