from flask import send_from_directory, jsonify, request, session
from user import User

from flask import Flask

app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"

@app.route("/")
def base():
	return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
	return send_from_directory('client/public', path)

@app.route("/register", methods=["POST"])
def register():
	username = request.get_json().get("username")
	password = request.get_json().get("password")
	name = request.get_json().get("name")
	email = request.get_json().get("email")
	if User.find_by_username(username):
		# log
		return jsonify(success=False, message="An account with such username already exists!")
	if User.find_by_email(email):
		# log
		return jsonify(success=False, message="An account with such email already exists!")
	values = (username, User.hash_password(password), name, email)
	User(*values).create()
	session["LOGGED_IN"] = True
	session["USERNAME"] = username
	# log
	return jsonify(success=True, message="Registration successful!")

@app.route("/login", methods=["POST"])
def login():
	username = request.get_json().get("username")
	password = request.get_json().get("password")
	print(username)
	print(password)
	user = User.find_by_username(username)
	if not user or not user.verify_password(password):
		print("ne vlezna")
		# log
		return jsonify(success=False, message="Incorrect username or password!")
	session["LOGGED_IN"] = True
	session["USERNAME"] = username
	print("vlezna")
	# log
	return jsonify(success=True, message="Login successful!")

@app.route("/rand")
def hello():
	return str(random.randint(0, 100))

if __name__ == "__main__":
	app.run(debug=True)