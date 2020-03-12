from flask import Flask, session
from flask import render_template, request, redirect, url_for, make_response
from users import User
from flask_restful import Resource, Api
from form_config import RegistrationForm, LoginForm

app = Flask(__name__)
api = Api(app)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"


class Users(Resource):
	def get(self):
		return User.all()

@app.route('/api/register', methods=["GET", "POST"])
def register():
	form = RegistrationForm()

	if form.validate_on_submit():
		values = (
			request.form['username'],
			User.hash_password(request.form['password']),
			request.form['name'],
			request.form['email']
		)
		User(*values).create()
		# success log
		return redirect('/api/users')
	# else:
		# error log

	return render_template('register.html', form = form)

@app.route('/api/login', methods=["GET", "POST"])
def login():
	form = LoginForm()

	if form.validate_on_submit():		
		# success log
		return redirect('/api/users')
	# else:
		# error lor

	return render_template('login.html', form = form)

api.add_resource(Users, '/api/users')

if __name__ == "__main__":
	app.run(debug=True)