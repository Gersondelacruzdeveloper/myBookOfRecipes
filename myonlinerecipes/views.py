from curses import flash
from myonlinerecipes import app, db, mail
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from myonlinerecipes.models import Recipes
from .models import User, Recipes, Comments
from flask_mail import Message
import os
from functools import wraps


# Login decorator allow just logged in users
# Code taken
# from https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            flash("Log in to access your account.")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Home function
@app.route("/")
def home():
    recipes = list(Recipes.query.filter_by(is_private=False))
    return render_template("home.html", recipes=recipes)


# Contact form
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        subject = request.form.get('subject')

        msg = Message(
            subject=subject,
            body= "E-mail: " + name + "\n" + message + "\n" + email,
            sender=os.environ.get("MAIL_USERNAME"),
            recipients=[os.environ.get("MAIL_USERNAME")],
        )
        mail.send(msg)
        return redirect(url_for('email_sent_comfirmation'))
    return render_template("contact.html")


# Give the user a nice comfirmation about their email
@app.route("/email_sent_comfirmation")
def email_sent_comfirmation():
    return render_template("email.html")


# details recipe function
@app.route("/detail_recepe/<recipe_id>", methods=["GET", "POST"])
def detail_recepe(recipe_id):

    if request.method == 'POST':
        user = User.query.filter_by(username=session["user"]).first()
        comment = request.form.get('comment'),
        new_comment = Comments(
            content=comment,
            created=date.today(),
            recipes_id=recipe_id,
            user=user.id,
        )
        # add the new comment to the database
        db.session.add(new_comment)
        db.session.commit()
        flash("You have commented on this recipe Succesfullly")
    recipe = Recipes.query.filter_by(id=recipe_id).first()
    return render_template("detail_recipe.html", recipe=recipe)


# Search function
@app.route("/search_result", methods=["GET", "POST"])
def search_result():
    search_input = request.form.get('search')
    # Select all public recipes
    public_recipes = Recipes.query.filter_by(is_private=False)
    recipes_array = []
    # check if recipe contains the user input
    # and if it does, then append it to recipes_array
    if search_input:
        for recipes in public_recipes:
            if (search_input in recipes.title or
                search_input in recipes.method or
                    search_input in recipes.Ingredients):
                recipes_array.append(recipes)
    else:
        recipes_array = list(Recipes.query.filter_by(is_private=False))

    return render_template(
        "search.html",
        recipes=recipes_array,
        search_input=search_input)


# my recipes function
@app.route("/myrecipes")
@login_required
def myrecipes():
    user = User.query.filter_by(username=session["user"]).first()
    recipes = user.recipes
    return render_template("myrecipes.html", recipes=recipes)


# Edit recipes function
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    if request.method == "POST":
        # Varaibles and filters
        user = User.query.filter_by(username=session["user"]).first()
        service_size = request.form.get('service_size') or None
        cooking_time = request.form.get('cooking_time') or None
        switch = request.form.get('switch')
        if switch:
            switch = True
        else:
            switch = False

        # Updating the data
        Recipes.query.filter_by(id=recipe_id).update(dict(
            user=user.id,
            title=request.form.get('title'),
            image_url=request.form.get('image'),
            Ingredients=request.form.get('ingredients'),
            method=request.form.get('method'),
            service_size=service_size,
            cooking_time=cooking_time,
            is_private=switch,
            date_created=date.today(),
            calories=request.form.get('calories'),
            fat=request.form.get('fat'),
            protein=request.form.get('protein'),
            carbohidrates=request.form.get('carbohidrates'),
            salt=request.form.get('salt'),
        ))
        db.session.commit()
        flash("Recipe updated Succesfullly")
        return redirect(url_for('myrecipes'))
    recipe = Recipes.query.filter_by(id=recipe_id).first()
    return render_template("edit_recipe.html", recipe=recipe)


# comfirm delete recipes
@app.route("/comfirm_delete/<recipe_id>")
@login_required
def comfirm_delete(recipe_id):
    recipe = Recipes.query.filter_by(id=recipe_id).first()
    return render_template("comfirm_delete.html", recipe=recipe)


# delete recipes
@app.route("/delete_recipe/<recipe_id>")
@login_required
def delete_recipe(recipe_id):
    recipe = Recipes.query.filter_by(id=recipe_id).first()
    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe delete Succesfullly")
    return redirect(url_for('myrecipes'))


# myrecipes form function
@app.route("/myrecipes_form", methods=["GET", "POST"])
@login_required
def myrecipes_form():
    if request.method == "POST":
        user = User.query.filter_by(username=session["user"]).first()
        service_size = request.form.get('service_size') or None
        cooking_time = request.form.get('cooking_time') or None
        switch = request.form.get('switch')

        if switch:
            switch = True
        else:
            switch = False

        # Assigning the user input to the model fields
        new_recipe = Recipes(
            user=user.id,
            title=request.form.get('title'),
            image_url=request.form.get('image'),
            Ingredients=request.form.get('ingredients'),
            method=request.form.get('method'),
            service_size=service_size,
            cooking_time=cooking_time,
            is_private=switch,
            date_created=date.today(),
            calories=request.form.get('calories'),
            fat=request.form.get('fat'),
            protein=request.form.get('protein'),
            carbohidrates=request.form.get('carbohidrates'),
            salt=request.form.get('salt'),
        )
        # add the new recipe to the database
        db.session.add(new_recipe)
        db.session.commit()

        flash("Recipe created Succesfullly")
        return redirect(url_for('myrecipes'))
    return render_template("myrecipes_form.html")


# Logout function
@app.route("/logout")
@login_required
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop('user')
    return redirect(url_for("login"))


# signup function
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # Getting user input info
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        # check if user already exist
        existing_user = User.query.filter_by(username=username).first()
        # check if email already exist
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
                email=email,
                username=username,
                password=generate_password_hash(password, method='sha256'),
                created_on=date.today(),
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
        # check if user already exist
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            # check_password_hash
            # ensure hashed password matches user imput
            if (
                check_password_hash(
                    existing_user.password, request.form.get("password"))):
                session["user"] = username
                return redirect(url_for("home"))
            else:
                # invalid password match
                flash("Username or password are incorrect")
                return redirect(url_for("login"))
        else:
            flash("Username or password are incorrect")
            return redirect(url_for("login"))

    return render_template("registration/login.html", username=username)


# Page not found 404 error
@app.errorhandler(404)
def page_not_found(e):
    # Display the custom 404, Page Not Found, page.
    return render_template("404.html"), 404


# Internal Server error
@app.errorhandler(500)
def server_error_500(e):
    # Display a custom 500 Page for internal error.
    return render_template("500.html"), 500
