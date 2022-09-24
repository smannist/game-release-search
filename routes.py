from flask import render_template, redirect, request, session
from app import app
from services import user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user.validate_user(username, password):
            session["username"] = username
            return redirect("/platforms")
        return render_template("signin.html")

@app.route("/signout")
def signout():
    del session["username"]
    return redirect("/")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return render_template("signup.html", message="Fields cannot be empty. Please try again.")
        if not user.create_user(username, password):
            return render_template("signup.html", message="Username already taken. Please try again.")
        return redirect("/signin")

@app.route("/platforms")
def platforms():
    return render_template("platforms.html")