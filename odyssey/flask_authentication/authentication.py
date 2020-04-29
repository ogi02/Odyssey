# Built-in imports
import json
import pymongo

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from flask_classes.user import User
from flask_classes.active_user import ActiveUser
from flask_logging.log_config import info_log, error_log

authentication_bp = Blueprint("authentication_bp", __name__)

@authentication_bp.route("/register", methods=["POST"])
def register():
	# Get information about user
	username = request.get_json().get("username")
	password = request.get_json().get("password")
	name = request.get_json().get("name")
	email = request.get_json().get("email")

	# Put information about user in a tuple
	values = (
		None, 
		username, 
		User.hash_password(password), 
		name,
		email,
		None
	)

	try:
		# Create user and update session
		User(*values).create()
		ActiveUser.logged_in = True
		ActiveUser.username = username
		info_log.info("User %s registered successfully." % username)

		return jsonify(success=True, message="Registration successful")

	except pymongo.errors.DuplicateKeyError as e:
		# Catch pymongo exception
		key = list(e.details.get('keyValue').keys())[0]
		value = e.details.get('keyValue').get(key)
		error_log.error("Duplicate %s: %s" % (key, value))
		return jsonify(success=False, message="Duplicate %s: %s" % (key, value)), 403


@authentication_bp.route("/login", methods=["POST"])
def login():
	# Get information about user and try to find him
	username = request.get_json().get("username")
	password = request.get_json().get("password")
	user = User.find_by_username(username)
	
	# Validate user
	if not user or not user.verify_password(password):
		error_log.error("Login failed!")
		
		return jsonify(success=False, message="Incorrect username or password"), 403 # forbidden
	
	# Update session
	ActiveUser.logged_in = True
	ActiveUser.username = username
	info_log.info("%s logged in successfully" % username)

	return jsonify(success=True, message="%s logged in successfully" % username)

@authentication_bp.route("/logout")
def user_logout():
	# Update session
	username = ActiveUser.username
	ActiveUser.logged_in = False
	ActiveUser.username = None
	info_log.info("%s logged out" % username)

	return jsonify(success=True, message="%s logged out" % username)