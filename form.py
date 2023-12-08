from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import email_validator

class RegistrationForm(FlaskForm):
	first_name = StringField('First Name', validators = [DataRequired(), Length(min=3, max=25)])
	last_name = StringField('Last Name', validators = [DataRequired(), Length(min=3, max=25)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

class BankerlogForm(FlaskForm):
	password = PasswordField('Password', validators = [DataRequired()])
	submit = SubmitField('Login')

class customer():
	def __init__(self,first_name,last_name,email,password):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password=password

	def get_email(self):
		return self.email

	def get_password(self):
		return self.password
	
	def get_first_name(self):
		return self.first_name
	
	def get_last_name(self):
		return self.last_name
