from sqlalchemy.sql import text
from db import db


def get_all_restaurants():
    sql = text("""SELECT R.id, R.name, R.latitude, R.longitude,
                  AVG(C.stars)::numeric(10,1) AS avg_stars
                  FROM restaurants R
                  LEFT JOIN comments C ON R.id=C.restaurant_id
                  WHERE visible=1
                  GROUP BY R.id, R.name
                  ORDER BY R.name""")
    return db.session.execute(sql).fetchall()

def get_restaurant_stars(restaurant_id):
    sql = text("""SELECT AVG(C.stars)::numeric(10,1)
                  FROM restaurants R, comments C
                  WHERE R.id=:id AND R.visible=1 AND R.id=C.restaurant_id
                  GROUP BY R.name""")
    return db.session.execute(sql, {"id":restaurant_id}).fetchone()

def get_restaurant_comments(restaurant_id):
    sql = text("""SELECT C.id AS comment_id, C.stars, C.comment, U.username AS username
                  FROM comments C
                  LEFT JOIN users U ON C.user_id=U.id
                  WHERE C.restaurant_id=:restaurant_id
                  ORDER BY C.id DESC
                  LIMIT 10""")
    return db.session.execute(sql, {"restaurant_id":restaurant_id}).fetchall()

def get_restaurant_basic_info(restaurant_id):
    sql = text("""SELECT R.id, R.name, AVG(C.stars)::numeric(10,1) AS avg_stars, R.description
                  FROM restaurants R
                  LEFT JOIN comments C ON R.id=C.restaurant_id
                  WHERE R.id=:restaurant_id AND R.visible=1
                  GROUP BY R.id, R.name""")
    return db.session.execute(sql, {"restaurant_id":restaurant_id}).fetchone()

def get_restaurant_extra_info(restaurant_id):
    sql = text("""SELECT I.key, I.value
                  FROM restaurants R, restaurantinformation I
                  WHERE R.id=:restaurant_id AND R.visible=1 AND I.visible=1
                  AND R.id=I.restaurant_id""")
    return db.session.execute(sql, {"restaurant_id":restaurant_id}).fetchall()

def add_restaurant(name, latitude, longitude, description):
    print(name, latitude, longitude, description)
    sql = text("""INSERT INTO restaurants (name, latitude, longitude, description, visible)
                  VALUES (:name, :latitude, :longitude, :description, 1)
                  RETURNING id""")
    id = db.session.execute(sql, {"name":name, "latitude":latitude, "longitude":longitude, "description":description}).fetchone()[0]
    db.session.commit()
    return id

def change_restaurant_visibility(restaurant_id, visible):
    if visible == 1:
        visible = 0
    else:
        visible = 1
    sql = text("""UPDATE restaurants SET visible=:visible
                  WHERE id=:id""")
    db.session.execute(sql, {"id":restaurant_id, "visible":visible})
    db.session.commit()

def change_restaurant_extra_info_visibility(information_id):
    if visible == 1:
        visible = 0
    else:
        visible = 1
    sql = text("""UPDATE restaurantinformation SET visible=:visible
                  WHERE id=:id""")
    db.session.execute(sql, {"id":information_id})
    db.session.commit()

def get_restaurants_in_group(group_id):
    sql = text("""SELECT R.id, R.name, AVG(C.stars)::numeric(10,1) AS avg_stars
                  FROM restaurantsingroups G
                  INNER JOIN restaurants R ON G.restaurant_id=R.id
                  INNER JOIN  comments C ON R.id=C.restaurant_id
                  WHERE R.visible=1 AND G.group_id=:group_id
                  GROUP BY G.group_id, R.id, R.name
                  ORDER BY avg_stars DESC""")
    return db.session.execute(sql, {"group_id":group_id}).fetchall()

def get_restaurants_by_text(search_string):
    sql = text("""SELECT R.id, R.name, AVG(C.stars)::numeric(10,1) AS avg_stars
                  FROM restaurants R 
                  LEFT JOIN comments C ON R.id=C.restaurant_id
                  WHERE R.visible=1 AND 
                  (R.name LIKE '%' || :search_string || '%' OR R.description LIKE '%' || :search_string || '%')
                  GROUP BY R.id
                  ORDER BY avg_stars DESC""")
    return db.session.execute(sql, {"search_string":search_string}).fetchall()
