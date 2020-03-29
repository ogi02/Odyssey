# Built-in imports
import json

# Third party library imports
from flask import Blueprint, request, session, jsonify

# Imports from .py files
from flask_classes.user import User

authentication_bp = Blueprint('authentication_bp', __name__)

@authentication_bp.route('/register', methods=['POST'])
def register():
	# Get information about user
	username = request.get_json().get('username')
	password = request.get_json().get('password')
	name = request.get_json().get('name')
	email = request.get_json().get('email')

	# Put information about user in a tuple
	values = (
		None, 
		username, 
		User.hash_password(password), 
		name,
		email,
		None
	)

	# Create user and update session
	User(*values).create()
	session['LOGGED_IN'] = True
	session['USERNAME'] = username
	# log
	return jsonify(success=True, message='Registration successful!')

@authentication_bp.route('/login', methods=['POST'])
def login():
	# Get information about user and try to find him
	username = request.get_json().get('username')
	password = request.get_json().get('password')
	user = User.find_by_username(username)
	
	# Validate user
	if not user or not user.verify_password(password):
		# log
		return jsonify(success=False, message='Incorrect username or password!'), 403 # forbidden
	
	# Update session
	session['LOGGED_IN'] = True
	session['USERNAME'] = username
	# log
	return jsonify(success=True)

@authentication_bp.route('/logout')
def user_logout():
	# Update session
	session['USERNAME'] = None
	session['LOGGED_IN'] = False
	# log
	return jsonify(success=True, message='successfully logged out')