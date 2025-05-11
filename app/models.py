from app import db

#Movie data
class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer)
    director = db.Column(db.String(50), nullable=False)
    run_time = db.Column(db.Integer)
    plot = db.Column(db.String(300), nullable=False)
    poster = db.Column(db.String(200), nullable=False)

    movie_genres = db.relationship('MovieGenre', back_populates='movie')
    collection = db.relationship('Collection', back_populates='movie')  

#A movie can have multiple genres
class MovieGenre(db.Model):
    movie_genre_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    genre = db.Column(db.String(20), nullable=False)

    movie = db.relationship('Movie', back_populates='movie_genres')

#Users we just have username, email and password no salting just yet
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    collection = db.relationship('Collection', back_populates='user')
    
#User and movie are attibutes of a collection as a single movie can be in multiple collections
class Collection(db.Model):
    collection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)
    watch_date = db.Column(db.Date, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(300), nullable=True)
    category = db.Column(db.String(50)) 
    
    user = db.relationship('User', back_populates='collection')
    movie = db.relationship('Movie', back_populates='collection')

#I think we should store firends as both way like A is a friend of B and B is also a friend of A
class Friend(db.Model):
    friendship_id = db.Column(db.Integer, primary_key=True)
    friend_a_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    friend_b_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    friend_a = db.relationship('User', foreign_keys=[friend_a_id])
    friend_b = db.relationship('User', foreign_keys=[friend_b_id])
    
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    movie_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])