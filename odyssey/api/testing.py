from flask import Flask, session
from flask import render_template, request, session, redirect, url_for
from users import User

app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"


@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	elif request.method == 'POST':


		values = (
			request.form['username'],
			User.hash_password(request.form['password']),
			request.form['name'],
			request.form['email']
		)
		User(*values).create()


		   
		