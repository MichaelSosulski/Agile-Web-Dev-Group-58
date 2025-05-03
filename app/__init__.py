from flask import Flask,  render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('WelcomePage.html')

@app.route('/Homepage')
def home():
    username = "Insert Username Here"

    return render_template('homepage.html', username=username)

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

if __name__ == '__main__':
    app.run()

from app import routes
