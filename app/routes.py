from flask import request, redirect, url_for, render_template
from app import app, db
from app.models import Movies, Collections, Users
from datetime import datetime

@app.route('/')
def welcome():
    return render_template('WelcomePage.html')

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

"""@app.route('/Collection')
def collection():
    watchList = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", 
                "The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club"]

    favList = ["The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction"]

    planList = ["Oppenheimer", "Barbie"]

    return render_template('CollectionPage.html', watchList=watchList, favList=favList, planList=planList)"""

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

@app.route('/add_film', methods=['POST'])
def add_film():
    title = request.form.get('filmTitle')
    release_year = request.form.get('filmYear')
    watch_date = request.form.get('watchDate')
    rating = request.form.get('starRating')
    review = request.form.get('filmReview')
    category = request.form.get('addToCategory')

    user_id = 1

    new_movie = Movies(
        name=title,
        release_year=int(release_year) if release_year else None,
        watch_date=datetime.strptime(watch_date, "%Y-%m-%d") if watch_date else None,
        rating=int(rating) if rating else None,
        review=review
    )
    db.session.add(new_movie)
    db.session.commit()

    collection_entry = Collections(
        user_id=user_id,
        movie_id=new_movie.movie_id,
        collection_name="default",
        category=category
    )
    db.session.add(collection_entry)
    db.session.commit()

    return redirect(url_for('collection'))

@app.route('/Collection')
def collection():
    user_id = 1
    collections = Collections.query.filter_by(user_id=user_id).all()

    watchList = [c.movie.name for c in collections if c.category == 'add to watched']
    planList = [c.movie.name for c in collections if c.category == 'add to planned']
    favList = [] 

    return render_template('CollectionPage.html', watchList=watchList, favList=favList, planList=planList)

