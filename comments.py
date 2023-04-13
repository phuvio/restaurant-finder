from sqlalchemy.sql import text
from db import db


def add_comment(restaurant_id, user_id, stars, comment):
    sql = text("""INSERT INTO comments
                  (restaurant_id, user_id, stars, comment)
                  VALUES 
                  (:restaurant_id, :user_id, :stars, :comment)""")
    db.session.execute(sql, {"restaurant_id":restaurant_id,
                             "user_id":user_id,
                             "stars":stars,
                             "comment":comment})
    db.session.commit()

def remove_comment(comment_id):
    sql = text("""DELETE FROM comments
                  WHERE id=:comment_id""")
    db.session.execute(sql, {"comment_id":comment_id})
    db.session.commit()
    return comment_id

def remove_users_all_comments(user_id):
    sql = text("""DELETE FROM comments
                  WHERE user_id=:user_id""")
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()
    return user_id
