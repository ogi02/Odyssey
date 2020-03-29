from flask import Flask, send_from_directory, jsonify, request, session
from user import User
from flask_cors import CORS
from info import Info
from bson import json_util, ObjectId
import json
from creatorSpecific import CreatorSpecific
import os
from werkzeug.utils import secure_filename
from flask import Flask
from helpers import allowed_image

upload_folder = './client/public/images'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OCML3BRawWEUeaxcuKHLpw'
CORS(app)

@app.route('/')
def base():
	return send_from_directory('client/public', 'index.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
	return send_from_directory('client/public', path)

@app.route('/checkLogin')
def check_login():
	if session.get('LOGGED_IN'):
		print('There is a user logged in')
		return jsonify(logged_in=True)
	print('There is not a user logged in')
	return jsonify(logged_in=False)

@app.route('/register', methods=['POST'])
def register():
	username = request.get_json().get('username')
	password = request.get_json().get('password')
	name = request.get_json().get('name')
	email = request.get_json().get('email')

	values = (
		None, 
		username, 
		User.hash_password(password), 
		name,
		email,
		None
	)

	User(*values).create()
	session['LOGGED_IN'] = True
	session['USERNAME'] = username
	# log
	return jsonify(success=True, message='Registration successful!')

@app.route('/editProfile', methods = ['POST'])
def edit_profile():
	username = session.get('USERNAME')
	password = request.get_json().get('password')
	email = request.get_json().get('email')
	if password:
		User.change_password(username, password)
	
	if email:
		User.change_email(username, email)
	
	return jsonify(success=True, message='Profile edited successful!')

@app.route('/becomeCreator', methods=['POST'])
def become_creator():
	user = User.get_from_db(session.get('USERNAME'))
	user_id = user.get('_id')
	result = request.get_json().get('result')
	
	values = (
		None,
		user_id,
		result.get('country_of_residence'),
		result.get('country_for_shipping'),
		result.get('full_name'),
		result.get('address'),
		result.get('suite'),
		result.get('city'),
		result.get('state'),
		result.get('postal_code'),
		result.get('phone_number'),
		result.get('facebook'), 
		result.get('twitter'),
		result.get('instagram'), 
		result.get('webtoon'),
		result.get('twitch'),
		result.get('youtube'),
		result.get('bio'),
		result.get('working_on'),
		None,
		None
	)
	Info(*values).create()

	values = (
		None,
		user_id,
		None,
		None,
		result.get('content_type')
	)
	CreatorSpecific(*values).create()

	# log
	return jsonify(success=True, message='Successfully updated to creator!')

@app.route('/login', methods=['POST'])
def login():
	username = request.get_json().get('username')
	password = request.get_json().get('password')
	user = User.find_by_username(username)
	if not user or not user.verify_password(password):
		# log
		return jsonify(success=False, message='Incorrect username or password!'), 403	# forbidden
	session['LOGGED_IN'] = True
	session['USERNAME'] = username
	# log
	return jsonify(success=True)

@app.route('/FpCerpd9Z7SIbjmN81Jy/username', methods=['POST'])
def check_username():
	username = request.get_json().get('username')
	user = User.find_by_username(username)
	if user:
		return jsonify(success=False, message='An account with such username already exists!')
	return jsonify(success=True)

@app.route('/FpCerpd9Z7SIbjmN81Jy/email', methods=['POST'])
def check_email():
	email = request.get_json().get('email')
	user = User.find_by_email(email)
	if user:
		return jsonify(success=False, message='An account with such email already exists!')
	return jsonify(success=True)

@app.route('/FpCerpd9Z7SIbjmN81Jy/upload_picture', methods=['POST'])
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

@app.route('/logout')
def user_logout():
	session['USERNAME'] = None
	session['LOGGED_IN'] = False
	# log
	return jsonify(success=True, message='successfully logged out')

@app.route('/profile')
def user_profile():
	if(session.get('LOGGED_IN')):
		user = User.get_from_db(session.get('USERNAME'))
		user = json.loads(json_util.dumps(user))
		info = Info.find_by_user_id(user.get('_id').get('$oid'))
		info = json.loads(json_util.dumps(info))

		return jsonify(success=True, user = user, info = info)
	return jsonify(success=False)

if __name__ == '__main__':
	app.run(debug=True)