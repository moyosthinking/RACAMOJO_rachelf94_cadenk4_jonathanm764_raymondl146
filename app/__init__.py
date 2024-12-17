from flask import Flask, render_template, session, request, flash, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DB_FILE = "user.db"  # Replace with the correct DB file

def get_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    return db

# Function to add a new user to the database
def addUser(username, password):
    db = get_db()
    c = db.cursor()
    # Check if username already exists
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        return False  # Username already exists

    # Hash the password before storing it
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    db.commit()
    return True

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return redirect(url_for('homepage'))
    return render_template("login.html")

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        c = db.cursor()
        # Hash the password to check against the stored hash
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = c.fetchone()

        if user:
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('homepage'))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for('home'))  # Redirect to login page on failure

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Both username and password are required.", "error")
            return render_template('register.html')

        # Validate if username is already taken
        if addUser(username, password):
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('home'))  # Redirect to login page
        else:
            flash("Username already exists. Please try again.", "error")
            return render_template('register.html')  # Render the registration page again

    return render_template('register.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    if 'username' not in session:
        return redirect(url_for('home'))

    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, image, upvotes, creatingUsername FROM memes")
    memes = c.fetchall()
    images = []
    images.append("https://www.southernliving.com/thmb/m3m-JadISxPYjCOcASeSw3mTmI0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Sunny_Side_Up_Eggs_007-fe57becdb5c4473092cba5e14e407bfc.jpg")
    for meme in memes:
        image = meme[1]
        images.append(image)

    return render_template("homepage.html", memes=images)

@app.route("/create_meme", methods=['GET', 'POST'])
def create_meme():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        image_url = request.form['image_url']
        username = session['username']

        db = get_db()
        c = db.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if c.fetchone() is None:
            flash("Invalid user", "error")
            return redirect(url_for('create_meme'))
        
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'data' in data and data['data']:
                return {"link": data['data']['images']["original"]["url"], "title": data['data']['title']}
            else:
                return "No image found"
    return render_template("create_meme.html")

@app.route("/memes")  # i don't see how this is different from homepage
def memes():
    if 'username' not in session:
        return redirect(url_for('home'))

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

if __name__ == "__main__":
    app.run(debug=True)
