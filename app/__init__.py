from flask import Flask,  render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('WelcomePage.html')

@app.route('/Homepage')
def home():
    return render_template('homepage.html')

@app.route('/Profile')
def profile():
    return render_template('ProfilePage.html')

@app.route('/Collection')
def collection():
    watchList = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", 
    "The Godfather Part II", "12 Angry Men", "Schindler's List", 
    "LOTR: Return of the King", "Pulp Fiction", "The Good, the Bad and the Ugly", "Fight Club"]

    favList = ["The Godfather Part II", "12 Angry Men", "Schindler's List", 
    "LOTR: Return of the King", "Pulp Fiction"]

    return render_template('CollectionPage.html', watchList=watchList, favList=favList)

@app.route('/Friends')
def friends():
    return render_template('FriendsPage.html')

@app.route('/Stats')
def stats():
    return render_template('StatsPage.html')

if __name__ == '__main__':
    app.run()

from app import routes
