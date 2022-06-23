
from curses import flash
from curses.ascii import isctrl
from myonlinerecipes import app
from myonlinerecipes import db
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from myonlinerecipes.models import Recipes
from .models import User, Recipes

# Home function 
@app.route("/")
def home():
    recipes = list(Recipes.query.filter_by(is_private = False))
    return render_template("home.html", recipes=recipes )

# About function 
@app.route("/about")
def about():
    return "<h1>about</h1>"

# my recipes function 
@app.route("/myrecipes")
def myrecipes():
    user = User.query.filter_by(username=session["user"]).first()
    recipes = user.recipes
    return render_template("myrecipes.html", recipes=recipes)

# my recipes form function  
@app.route("/myrecipes_form", methods=["GET", "POST"])
def myrecipes_form():

    user = User.query.filter_by(username=session["user"]).first()
    if request.method == "POST":

        service_size = request.form.get('service_size') or 0
        cooking_time = request.form.get('cooking_time') or 0
        switch = request.form.get('switch')

        if switch:
            switch = True

        new_recipe = Recipes(
            user = user.id,
            title = request.form.get('title'),
            image_url = request.form.get('image'),
            Ingredients = request.form.get('ingredients'),
            method =  request.form.get('method'),
            service_size = service_size,
            cooking_time = cooking_time,
            is_private = switch,
            date_created = date.today(),
            calories = request.form.get('calories'),
            fat = request.form.get('fat'),
            protein = request.form.get('protein'),
            carbohidrates = request.form.get('carbohidrates'),
            salt = request.form.get('salt'),
        )
         # add the new recipe to the database
        db.session.add(new_recipe)
        db.session.commit()

        flash("Recipe created Succesfullly")
        return redirect(url_for('myrecipes'))
    return render_template("myrecipes_form.html")

# logout function 
@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop('user')
    return redirect(url_for("login"))

# signup function 
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    today = date.today()
    if request.method == "POST":
         #check if user already exist
        existing_user = User.query.filter_by(username=username).first()
        #check if email already exist
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User already exits")
            return redirect(url_for("sign_up"))
    
        elif existing_user_email:
            flash("Email already exits")
            return redirect(url_for("sign_up"))

        elif password != repeat_password:
            flash("The passwords do not match")
            return redirect(url_for("sign_up"))
        else:
            new_user = User(
            email = email, 
            username = username,
            password = generate_password_hash(password, method='sha256'),
            created_on = today, 
        )
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash("Registration succesful")
        return redirect(url_for("login"))
    return render_template("registration/signup.html")


# Login function 
@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get('username')
    if request.method == "POST":
        username = request.form.get('username')
        #check if user already exist
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            # check_password_hash
            #ensure hashed password matches user imput
            if check_password_hash(existing_user.password, request.form.get("password")):
                session["user"] = username
                return redirect(url_for("home"))
            else:
                #invalid password match
                flash("Username or password are incorrect")
                return redirect(url_for("login"))
        else:
            flash("Username or password are incorrect")
            return redirect(url_for("login"))

    return render_template("registration/login.html", username=username)