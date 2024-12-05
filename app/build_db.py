import sqlite3
import csv

DB_FILE = "user.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

# Function to create a new database connection per request (Flask-friendly)
def get_db():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    return db

# Makes tables in the database (run this once, or after changes)
def makeDb():
    db = get_db()
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS memes (id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB, upvotes INTEGER, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id))")
    db.commit()

# Registers a user with a username and password
def addUser(u, p):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)")
    exportUsers()
    db.commit()

# Adds a meme to the database
def addMeme(img, userId):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO memes (image, upvotes, id) VALUES (?,0,?)")
    exportBlogs()
    db.commit()

# Gets a list of entries for a specific blog given the blog name
def getMeme(id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT title, entry, date FROM entries WHERE blogname = ?", (id,))
    return c.fetchall()

# Gets a specific entry based on title
def getMeme(id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT image, upvotes, date FROM memes WHERE id = ?", (id,))
    return c.fetchone()  # This returns the first matching row, or None if no match is found

# Gets the user's password (for verification purposes)
def getPass(user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * password FROM users WHERE username =  ?" )
    return c.fetchone()

def getCreatedMemes(username):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    c.execute("SELECT meme FROM memes WHERE user_id =?", (result,))
    return c.fetchall()

# Gets a list of all blognames (no entries)
def listAllMemes():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT meme FROM memes")
    return c.fetchall()

# Deletes a blog
def deleteMeme(id):
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM memes WHERE id = ?", (id,))
    exportMemes()
    db.commit()

# Deletes a user
def deleteUser(id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT meme FROM memes WHERE user_id = ?", (id,))
    allMemes = [row[0] for row in c.fetchall()]
    for meme in allMemes:
        deleteMeme(meme)
    c.execute("DELETE FROM users WHERE id = ?",(id,))
    exportUsers()
    db.commit()

# Helper function to export data to CSV
def exportToCSV(query, filename):
    db = get_db()
    c = db.cursor()
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        c.execute(query)
        writer.writerow([i[0] for i in c.description])  # Write header
        writer.writerows(c.fetchall())  # Write data

def exportUsers():
    exportToCSV("SELECT * FROM users", 'users.csv')

def exportMemes():
    exportToCSV("SELECT * FROM memes", 'memes.csv')

makeDb()

#testing ground
exportMemes()




db.close()
