from flask import render_template
from myonlinerecipes import app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return "<h1>about</h1>"
