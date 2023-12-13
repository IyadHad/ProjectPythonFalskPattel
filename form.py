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
	def __init__(self,first_name,last_name,email,password,current,savings):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password=password
		self.current = current
		self.savings = savings

	def get_email(self):
		return self.email

	def get_password(self):
		return self.password
	
	def get_first_name(self):
		return self.first_name
	
	def get_last_name(self):
		return self.last_name
	
	def set_current(self, value):
		self.current = value

	def set_savings(self, value):
		self.savings = value

	def to_dictionary(self):
		return {"first_name": self.first_name, "last_name": self.last_name, "email": self.email, "password": self.password, "current": self.current, "savings": self.savings}
	
	def tostring(self):
		return f"{self.first_name}-{self.last_name}-{self.email}-{self.password}-{self.current}-{self.savings}"
	

class BankerCreate(FlaskForm):
	first_name = StringField('First Name', validators = [DataRequired(), Length(min=3, max=25)])
	last_name = StringField('Last Name', validators = [DataRequired(), Length(min=3, max=25)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	submit = SubmitField('Create')
