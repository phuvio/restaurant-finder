from db import db
from sqlalchemy.sql import text


def get_all_restaurants():
    sql = text("""SELECT id, name, location
                  FROM restaurants
                  WHERE visible=1""")
    return db.session.execute(sql).fetchall()

def get_restaurant_stars(restaurant_id):
    sql = text("""SELECT AVG(C.stars)::numeric(10,0)
                  FROM restaurants R, comments C
                  WHERE R.id=:id AND R.visible=1 AND R.id=C.restaurant_id
                  GROUP BY R.name""")
    return db.session.execute(sql, {"id":restaurant_id}).fetchone()

def get_restaurant_comments(restaurant_id):
    sql = text("""SELECT C.id, C.stars, C.comment
                  FROM restaurants R, comments C
                  WHERE R.id=:id AND R.visible=1 AND R.id=C.restaurant_id""")
    return db.session.execute(sql, {"id":restaurant_id}).fetchall()

def get_restaurant_extra_info(restaurant_id):
    sql = text("""SELECT I.key, I.value,
                  FROM restaurants R, restaurantinformation I
                  WHERE R.id=:id AND R.visible=1 AND R.id=I.restaurant_id""")
    return db.session.execute(sql, {"id":restaurant_id}).fetchall()

def add_restaurant(name, location):
    sql = text("""INSERT INTO restaurants (name, location, visible)
                  VALUES (:name, :location, 1)
                  RETURNING id""")
    return db.session.execute(sql, {"name":name, "location":location}).fetchone()[0]

def change_restaurant_visibility(restaurant_id, visible):
    if visible == 1:
        visible = 0
    else:
        visible = 1
    sql = text("""UPDATE restaurants SET visible=:visible
                  WHERE id=:id""")
    db.session.execute(sql, {"id":restaurant_id, "visible":visible})
    db.session.commit()

def get_restaurants_in_group(group_id):
    sql = text("""SELECT R.id, R.name
                  FROM restaurants R, restaurantsingroups G
                  WHERE R.id=G.restaurant_id AND G.group_id=:group_id AND R.visible=1""")
    return db.session.execute(sql, {"group_id":group_id}).fetchall()

def get_restaurants_by_text(search_string):
    sql = text("""SELECT R.id, R.name
                  FROM restaurants R, 
                  LEFT JOIN restaurantinformation I On R.id=I.restaurant_id
                  WHERE R.visible=1 AND 
                  (R.name like '%' || :search_string '%' OR i.value like '%' || :search_string '%')""")
    return db.session.execute(sql, {"search_string":search_string}).fetchall()
