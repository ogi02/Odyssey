from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, EqualTo, Length, NoneOf, ValidationError

from user import User

# registration form
class RegistrationForm(FlaskForm):
    # username -> input type - string, required, unique
    username = StringField("username", [InputRequired(), NoneOf(User.all_usernames(), message = "An user with this username already exists!")], render_kw={"placeholder": "Username"})

    # password -> input type - password, required, at least 8 characters long
    password = PasswordField("password", [InputRequired(), Length(min = 8, message = "Password must be at least 8 characters!")], render_kw={"placeholder": "Password"})

    # confirm -> input type - password, equal to password
    confirm = PasswordField("confirm", [EqualTo("password", message = "Passwords must match!")], render_kw={"placeholder": "Confirm Password"})

    # name -> input type - string, required
    name = StringField("name", [InputRequired()], render_kw={"placeholder": "Name"})

    # email -> input type - email, required
    email = StringField("email", [InputRequired(), NoneOf(User.all_emails(), message = "An user with this email address already exists!")], render_kw={"placeholder": "Email"})

# check login password
def check_password(form, password):
    # get admin trying to log in
    user = User.find_by_username(request.form["username"])

    # if user exists and his password is correct
    if not user or not user.verify_password(password.data):
        raise ValidationError("Incorrect Username or Password!")

# login form
class LoginForm(FlaskForm):
    # username -> input type - string, required
    username = StringField("username", [InputRequired(message = "Username is required!")], render_kw={"placeholder": "Username"})

    # password -> input type - password, verification if password is correct in db
    password = PasswordField("password", [InputRequired(message = "Password is required"), check_password], render_kw={"placeholder": "Password"})