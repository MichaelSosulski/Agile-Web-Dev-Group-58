from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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

# Users have username and hashed password
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)
    collection = db.relationship('Collection', back_populates='user')
    
    friend_requests_sent = db.relationship(
        'Friend',
        foreign_keys='Friend.friend_a_id',
        back_populates='friend_a',
        cascade='all, delete-orphan'
    )

    friend_requests_received = db.relationship(
        'Friend',
        foreign_keys='Friend.friend_b_id',
        back_populates='friend_b',
        cascade='all, delete-orphan'
    )
    
    def get_id(self):
        return str(self.user_id)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Get list of friends where is_friend is True
    def friends(self):
        sent = [f.friend_b for f in self.friend_requests_sent if f.is_friend]
        received = [f.friend_a for f in self.friend_requests_received if f.is_friend]
        return sent + received
    
    def send_friend_request(self, user):
        if self == user or self.is_friends_with(user):
            return  # Already friends or same user
        friend_request = Friend(friend_a=self, friend_b=user, is_friend=False)
        db.session.add(friend_request)
        db.session.commit()
        
    def accept_friend_request(self, user):
        friend_request = Friend.query.filter_by(friend_a=user, friend_b=self, is_friend=False).first()
        if friend_request:
            friend_request.is_friend = True
            db.session.commit()
    
    def remove_friend(self, user):
        relation = Friend.query.filter(
            ((Friend.friend_a_id == self.user_id) & (Friend.friend_b_id == user.user_id)) |
            ((Friend.friend_b_id == self.user_id) & (Friend.friend_a_id == user.user_id))
        ).filter_by(is_friend=True).first()
        if relation:
            db.session.delete(relation)
            db.session.commit()

    def is_friends_with(self, user):
        return any(friend.user_id == user.user_id for friend in self.friends())

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

#Relationship between users for sharing of data mutually
class Friend(db.Model):
    friendship_id = db.Column(db.Integer, primary_key=True)
    friend_a_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) #person sending request
    friend_b_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) #person receiving request
    is_friend = db.Column(db.Boolean, nullable=False) #boolean that is False when only a request has been sent

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
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))