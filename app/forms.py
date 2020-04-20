from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length

from app import app

class UploadForm(FlaskForm):
    validators = [FileRequired(message='No selected file')]
    file = FileField('', validators=validators)
    submit = SubmitField(label="Upload")

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