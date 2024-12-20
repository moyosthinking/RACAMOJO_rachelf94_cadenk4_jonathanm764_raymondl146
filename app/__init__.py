from flask import Flask, render_template, session, request, flash, redirect, url_for
import sqlite3
#import requests
import shutil
import hashlib
import urllib
#from app import build_db, config

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
count = 0

DB_FILE = "user.db" 

def get_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    return db

def addUser(username, password):
    db = get_db()
    c = db.cursor()
    existing_users = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if existing_users is not None:
        return False  # Username already exists

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    db.commit()

    return True

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return redirect(url_for('homepage'))
    return render_template("login.html")

def checkPass(user, p):
    db = get_db()
    c = db.cursor()
    expected_password = c.execute("SELECT password FROM users WHERE username =  ?", (user,)).fetchone()[0]
    actual_password = hashlib.sha256(p.encode()).hexdigest()

    print("expected", expected_password, "actual", actual_password)
    return expected_password == actual_password

@app.route("/auth", methods=['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    success = checkPass(username, password)

    if success:
        session['username'] = username
        redirect(url_for('homepage'))

    flash("Wrong password!", "error")
    return redirect(url_for("homepage"))

@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')

@app.route("/create", methods=["POST"])
def create():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        flash("Both username and password are required.", "error")
        return render_template('register.html')

    # Validate if username is already taken
    if addUser(username, password):
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('home')) 
    else:
        flash("Username already exists. Please try again.", "error")
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
        return redirect(url_for('home'))  # Redirect to login if not logged in
    username = session['username']

    generate_image()

    # api
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category'
    api_key = config.randomImage_Key
    response = requests.get(api_url, headers={'X-Api-Key': api_key, 'Accept': 'image/jpg'}, stream=True) # generates a random image
    if response.status_code == requests.codes.ok:
        image_url = response.raw.read() #use this with meme api
    else:
        print(f"Error: {response.status_code} - {response.reason}")

    if request.method == 'POST':
        db = get_db()
        c = db.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if c.fetchone() is None:
            flash("Invalid user", "error")
            return redirect(url_for('create_meme'))

        if addMeme(image_url, username):
            flash("Meme created successfully!", "success")
            return redirect(url_for('homepage'))  # Redirect to homepage after meme creation
        else:
            flash("Failed to create meme", "error")
            return redirect(url_for('create_meme'))
    
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'data' in data and data['data']:
                return {"link": data['data']['images']["original"]["url"], "title": data['data']['title']}
            else:
                return "No image found"
    except Exception as e:
        print(f"Error: {e}", e)

    return render_template("create_meme.html")

@app.route("/memes") 
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
