from flask import request
from app import app

@app.route('/user/')
def show_user_profile(username):
    username = request.args.get('username')
    return f'User %s' % username

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        'do_the_login()'
    else:
        'show_the_login_form()'

@app.route('/looping', methods=['GET', 'POST'])
def loop():
    thisURL = url_for('loop')
    return "<a href={}> Let's go back to {} </a>".format(thisURL, thisURL)