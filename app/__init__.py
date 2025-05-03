from flask import Flask,  render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/Profile')
def profile():
    return render_template('ProfilePage.html')

@app.route('/Collection')
def collection():
    return render_template('CollectionPage.html')

@app.route('/Friends')
def friends():
    return render_template('FriendsPage.html')

@app.route('/Stats')
def stats():
    return render_template('StatsPage.html')

@app.route('/Welcome')
def welcome():
    return render_template('WelcomePage.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

from app import routes
