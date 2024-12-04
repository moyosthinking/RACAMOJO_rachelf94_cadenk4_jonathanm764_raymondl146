from flask import Flask, render_template, request, session #this one stores like everything
import os
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def register():
    return render_template("homepage.html");


if __name__ == "__main__":
    app.debug = True
    app.run()
