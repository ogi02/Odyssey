# Third party library imports
from flask import Blueprint, jsonify

# Imports from .py files
from flask_classes.user import User
from flask_classes.active_user import ActiveUser

user_checks_bp = Blueprint('user_checks_bp', __name__)

@user_checks_bp.route("/checkLogin")
def check_login():
	# Check if there is a user logged in
	if ActiveUser.logged_in:
		return jsonify(logged_in=True)

	return jsonify(logged_in=False)

@user_checks_bp.route("/checkCreator")
def check_creator():
	# Check if the current user is creator
	if ActiveUser.logged_in:
		if User.get_from_db(ActiveUser.username).get("role") == "creator":
			return jsonify(is_creator=True)

	return jsonify(is_creator=False)