from flask import render_template, redirect, request, session, make_response
from app import app
from services import user, platform, game
from utils import util

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
            return redirect("/platforms")
        return render_template("signin.html", error=True)

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
        if user.create_user(username, password):
            return redirect("/signin")
        return render_template("signup.html", error=True)

@app.route("/platforms")
def platforms():
    platforms = platform.get_platform()
    return render_template("platforms.html", platforms=platforms)

@app.route("/platforms/<string:platform>/games", methods=["GET", "POST"])
def games(platform):
    if request.method == "GET":
        games = game.get_game_info(platform)
        all_ratings = game.get_rating_info()
        return render_template("games.html", games=games, all_ratings=all_ratings, platform=platform)
    if request.method == "POST":
        user.check_csrf()
        rating_info = util.string_to_list(request.form["rating_info"])
        rating = rating_info[0]
        game_id = rating_info[1]
        user_id = session["user_id"]
        game.set_rated_true(game_id)
        game.rate_game(rating, user_id, game_id)
        return redirect(f"/platforms/{platform}/games")

@app.route("/image/<int:id>")
def images(id):
    data = platform.get_platform_image(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/<string:username>/myratings")
def myratings(username):
    if session["username"] == username:
        user_ratings = game.get_user_rated_games(username)
        return render_template("myratings.html", user_ratings=user_ratings)
    return render_template("restrict.html")