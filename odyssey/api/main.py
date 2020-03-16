from flask import url_for
from user import User
from flask_restful import Resource

from app_config import app, api
from account_management import register, login

class Users(Resource):
	def get(self):
		return User.all()

api.add_resource(Users, '/api/users')

if __name__ == "__main__":
	app.run(debug=True)