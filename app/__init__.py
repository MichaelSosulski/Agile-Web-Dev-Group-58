from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'welcome'

from app import routes, models


from flask import Flask, g
from flask_login import current_user

def create_app():
    app = Flask(__name__)

    @app.context_processor
    def inject_username():
        # Make sure the user is authenticated before trying to access `current_user`
        if current_user.is_authenticated:
            return dict(username=current_user.username)
        return dict(username=None)  # or any default value you want when not authenticated

    return app


from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images/characters'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['UPLOAD_FOLDER'] = 'static/images/characters'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Assuming you have a user model with a profile_image field
        current_user.profile_image = f'images/characters/{filename}'
        db.session.commit()
        flash('File successfully uploaded')
        return redirect(url_for('profile'))