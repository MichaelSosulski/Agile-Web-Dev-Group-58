from flask import render_template, flash, redirect, request
from app import app

from app.forms import LoginForm, SignupForm

@app.route('/', methods=['GET', 'POST'])
def welcome():
    lForm = LoginForm()
    sForm = SignupForm()

    if 'submit_login' in request.form and lForm.validate_on_submit():
        flash('Login requested for user {}'.format(lForm.username.data))
        print("login sent")
        return redirect('/Homepage')
    if 'submit_signup' in request.form and sForm.validate_on_submit():
        flash('Sign up requested for user {}'.format(sForm.username.data))
        #ADD NEW ACCOUNT INFORMATION TO DATABASE
        print("sign up sent")
    return render_template('WelcomePage.html', lForm=lForm, sForm=sForm)

@app.route('/Homepage')
def home():
    username = "Insert Username Here"

    popular = ["The Dark Knight", "The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club"]

    watchList = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", 
                "The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club"]

    recommended = [{"username": "Gary", "film": {"title": "Oppenheimer", "image": "static/images/placeholder.jpg", "rating": "⭐⭐⭐⭐⭐"}},
                    {"username": "Lauren", "film": {"title": "Ninja Turtles", "image": "static/images/placeholder.jpg", "rating": "⭐⭐⭐"}},
                    {"username": "Sam", "film": {"title": "Jurassic Park", "image": "static/images/placeholder.jpg", "rating": "⭐⭐⭐⭐"}}]

    return render_template('homepage.html', username=username, popular=popular, watchList=watchList, recommended=recommended)

@app.route('/Profile')
def profile():
    user = {"name": "Insert User Name", "image": "static/images/placeholder.jpg", "bio": "My Bio"}
    watchList = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", 
                "The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club"]
    
    favList = ["The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction"]

    friends = [{"username":"Friend_1", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_2", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_3", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_4", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_5", "image":"static/images/placeholder.jpg"}]
    
    return render_template('ProfilePage.html', user=user, watchList=watchList, favList=favList, friends=friends)

@app.route('/Collection')
def collection():
    watchList = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", 
                "The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club"]

    favList = ["The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction"]

    planList = ["Oppenheimer", "Barbie"]

    return render_template('CollectionPage.html', watchList=watchList, favList=favList, planList=planList)

@app.route('/Friends')
def friends():
    friends = [{"username":"Friend_1", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_2", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_3", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_4", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_5", "image":"static/images/placeholder.jpg"}]

    return render_template('FriendsPage.html', friends=friends)

@app.route('/Stats')
def stats():
    return render_template('StatsPage.html')