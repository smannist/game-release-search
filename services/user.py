import secrets
from flask import session, abort, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from utils import util

def create_user(username, password):
    if util.check_user(username, password):
        hash_value = generate_password_hash(password)
        try:
            sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
            return True
        except:
            return False
    return False

def validate_user(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
    return False

def is_admin():
    try:
        user_id = session["user_id"]
        sql = "SELECT role FROM roles WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        role = result.fetchone()[0]
        if role == "admin":
            return True
    except:
        return False
    return False

def get_user_info():
    sql = "SELECT id,username FROM users"
    result = db.session.execute(sql)
    return result.fetchall()

def get_user_by_id(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
