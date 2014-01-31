from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, ValidationError
from models import db, Signup 

class YoutubeForm(Form):
	url = TextField('Enter a YouTube link here!', [validators.Required()])
	submit = SubmitField("Let's Practice!", [validators.Required()])

class RegisterForm(Form):
	name = TextField('Name', [validators.Required()])
	email = TextField('Email', [validators.Required(), 
							    validators.Email()])
	submit = SubmitField('Keep Me Posted!')

