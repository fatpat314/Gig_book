from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Gig_book')
client = MongoClient() #MongoClient(host=f'{host}?retryWrites=false')
db = client.Gig_book #client.get_default_database()
songs_collection = db.songs
comments = db.comments

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
    song = songs_collection.find_one({'_id': ObjectId(song_id)})

    song_comments = comments.find({'song_id': ObjectId(song_id)})
    return render_template('show.html', song=song, comments=song_comments)

"""Edit the song"""
@app.route('/detail/<song_id>/edit')
def song_edit(song_id):
    """Edit song"""
    song = songs_collection.find_one({'_id': ObjectId(song_id)})
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

"""Comments"""
@app.route('/detail/<song_id>/comments', methods=['POST'])
def comments_new():
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'song_id': ObjectId(request.form.get('song_id'))
    }

    print('comment')
    comment_id = comment.insert_one(comment).inserted_id
    return redirect(url_for('show', song_id=request.form.get(song_id)))

"""Comment Delete"""
@app.route('/detail/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('show', song_id=comment.get('song_id')))
    #I think this URL redirect is not right. I want it to go to details page.



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
