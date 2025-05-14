from flask import request, redirect, url_for, render_template, flash
from app import app, db
from app.models import Movie, Collection, User, MovieGenre
from datetime import datetime
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app.forms import LoginForm, SignupForm, AddFilmForm
from flask import jsonify
from sqlalchemy import func

@app.route('/', methods=['GET', 'POST'])
def welcome():
    lForm = LoginForm()
    sForm = SignupForm()

    if 'submit_login' in request.form and lForm.validate_on_submit():    
        user = db.session.scalar(
            sa.select(User).where(User.username == lForm.username.data))
        if user is None or not user.check_password(lForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('welcome'))
        login_user(user)
        flash('Logged in successfully')
        print("login sent")
        return redirect('/Homepage')
    
    if 'submit_signup' in request.form and sForm.validate_on_submit():
        user = User(username=sForm.username.data)
        user.set_password(sForm.password.data) 
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        flash('Welcome, you are now logged in!')
        return redirect('/Homepage')
        
    return render_template('WelcomePage.html', lForm=lForm, sForm=sForm)

@app.route('/Homepage')
@login_required
def home():
    username = current_user.username

    popular = ["The Dark Knight", "The Godfather Part II", "12 Angry Men", "Schindler's List", 
                "LOTR: Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club"]
    
    collections = current_user.collection
    watchList = [(c.movie.title, c.movie.poster) for c in collections if c.category == 'Watched']

    recommended = [{"username": "Gary", "film": {"title": "Oppenheimer", "image": "static/images/placeholder.jpg", "rating": "⭐⭐⭐⭐⭐"}},
                    {"username": "Lauren", "film": {"title": "Ninja Turtles", "image": "static/images/placeholder.jpg", "rating": "⭐⭐⭐"}},
                    {"username": "Sam", "film": {"title": "Jurassic Park", "image": "static/images/placeholder.jpg", "rating": "⭐⭐⭐⭐"}}]

    return render_template('homepage.html', username=username, popular=popular, watchList=watchList, recommended=recommended)

@app.route('/Profile')
@login_required
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

@app.route('/Friends')
@login_required
def friends():
    friends = [{"username":"Friend_1", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_2", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_3", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_4", "image":"static/images/placeholder.jpg"},
                {"username":"Friend_5", "image":"static/images/placeholder.jpg"}]

    return render_template('FriendsPage.html', friends=friends)

@app.route('/Stats')
@login_required
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
@login_required
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

        user_id = current_user.user_id

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

@app.route('/get_film/<query>')
@login_required
def get_film(query):
    films = get_movie_collection(current_user.user_id, search=query)
    return films

@app.route('/Collection')
@login_required
def collection():
    add_film_form = AddFilmForm()
    
    user_id = current_user.user_id
    collections = get_movie_collection(user_id)
    watchList = []
    planList = []
    favList = [] 
    for item in collections:
        if item['category'] == 'Watched':
            watchList.append(item)
        elif item['category'] == 'Planning To Watch':
            planList.append(item)
        elif item['category'] == 'Favourite':
            favList.append(item)

    return render_template('CollectionPage.html', add_form=add_film_form, watchList=watchList, favList=favList, planList=planList)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

def get_movie_collection(user_id, search=None):
    """
    Retrieves movie collection data for a given user, including movie details and genres.
    """
    if search:
        collections = Collection.query.join(Movie).filter(Collection.user_id == user_id, Movie.title == search)
    else:
        collections = Collection.query.join(Movie).filter(Collection.user_id == user_id)

    # Process the results into a list of dictionaries
    results = []
    if collections != None:
        for collection in collections:
            movie = collection.movie
            genres = [mg.genre for mg in movie.movie_genres]
            results.append({
                'movie_id': movie.movie_id,
                'title': movie.title,
                'poster': movie.poster,
                'release_year': movie.release_year,
                'plot': movie.plot,
                'director': movie.director,
                'run_time': movie.run_time,
                'watch_date': collection.watch_date,
                'rating': collection.rating,
                'review': collection.review,
                'genres': ", ".join(genres),  # String of genres
                'category': collection.category,
            })
        return results
    return None