from flask import Flask, render_template, session, request, flash, redirect
import sqlite3

app = Flask(__name__)

DB_FILE="user.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
c.execute("CREATE TABLE IF NOT EXISTS user_information (username TEXT, password TEXT)")
@app.route("/")
def login():
    if 'username' in session and 'password' in session:
        username = session['username']
        return render_template('homepage.html')
    return render_template("login.html")
@app.route("/auth", methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        c.execute("SELECT * FROM user_information WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            session['username'] = username
            session['password'] = password
            flash("Woo!", "success")
            return redirect('blog.html')
        else:
            flash(":( try again", "error")
            return redirect('/create')
    return redirect('/')
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            c.execute('INSERT INTO user_information (username, password) VALUES (?, ?)', (username, password))
            db.commit()
            c.execute(f'''CREATE TABLE IF NOT EXISTS {username} (title TEXT, content TEXT, datePublished TEXT)''')
            db.commit()
            session['username'] = username
            session['password'] = password
            flash("Registration successful!", "success")
            return render_template("blog.html")
        except sqlite3.IntegrityError:
            flash("Username already exists. Choose a different one.", "error")
            return render_template('create_meme.html')
    return render_template('create_meme.html')
@app.route("/")
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route("/entry", methods=['GET', 'POST'])
def createBlog():
    if 'username' not in session:
        return redirect('/')  # not logged in
    if request.method == 'POST':
        blog = (request.form['title'], request.form['content'], request.form['datePublished'])
        username = session['username']
        c.execute(f"INSERT INTO {username} (title, content, datePublished) VALUES (?, ?, ?)", (blog))
        db.commit()
        flash("You made a blog!", "success")
        return redirect('/reading')  # go to all blogs
    return render_template('entry.html', username=username)
@app.route("/reading")
def reading():
    if 'username' not in session:
        return redirect('/')  # not logged in

    username = session['username']

    c.execute(f"SELECT * FROM {username}")
    blogs = c.fetchall()

    return render_template('reading.html', blogs=blogs)

if __name__ == "__main__":
    app.debug = True
    app.run()
