# RACAMOJO -
# SoftDev
# P01
# 2024-12-03
# time spent: 1.5 hrs

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
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    #change image back into blob later, is text rn for testing purposes
    c.execute("CREATE TABLE IF NOT EXISTS memes (id INTEGER PRIMARY KEY AUTOINCREMENT, image TEXT, upvotes INTEGER, creatingUsername TEXT NOT NULL, FOREIGN KEY (creatingUsername) REFERENCES users (username))")
    db.commit()

# Registers a user with a username and password
def addUser(u, p):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u,p))
    exportUsers()
    db.commit()

# Adds a meme to the database
def addMeme(img, user):
    db = get_db()
    c = db.cursor()
    c.execute("INSERT INTO memes (image, upvotes, creatingUsername) VALUES (?,0,?)",(img,user,))
    exportMemes()
    db.commit()

# Gets a list of entries for a specific blog given the blog name
def getUserMemes(username):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, image, upvotes FROM memes WHERE creatingUsername = ?", (username,))
    return c.fetchall()

# Gets a specific meme based on id
def getMeme(id):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, image, upvotes, creatingUsername FROM memes WHERE id = ?", (id,))
    return c.fetchone()  # This returns the first matching row, or None if no match is found

# Gets the user's password (for verification purposes)
def getPass(user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT password FROM users WHERE username =  ?",(user,))
    return c.fetchone()

# Gets a list of all memes
def listAllMemes():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, image, upvotes, creatingUsername FROM memes")
    return c.fetchall()

# Deletes a meme, helper function only
def deleteMeme(id):
    db = get_db()
    c = db.cursor()
    c.execute("DELETE FROM memes WHERE id = ?", (id,))
    exportMemes()
    db.commit()

# Deletes a user
def deleteUser(user):
    db = get_db()
    c = db.cursor()
    c.execute("SELECT meme FROM memes WHERE creatingUsername = ?", (user,))
    allMemes = [row[0] for row in c.fetchall()]
    for meme in allMemes:
        deleteMeme(meme)
    c.execute("DELETE FROM users WHERE username = ?",(user,))
    exportUsers()
    db.commit()
#upvotes a meme
def upvote(id):
    db = get_db()
    c = db.cursor()
    c.execute("UPDATE memes SET upvotes = upvotes + 1 WHERE id = ?", (id,))
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

#print(getMeme(1))
#upvote(1)
print(getMeme(1))

print(listAllMemes())
deleteMeme(5)
print(listAllMemes())

db.close()
