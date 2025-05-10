from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, EmailField, PasswordField, IntegerField,TextAreaField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit_login = SubmitField("Login")

class SignupForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    email = EmailField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirmPassword = PasswordField("confirm password:", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit_signup = SubmitField("Sign up")

class AddFilmForm(FlaskForm):
    film_title = StringField("Film Title:", validators=[DataRequired()])
    release_year = IntegerField("Release Year:", validators=[DataRequired()])
    watch_date = DateField("Watch Date (if you've seen it):", validators=[Optional()])
    user_rating = RadioField("Rating:", choices=[1,2,3,4,5], validators=[DataRequired()])
    user_review = TextAreaField("How was it?", validators=[Optional()])
    category = RadioField("Category:", choices=["Watched", "Planning To Watch"], validators=[DataRequired()])

    #hidden film data
    director = HiddenField()
    genres = HiddenField()
    run_time = HiddenField()
    plot = HiddenField()
    poster_url = HiddenField()

    submit_film = SubmitField("Add film")