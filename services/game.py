from db import db

def get_game_info(platform):
    platform.replace("%20", " ")
    sql = "SELECT title, synopsis, to_char(release_date, 'DD/MM/YYYY') AS release_date, name, games.id, israted FROM games\
           INNER JOIN platforms ON platforms.id=games.platform_id \
           WHERE platforms.name=:platform \
           ORDER BY games.id"
    result = db.session.execute(sql, {"platform":platform})
    return result.fetchall()

def get_rating_info():
    sql = "SELECT TRUNC(AVG(rating),2) AS rating, game_id FROM ratings \
           INNER JOIN games ON games.id=ratings.game_id \
           WHERE games.id=ratings.game_id \
           GROUP BY game_id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_user_rated_games(username):
    sql = "SELECT rating, games.title, users.username FROM ratings \
          INNER JOIN games ON games.id=ratings.game_id \
          INNER JOIN users ON users.id=ratings.user_id \
          WHERE games.id=ratings.game_id AND users.username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchall()

## insert if game rating doesn't exist, else update game rating
def rate_game(rating,user_id,game_id):
    sql_insert = "INSERT INTO ratings (rating,user_id,game_id) \
                  SELECT :rating,:user_id,:game_id \
                  WHERE NOT EXISTS \
                  (SELECT user_id,game_id FROM ratings WHERE user_id=:user_id AND game_id=:game_id)"
    sql_update = "UPDATE ratings SET rating=:rating WHERE user_id=:user_id AND game_id=:game_id"
    db.session.execute(sql_insert, {"rating":rating, "user_id":user_id, "game_id":game_id})
    db.session.commit()
    db.session.execute(sql_update, {"rating":rating,"user_id":user_id, "game_id":game_id})
    db.session.commit()

def set_rated_true(game_id):
    sql = "UPDATE games SET israted=TRUE WHERE id=:game_id"
    db.session.execute(sql, {"game_id":game_id})
    db.session.commit()

def get_distinct_games():
    sql = "SELECT MAX(id) AS id, MAX(title) AS title FROM games GROUP BY title"
    result = db.session.execute(sql)
    return result.fetchall()

def games_by_platform():
    sql = "SELECT games.id AS id,games.title,platforms.name FROM platforms \
           INNER JOIN games ON games.platform_id=platforms.id \
           WHERE games.platform_id=platforms.id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_game(id):
    sql = "SELECT title FROM games WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def add_game(title,synopsis,release_date,platform_id):
    sql = "INSERT INTO games (title,synopsis,release_date,platform_id) \
           SELECT :title,:synopsis,:release_date,:platform_id \
           WHERE NOT EXISTS \
           (SELECT title, platform_id FROM games WHERE title=:title AND platform_id=:platform_id)"
    db.session.execute(sql, {"title":title, "synopsis":synopsis, "release_date":release_date, "platform_id":platform_id})
    db.session.commit()

def edit_game(title,synopsis,release_date,platform_id,game_id):
    sql = "UPDATE games SET title=:title, synopsis=:synopsis, release_date=:release_date, platform_id=:platform_id, id=:game_id \
           WHERE id=:game_id"
    db.session.execute(sql, {"title":title, "synopsis":synopsis, "release_date":release_date, "platform_id":platform_id, "game_id":game_id})
    db.session.commit()

def delete_game(id):
    sql = "DELETE FROM games WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
