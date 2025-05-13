from flask import request, redirect, url_for, render_template, flash
from app import app, db
from app.models import Movie, Collection, User, MovieGenre
from datetime import datetime

from app.forms import LoginForm, SignupForm, AddFilmForm
from flask import jsonify
from sqlalchemy import func

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
    user_id = 1

    # Top genres
    genre_counts = (
        db.session.query(MovieGenre.genre, func.count(MovieGenre.genre))
        .join(Movie)
        .join(Collection)
        .filter(Collection.user_id == user_id)
        .group_by(MovieGenre.genre)
        .all()
    )
    genres = [g[0] for g in genre_counts]
    genre_values = [g[1] for g in genre_counts]

    # Total watch time
    total_watch_time = (
        db.session.query(func.sum(Movie.run_time))
        .join(Collection)
        .filter(Collection.user_id == user_id, Collection.category == 'Watched')
        .scalar()
    ) or 0

    # Watched films
    watched_films = (
        db.session.query(Movie.title, Collection.rating)
        .join(Collection)
        .filter(Collection.user_id == user_id, Collection.category == 'Watched')
        .all()
    )
    watched_titles = [f[0] for f in watched_films]
    watched_ratings = [f[1] if f[1] is not None else 0 for f in watched_films]

    # Favourite directors
    director_counts = (
        db.session.query(Movie.director, func.count(Movie.director))
        .join(Collection)
        .filter(Collection.user_id == user_id, Collection.category == 'Watched')
        .group_by(Movie.director)
        .order_by(func.count(Movie.director).desc())
        .all()
    )
    director_names = [d[0] for d in director_counts]
    director_freqs = [d[1] for d in director_counts]

    return render_template('StatsPage.html',
                           genres=genres,
                           genre_values=genre_values,
                           watch_time=total_watch_time,
                           watched_titles=watched_titles,
                           watched_ratings=watched_ratings,
                           director_names=director_names,
                           director_freqs=director_freqs)


@app.route('/add_film', methods=['POST'])
def add_film():
    add_form = AddFilmForm()

    if add_form.validate_on_submit():
        #film data
        title = add_form.film_title.data
        release_year = add_form.release_year.data
        director = add_form.director.data
        genres = add_form.genres.data.split(',') #array of genres
        run_time = add_form.run_time.data
        plot = add_form.plot.data
        poster_url = add_form.poster_url.data

        #user watch data
        watch_date = add_form.watch_date.data
        rating = add_form.user_rating.data
        review = add_form.user_review.data
        category = add_form.category.data

        user_id = 1

        new_movie = Movie(
            title = title,
            release_year = int(release_year) if release_year else None,
            director = director,
            run_time = run_time,
            plot = plot,
            poster = poster_url
        )
        db.session.add(new_movie)
        db.session.commit()

        for g in genres:
            film_to_genre = MovieGenre(
                movie_id = new_movie.movie_id,
                genre = g
            )
            db.session.add(film_to_genre)
            db.session.commit()

        collection_entry = Collection(
            user_id=user_id,
            movie_id=new_movie.movie_id,
            watch_date=datetime.strptime(str(watch_date), "%Y-%m-%d") if watch_date else None,
            rating=int(rating) if rating else None,
            review=review,
            category=category
        )
        db.session.add(collection_entry)
        db.session.commit()

    return redirect(url_for('collection'))

@app.route('/Collection')
def collection():
    add_film_form = AddFilmForm()
    
    user_id = 1
    collections = Collection.query.filter_by(user_id=user_id).all()

    watchList = [(c.movie.title, c.movie.poster) for c in collections if c.category == 'Watched']
    planList = [(c.movie.title, c.movie.poster) for c in collections if c.category == 'Planning To Watch']
    favList = [] 

    return render_template('CollectionPage.html', add_form=add_film_form, watchList=watchList, favList=favList, planList=planList)

