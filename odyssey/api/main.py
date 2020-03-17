from flask import url_for, send_from_directory
from user import User
import random

from app_config import app, api
from account_management import register
#, login

@app.route("/")
def base():
	return send_from_directory('client/public', 'index.html')

# @app.route("/<path>")
# def home(path):
# 	return send_from_directory('client/public', path + '.html', form = form)

@app.route("/rand")
def hello():
	return str(random.randint(0, 100))

if __name__ == "__main__":
	app.run(debug=True)