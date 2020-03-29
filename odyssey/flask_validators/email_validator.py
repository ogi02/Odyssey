# Built-in imports
import json

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from flask_classes.user import User

email_validator_bp = Blueprint('email_validator_bp', __name__)

@email_validator_bp.route('/FpCerpd9Z7SIbjmN81Jy/email', methods=['POST'])
def check_email():
	email = request.get_json().get('email')
	user = User.find_by_email(email)
	if user:
		return jsonify(success=False, message='An account with such email already exists!')
	return jsonify(success=True)