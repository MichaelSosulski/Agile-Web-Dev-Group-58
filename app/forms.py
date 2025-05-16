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
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        self.meta.user = user
        if user is None:
            raise ValidationError('User does not exist')
        
    def validate_password(self, password):
        if self.meta.user and not self.meta.user.check_password(password.data):
            raise ValidationError('Incorrect password')

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
    
    film_title = StringField("Film Title", validators=[DataRequired(), Length(max=50)])
    release_year = IntegerField("Release Year", validators=[NumberRange(min=1910, max=datetime.datetime.now().year)])
    watch_date = DateField("Watch Date")
    user_rating = RadioField("Rating", choices=[1,2,3,4,5], validators=[Optional()])
    user_review = TextAreaField("Review", validators=[Length(max=300)])
    category = RadioField("Category", choices=["Watched", "To Watch"], validators=[DataRequired()])

    #hidden film data
    director = HiddenField()
    genres = HiddenField()
    run_time = HiddenField()
    plot = HiddenField()
    poster_url = HiddenField()

    submit_film = SubmitField("Add Film")
    
    def validate_watch_date(form, field):
        if form.category.data == "To Watch" and field.data:
            raise ValidationError("Error: You haven't seen this film yet")
        if field.data and form.category.data == "Watched":
            if field.data > datetime.date.today():
                raise ValidationError("Error: Watch date cannot be in the future")
        elif form.category.data == "Watched" and not field.data:
            raise ValidationError("Error: Please Select a date.")

    def validate_user_rating(form, field):
        if form.category.data == "To Watch" and field.data:
            raise ValidationError("Error: You haven't seen this film yet")
        if form.category.data == "Watched" and not field.data:
            raise ValidationError("Error: Please input a rating")

    def validate_user_review(form, field):
        if form.category.data == "To Watch" and field.data:
            raise ValidationError("Error: You haven't seen this film yet")

# Friend management forms
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