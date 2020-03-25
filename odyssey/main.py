from flask import Flask, send_from_directory, jsonify, request, session
from user import User
from flask_cors import CORS
from info import Info
from bson import json_util, ObjectId
import json
from creatorSpecific import CreatorSpecific

from flask import Flask

app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"
CORS(app)

@app.route("/")
def base():
	return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
	return send_from_directory('client/public', path)

@app.route("/checkLogin")
def check_login():
	if session.get("LOGGED_IN"):
		print("There is a user logged in")
		return jsonify(logged_in=True)
	print("There is not a user logged in")
	return jsonify(logged_in=False)

@app.route("/register", methods=["POST"])
def register():
	username = request.get_json().get("username")
	password = request.get_json().get("password")
	name = request.get_json().get("name")
	email = request.get_json().get("email")

	values = (
		None, 
		username, 
		User.hash_password(password), 
		name,
		email,
		None
	)

	User(*values).create()
	session["LOGGED_IN"] = True
	session["USERNAME"] = username
	# log
	return jsonify(success=True, message="Registration successful!")

@app.route("/becomeCreator", methods=["POST"])
def become_creator():
	user = User.get_from_db(session.get("USERNAME"))
	user_id = user.get('_id')
	result = request.get_json().get("result")
	
	values = (
		None,
		user_id,
		result.get("country_of_residence"),
		result.get("country_for_shipping"),
		result.get("full_name"),
		result.get("address"),
		result.get("suite"),
		result.get("city"),
		result.get("state"),
		result.get("postal_code"),
		result.get("phone_number"),
		result.get("facebook"), 
		result.get("twitter"),
		result.get("instagram"), 
		result.get("webtoon"),
		result.get("twitch"),
		result.get("youtube"),
		result.get("bio"),
		result.get("working_on"),
		None,
		None
	)
	Info(*values).create()

	values = (
		None,
		user_id,
		None,
		None,
		result.get("content_type")
	)
	CreatorSpecific(*values).create()

	# log
	return jsonify(success=True, message="Successfully updated to creator!")

@app.route("/login", methods=["POST"])
def login():
	username = request.get_json().get("username")
	password = request.get_json().get("password")
	user = User.find_by_username(username)
	if not user or not user.verify_password(password):
		# log
		return jsonify(success=False, message="Incorrect username or password!"), 403	# forbidden
	session["LOGGED_IN"] = True
	session["USERNAME"] = username
	# log
	return jsonify(success=True)

@app.route("/FpCerpd9Z7SIbjmN81Jy/username", methods=["POST"])
def check_username():
	username = request.get_json().get("username")
	user = User.find_by_username(username)
	if user:
		return jsonify(success=False, message="An account with such username already exists!")
	return jsonify(success=True)

@app.route("/FpCerpd9Z7SIbjmN81Jy/email", methods=["POST"])
def check_email():
	email = request.get_json().get("email")
	user = User.find_by_email(email)
	if user:
		return jsonify(success=False, message="An account with such email already exists!")
	return jsonify(success=True)

@app.route("/logout")
def user_logout():
	session["USERNAME"] = None
	session["LOGGED_IN"] = False
	# log
	return jsonify(success=True, message="successfully logged out")

@app.route("/profile")
def user_profile():
	user = User.get_from_db(session.get("USERNAME"))
	user = json.loads(json_util.dumps(user))
	info = Info.find_by_user_id(user.get('_id').get("$oid"))
	info = json.loads(json_util.dumps(info))

	return jsonify(user = user, info = info)

if __name__ == "__main__":
	app.run(debug=True)