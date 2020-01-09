from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Gig_book
songs_collection = db.songs

app = Flask (__name__)


"""HOME"""
@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Gig_book')

"""List on songs in a given subgenre"""
@app.route("/list/<subgenre>")
def subgenre_index(subgenre):
    """show a list of songs in a subgenre"""
    songs = songs_collection.find({"subgenre": subgenre })
    print("HERE1")
    return render_template("list.html", subgenre=subgenre, songs=songs)

"""Form to add a new song"""
@app.route("/songs_new")
def songs_new():
    """create a new song"""
    return render_template("songs_new.html", song = {}, title = "new song")

"""Submit the new song"""
@app.route('/list', methods=['POST'])
def song_submit():
    """Submit a new song"""
    song = {
        'title': request.form.get('title'),
        'composer': request.form.get('composer'),
        'subgenre': request.form.get('subgenre')
        }
    song_id = songs_collection.insert_one(song).inserted_id
    return redirect(url_for('subgenre_index', subgenre=song["subgenre"]))
    print("HERE2")


"""View the song"""
@app.route('/detail/<song_id>')
def song_show(song_id):
    """show a single song"""
    print("HERE 3")
    song = songs_collection.find_one({'_id': ObjectId(song_id)})
    return render_template('show.html', song=song)

"""Edit the song"""
@app.route('/detail/<song_id>/edit')
def song_edit(song_id):
    """Edit song"""
    song = songs_collection.find_one({'_id': ObjectId(song_id)})
    print("Here4")
    return render_template('song_edit.html')

""" Update the song """
@app.route('/detail/<song_id>', methods=['POST'])
def song_update(song_id):
    song_ids = request.form.get('song_ids').split()

    updated_song = {
        'title': request.form.get('title'),
        'composer': request.form.get('composer'),
        }
    songs_collection.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_song})

    return redirect(url_for('show', song_id=song_id))


"""Delete the song"""
@app.route('/detail/<song_id>/delete', methods=['POST'])
def song_delete(song_id):
    """Deletes one song"""
    songs_collection.delete_one({'_id': ObjectId(song_id)})
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)
