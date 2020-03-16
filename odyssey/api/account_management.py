from flask import render_template, redirect, request
from user import User
from form_config import RegistrationForm, LoginForm

from app_config import app, api

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