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
    c.execute("CREATE TABLE IF NOT EXISTS memes (id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB, caption TEXT, upvotes INTEGER, FOREIGN KEY(user_id) REFERENCES users(id)")
    db.commit()

# Registers a user with a username and password
def addUser(u, p):
    db = get_db()
    c = db.cursor()
    c.execute(INSERT INTO users (username, password) VALUES (?, ?))
    exportUsers()
    db.commit()

# Adds a meme to the database
def addMeme(user, b):
    db = get_db()
    c = db.cursor()
    c.execute(UPDATE users SET blogname = ? WHERE username = ?)
    c.execute(INSERT INTO memes (image, caption, upvotes) VALUES (?,?,0))
    exportBlogs()
    db.commit()

# Gets a list of entries for a specific blog given the blog name
def getMeme(bname):
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT title, entry, date FROM entries WHERE blogname = '{bname}'")
    return c.fetchall()

# Update an existing blog entry
def updateEntry(oldTitle, newTitle, newText, newDate):
    db = get_db()
    c = db.cursor()

    # Update the entry based on the old title
    c.execute(f'''UPDATE entries
                 SET title = '{newTitle}', entry = '{newText}', date = '{newDate}'
                 WHERE title = '{oldTitle}' ''')

    db.commit()

# Gets a specific entry based on title
def getEntry(title):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname, entry, date FROM entries WHERE title = ?", (title,))
    return c.fetchone()  # This returns the first matching row, or None if no match is found

# Gets a random entry from the entries table
def getRandomEntry():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname, title, entry, date FROM entries ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()  # Fetches a random entry

    # If no result is found, return a tuple with None values
    return result if result else (None, None, None, None)

def getMostRecentEntry(username):
    db = get_db()
    c = db.cursor()
    c.execute("""
        SELECT b.blogname, e.title, e.entry, e.date
        FROM entries e
        JOIN blogs b ON e.blogname = b.blogname
        JOIN users u ON b.blogname = u.blogname
        WHERE u.username = ?
        ORDER BY e.date DESC
        LIMIT 1
    """, (username,))

    return c.fetchone()

def getEntry(title):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname, entry, date FROM entries WHERE title = ?", (title,))
    result = c.fetchone()
    return result


# Gets the user's password (for verification purposes)
def getPass(user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * password FROM users WHERE username =  ?")
    return c.fetchone()

def getCreatedMemes(username):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    c.execute("SELECT meme FROM memes WHERE user_id =?", (result,))
    return result[0] if result else None

# Gets a list of all blognames (no entries)
def listAllMemes():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT blogname FROM blogs")
    return c.fetchall()

# Deletes a blog
def deleteMeme(id):
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM memes WHERE id = ?", (id,))
    exportMemes()
    db.commit()

# Deletes a user
def deleteUser(username):
    db = get_db()
    c = db.cursor()
    c.execute(f"SELECT blogname FROM users WHERE username = '{username}'")
    blognames = [row[0] for row in c.fetchall()]
    for blog in blognames:
        deleteBlog(blog)
    c.execute(f"DELETE FROM users WHERE username = '{username}'")
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
    exportToCSV("SELECT * FROM blogs", 'memes.csv')

makeDb()
db.close()
