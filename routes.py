from flask import render_template, redirect, request, session, make_response, flash
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
    del session["csrf_token"]
    del session["user_id"]
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
    return render_template("unauthorized.html")

@app.route("/adminportal")
def admin_portal():
    if user.is_admin():
        return render_template("adminportal.html")
    return render_template("unauthorized.html")

@app.route("/adminportal/manageplatforms")
def manage_platforms():
    if user.is_admin():
        platforms = platform.get_platform()
        return render_template("manageplatforms.html", platforms=platforms)
    return render_template("unauthorized.html")

@app.route("/addplatform", methods=["POST"])
def add_platform():
    user.check_csrf()
    platforms = platform.get_platform()
    name = request.form["name"]
    file = request.files["file"]
    image = file.read()
    if name.isspace():
        return render_template("manageplatforms.html", platforms=platforms, errorName=True)
    if util.validate_img_type(file) and len(image) < 100*1024:
        platform.add_platform(name, image)
        return render_template("manageplatforms.html", platforms=platforms, add=True)
    else:
        return render_template("manageplatforms.html", platforms=platforms, errorFile=True)

@app.route("/deleteplatform", methods=["POST"])
def delete_platform():
    user.check_csrf()
    id = request.form["id"]
    platform.delete_platform(id)
    flash("Platform deleted successfully!")
    return redirect("/adminportal/manageplatforms")

@app.route("/editplatform", methods=["POST"])
def edit_platform():
    user.check_csrf()
    name = request.form["name_edit"]
    file = request.files["file_edit"]
    id = request.form["id_edit"]
    image = file.read()
    if name.isspace():
        return redirect("/adminportal/manageplatforms")
    if util.validate_img_type(file) and len(image) < 100*1024:
        platform.edit_platform(name, image, id)
        return redirect("/adminportal/manageplatforms")
    return redirect("/adminportal/manageplatforms")

@app.route("/adminportal/managegamerating")
def managegamerating():
    if user.is_admin():
        platforms = platform.get_platform()
        games = game.get_all_games()
        return render_template("managegamerating.html", platforms=platforms, games=games)
    return render_template("unauthorized.html")

@app.route("/addgame", methods=["POST"])
def add_game():
    user.check_csrf()
    platform_id = request.form["id_p_add"]
    title = request.form["title_add"]
    synopsis = request.form["synopsis_add"]
    release_date = request.form["release_add"]
    game.add_game(title,synopsis,release_date,platform_id)
    return redirect("/adminportal/managegamerating")

@app.route("/editgame", methods=["POST"])
def edit_game():
    user.check_csrf()
    game_id = request.form["id_g_edit"]
    platform_id = request.form["id_p_edit"]
    title = request.form["title_edit"]
    synopsis = request.form["synopsis_edit"]
    release_date = request.form["release_edit"]
    game.edit_game(title,synopsis,release_date,platform_id,game_id)
    return redirect("/adminportal/managegamerating")

@app.route("/deletegame", methods=["POST"])
def delete_game():
    id = request.form["id_delete"]
    game.delete_game(id)
    return redirect("/adminportal/managegamerating")