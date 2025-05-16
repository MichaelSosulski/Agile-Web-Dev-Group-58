from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'welcome'
babel = Babel()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
