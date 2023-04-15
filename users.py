import os
from sqlalchemy.sql import text
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    sql = text("""SELECT id, password, role
                  FROM users 
                  WHERE username=:username""")

    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[1], password):
        return False
    session["user_id"] = user[0]
    session["user_username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    del session["user_id"]
    del session["user_username"]
    del session["user_role"]
    del session["csrf_token"]

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = text("""INSERT INTO users (username, password, role)
                      VALUES (:username, :password, :role)""")
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id")

def require_role(role):
    if role != session.get("user_role"):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def get_all_basic_users():
    sql = text("""SELECT id, username
                  FROM users
                  WHERE role=1
                  ORDER BY username""")
    return db.session.execute(sql).fetchall()

def get_all_admin_users():
    sql = text("""SELECT id, username
                  FROM users
                  WHERE role=0
                  ORDER BY username""")
    return db.session.execute(sql).fetchall()

def change_users_role(users_id, role):
    if role == 1:
        role = 0
    else:
        role = 1
    sql = text("""UPDATE users SET role=:role
                  WHERE id=:id""")
    db.session.execute(sql, {"id":users_id, "role":role})
    db.session.commit()
    return id

def remove_user(users_id):
    sql = text("""DELETE FROM users
                  WHERE id=:id""")
    db.session.execute(sql, {"id":users_id})
    db.session.commit()
    return id
