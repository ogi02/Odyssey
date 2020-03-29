# Third party library imports
from flask_cors import CORS
from flask import Flask, send_from_directory, jsonify, session

# Blueprint imports
from flask_profile.profile import profile_bp
from flask_creator.become_creator import become_creator_bp
from flask_validators.email_validator import email_validator_bp
from flask_authentication.authentication import authentication_bp
from flask_validators.username_validator import username_validator_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OCML3BRawWEUeaxcuKHLpw'
CORS(app)

app.register_blueprint(profile_bp)
app.register_blueprint(become_creator_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(email_validator_bp)
app.register_blueprint(username_validator_bp)

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

if __name__ == '__main__':
	app.run(debug=True)