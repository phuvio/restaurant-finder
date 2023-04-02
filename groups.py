from sqlalchemy.sql import text
from db import db


def get_all_groups():
    sql = text("""SELECT id, name
                  FROM groups
                  WHERE visible=1""")
    return db.session.execute(sql).fetchall()

def find_group(name):
    sql = text("""SELECT name
                  FROM groups
                  WHERE name=:name""")
    return db.session.execute(sql, {"name":name}).fetchone()[0]

def add_group(name):
    sql = text("""INSERT INTO groups (name, visible)
                  VALUES (:name, 1)
                  RETURNING id""")
    return db.session.execute(sql, {"name":name}).fetchone()[0]

def change_group_visibility(group_id, visible):
    if visible == 1:
        visible = 0
    else:
        visible = 1
    sql = text("""UPDATE groups SET visible=:visible
                  WHERE id=:id""")
    db.session.execute(sql, {"id":group_id, "visible":visible})
    db.commit()

def add_restaurant_into_group(group_id, restaurant_id):
    sql = text("""INSERT INTO restaurantsingroups (group_id, restaurant_id)
                  VALUES (:group_id, :restaurant_id)""")
    db.session.execute(sql, {"group_id":group_id, "restaurant_id":restaurant_id})
    db.session.commit()

def remove_restaurant_from_group(group_id, restaurant_id):
    sql = text("""DELETE FROM restaurantsingroups
                  WHERE group_id=:group_id AND restaurant_id=:restaurant_id""")
    db.session.execute(sql, {"group_id":group_id, "restaurant_id":restaurant_id})
    db.session.commit()
