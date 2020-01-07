from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Swing
swing_songs = db.swing_songs

app = Flask (__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Gig_book')

@app.route('/swing')
def swing():
    """Show Swing songs"""
    return render_template('swing.html', swing_songs=swing_songs.find())


if __name__ == '__main__':
    app.run(debug=True)
