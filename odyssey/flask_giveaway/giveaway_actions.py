# Built-in imports
import os
import json
import datetime
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, jsonify

# Imports from .py files
from helpers import allowed_image
from flask_classes.user import User
from flask_classes.info import Info
from flask_classes.giveaway import Giveaway
from flask_classes.active_user import ActiveUser
from flask_logging.log_config import info_log, error_log

upload_folder = "./client/public/images"

giveaway_actions_bp = Blueprint('giveaway_actions_bp', __name__)

@giveaway_actions_bp.route('/createGiveaway', methods=['POST'])
def create_giveaway():
	# Get user from session
	username = ActiveUser.username
	user = User.get_from_db(username)
	user_id = user.get('_id')

	# Get image from request
	image = request.files["image"]

	# Check image type
	description = request.args.get("description")
	required_id = request.args.get("required_id")

	# Get time of post creation
	now = datetime.datetime.now()
	
	# Validate image
	if allowed_image(image.filename):

		values = (
			None,
			user_id,
			None,
			now, # date
			now.strftime("%m-%d-%Y-%H-%M-%S"), # image_path
			description,
			required_id,
			True,
			None, # deadline
			None
		)
		Giveaway(*values).create()

		# Define path where the image will go ("public/images/{user"s username}/)
		path = os.path.join(upload_folder, username)

		# Name for the picture
		filename = now
		
		# Check if path exists and create one if it doesn"t
		if not os.path.exists(path):
			os.makedirs(path)

		# Save image
		image.save(os.path.join(path, now.strftime("%m-%d-%Y-%H-%M-%S")))
		info_log.info("%s added a new giveaway" % username)
	
		return jsonify(success=True, message="%s added a new giveaway" % username)
		
	else:
		error_log.error("Image extension is not allowed or doesn't exist!")

		return jsonify(success=False, message="Allowed extensions: 'pdf', 'png', 'jpeg', 'jpg', 'gif'"), 403

@giveaway_actions_bp.route('/getTotalContestantsCount', methods=['POST'])
def get_total_contestants_count():
	# Get information about the giveaway
	giveaway_id = request.get_json().get('giveaway_id')
	count = Giveaway.get_all_contestants_count(giveaway_id)
		
	return jsonify(success=True, participant_count = count)

@giveaway_actions_bp.route('/joinGiveaway', methods=['POST'])
def join_giveaway():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the giveaway
	giveaway_id = request.get_json().get('giveaway_id')
	
	Giveaway.join_giveaway(activeUser_id, giveaway_id)

	info_log.info("%s joined giveaway with id: %s." % (ActiveUser.username, giveaway_id))
	
	return jsonify(success=True, message='Successfully joined giveaway!')

@giveaway_actions_bp.route('/hasJoinedGiveaway', methods=['POST'])
def has_joined_giveaway():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the giveaway
	giveaway_id = request.get_json().get('giveaway_id')
	
	if Giveaway.has_joined(activeUser_id, giveaway_id):
		return jsonify(joined=True)
	
	return jsonify(joined=False)

@giveaway_actions_bp.route('/canViewGiveaway', methods=['POST'])
def can_view_giveaway():
	# Get user from session
	activeUser = User.get_from_db(ActiveUser.username)
	activeUser_id = activeUser.get('_id')

	# Get information about the post
	giveaway_id = request.get_json().get('giveaway_id')
	
	if Giveaway.can_view(activeUser_id, giveaway_id):
		return jsonify(view=True)
	
	return jsonify(view=False)

@giveaway_actions_bp.route('/closeGiveaway', methods=['POST'])
def close_giveaway():
	# Get information about the giveaway
	giveaway_id = request.get_json().get('giveaway_id')
	
	Giveaway.close(giveaway_id)
	info_log.info("Successfully closed giveaway with id: %s" % giveaway_id)
	
	return jsonify(success=True, message='Successfully closed giveaway!')

@giveaway_actions_bp.route('/chooseGiveawayWinner', methods=['POST'])
def choose_winner():
	# Get information about the survey
	winner_id = request.get_json().get('winner_id')
	giveaway_id = request.get_json().get('giveaway_id')

	winner = User.find_by_id(winner_id)

	Giveaway.choose_winner(giveaway_id, winner.get('username'))

	info_log.info("Successfully announced winner %s on giveaway with id: %s" % (winner.get('username'), giveaway_id))

	return jsonify(success=True, message='Successfully announced winner!', winner = winner.get('username'))

@giveaway_actions_bp.route('/generateRandomWinner', methods=['POST'])
def generate_random_winner():
	# Get information about the survey
	giveaway_id = request.get_json().get('giveaway_id')

	winner_id = Giveaway.get_random_winner(giveaway_id)

	return jsonify(success=True, winner_id = str(winner_id))
