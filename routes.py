from flask import render_template, request
from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def singup():
    return render_template("signup.html")

@app.route("/platforms")
def platforms():
    return render_template("platforms.html")