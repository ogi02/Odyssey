# Built-in imports
import os
import json
from bson import json_util, ObjectId

# Third party library imports
from flask import Blueprint, request, session, jsonify

# Imports from .py files
from helpers import allowed_image
from flask_classes.user import User
from flask_classes.info import Info

profile_bp = Blueprint('profile_bp', __name__)

upload_folder = './client/public/images'

@profile_bp.route('/profile')
def user_profile():
	if(session.get('LOGGED_IN')):
		user = User.get_from_db(session.get('USERNAME'))
		user = json.loads(json_util.dumps(user))
		info = Info.find_by_user_id(user.get('_id').get('$oid'))
		info = json.loads(json_util.dumps(info))

		return jsonify(success=True, user = user, info = info)
	return jsonify(success=False)

@profile_bp.route('/FpCerpd9Z7SIbjmN81Jy/upload_picture', methods=['POST'])
def upload_picture():
	image = request.files['image']
	picture_type = request.args.get('type')
	username = session.get('USERNAME')
	if allowed_image(image.filename):
		path = os.path.join(upload_folder, username)
		filename = picture_type + '_picture'
		if not os.path.exists(path):
			os.makedirs(path)
		image.save(os.path.join(path, filename))
		return jsonify(success=True)
	else:
		return jsonify(success=False, message='Allowed extensions: "pdf", "png", "jpeg", "jpg", "gif".')

@profile_bp.route('/editProfile', methods = ['POST'])
def edit_profile():
	username = session.get('USERNAME')
	password = request.get_json().get('password')
	email = request.get_json().get('email')
	if password:
		User.change_password(username, password)
	
	if email:
		User.change_email(username, email)
	
	return jsonify(success=True, message='Profile edited successful!')