# Third party library imports
from flask_cors import CORS
from flask_mail import Mail, Message
from flask import Flask, send_from_directory, jsonify, session, render_template

# Imports from .py files
from flask_classes.user import User
from flask_classes.active_user import ActiveUser

# Blueprint imports
from flask_follow.follow import follow_bp
from flask_profile.profile import profile_bp
from flask_tier.tier_actions import tier_actions_bp
from flask_post.post_actions import post_actions_bp
from flask_survey.survey_actions import survey_actions_bp
from flask_creator.become_creator import become_creator_bp
from flask_giveaway.giveaway_actions import giveaway_actions_bp
from flask_validators.email_validator import email_validator_bp
from flask_authentication.authentication import authentication_bp
from flask_validators.username_validator import username_validator_bp
from flask_validators.tier_name_validator import tier_name_validator_bp
from flask_validators.tier_price_validator import tier_price_validator_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mail.odyssey.2020@gmail.com'
app.config['MAIL_PASSWORD'] = 'odyssey2020'
app.config['MAIL_DEFAULT_SENDER'] = 'mail.odyssey.2020@gmail.com'
app.config['MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
CORS(app)

mail = Mail(app)

ActiveUser.logged_in = False
ActiveUser.username = None

# Register blueprints
app.register_blueprint(follow_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(tier_actions_bp)
app.register_blueprint(post_actions_bp)
app.register_blueprint(survey_actions_bp)
app.register_blueprint(become_creator_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(email_validator_bp)
app.register_blueprint(giveaway_actions_bp)
app.register_blueprint(username_validator_bp)
app.register_blueprint(tier_name_validator_bp)
app.register_blueprint(tier_price_validator_bp)

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

@app.route("/checkCreator")
def check_creator():
	# Check if the current user is creator
	if ActiveUser.logged_in:
		if User.get_from_db(ActiveUser.username).get("role") == "creator":
			return jsonify(is_creator=True)

	return jsonify(is_creator=False)

if __name__ == "__main__":
	app.run(debug=True)