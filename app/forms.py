from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, IntegerField,TextAreaField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Optional, ValidationError
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit_login = SubmitField("Login")

class SignupForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit_signup = SubmitField("Sign Up")
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username')

class AddFilmForm(FlaskForm):
    film_title = StringField("Film Title:", validators=[DataRequired()])
    release_year = IntegerField("Release Year (optional):", validators=[Optional()])
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
    
class SendRequestForm(FlaskForm):
    submit = SubmitField('Send Request')

class AcceptRequestForm(FlaskForm):
    submit = SubmitField('Accept Request')

class DeclineRequestForm(FlaskForm):
    submit = SubmitField('Decline Request')

class RemoveFriendForm(FlaskForm):
    submit = SubmitField('Remove Friend') 
    
class CancelRequestForm(FlaskForm):
    submit = SubmitField('Cancel Request')