from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Gig_book
songs_collection = db.songs

app = Flask (__name__)

# songs = [
#     {'title': 'Dont mean a thing', 'composer': 'Duke Ellington', 'subgenre': 'swing'},
# ]

"""HOME"""
@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Gig_book')

@app.route("/list/<subgenre>")
def subgenre_index(subgenre):
    """show a list of songs in a subgenre"""
    songs = songs_collection.find({"subgenre": subgenre })
    return render_template("list.html", subgenre=subgenre, songs=songs)


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

@app.route('/list/<song_id>/delete', methods=['POST'])
def songs_delete(song_id):
    """Deletes one song"""
    songs_collection.delete_one({'_id': ObjectId(song_id)})
    return redirect(url_for('index'))

""" Show route is not working """
# @app.route('/show/{{ song._id }}')
# def song_show(song_id):
#     """show a single song"""
#     song = songs_collection.find_one({'_id': ObjectId(song_id)})
#
#     return render_template('show.html', song=song)


@app.route("/songs_new")
def songs_new():
    """create a new song"""
    return render_template("songs_new.html", song = {}, title = "new song")


"""-------------------------------JAZZ---------------------------------------"""

# @app.route('/index/swing')
# def swing():
#     """Show Swing songs"""
#     return render_template('index.html', swing_songs=songs_collection.find({"subgenre": "swing"}))

# @app.route('/index/bebop')
# def bebop():
#     """Show Bebop Songs"""
#     return render_template('index.html', bebop_songs=songs_collection.find({"subgenre": "bebop"}))


# @app.route('/swing_index')
# def swing():
#     """Show Swing songs"""
#     return render_template('swing_index.html', swing_songs=songs_collection.find({"subgenre": "swing"}))
#
# @app.route('/swing_songs/new')
# def swing_songs_new():
#     """Add a new swing song"""
#     return render_template('swing_songs_new.html')
#
# @app.route('/swing_songs', methods=['POST'])
# def swing_songs_submit():
#     """Submit a new swing song"""
#     #Grab the song IDS and make a list out of them
#     swing_song_ids = request.form.get('swing_song_ids').split()
#
#
#
#     swing_song = {
#         'subgenre': 'swing',
#         'title': request.form.get('title'),
#         'description': request.form.get('description'),
#         'swing_song_list': swing_song_list,
#         'swing_song_ids': swing_song_ids
#     }
#     swing_songs.insert_one(swing_song)
#     print(request.form.to_dict())
#     return redirect(url_for('swing_index'))
#
# """Bebop"""
# @app.route('/bebop_index')
# def bebop():
#     """Show Bebop songs"""
#     return render_template('bebop_index.html')
#
# """Big Band"""
# @app.route('/big_band_index')
# def big_band():
#     """Show Big Band songs"""
#     return render_template('big_band_index.html')
#
# """Django"""
# @app.route('/django_index')
# def django():
#     """Show Django songs"""
#     return render_template('django_index.html')
#
# """Latin"""
# @app.route('/latin_index')
# def latin():
#     """Show Latin Songs"""
#     return render_template('latin_index.html')
#
# """Dixieland"""
# @app.route('/dixieland_index')
# def dixieland():
#     """Show Dixieland Songs"""
#     return render_template('dixieland_index.html')
#
#
# """-------------------------------------CLASSICAL----------------------------"""
#
# """Baroque"""
# @app.route('/baroque_index')
# def baroque():
#     """Show Baroque songs"""
#     return render_template('baroque_index.html')
#
# """Modern Composition"""
# @app.route('/modern_composition_index')
# def modern_composition():
#     """Show Modern Composition Songs"""
#     return render_template('modern_composition_index.html')
#
# """Opera"""
# @app.route('/opera_index')
# def opera():
#     """Show Opera Songs"""
#     return render_template("opera_index.html")
#
# """Romantic"""
# @app.route('/romantic_index')
# def romantic():
#     """Show Romantic Songs"""
#     return render_template("romantic_index.html")
#
# """Impressionist"""
# @app.route('/impressionist_index')
# def impressionist():
#     """Show Impressionist Songs"""
#     return render_template("impressionist_index.html")
#
# """Minimalism"""
# @app.route('/minimalism_index')
# def minimalism():
#     """Show Minimalism Songs"""
#     return render_template("minimalism_index.html")
#
#
# """------------------------------------POP-----------------------------------"""
#
# @app.route('/adult_contemperary_index')
# def adult_contemperary():
#     """Show Adult Contemporary Songs"""
#     return render_template("adult_contemperary_index.html")
#
#
#
#


if __name__ == '__main__':
    app.run(debug=True)
