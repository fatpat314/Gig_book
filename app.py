from flask import Flask, render_template

app = Flask (__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Gig_book')

@app.route('/swing')
def swing():
    """Show Swing songs"""
    return render_template('swing.html')

@app.route('/Benny_Goodman')
def Benny_Goodman():
    return render_template('Benny_Goodman.html')


if __name__ == '__main__':
    app.run(debug=True)
