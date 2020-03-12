from flask import Flask, session
from flask import render_template, request, redirect, url_for
from users import User
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"


class Users(Resource):
	def get(self):
		return User.all()

class Register(Resource):
	def get(self):


	def post(self):


@app.route('/api/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	elif request.method == 'POST':


		values = (
			request.json['username'],
			User.hash_password(request.json['password']),
			request.json['name'],
			request.json['email']
		)
		User(*values).create()

api.add_resource(Users, '/api/users')

if __name__ == "__main__":
	app.run(debug=True)