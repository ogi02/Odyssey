# Built-in imports
import json

# Third party library imports
from flask import Blueprint, request, jsonify, session

# Imports from .py files
from flask_classes.user import User
from flask_classes.tier import Tier

tier_price_validator_bp = Blueprint('tier_price_validator_bp', __name__)

@tier_price_validator_bp.route('/FpCerpd9Z7SIbjmN81Jy/tier_price', methods=['POST'])
def check_tier_name():
	# Get current user
	user_id = User.get_from_db(session.get("USERNAME")).get('_id')

	# Get tier name from request
	tier_price = request.get_json().get('tier_price')

	# If tier with that such price exists, return duplication error
	tier = Tier.find_by_price(user_id, tier_price)
	print(tier)
	if tier:
		return jsonify(success=False, message='Tier price already used!')

	return jsonify(success=True, message='Tier price %s is not taken' % tier_price)