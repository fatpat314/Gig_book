from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Swing
swing_songs = db.swing_songs

app = Flask (__name__)

def swing_song_url_creator(id_lst):
    swing_song_list = []
    for swing_song_id in id_lst:
        swing_peice = 'https://youtube.com/embed/' + swing_song_id
        swing_song_list.append(swing_peice)
    return swing_song_list

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Gig_book')

"""SWING"""

@app.route('/swing_index')
def swing():
    """Show Swing songs"""
    return render_template('swing_index.html', swing_songs=swing_songs.find())

@app.route('/swing_songs/new')
def swing_songs_new():
    """Add a new swing song"""
    return render_template('swing_songs_new.html')

@app.route('/swing_songs', methods=['POST'])
def swing_songs_submit():
    """Submit a new swing song"""
    #Grab the song IDS and make a list out of them
    swing_song_ids = request.form.get('swing_song_ids').split()
    #call out helper function to create the list of links
    swing_song_list = swing_song_url_creator(swing_song_ids)

    swing_song = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'swing_song_list': swing_song_list,
        'swing_song_ids': swing_song_ids
    }
    swing_songs.insert_one(swing_song)
    print(request.form.to_dict())
    return redirect(url_for('swing_index'))




if __name__ == '__main__':
    app.run(debug=True)
