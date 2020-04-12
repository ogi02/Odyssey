# Third party library imports
from flask_cors import CORS
from flask_session import Session
from flask import Flask, send_from_directory, jsonify, session

# Imports from .py files
from flask_classes.active_user import ActiveUser

# Blueprint imports
from flask_follow.follow import follow_bp
from flask_profile.profile import profile_bp
from flask_profile.tier_actions import tier_actions_bp
from flask_creator.become_creator import become_creator_bp
from flask_validators.email_validator import email_validator_bp
from flask_authentication.authentication import authentication_bp
from flask_validators.username_validator import username_validator_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
CORS(app)

ActiveUser.logged_in = False
ActiveUser.username = None

# Register blueprints
app.register_blueprint(follow_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(tier_actions_bp)
app.register_blueprint(become_creator_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(email_validator_bp)
app.register_blueprint(username_validator_bp)

@app.route("/")
def base():
	# Main path
	return send_from_directory("client/public", "index.html")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def home(path):
	# Default path
	return send_from_directory("client/public", path)

@app.route("/checkLogin")
def check_login():
	# Check if there is a user logged in
	if ActiveUser.logged_in:
		return jsonify(logged_in=True)
		
	return jsonify(logged_in=False)

if __name__ == "__main__":
	app.run(debug=True)