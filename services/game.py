from flask import Flask
from db import db

def get_game_info(platform):
    platform.replace("%20", " ")
    sql = "SELECT title, synopsis, to_char(release_date, 'DD/MM/YYYY') AS release_date, name, games.id FROM games \
           INNER JOIN platforms ON platforms.id=games.platform_id \
           WHERE platforms.name=:platform"
    result = db.session.execute(sql, {"platform":platform})
    return result.fetchall()

def get_average_game_rating():
      sql = "SELECT TRUNC(AVG(rating),2) AS rating, game_id FROM ratings \
            INNER JOIN games on games.id=ratings.game_id \
            WHERE games.id=ratings.game_id \
            GROUP BY game_id"
      result = db.session.execute(sql)
      return result.fetchall()