from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, IntegerField,TextAreaField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Optional, ValidationError, Length, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User
import datetime

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
    release_year = IntegerField("Release Year (optional):", validators=[NumberRange(min=1910, max=datetime.datetime.now().year)])
    watch_date = DateField("Watch Date (if you've seen it):")
    user_rating = RadioField("Rating:", choices=[1,2,3,4,5])
    user_review = TextAreaField("How was it?", validators=[Length(max=300)])
    category = RadioField("Category:", choices=["Watched", "Planning To Watch"], validators=[DataRequired()])

    #hidden film data
    director = HiddenField()
    genres = HiddenField()
    run_time = HiddenField()
    plot = HiddenField()
    poster_url = HiddenField()

    submit_film = SubmitField("Add film")

    def validate_watch_date(form, field):
        if form.category.data == "Planning To Watch" and field.data:
            raise ValidationError("Error: You haven't seen this film yet")
        if field.data and form.category.data == "Watched": # added a check to make sure that the date is not in the future
            if field.data > datetime.date.today():
                raise ValidationError("Error: Watch date cannot be in the future")
    
    def validate_user_rating(form, field):
        if form.category.data == "Planning To Watch" and field.data:
            raise ValidationError("Error: You haven't seen this film yet")
        
    def validate_user_review(form, field):
        if form.category.data == "Planning To Watch" and field.data:
            raise ValidationError("Error: You haven't seen this film yet")