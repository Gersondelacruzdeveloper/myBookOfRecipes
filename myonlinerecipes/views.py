from curses import flash
from myonlinerecipes import app
from myonlinerecipes import db
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from myonlinerecipes.models import Recipes
from .models import User

# Home function 
@app.route("/")
def home():
    recipes = list(Recipes.query.all())
    return render_template("home.html", recipes=recipes )

# About function 
@app.route("/about")
def about():
    return "<h1>about</h1>"


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
        existing_user_email = User.query.filter_by(email=email).first()
        # generate_password_hash(password, method='sha256')
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
            password = password,
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
        password = request.form.get('password')
        #check if user already exist
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            # check_password_hash
            #ensure hashed password matches user imput
            if existing_user.password == password:
                session["user"] = username
                flash("Welcome")
                return redirect(url_for("home"))
            else:
                #invalid password match
                flash("Username or password are incorrect")
                return redirect(url_for("login"))
        else:
            flash("Username or password are incorrect")
            return redirect(url_for("login"))

    return render_template("registration/login.html", username=username)