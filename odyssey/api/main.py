from flask import send_from_directory, jsonify, request, session
from functools import wraps
from user import User
from flask_cors import CORS
from info import Info
from creatorSpecific import CreatorSpecific

from flask import Flask

app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"
CORS(app)

def require_login(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		# if there isn't a logged user
		if not session.get("SIGNED_IN"):
			return redirect('/login')
		return func(*args, **kwargs)
	return wrapper

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
	user = user.find_by_username("USERNAME")
	user_id = user._id
	full_name = request.get_json().get("full_name")
	country_of_residence = request.get_json().get("country_of_residence")
	country_for_shipping = request.get_json().get("country_for_shipping")
	address = request.get_json().get("address")
	suite = request.get_json().get("suite")
	city = request.get_json().get("city")
	state = request.get_json().get("state")
	postal_code = request.get_json().get("postal_code")
	phone_number = request.get_json().get("phone_number")
	facebook = request.get_json().get("facebook")
	twitter = request.get_json().get("twitter")
	instagram = request.get_json().get("instagram")
	webtoon = request.get_json().get("webtoon")
	twitch = request.get_json().get("twitch")
	youtube = request.get_json().get("youtube")
	bio = request.get_json().get("bio")


	values = (
		None,
		user_id,
		country_of_residence,
		country_for_shipping,
		full_name,
		address,
		suite,
		city,
		state,
		postal_code,
		phone_number,
		facebook, twitter,
		instagram, webtoon,
		twitch,
		youtube,
		bio,
		None,
		None
	)
	Info(*values).create()

	content_type = request.get_json().get("content_type")

	values = (
		None,
		user_id,
		None,
		None,
		content_type
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
@require_login
def user_logout():
	session["USERNAME"] = None
	session["LOGGED_IN"] = False
	# log
	return jsonify(success=True, message="successfully logged out")


if __name__ == "__main__":
	app.run(debug=True)