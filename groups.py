from sqlalchemy.sql import text
from db import db


def get_all_groups():
    sql = text("""SELECT id, name
                  FROM groups
                  WHERE visible=1
                  ORDER BY name""")
    return db.session.execute(sql).fetchall()

def get_all_unvisible_groups():
    sql = text("""SELECT id, name
                  FROM groups
                  WHERE visible=0
                  ORDER BY name""")
    return db.session.execute(sql).fetchall()

def find_group(name):
    sql = text("""SELECT EXISTS
                  (SELECT 1
                  FROM groups
                  WHERE name=:name)""")
    return db.session.execute(sql, {"name":name}).fetchone()[0]

def add_group(name):
    sql = text("""INSERT INTO groups (name, visible)
                  VALUES (:name, 1)
                  RETURNING id""")
    db.session.execute(sql, {"name":name}).fetchone()[0]
    db.session.commit()
    return name

def change_group_visibility(group_id, visible):
    if visible == 1:
        visible = 0
    else:
        visible = 1
    sql = text("""UPDATE groups SET visible=:visible
                  WHERE id=:id""")
    db.session.execute(sql, {"id":group_id, "visible":visible})
    db.session.commit()
    return group_id

def add_restaurant_into_group(group_id, restaurant_id):
    sql = text("""INSERT INTO restaurantsingroups (group_id, restaurant_id)
                  VALUES (:group_id, :restaurant_id)""")
    db.session.execute(sql, {"group_id":group_id, "restaurant_id":restaurant_id})
    db.session.commit()
    return restaurant_id

def remove_restaurant_from_group(group_id, restaurant_id):
    sql = text("""DELETE FROM restaurantsingroups
                  WHERE group_id=:group_id AND restaurant_id=:restaurant_id""")
    db.session.execute(sql, {"group_id":group_id, "restaurant_id":restaurant_id})
    db.session.commit()
    return restaurant_id
