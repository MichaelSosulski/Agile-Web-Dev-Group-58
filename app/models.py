from app import db

#For movies we currently have name, runtime and genre lmk if we need more data
class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)

#Users we just have username, email and password no salting just yet
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
#User and movie are attibutes of a collection as a single movie can be in multiple collections
class Collections(db.Model):
    collection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    collection_name = db.Column(db.String(100), nullable=False)
    user = db.relationship('Users', back_populates='collections')
    movie = db.relationship('Movies', back_populates='collections')

#I think we should store firends as both way like A is a friend of B and B is also a friend of A
class Friends(db.Model):
    friendship_id = db.Column(db.Integer, primary_key=True)
    friend_a_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_b_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_a = db.relationship('Users', foreign_keys=[friend_a_id])
    friend_b = db.relationship('Users', foreign_keys=[friend_b_id])
    
class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    movie_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    sender = db.relationship('Users', foreign_keys=[sender_id])
    receiver = db.relationship('Users', foreign_keys=[receiver_id])