from flask import send_from_directory, redirect, request
from user import User
from form_config import RegistrationForm, LoginForm

from app_config import app, api

@app.route('/register', methods=["GET", "POST"])
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

	return send_from_directory('client/public', 'register.html', form = form)

@app.route('/login', methods=["GET", "POST"])
def login():
	form = LoginForm()

	if form.validate_on_submit():		
		# success log
		return redirect('/api/users')
	# else:
		# error lor

	return render_template('login.html', form = form)