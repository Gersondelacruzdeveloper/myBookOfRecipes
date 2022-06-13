from myonlinerecipes import app
from flask import render_template, request, redirect, url_for
from myonlinerecipes.models import Recipes

@app.route("/")
def home():
    recipes = list(Recipes.query.all())
    return render_template("home.html", recipes=recipes )

@app.route("/about")
def about():
    return "<h1>about</h1>"
