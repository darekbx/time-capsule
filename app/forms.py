from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

from app import app

class LoginForm(FlaskForm):
	pin = PasswordField('Pin', validators = [
		DataRequired(),
		Length(min=4, message='Pin is too short')
	])
	submit = SubmitField('Log In')

	def validate(self):
		initial_validation = super(LoginForm, self).validate()
		if not initial_validation:
			return False
		if self.pin.data != app.config["PIN"]:
			self.pin.errors.append('Invalid Pin')
			return False
		return True