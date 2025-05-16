import unittest
from app import create_app, db
from app.config import TestingConfig
from app.forms import SignupForm, LoginForm
from werkzeug.datastructures import MultiDict
from app.models import User
import sqlalchemy as sa
from app.models import Movie


class FormValidationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_valid_signup(self):
        form = SignupForm(formdata=MultiDict({
            "username": "Literally any username works",
            "password": "Any password too",
            "confirmPassword": "Any password too",
            "submit_signup": "Sign Up"
        }))
        self.assertTrue(form.validate(), msg=form.errors)

    def test_password_is_hashed(self):
        u = User(username="Literally any username works")
        u.set_password("Any password too")
        self.assertNotEqual(u.password_hash, "Any password too")
        self.assertTrue(u.check_password("Any password too"))

    def test_login_valid(self):
        u = User(username="Literally any username works")
        u.set_password("Any password too")
        db.session.add(u)
        db.session.commit()

        form = LoginForm(username="Literally any username works", password="Any password too")
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("Any password too"))

    def test_login_invalid(self):
        form = LoginForm(username="New username", password="Random password")
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        self.assertIsNone(user)

    def test_movie_fields_not_null(self):
        m = Movie(title=None, plot="...", director="...")
        db.session.add(m)
        with self.assertRaises(Exception):
            db.session.commit()
            
    def test_movie_fields_not_null(self):
        from sqlalchemy.exc import IntegrityError
        m = Movie(title=None, plot="...", director="...")
        db.session.add(m)
        with self.assertRaises(IntegrityError):
            db.session.commit()
