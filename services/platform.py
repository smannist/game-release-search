from cmath import exp
from db import db

def get_platform_image(id):
    sql = "SELECT image FROM platforms WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_platform_info():
    sql = "SELECT id, name FROM platforms"
    result = db.session.execute(sql)
    return result.fetchall()

def get_platform(id):
    sql = "SELECT name FROM platforms WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def add_platform(name, image):
    try:
        sql = "INSERT INTO platforms (name, image) VALUES (:name, :image)"
        db.session.execute(sql, {"name":name, "image":image})
        db.session.commit()
        return True
    except:
        return False

def delete_platform(id):
    sql = "DELETE FROM platforms WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def edit_platform(name, image, id):
    sql = "UPDATE platforms SET name=:name, image=:image WHERE id=:id"
    db.session.execute(sql, {"name":name, "image":image, "id":id})
    db.session.commit()
    