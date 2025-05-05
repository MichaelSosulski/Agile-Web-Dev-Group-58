from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField,TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    email = EmailField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirmPassword = PasswordField("confirm password:", validators=[DataRequired()])
    submit = SubmitField("Sign up")