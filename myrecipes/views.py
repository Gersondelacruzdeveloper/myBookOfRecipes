from myrecipes import app

@app.route("/")
def home():
    return "hellow world"

@app.route("/about")
def about():
    return "<h1>about</h1>"
