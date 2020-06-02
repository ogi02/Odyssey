# Built-in imports
import json

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from flask_classes.user import User
from flask_classes.tier import Tier
from flask_classes.active_user import ActiveUser

tier_name_validator_bp = Blueprint('tier_name_validator_bp', __name__)

@tier_name_validator_bp.route('/FpCerpd9Z7SIbjmN81Jy/tier_name', methods=['POST'])
def check_tier_name():
	# Get current user
	user_id = User.get_from_db(ActiveUser.username).get('_id')

	# Get tier name from request
	tier_name = request.get_json().get('tier_name')

	# If tier with that such name exists, return duplication error
	tier = Tier.find_by_name(user_id, tier_name)
	if tier:
		return jsonify(success=False, message='Tier name already used!')

	return jsonify(success=True, message='Tier name %s is not taken' % tier_name)