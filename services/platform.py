from flask import Flask
from db import db

def get_platform_image(id):
    sql = "SELECT image FROM platforms WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_platform():
    sql = "SELECT id, name FROM platforms"
    result = db.session.execute(sql)
    return result.fetchall()

def add_platform(name, image):
    sql = "INSERT INTO platforms (name, image) VALUES (:name, :image)"
    db.session.execute(sql, {"name":name, "image":image})
    db.session.commit()