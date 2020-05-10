# Built-in imports
import json

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from flask_classes.user import User

username_validator_bp = Blueprint('username_validator_bp', __name__)

@username_validator_bp.route('/FpCerpd9Z7SIbjmN81Jy/username', methods=['POST'])
def check_username():
	# Get username from request
	username = request.get_json().get('username')

	# If user with that username exists, return duplication error
	user = User.find_by_username(username)
	if user:
		return jsonify(success=False, message='Username already taken!')
		
	return jsonify(success=True, message='Username %s is not taken' % username)