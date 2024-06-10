from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField("Username", validators = [InputRequired(), Length(min = 1, max = 20)])
    password = PasswordField("Password", validators = [InputRequired()])

class RegisterForm(FlaskForm):
    """Register User"""  
    username = StringField("Username", validators = [InputRequired(), Length(min = 1, max = 20)])
    password = PasswordField("Password", validators = [InputRequired()])
    email = StringField("Email", validators = [InputRequired()])
    first_name = StringField("First Name", validators = [InputRequired(), Length(max = 30)])
    last_name = StringField("Last Name", validators = [InputRequired(), Length(max = 30)])

class FeedbackForm(FlaskForm):
    """Feedback """
    title = StringField("Title", validators = [InputRequired()])
    content = StringField("Content", validators = [InputRequired()])

class DeleteForm(FlaskForm):
    """Delete Feedback"""