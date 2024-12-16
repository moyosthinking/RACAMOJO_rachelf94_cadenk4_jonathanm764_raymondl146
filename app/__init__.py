from flask import Flask, render_template, session, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DB_FILE = "user.db"

def get_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    return db

@app.route("/")
def login():
    if 'username' in session:
        return redirect(url_for('homepage'))
    return render_template("login.html")

@app.route("/auth", methods=['POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        c = db.cursor()
        c.execute("SELECT * FROM user_information WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            session['username'] = username
            flash("Woo! You are logged in.", "success")
            return redirect(url_for('homepage'))
        else:
            flash(":( Try again.", "error")
            return redirect(url_for('login'))

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        c = db.cursor()
        try:
            c.execute('INSERT INTO user_information (username, password) VALUES (?, ?)', (username, password))
            db.commit()
            c.execute(f'''CREATE TABLE IF NOT EXISTS {username} (title TEXT, content TEXT, datePublished TEXT)''')
            db.commit()
            session['username'] = username
            flash("Registration successful!", "success")
            return redirect(url_for('homepage'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Choose a different one.", "error")
            return render_template('create_meme.html')
    return render_template('create_meme.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, image, upvotes, creatingUsername FROM memes")
    memes = c.fetchall()

    return render_template("homepage.html", memes=memes)

@app.route('/generate_meme', methods=['GET'])
def generate_meme():
    response = requests.get("http://alpha-meme-maker.herokuapp.com/")
    
    if response.status_code == 200:
        meme_url = response.json().get("url", "")
        return render_template('meme.html', meme_url=meme_url)
    else:
        return jsonify({"error"}), 500


@app.route("/create_meme", methods=['GET', 'POST'])
def create_meme():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        image_url = request.form['image_url']
        username = session['username']

        db = get_db()
        c = db.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if c.fetchone() is None:
            flash("Invalid user", "error")
            return redirect(url_for('create_meme'))
        
        if addMeme(image_url, username):
            flash("Meme created successfully!", "success")
            return redirect(url_for('homepage'))
        else:
            flash("Failed to create meme", "error")
            return redirect(url_for('create_meme'))
    
    return render_template("create_meme.html")

@app.route("/upvote_meme/<int:meme_id>")
def upvote_meme(meme_id):
    db = get_db()
    c = db.cursor()
    if upvote(meme_id):
        flash("Meme upvoted!", "success")
    else:
        flash("Meme not found.", "error")
    return redirect(url_for('homepage'))

@app.route("/memes")
def memes():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, image, upvotes, creatingUsername FROM memes")
    memes = c.fetchall()

    return render_template("memes.html", memes=memes)

def addMeme(image_url, username):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO memes (image, upvotes, creatingUsername) VALUES (?, 0, ?)", (image_url, username))
    db.commit()
    return True

def upvote(id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM memes WHERE id = ?", (id,))
    if c.fetchone() is None:
        return False
    c.execute("UPDATE memes SET upvotes = upvotes + 1 WHERE id = ?", (id,))
    db.commit()
    return True

if __name__ == "__main__":
    app.run(debug=True)
