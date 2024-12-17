# RACAMOJO -
# SoftDev
# P01
# 2024-12-03
# time spent: 2 hrs

from flask import Flask, render_template, session, request, flash, redirect, url_for
import sqlite3
import requests
import shutil
import config

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
count = 0

DB_FILE = "user.db"

def get_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    return db

@app.route("/",methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return redirect(url_for('homepage'))
    return render_template("login.html")

@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db() # can't this be reaplced by addUser
        c = db.cursor()
        c.execute("SELECT * FROM user_information WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        # if user:
        #     session['username'] = username
        #     flash("Woo! You are logged in.", "success")
        #     return redirect(url_for('homepage'))
        # else:
        #     flash(":( Try again.", "error")
        #     return redirect(url_for('login'))
    return render_template("register.html")


# @app.route('/generate_image', methods=['GET', 'POST'])
# def generate_image():

#     api_url = 'https://api.api-ninjas.com/v1/randomimage?category'
#     api_key = config.randomImage_Key
#     response = requests.get(api_url, headers={'X-Api-Key': api_key, 'Accept': 'image/jpg'}, stream=True) # generates a random image
#     count2 = count + 1
#     if response.status_code == requests.codes.ok:
#         image_data = response.raw.read()
#         username = session['username']
#         addImage(image_data, username) #stores image data in database
#         image = getUserMemes(username)
#         # filename = f'img{count2}.jpg' #creates a file of random image and stores it in current directory
#         # with open(filename, 'wb') as out_file:
#         #     shutil.copyfileobj(response.raw, out_file)
#         return render_template('create_meme.html', image=image)
#     else:
#         print(f"Error: {response.status_code} - {response.reason}")
#     return redirect(url_for('create'))

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
    return render_template('logout.html')

@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
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
        username = session['username']
        db = get_db()
        c = db.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if c.fetchone() is None:
            flash("Invalid user", "error")
            return redirect(url_for('create_meme'))
        
        api_url = 'https://api.api-ninjas.com/v1/randomimage?category'
        api_key = config.randomImage_Key
        response = requests.get(api_url, headers={'X-Api-Key': api_key, 'Accept': 'image/jpg'}, stream=True) # generates a random image
        if response.status_code == requests.codes.ok:
            image_url = response.raw.read()
            # filename = f'img{count2}.jpg' #creates a file of random image and stores it in current directory
            # with open(filename, 'wb') as out_file:
            #     shutil.copyfileobj(response.raw, out_file)
        else:
            print(f"Error: {response.status_code} - {response.reason}")

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

@app.route("/memes") # i dont see how this is different from homepage
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