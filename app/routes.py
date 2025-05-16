from flask import request, redirect, url_for, render_template, flash
from app import app, db
from app.models import Movie, Collection, User, MovieGenre, Friend
from datetime import datetime
from flask_login import current_user, login_user, login_required, logout_user
import sqlalchemy as sa
from app.forms import LoginForm, SignupForm, AddFilmForm, SendRequestForm, AcceptRequestForm, DeclineRequestForm, RemoveFriendForm, CancelRequestForm
from flask import jsonify
from sqlalchemy import func

@app.route('/', methods=['GET', 'POST'])
def welcome():
    lForm = LoginForm()
    sForm = SignupForm()

    show = None

    if 'submit_login' in request.form:
        show = 'login'
        if lForm.validate_on_submit():    
            user = db.session.scalar(
                sa.select(User).where(User.username == lForm.username.data))
            if user is None or not user.check_password(lForm.password.data):
                flash('Invalid username or password', 'error')
                print("Login Errors:", lForm.errors)
            else: 
                login_user(user)
                flash('Logged in successfully', 'success')
                return redirect('/Homepage')
                
    elif 'submit_signup' in request.form:
        show = 'signup'
        if sForm.validate_on_submit():
            user = User(username=sForm.username.data)
            user.set_password(sForm.password.data) 
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            login_user(user)
            flash('Welcome, you are now logged in!')
            return redirect('/Homepage')
            
    return render_template('WelcomePage.html', lForm=lForm, sForm=sForm, 
                            login_errors=lForm.errors, signup_errors=sForm.errors, show=show)

@app.route('/Homepage')
@login_required
def home():
    username = current_user.username
    
    popular = [
        {"title": "The Dark Knight", "poster": "static/images/The_Dark_Knight.png"},
        {"title": "The Godfather Part II", "poster": "static/images/The_Godfather_Part_II.png"},
        {"title": "12 Angry Men", "poster": "static/images/12_Angry_Men.png"},
        {"title": "Schindler's List", "poster": "static/images/Schindler's_List.png"},
        {"title": "LOTR: Return of the King", "poster": "static/images/LOTR_Return_of_the_King.png"},
        {"title": "Pulp Fiction", "poster": "static/images/Pulp_Fiction.png"},
        {"title": "The Good, the Bad and the Ugly", "poster": "static/images/The_Good_the_Bad_and_the_Ugly.png"},
        {"title": "Fight Club", "poster": "static/images/Fight_Club.png"}
    ]
    
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
    send_request_form = SendRequestForm()
    cancel_request_form = CancelRequestForm()
    
    # List of friends of user (is_friend = True)
    friends = current_user.friends()
    friend_ids = [friend.user_id for friend in current_user.friends()] # used for filtering
    
    # List of received and pending friend requests (is_friend = False)
    pending_requests  = Friend.query.filter_by(friend_b_id=current_user.user_id, is_friend=False).all()   
    pending_request_senders = [fr.friend_a for fr in pending_requests] # to show in pending request list 
    pending_request_sender_ids = [user.user_id for user in pending_request_senders] # used for filtering
    
    # All users the current user can send a request to
    # Cannot send friend request to current friends, sender of incoming pending requests, and self
    excluded_ids = friend_ids + pending_request_sender_ids + [current_user.user_id]
    users_to_request = User.query.filter(~User.user_id.in_(excluded_ids)).all()
    
    # Friend requests that the current user has sent and are still pending
    outgoing_pending_requests = Friend.query.filter_by(friend_a_id=current_user.user_id, is_friend=False).all()
    pending_recipient_ids = [fr.friend_b_id for fr in outgoing_pending_requests]

    return render_template('FriendsPage.html',
                            send_request_form=send_request_form,
                            cancel_request_form=cancel_request_form,
                            friends=friends,
                            requests=pending_request_senders,
                            users_to_request=users_to_request, 
                            pending_recipient_ids=pending_recipient_ids)

@app.route('/Friends/request/send/<username>', methods=['POST'])
@login_required
def send_request(username):
    
    form = SendRequestForm()
    if form.validate_on_submit():
        # Find the user to send request to
        friend_b = User.query.filter_by(username=username).first_or_404()

        # Check if a friend request or friendship already exists
        existing = Friend.query.filter(
            ((Friend.friend_a_id == current_user.user_id) & (Friend.friend_b_id == friend_b.user_id)) |
            ((Friend.friend_a_id == friend_b.user_id) & (Friend.friend_b_id == current_user.user_id))
        ).first()
        
        if not existing:
            # Create a new friend request (is_friend = False)
            friend_request = Friend(friend_a_id=current_user.user_id, friend_b_id=friend_b.user_id, is_friend=False)
            db.session.add(friend_request)
            db.session.commit()
            flash(f"Friend request sent to {username}.")
        else:
            flash(f"A friend request or friendship already exists with {username}.")       
    else:
        flash("Invalid form submission.")
        
    return redirect(url_for('friends'))

@app.route('/Friends/request/cancel/<username>', methods=['POST'])
@login_required
def cancel_request(username):
    user_to_cancel = User.query.filter_by(username=username).first_or_404()
    
    # Delete the friend request where current user is sender
    friend_request = Friend.query.filter_by(
        friend_a_id=current_user.user_id,
        friend_b_id=user_to_cancel.user_id,
        is_friend=False
    ).first()

    if friend_request:
        db.session.delete(friend_request)
        db.session.commit()

    return redirect(url_for('friends'))

@app.route('/Friends/request/accept/<username>')
@login_required
def accept_request(username):
    # Find the user who sent the request
    friend_a = User.query.filter_by(username=username).first_or_404()

    # Find the friend request where current user is recipient
    friend_request = Friend.query.filter_by(friend_a_id=friend_a.user_id, friend_b_id=current_user.user_id, is_friend=False).first()

    if friend_request:
        friend_request.is_friend = True
        db.session.commit()

    return redirect(url_for('friends'))

@app.route('/Friends/request/decline/<username>')
@login_required
def decline_request(username):
    # Find the user who sent the request
    friend_a = User.query.filter_by(username=username).first_or_404()

    # Find the friend request where current user is recipient
    friend_request = Friend.query.filter_by(friend_a_id=friend_a.user_id, friend_b_id=current_user.user_id, is_friend=False).first()

    if friend_request:
        db.session.delete(friend_request)
        db.session.commit()

    return redirect(url_for('friends'))

@app.route('/Friends/request/remove/<username>')
@login_required
def remove_friend(username):
    # Find the friend user
    friend = User.query.filter_by(username=username).first_or_404()

    # Find the friendship (friendship could be in either direction)
    friendship = Friend.query.filter(
        ((Friend.friend_a_id == current_user.user_id) & (Friend.friend_b_id == friend.user_id)) |
        ((Friend.friend_a_id == friend.user_id) & (Friend.friend_b_id == current_user.user_id))
    ).filter_by(is_friend=True).first()

    if friendship:
        db.session.delete(friendship)
        db.session.commit()

    return redirect(url_for('friends'))

@app.route('/Stats')
@login_required
def stats():
    user_id = current_user.user_id

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

        #Check if collection row is already in Collection
        in_collection = Collection.query.join(Movie).filter(Collection.user_id == user_id,
            Movie.title == title, Movie.release_year == release_year).one_or_none()
        if in_collection != None:
            flash("This film is already in your collection.")
            return redirect(url_for('collection'))

        #Check if movie is already in db, if it is not, add it
        find_film = Movie.query.filter(Movie.title==title, Movie.release_year==release_year).one_or_none()
        if find_film is None:
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
        else:
            new_movie = find_film

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
    
    return render_collection_page(add_form, show='add')

@app.route('/fav_film', methods=['POST'])
@login_required
def fav_film():
    user_id = current_user.user_id
    if request.method == 'POST':
        id = request.form['id']
        film = Collection.query.join(Movie).filter(Collection.user_id == user_id,
            Movie.movie_id == id, Collection.category == 'Watched').one_or_none()
        if film != None:
            film.category = 'Favourite'
            db.session.add(film)
            db.session.commit()
        else:
            flash("film is not in Watched List")
    return redirect(url_for('collection'))

@app.route('/rm_film', methods=['POST'])
@login_required
def rm_film():
    user_id = current_user.user_id
    print(user_id)
    if request.method == 'POST':
        id = request.form['id']
        film = Collection.query.join(Movie).filter(Collection.user_id == user_id,
            Movie.movie_id == id).one_or_none()
        if film != None:
            db.session.delete(film)
            db.session.commit()
        else:
            flash("Can't delete non-existent collection item.")
    return redirect(url_for('collection'))

@app.route('/get_film/<query>')
@login_required
def get_film(query):
    films = get_movie_collection(current_user.user_id, search=query)
    return films

def render_collection_page(add_form, show=None):
    user_id = current_user.user_id
    collections = get_movie_collection(user_id)
    watchList = []
    planList = []
    favList = [] 
    for item in collections:
        if item['category'] == 'Watched' or item['category'] == 'Favourite':
            watchList.append(item)
        elif item['category'] == 'To Watch':
            planList.append(item)
        if item['category'] == 'Favourite':
            favList.append(item)

    return render_template('CollectionPage.html', add_form=add_form, watchList=watchList, favList=favList, planList=planList, show=show)

@app.route('/Collection')
@login_required
def collection():
    add_film_form = AddFilmForm()
    return render_collection_page(add_film_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

def get_movie_collection(user_id, search=None):
    """
    Retrieves movie collection data for a given user, including movie details and genres.
    """
    if search:
        search_without_spaces_lower = search.replace(' ', '').lower()

        collections = Collection.query.join(Movie).filter(
        Collection.user_id == user_id,
        func.lower(func.replace(Movie.title, ' ', '')) == search_without_spaces_lower
        )
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