# Built-in imports
import json
import pymongo

# Third party library imports
from flask_mail import Message
from flask import Blueprint, request, jsonify, render_template, redirect, session

from database_config import CLIENT_URL, FLASK_RUN_PORT, FLASK_RUN_HOST

# Imports from .py files
import main
from flask_classes.user import User
from flask_classes.info import Info
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
		None,
		False
	)

	try:
		# Create user and update session
		User(*values).create()

		user_id = User.get_from_db(username).get('_id')

		Info.create(user_id)

		info_log.info("User %s registered successfully." % username)

		if main.app.config['TESTING'] == False:
			msg = Message('Testing Email Verification', recipients = [email],
				html = render_template('activation_email.html', username = username, host = FLASK_RUN_HOST, port = FLASK_RUN_PORT))
			main.mail.send(msg)
			info_log.info("Sent activation email to %s" % username)
		
		return jsonify(success=True, message="Registration successful")

	except pymongo.errors.DuplicateKeyError as e:
		# Catch pymongo exception
		key = list(e.details.get('keyValue').keys())[0]
		value = e.details.get('keyValue').get(key)
		error_log.error("Duplicate %s: %s" % (key, value))

		return jsonify(success=False, message="Duplicate %s: %s" % (key, value)), 403 # forbidden

@authentication_bp.route("/verify/<username>", methods=["GET"])
def verify_account(username):

	User.verify_account(username)
	return redirect(CLIENT_URL + "/login")

@authentication_bp.route("/login", methods=["POST"])
def login():

	# Get information about user and try to find him
	username = request.json.get("username")
	password = request.json.get("password")
	user = User.find_by_username(username)
	
	# Validate user
	if not user or not user.verify_password(password):
		error_log.error("Login failed!")
		
		return jsonify(success=False, message="Incorrect username or password"), 403 # forbidden

	# Check if user is verified
	if user.verified == False:
		error_log.error("Login failed!")
		
		return jsonify(success=False, message="Account is not verified!"), 403 # forbidden

	# Update session
	session["LOGGED_IN"] = True
	session["USERNAME"] = username
	info_log.info("%s logged in successfully" % username)

	print('success')

	return jsonify(success=True, message="%s logged in successfully" % username)

@authentication_bp.route("/logout")
def user_logout():
	# Update session
	session["LOGGED_IN"] = False
	session["USERNAME"] = None
	info_log.info("User logged out")

	return jsonify(success=True, message="User logged out")