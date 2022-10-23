from flask import render_template, redirect, request, session, make_response, flash
from app import app
from services import user, platform, game
from utils import util

@app.route("/")
def index():
    is_admin = user.is_admin()
    return render_template("index.html", admin=is_admin)

@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user.validate_user(username, password):
            if user.is_admin():
                return redirect("/adminportal")
            return redirect("/platforms")
        flash("Invalid username or password", "signin")
        return render_template("signin.html")
    return render_template("signin.html")

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
        flash("Username is already taken or invalid input", "signup")
        return render_template("signup.html")
    return render_template("signup.html")

@app.route("/platforms")
def platforms():
    is_admin = user.is_admin()
    get_platforms = platform.get_platform_info()
    return render_template("platforms.html", platforms=get_platforms, admin=is_admin)

@app.route("/platforms/<string:platform>/games", methods=["GET", "POST"])
def games(platform):
    is_admin = user.is_admin()
    if request.method == "GET":
        get_games = game.get_game_info(platform)
        all_ratings = game.get_rating_info()
        return render_template("games.html", games=get_games, all_ratings=all_ratings, platform=platform, admin=is_admin)
    if request.method == "POST":
        user.check_csrf()
        rating_info = util.string_to_list(request.form["rating_info"])
        rating = rating_info[0]
        game_id = rating_info[1]
        user_id = session["user_id"]
        target_game = game.get_game(game_id)
        game.set_rated_true(game_id)
        game.rate_game(rating, user_id, game_id)
        flash(f"You rated {target_game} {rating}/5!", "rated")
        return redirect(f"/platforms/{platform}/games")
    return render_template("games.html", games=games, all_ratings=all_ratings, platform=platform, admin=is_admin)

@app.route("/image/<int:id>")
def images(id):
    data = platform.get_platform_image(id)
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/<string:username>/myratings")
def myratings(username):
    is_admin = user.is_admin()
    if session["username"] == username:
        user_ratings = game.get_user_rated_games(username)
        return render_template("myratings.html", user_ratings=user_ratings, admin=is_admin)
    return render_template("unauthorized.html")

@app.route("/adminportal")
def admin_portal():
    is_admin = user.is_admin()
    if user.is_admin():
        return render_template("adminportal.html", admin=is_admin)
    return render_template("unauthorized.html")

@app.route("/adminportal/manageplatforms")
def manage_platforms():
    is_admin = user.is_admin()
    if user.is_admin():
        platforms = platform.get_platform_info()
        return render_template("manageplatforms.html", platforms=platforms, admin=is_admin)
    return render_template("unauthorized.html")

@app.route("/addplatform", methods=["POST"])
def add_platform():
    user.check_csrf()
    name = request.form["name"]
    file = request.files["file"]
    image = file.read()
    if name.isspace():
        flash("Platform name cannot contain only spaces", "add")
        return redirect("/adminportal/manageplatforms")
    if util.validate_img_type(file) and len(image) < 100*1024:
        if platform.add_platform(name, image):
            flash(f"Platform {name} added successfully!", "add")
            return redirect("/adminportal/manageplatforms")
        else:
            flash(f"Platform {name} already exists", "add")
            return redirect("/adminportal/manageplatforms")
    flash("Image size to large (max 100 kB) or wrong type (not PNG/JPG)", "add")
    return redirect("/adminportal/manageplatforms")

@app.route("/deleteplatform", methods=["POST"])
def delete_platform():
    user.check_csrf()
    id = request.form["id"]
    target_platform = platform.get_platform(id)
    platform.delete_platform(id)
    flash(f"Platform {target_platform} deleted successfully!", "delete")
    return redirect("/adminportal/manageplatforms")

@app.route("/editplatform", methods=["POST"])
def edit_platform():
    user.check_csrf()
    name = request.form["name_edit"]
    file = request.files["file_edit"]
    id = request.form["id_edit"]
    image = file.read()
    target_platform = platform.get_platform(id)
    if name.isspace():
        flash("Platform name cannot contain only spaces", "edit")
        return redirect("/adminportal/manageplatforms")
    if util.validate_img_type(file) and len(image) < 100*1024:
        platform.edit_platform(name, image, id)
        flash(f"Platform {target_platform} edited successfully!", "edit")
        return redirect("/adminportal/manageplatforms")
    flash("Image size to large (max 100 kB) or wrong type (not PNG/JPG)", "edit")
    return redirect("/adminportal/manageplatforms")

@app.route("/adminportal/managegamerating")
def managegamerating():
    is_admin = user.is_admin()
    if user.is_admin():
        platforms = platform.get_platform_info()
        users = user.get_user_info()
        games = game.get_distinct_games()
        games2 = game.games_by_platform()
        return render_template("managegamerating.html", users=users, platforms=platforms, games=games, games2=games2, admin=is_admin)
    return render_template("unauthorized.html")

@app.route("/addgame", methods=["POST"])
def add_game():
    user.check_csrf()
    platform_id = request.form["id_p_add"]
    title = request.form["title_add"]
    synopsis = request.form["synopsis_add"]
    release_date = request.form["release_add"]
    if len(synopsis) > 125:
        flash("Synopsis should be no longer than 125 characters", "add")
        return redirect("/adminportal/managegamerating")
    if not util.validate_date(release_date):
        flash("Date should be in YYYY-MM-DD format", "add")
        return redirect("/adminportal/managegamerating")
    if title.isspace() or synopsis.isspace() or release_date.isspace():
        flash("Fields cannot contain only spaces", "add")
        return redirect("/adminportal/managegamerating")
    game.add_game(title,synopsis,release_date,platform_id)
    flash(f"Game {title} added successfully (if it did not already exist)!", "add")
    return redirect("/adminportal/managegamerating")

@app.route("/editgame", methods=["POST"])
def edit_game():
    user.check_csrf()
    game_id = request.form["id_g_edit"]
    platform_id = request.form["id_p_edit"]
    title = request.form["title_edit"]
    synopsis = request.form["synopsis_edit"]
    release_date = request.form["release_edit"]
    target_game = game.get_game(game_id)
    if len(synopsis) > 125:
        flash("Synopsis should be no longer than 125 characters", "edit")
        return redirect("/adminportal/managegamerating")
    if not util.validate_date(release_date):
        flash("Date should be in YYYY-MM-DD format", "edit")
        return redirect("/adminportal/managegamerating")
    if title.isspace() or synopsis.isspace() or release_date.isspace():
        flash("Fields cannot contain only spaces", "edit")
        return redirect("/adminportal/managegamerating")
    game.edit_game(title,synopsis,release_date,platform_id,game_id)
    flash(f"Game {target_game} edited successfully!", "edit")
    return redirect("/adminportal/managegamerating")

@app.route("/deletegame", methods=["POST"])
def delete_game():
    user.check_csrf()
    id = request.form["id_delete"]
    target_game = game.get_game(id)
    game.delete_game(id)
    flash(f"Game {target_game} deleted successfully!", "delete")
    return redirect("/adminportal/managegamerating")

@app.route("/deleterating", methods=["POST"])
def delete_rating():
    user.check_csrf()
    id = request.form["id_rating"]
    target_user = user.get_user_by_id(id)
    game.delete_ratings(id)
    flash(f"Ratings by {target_user} deleted successfully!", "rating")
    return redirect("/adminportal/managegamerating")
