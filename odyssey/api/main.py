from flask import send_from_directory, jsonify, request, session
from functools import wraps
from user import User
from flask_cors import CORS

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
	if not username or not password or not name or not email:
		# log
		return jsonify(success=False, message="All inputs are required!"), 403
	if len(password) < 8:
		# log
		return jsonify(success=False, message="Password must be at least 8 characters!"), 403
	if User.find_by_username(username):
		# log
		return jsonify(success=False, message="An account with such username already exists!"), 403
	if User.find_by_email(email):
		# log
		return jsonify(success=False, message="An account with such email already exists!"), 403
	values = (None, username, User.hash_password(password), name, email, None)
	User(*values).create()
	session["LOGGED_IN"] = True
	session["USERNAME"] = username
	# log
	return jsonify(success=True, message="Registration successful!")

@app.route("/login", methods=["POST"])
def login():
	username = request.get_json().get("username")
	password = request.get_json().get("password")
	if not username or not password:
		# log
		return jsonify(success=False, message="All inputs are required!"), 403
	user = User.find_by_username(username)
	if not user or not user.verify_password(password):
		# log
		return jsonify(success=False, message="Incorrect username or password!"), 403
	session["LOGGED_IN"] = True
	session["USERNAME"] = username
	# log
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