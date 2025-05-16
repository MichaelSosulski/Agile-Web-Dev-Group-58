from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'welcome'  # Ensure the login view is correctly set

# Register routes and models
from app import routes, models

# Context processor to inject the username if the user is authenticated
from flask_login import current_user

@app.context_processor
def inject_username():
    # Make sure the user is authenticated before trying to access `current_user`
    if current_user.is_authenticated:
        return dict(username=current_user.username)
    return dict(username=None)  # or any default value you want when not authenticated


